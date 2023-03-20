import string

ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
import urllib.parse
coolstuff = []
import random
print(''.join(random.choice(ln) for _ in range(30)))
def numbertobase2(n):
    if n == 0: return "0"
    digits = ""
    while n:
        digits += str(n % 2)
        n //= 2
    return digits[::-1]

def tocoolstring(input):
    for i in list(input):
        e = numbertobase2(ln.index(i))
        print(i)
        print(ln.index(i))
        print(e)

        print("-----------------")

# print(ord("0"))

# def tosmall(input):
    # for i in list(input):

# print(numbertobase3(405))

a = 5
a -= 1
print(a)