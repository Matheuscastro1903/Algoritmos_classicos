"""
Objetivo é fazer uma função recursiva que verifique se o número é divisível por 6 ou não
"""

def divisivel_6(valor,tabuada):
    if valor==tabuada*6:
        return "True"
    elif valor<tabuada*6:
        return "False"
    else:
        tabuada+=1
        return divisivel_6(valor,tabuada)





print(divisivel_6(41,0))