"""
Qual é a probabilidade de n pessoas não fazerem aniversário no mesmo dia no intevalo de tempo??

vamos considerar que no seguinte exemplo,o intervalo é de 1 ano,365 dias

1 pessoa=365/365
2 pessoa=364/365
3 pessoa=363/365
...
n pessoa=365-(n-1)/365

ao final,multiplica tudo
"""


def birthday(n,tempo):
    total_completo=1 #total completo=100%
    mult=1 #variável mult servirá apenas para guardar o valor das multiplicações
    for i in range(n):
        #n do range já é igual a (n-1) ,pois no loop,elimina o último elemento
        mult*=(365-i)/365

    return 1-mult

print(birthday(20,365)) #resultado=0.41143838358058027 ou seja aproximadamente 41% de chance de que 
#20 pessoas não farão aniversário no mesmo dia


