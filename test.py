ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
import urllib.parse
coolstuff = []
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

# tocoolstring("000")
# tosmall("asd")

a = "12345678"
