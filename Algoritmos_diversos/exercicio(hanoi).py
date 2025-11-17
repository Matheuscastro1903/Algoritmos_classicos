"""Algotitmo para torre de hanoi"""

def hanoi(n):
    if n<=0:
        return 0
    elif n==1:
        return 1
    
    else:
        pot=n-1
        soma=2**pot
        return soma+hanoi(n-1)
    

print(hanoi(3))