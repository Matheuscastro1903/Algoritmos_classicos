def quicksort(array):
    if len(array)<2:
        return array
    else:
        pivo=array[0]
        menores=[]
        maiores=[]
        for i in array[1:]:
            if i<=pivo:
                menores.append(i)
            elif i>=pivo:
                maiores.append(i)

        """
        O segredo do funcionamento desse algoritmo é empilhar essas chamadas,dando no fim o 
        resultado desejado
        """

        return quicksort(menores)+[pivo]+quicksort(maiores)
    

print(quicksort([10,5,2,3]))


"""
ANÁLISE DAS INTERAÇÕES:
1-
pivo=10
menores=[5,2,3]
maiores=[]

2-
pivo=5
menores=[2,3]
maiores=[]

3-
pivo=2
menores=[]
maiores=[3]

4-
return 3


soma final da pilha

{  [  [ ()+(2)+(3) ] + (5) +()  ] + (10) + () }
"""