from sympy import isprime, randprime
import math
import random

def gerarnumero():
    numero = random.getrandbits(1024)
    numero |= (1<<1023)
    numero |= 1
    return numero 

def miller_rabin(n,k=40):
    if n<2:
        return False
    if n%2==0:
        return False
    r=0
    d=n-1
    while d % 2 == 0:
        d //= 2
        r+=1
    counter=0
    for  _ in range(k):
        a=random.randrange(2,n-1)
        x=pow(a,d,n)
        if x == 1 or x==n-1:
            continue
        composto = True
        for _ in range (r-1):
            x=pow(x,2,n)
            if x==n-1:
                composto=False
                break
        if composto:
            return False
    return True

def gerarprimo():
    while True:
        numero = gerarnumero()
        if miller_rabin(numero):
            return numero

def egcd(a, b):
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    
    return a, x0, y0

def modinv(a, m):
    mdc, x, y = egcd(a, m)
    if mdc != 1:
        raise ValueError("erro em modinv")
    return x % m

def gerarprimos():
    primeiro=gerarprimo()
    segundo = gerarprimo()
    return primeiro, segundo


def gerarchave(primeiro,segundo):
    
    n = primeiro*segundo
    totiente = (primeiro-1)*(segundo-1)
    e=65537
    if(totiente % e==0):
        raise ValueError("erro em gerarchave")
    d=modinv(e,totiente)
    chavepub=(e,n)
    chavepriv=(d,n)
    return  chavepub,chavepriv


