# TODO
import cs50

x = 0
while x == 0:
    number = cs50.get_int("Enter Credit card number? ")
    if number > 0:
        break

# conerting to string and get length
y = number
string = str(number)
length = len(string)
sum1 = 0
sum2 = 0

ftn = int(string[:2])

for foo in range(length):
    x = y % 10
    if (foo % 2) > 0:
        p = x * 2
        if p > 9:
            sum1 = sum1 + ((p % 10) + int((p / 10)))
        else:
            sum1 = sum1 + p
    else:
        sum2 = sum2 + x
    y = int(y / 10)

sum1 = sum1 + sum2

if sum1 % 10 == 0:
    if length == 15 and (ftn == 34 or ftn == 37):
        print("AMEX")
    elif length == 16 and (ftn == 51 or ftn == 52 or ftn == 53 or ftn == 54 or ftn == 55):
        print("MASTERCARD")
    elif (length == 16 or length == 13) and int(ftn / 10) == 4:
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")
