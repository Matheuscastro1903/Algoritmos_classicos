"""
Sequência de fibonacci:
0 1 1 2 3 5 8 13 21 34...

Esse algoritmo busca descobrir qual o valor da posição n

execução=

-fibonacci do índice 5 é igual ao fibonacci do índice 4 + fibonacci do índice 3
fib(5)=fib(4)+fib(3)

fib(4)=fib(3)+fib(2)

fib(3)=fib(2)+fib(1)

fib(2)=fib(1)+fib(0)

fib(1)=1

fib(0)= 0


Substituindo:

fib(2)=1+0=1

fib(3)=1+1=2

fib(4)=2+1=3

fib(5)=3+2
"""

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
    

print(fibonacci(10))


"""
TESTE n=10

fib(10)=fib(9)+fib(8)

fib9=fib(8)+fib(7)

fib(8)=fib(7)+fib(6)

fib(7)=fib(6)+fib(5)

fib(6)=fib(5)+fib(4)

fib(5)=fib(4)+fib(3)

fib(4)=fib(3)+fib(2)

fib(3)=fib(2)+fib(1)

fib(2)=fib(1)+fib(0)


já temos o valor de fib(5)=5 e fib(4)=3

então

fib(6)=5+3=8
fib(7)=8+5=13
fib(8)=13+8=21
fib(9)=21+13=34
fib(10)=34+21=55
"""
