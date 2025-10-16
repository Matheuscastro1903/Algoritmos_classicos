

def fat(n):
    if n<0:
        return "Número inválido"
    elif n==0:
        return 1
    else:
        return n*fat(n-1)



print(fat(5))

"""
Explicação do código

5*fat(5-1)-->4*fat(4-1)-->3*fat(3-1)-->2*fat(2-1)-->1*(fat-1)-->caso base return 1

completa os returns
1*2*3*4*5*=fatorial de 5


"""