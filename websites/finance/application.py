import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    currentCash = getCurrentCash()
    userPurchases = db.execute('SELECT "stock_name", SUM("stock_quantity") AS "stock_quantity", ' +
                               'MAX("stock_price") AS "stock_price", SUM("tot_payed") AS "tot_payed" FROM "transaction" '+
                               'WHERE user_id = :user_id GROUP BY "stock_name"',
                                user_id = session["user_id"])
    userPurchasesList = []
    groundTotal = currentCash
    for purchase in userPurchases:
        groundTotal += purchase["tot_payed"]
        purchase["tot_payed"] = usd(abs(purchase["tot_payed"]))
        purchase["stock_price"] = usd(abs(purchase["stock_price"]))
        userPurchasesList.append(list(purchase.values()))

    return render_template("index.html", userPurchasesList = userPurchasesList,
                            currentCash = usd(currentCash), groundTotal = usd(groundTotal))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("please provide a symbol", 403)
        if lookup(request.form.get("symbol")) == None:
            return apology("please indicate a valid symbol")

        if not request.form.get("shares"):
            return apology("please indicate the number of shares", 403)
        try:
            shares = int(request.form.get("shares"))
        except (ValueError):
            return apology("please indicate the number of shares", 400)
        if shares < 1:
            return apology("please indicate a number of shares greater or equal to 1", 400)

        price = lookup(request.form.get("symbol"))["price"]
        currentCash = getCurrentCash()
        paymentRequired = price * shares
        if (currentCash < paymentRequired):
            return apology("sorry, you do not have enough money", 403)

        db.execute('INSERT INTO "transaction" ("stock_name", "stock_price", "stock_quantity", "user_id", "tot_payed") ' +
                   'VALUES (:stock_name, :stock_price, :stock_quantity, :user_id, :tot_payed)',
                    stock_name = lookup(request.form.get("symbol"))["name"].split(',')[0],
                    stock_price = price,
                    stock_quantity = shares,
                    user_id = session["user_id"],
                    tot_payed = paymentRequired)

        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id",
                    cash = currentCash - paymentRequired,
                    user_id = session["user_id"])

        return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    if request.method == "GET":
        username = request.args.get('username', 0, type=str)
        if len(username) <= 1:
            return jsonify(isUsernameTaken = "false")
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)
        if rows:
            return jsonify(isUsernameTaken = "false")
        return jsonify(isUsernameTaken = "true")


@login_required
def getCurrentCash():
    currentCashDict = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])[0]
    return list(currentCashDict.values())[0]


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    userPurchases = db.execute('SELECT "stock_name", "stock_quantity", "stock_price", "timestamp" FROM "transaction" ' +
                               'WHERE user_id = :user_id',
                                user_id = session["user_id"])
    userPurchasesList = []
    for purchase in userPurchases:
        purchase["stock_price"] = usd(abs(purchase["stock_price"]))
        userPurchasesList.append(list(purchase.values()))

    return render_template("history.html", userPurchasesList = userPurchasesList)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/passChange", methods=["GET", "POST"])
@login_required
def passChange():
    if request.method == "GET":
        return render_template("passChange.html")

    if request.method == "POST":
        if not request.form.get("oldPassword"):
            return apology("please write previous password", 403)
        if not request.form.get("newPassword"):
            return apology("please write new password", 403)
        if not request.form.get("confirmation"):
            return apology("please write confirmation of new password", 403)

        rows = db.execute('SELECT "hash" FROM "users" WHERE id = :ID',
                          ID = session["user_id"])
        if not rows:
            return apology("ehm, looks like you do not exist", 403)

        if not check_password_hash(rows[0]["hash"], request.form.get("oldPassword")):
            return apology("old password is wrong", 403)

        if not request.form.get("confirmation") == request.form.get("newPassword"):
            return apology("password and confirmation are different", 403)

        db.execute('UPDATE "users" SET hash = :hashedPsw WHERE id = :ID',
                    ID = session["user_id"],
                    hashedPsw = generate_password_hash(request.form.get("newPassword")))

        return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("please provide a symbol", 400)

        if lookup(request.form.get("symbol")) == None:
            return apology("please indicate a valid symbol")

        return render_template("quoted.html", data = lookup(request.form.get("symbol")))

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("password and confirmation are different", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashedPsw)",
                    username = request.form.get("username"),
                    hashedPsw = generate_password_hash(request.form.get("password")))

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        symbols = db.execute('SELECT DISTINCT "stock_name" FROM "transaction" WHERE user_id = :username',
                              username = session["user_id"])
        return render_template("sell.html", symbols = symbols)

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("please provide a symbol", 403)
        if lookup(request.form.get("symbol")) == None:
            return apology("please indicate a valid symbol")

        stockName = lookup(request.form.get("symbol"))["name"].split(',')[0]
        rows = db.execute('SELECT "stock_name", "stock_price", "stock_quantity" FROM "transaction" '
                        + 'WHERE stock_name = :stockName AND user_id = :username',
                        stockName = stockName, username = session["user_id"])
        stocksOwn = 0
        for row in rows:
            stocksOwn += row["stock_quantity"]

        if stocksOwn <= 0:
            return apology("you do not own this stock")

        if not request.form.get("shares"):
            return apology("please indicate the number of shares", 403)
        try:
            shares = int(request.form.get("shares"))
        except (ValueError):
            return apology("please indicate the number of shares", 403)
        if shares < 1:
            return apology("please indicate a number of shares greater or equal to 1", 403)
        if shares > stocksOwn:
            return apology("you do not have enough stocks")

        price = (-1) * lookup(request.form.get("symbol"))["price"]
        currentCash = getCurrentCash()
        paymentRequired = price * shares

        db.execute('INSERT INTO "transaction" ("stock_name", "stock_price", "stock_quantity", "user_id", "tot_payed") ' +
                   'VALUES (:stock_name, :stock_price, :stock_quantity, :user_id, :tot_payed)',
                    stock_name = lookup(request.form.get("symbol"))["name"].split(',')[0],
                    stock_price = price,
                    stock_quantity = (-1) * shares,
                    user_id = session["user_id"],
                    tot_payed = paymentRequired)

        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id",
                    cash = currentCash - paymentRequired,
                    user_id = session["user_id"])

        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
