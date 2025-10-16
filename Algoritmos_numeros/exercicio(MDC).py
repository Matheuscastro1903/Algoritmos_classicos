"""
arquivo destinado a guardar algoritmos de MDC
"""

def mdc(a,b):

    if a<0 or b<0:
        return "MDC INVÁLIDO"

    if b==0:
        return a
    else:
        return mdc(b,a%b)


print(mdc(9,18))

"""
Explicação:

Algoritmo de Euclides
mdc(a,b)=mdc(b,a%b)--> e assim segue o flux,até chegar no caso base,resto=0



primeiro if=verifica se os números não são nulos

segundo if=caso base,verifica se b=0

interações:

(9,18)-->(18,9)-->(9,0) chegou no caso base=resto é igual a 0
"""