def exponencial(a, n):

    exp = 1
    if n == 0:
        return exp

    if a == 0 and n == 0:
        return "Impossível calcular"

    else:
        exp *= a

        # segue o mesmo principio do fatorial
        return exp * exponencial(a, n-1)

    pass


print(exponencial(30,5))

#1125899906842624
#1073741824
#24300000

#102400000

#3200000
#1048576

#1073741824
#24300000