"""
===============================
📘 ALGORITMO: BUBBLE SORT
===============================

🧠 IDEIA CENTRAL:
----------------
O Bubble Sort (ou "ordenação por bolha") funciona simulando o movimento de bolhas em um líquido:
os valores **maiores "flutuam" para o final da lista** a cada passada.

A ideia é simples:
- Percorremos a lista comparando pares de elementos vizinhos.
- Se o elemento da esquerda for MAIOR que o da direita, trocamos os dois.
- Ao final de cada varredura, o maior elemento já estará na posição correta (no final da lista).

--------------------------------
🔁 LÓGICA PASSO A PASSO (em palavras):
--------------------------------
1. Compare o primeiro e o segundo elemento.
   - Se o primeiro > segundo → troque-os.

2. Vá para o próximo par (segundo e terceiro), e assim por diante.

3. Ao fim da primeira passada, o maior valor estará no final da lista.

4. Repita o processo, mas ignorando o último elemento (que já está ordenado).

5. Continue até que nenhuma troca seja feita (lista ordenada).

--------------------------------
🧩 EXEMPLO PRÁTICO:
--------------------------------
Vamos ordenar a lista: [5, 3, 8, 4, 2]

PASSO 1 (primeira varredura):
Comparações e trocas:
- (5,3) → troca → [3,5,8,4,2]
- (5,8) → ok
- (8,4) → troca → [3,5,4,8,2]
- (8,2) → troca → [3,5,4,2,8]
Maior elemento (8) foi para o final ✅

PASSO 2:
- (3,5) → ok
- (5,4) → troca → [3,4,5,2,8]
- (5,2) → troca → [3,4,2,5,8]
Maior elemento (5) foi para a penúltima posição ✅

PASSO 3:
- (3,4) → ok
- (4,2) → troca → [3,2,4,5,8]
Maior elemento (4) sobe ✅

PASSO 4:
- (3,2) → troca → [2,3,4,5,8]
Lista ordenada ✅

--------------------------------
⏱️ COMPLEXIDADE:
--------------------------------
- Melhor caso: O(n) (quando já está ordenado e você otimiza para parar cedo)
- Pior caso:  O(n²)
- Média:       O(n²)

--------------------------------
⚙️ CARACTERÍSTICAS:
--------------------------------
Tipo:          Ordenação por comparação
Estável:       ✅ Sim (mantém a ordem de elementos iguais)
In-place:      ✅ Sim (usa pouca memória extra)
Complexidade:  O(n²)
Melhor uso:    Listas pequenas ou quase ordenadas

--------------------------------
💡 DICA DE ESTUDO:
--------------------------------
1️⃣ Comece simulando manualmente em uma lista pequena, como [4, 2, 3].
2️⃣ Observe o “movimento” dos elementos a cada varredura.
3️⃣ Só depois transforme o raciocínio em código.



"""
#0 sem trocas
#1 foi trocado



"""

[5, 3, 8, 4, 2]

3 5 8 4 2        1




"""


def bubble_sort(lista):
    lista_verificador=[]
    verificador=None
    i=0
    while i<len(lista)-1:
        primeiro=lista[i]
        segundo=lista[i+1]

        if primeiro>=segundo:
            lista[i]=segundo
            lista[i+1]=primeiro
            
            verificador=True # precisa de uma nova comparação

            
        i+=1
    
    if  verificador==True:
        #só irá chamar recursivamente a função se tiver havido alguma troca,verificador=True
        return bubble_sort(lista)
    else:
        return f"Lista ordenada {lista}"

  


        pass




print(bubble_sort([5, 3, 8, 4, 2]))