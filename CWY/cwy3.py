from math import sin
from math import cos
from math import tan

t = input("Enter a trigonometric function (sin/cos/tan): ")
while t != "sin" and t != "cos" and t != "tan":
    t = input("Enter a trigonometric function (sin/cos/tan): ")
if t == "sin":
    c = 0
elif t == "cos":
    c = 1
else:
    c = 2

n = float(input("Enter an positive integer n: "))
while int(n) != n or n <= 0:
    #If n is floating point numbers or negative number 
    n = float(input("Enter an positive integer n: "))
n = int(n)

print("Enter two numbers a and b below. b should be greater than or equal to a.")
a = float(input("Enter a: "))
b = float(input("Enter b: "))
while a > b:
    print("Enter two numbers a and b below. b should be greater than or equal to a.")
    a = float(input("Enter a: "))
    b = float(input("Enter b: "))

def g(a,b,c,n,i):
    if c == 0:
        d = sin(a + (b-a)/n * (i - 1/2))
    elif c == 1:
        d = cos(a + (b-a)/n * (i - 1/2))
    else:
        d = tan(a + (b-a)/n * (i - 1/2))
    return (b-a)/n * d

sum = 0
for i in range(1, n+1):
    sum += g(a,b,c,n,i)

print("The value of the integegration is ",sum,".")