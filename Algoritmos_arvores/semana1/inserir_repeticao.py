
"""
Todo nodo deve ter os 4 atríbutos básicos abaixo
"""
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None  
        self.pai= None


class ArvoreBinaria:
    def __init__(self):
        #a árvore nasce vazia,não podendo pedir o parâmetro
        #root logo de cara
        self.root= None


    def inserir_e_checar_repeticao(self, valor):
        # Se a árvore está vazia, o primeiro elemento vira a raiz
        if self.root == None:
            self.root = Nodo(valor)
            return False # Não é repetido

        # Se não está vazia, vamos começar a descer a partir da raiz
        atual = self.root #isso aponta para algum objeto que possui valor

        while True: #loop infinito que irá parar apenas quando tiver 
            #algum return
            
            # O valor já existe-->verificando a raiz sempre
            if valor == atual.valor:
                return True #número repetido,Aborta a inserção.

            #O valor é MENOR que o atual? Vai para a esquerda
            elif valor < atual.valor:
                #se não tiver filh=none,então já pode colocar
                if atual.esquerda == None:
                    #Cria o nodo aqui.
                    novo_nodo = Nodo(valor)
                    novo_nodo.pai = atual #Conecta o filho ao pai
                    atual.esquerda = novo_nodo #Conecta o pai ao filho
                    return False
                else:
                    # Já tem alguém lá, então desce mais um nível para a esquerda
                    #agora o valor atual é o valor do filho esquerdo do atual pai
                    atual = atual.esquerda

            #O valor é MAIOR que o atual? Vai para a direita
            else:
                if atual.direita == None:
                    # Espaço vazio encontrado,Cria o nodo aqui.
                    novo_nodo = Nodo(valor)
                    novo_nodo.pai = atual #Conecta o filho ao pai
                    atual.direita = novo_nodo #Conecta o pai ao filho
                    return False
                else:
                    #Já tem alguém lá, então desce mais um nível para a direita
                    #e o atual virá o filho direito do
                    atual = atual.direita



def getInfo(p):
    return p.valor if p is not None else None

def getLeft(p):
    return p.esquerda if p is not None else None

def getRight(p):
    return p.direita if p is not None else None

def getFather(p):
    return p.pai if p is not None else None



#simulação
lista_desordenada = [14, 15, 4, 9, 15, 20]

#Cria a árvore (ela nasce 100% vazia)
minha_arvore = ArvoreBinaria()

print(f"Iniciando a leitura da lista: {lista_desordenada}\n")

#dados da lista para a árvore serão passados um por um
for numero in lista_desordenada:
    print(f"Lendo o número: {numero}...")
    
    #A árvore tenta inserir. Se ela retornar True, é repetido!
    eh_repetido = minha_arvore.inserir_e_checar_repeticao(numero)
    
    if eh_repetido:
        print(f"-> ALERTA: O número {numero} é repetido! Parando a busca.")
        break 
    else:
        print(f"-> Inserido na árvore. Tudo ok.")



"""
O objetivo do método verificar_repeticao_com insercao é matar dois coelhos com uma cajadada só, resolvendo exatamente aquele problema que o professor propôs: encontrar números repetidos em uma 
lista numérica desordenada.

Imagine que você tem uma lista gigante de números e precisa saber se tem algum duplicado.

O jeito lento (sem árvore): Você pegaria o 1º número e compararia com todos os outros da lista. 
Depois pegaria o 2º e compararia com todos os outros... O professor menciona que comparar cada número com todos em uma lista desordenada levaria um custo de tempo 
impraticável para listas grandes.

O jeito inteligente (o objetivo deste método): Nós vamos ler a lista de números uma única vez. 
Para cada número que lermos, chamaremos esse método para tentar guardá-lo na nossa Árvore Binária.

A mágica do método acontece graças às regras de navegação da árvore (se for menor, desce para a esquerda; 
se for maior, desce para a direita). Quando você manda o método inserir um número, ele vai descendo pela árvore e só tem dois finais possíveis:

Ele encontra um espaço vazio (None): Isso significa que o número percorreu o caminho todo e não trombou com ninguém com o mesmo valor. 
Logo, ele constrói a "caixinha" (o Nodo), guarda o número lá e retorna False (ou seja, "Pode ficar tranquilo, inseri aqui e ele não era repetido").

Ele tromba com um nó que tem exatamente o mesmo valor: 
Isso significa que, em algum momento anterior, nós já havíamos lido esse número da lista e colocado na árvore! Nesse exato milissegundo, a árvore detecta a repetição. O método aborta a inserção e retorna True (ou seja, 
"Alerta! Achei um número repetido!").

Resumindo: O método é um "verificador através de inserção". 
Ele tenta inserir o número na estrutura; se achar um espaço vazio, é porque o número é inédito. Se esbarrar no mesmo valor no meio do caminho, ele cumpre o objetivo do exercício e detecta a repetição.

"""