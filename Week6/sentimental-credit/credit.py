from cs50 import get_int

num = get_int("Number: ")
numcopy = num
ot = 0
et = 0
count = 0
while numcopy > 0:
    if count % 2 == 0:
        ot += numcopy % 10
        print("ot" + str(ot))
    else:
        temp = (numcopy % 10) * 2
        et += temp
        if temp > 9:
            et -= 9
        print("et" + str(et))
    numcopy //= 10

    count += 1
total = ot + et
print(total)
if total % 10 == 0:
    if num < 5000000000000 and num >= 4000000000000:
        print("VISA")
    elif num < 5000000000000000 and num >= 4000000000000000:
        print("VISA")
    elif num < 350000000000000 and num >= 340000000000000:
        print("AMEX")
    elif num < 380000000000000 and num >= 370000000000000:
        print("AMEX")
    elif num < 5600000000000000 and num >= 5100000000000000:
        print("MASTERCARD")
    else:
        print("INVALID")
else:
    print("INVALID")
