"""
a ideia do selection sort é comparar todo os elementos de uma lista_inicial e encontrar o menor entre todos eles,e trocar esse menor para a lista_nova
e seguir comparando até a lista_inicial inical ficar vazia

complexidade=O(n)

"""


def selection_sort(lista_inicial,lista_nova):
    lista_nova
    
    #esse while vai continuar rodando até a lista_inicial ficar vazia
    while lista_inicial:
        #supôe que o primeiro elemento da lista_inicial é o menor
        elemento=lista_inicial[0]
        
        for i in lista_inicial:
            if i<=elemento:
                menor=i

        #retira o menor elemento da lista_inicial
        lista_inicial.remove(menor)
        #adiciona o menor elemento comparado com toda a lista_inicial a nova lista_inicial
        lista_nova.append(menor)

    return lista_nova





lista_nova=[]
print(selection_sort([5, 3, 6, 2, 10],lista_nova))