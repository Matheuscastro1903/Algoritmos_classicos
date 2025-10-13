#No insertion sort utilizaremos apenas uma lista para organizar



def insertion_sort(lista):
    # Loop externo: percorre do segundo elemento até o final
    for i in range(1, len(lista)):
        chave = lista[i]       #O elemento que usaremos para fazer a comparação
        j = i - 1              #Valor do índice j

        #só entrará no loop se o valor de j>=0(o tamanho mínimo da lista) e se o elemento j(elemento sempre que vem antes) é maior que a chave
        #elemento seguinte
        while j >= 0 and lista[j] > chave:
            lista[j + 1] = lista[j]  #Empurra o elemento para a direita
            j -= 1                    #Diminui o valor de j para compara com os elementos que vem após e verificar se vai entrar no loop ou não

        # Insere a chave na posição correta
        lista[j + 1] = chave

# Exemplo de uso
numeros = [5, 3, 4, 1, 2]
insertion_sort(numeros)
print(numeros)  # Saída: [1, 2, 3, 4, 5]


"""
1-Interação while
chave=3
lista[0]=5

empurra o 5 para frente do 3
lista=[3,5,4,1,2]


***************************************
2-interação while

chave=4
lista[1]=5

1-interação for
empurra o 5 para frente do 4
2-interação for
j=0,mas lista[j]=3 e chave=4,logo não entrará no loop for

lista=[3,4,5,1,2]

***************************************************
3-interação while

chave=1
lista[2]=5

1-intereação for
empurra o 5 para frente do 1   j=2

2-interação for 
empurra o 4 para frente do 1    j=1

3-interação for 
empurra o 3 para frente do 1    j=0

!não existe mais interações pois a lista acaba depois do índice ficar 0

**********************************************************

4-interação while

chave=2
lista[3]=5

1 interação for
empurra o 5 para frente do 2 j=3

2 interação for
empurra o 4 para frente do 2 j=2

3 interação for
empurra o 3 para frente do 2 j=1

4 interacao for
não entra no loop pois o elemento lista[j=0] é menor que a chave=2


***********************************************
algoritmo acaba por percorrer toda a lista incial

tempo de execução O(n) se só precisar verificar e O(n^2) no medio e pior caso,pois precisará verificar n elementos n vezes
 

"""