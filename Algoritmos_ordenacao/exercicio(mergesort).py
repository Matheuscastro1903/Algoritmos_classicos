def merge_sort(lista):
    # Caso base: se a lista tem 0 ou 1 elementos, já está ordenada
    if len(lista) <= 1:
        return lista

    # Passo 1: dividir a lista no meio
    meio = len(lista) // 2
    esquerda = lista[:meio]
    direita = lista[meio:]

    # Passo 2: ordenar recursivamente cada metade
    esquerda_ordenada = merge_sort(esquerda)
    direita_ordenada = merge_sort(direita)

    # Passo 3: combinar as duas metades ordenadas
    return merge(esquerda_ordenada, direita_ordenada)

def merge(esquerda, direita):
    resultado = []
    i = j = 0

    # Comparar elementos das duas listas e adicionar o menor
    while i < len(esquerda) and j < len(direita):
        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    # Adicionar o que sobrou da lista esquerda ou direita
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])

    return resultado

# Exemplo de uso
numeros = [5, 3, 4, 1, 2]
ordenados = merge_sort(numeros)
print(ordenados)  # Saída: [1, 2, 3, 4, 5]


#a cada interação é criado uma nova lista resultado

"""
1-interação da função merge sort
esquerda=[5,3]-->esquerda=[5] e direita=[3] e fará puxará a função merge da esquerda e da direita
i=j=0 enquanto i for menor que o tamanho total da lista(lembrando que o tamanho total fica diferente do índice da lista)

irá fazer a comparação e verá que o da direita é menor que o da esquerda,adicionando no valor do resultado, e somará i++,impossibilitando de entrar 
no outro loop,mas adicionando no final tudo que resta na lista da esquerda,no caso apenas o elemento 5

resultado=[3,5]

****************************************************************************************************

direita=[4,1,2]-->esquerda=[4] direita=[1,2] --> mesmo processo do anterior,mas agora o da esquerda é menor,então é adicionado ao resultado primeiro
e depois o da direita é adicionado,resultado=[1,2]

após resolver a primeira recursão,irá fazer o merge da esquerda_ordenada=[4] pois quando é um array de um elemento só retorna automaticamente
e da direita_ordenada=[1,2]

irá ter a comparação do primeiro elemento de cada lista,vendo que o um é menor que quatro,logo sendo adicionado ao resultado primerio, e somando j++,
que pegará o elemento de índice 1=2 do da direita,comparará com o 4 e será adicionado primeiro ao resultado,somando no final j++,impossibilitando
de continuar o loop e adicionando tudo que restou da esquerda a partir do índice 0=[4] e da direita a partir do índice 2 =[]

******************************************************************************************************
agora o esquerda_ordenado=[3,5] e o direita ordenado[1,2,4]

repetindo o mesmo processo do caso de cima
comparará 
3 e 1 -->adiciona 1 no resultado j++
3 e 2-->adiciona 2 no resultado  J++
3 e 4-->adicona 3 i++
5 e 3-->adiciona 4 J++
não entrará mais em loop pois o valor de j=3 e o len(direita_ordenado)=3
e adiciona tudo que resta da esquerda a partir do índice 1=[5] e tudo que resta da direita a partir do índice 3=[]






"""
