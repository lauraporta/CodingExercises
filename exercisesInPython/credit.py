# TODO both in python and c script:
# 3. check again the functionality of the program

import cs50 as cs


def main():

    minValCard =      3999999999999      # 3 9999 9999 9999
    maxValCard =   5600000000000000      # 5600 0000 0000 0000

    minVISAandMC = 3900000000000000      # 3900 0000 0000 0000
    normFactor1 =   100000000000000      # 100 0000 0000 0000

    minAMEX =       330000000000000      # 330 0000 0000 0000
    normFactor2 =    10000000000000      # 10 0000 0000 0000

    minVISA =         3999999999999      # 3 9000 0000 0000
    normFactor3 =     1000000000000      # 1 0000 0000 0000

    while True:
        card = cs.get_float("Number: ")

        if card > minValCard and card < maxValCard:

            if (checkSum(card)):

                if card > minVISAandMC:                         # 16 digit long cards
                    lastDigs = card // normFactor1

                    if lastDigs > 39 and lastDigs < 50:
                        print("VISA")
                        return
                    elif lastDigs > 50:
                        print("MASTERCARD")
                        return
                    else:
                        print("INVALID")
                        return

                elif card > minAMEX:                            # 15 digit long cards
                    lastDigs = card // normFactor2

                    if lastDigs == 34 or lastDigs == 37:
                        print("AMEX")
                        return
                    else:
                        print("INVALID")
                        return

                elif card > minVISA:                           # 13 digit long cards
                    lastDigs = card // normFactor3

                    if lastDigs == 4:
                        print("VISA")
                        return
                    else:
                        print("INVALID")
                        return
                else:                           # unknown card
                    print("INVALID")
                    return
            else:                               # checksum gave false
                print("INVALID")
                return
        else:                                   # wrong card length
            print("INVALID")
            return


def checkSum(kard):

    evenSum = 0
    oddSum = 0

    for j in range(len(str(kard))):
        currentDigit = kard % 10

        if j % 2 == 1:
            mult = currentDigit * 2

            if mult > 9:
                mult = (mult // 10) + (mult % 10)

            evenSum += mult

        else:
            oddSum += currentDigit

        kard //= 10

    mainSum = oddSum + evenSum

    return mainSum % 10 == 0


if __name__ == "__main__":
    main()