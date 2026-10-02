from ..semana1.arvorebinaria import (
    ArvoreBinaria,
    Nodo,
    getInfo,
    getLeft,
    getRight,
    getFather,
)

class NodoRubroNegro:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.pai = None
        self.cor = "V"  # O motor estrutural da Rubro-Negra




def getCor(p):
    # Se o nodo existe, retorna a cor dele. Se for None (NIL), ele é PRETO ("P").
    return p.cor if p is not None else "P"

def getTio(nodo):
    pai = getFather(nodo)
    avo = getFather(pai)
    
    if avo is None:
        return None
        
    #O pai é o braço esquerdo do avô?
    if pai == getLeft(avo):
        return getRight(avo) # Então o tio é o braço direito
    else:
        return getLeft(avo)  # Senão, o tio é o braço esquerdo

class ArvoreRubroNegra(ArvoreBinaria):
    def __init__(self):
        super().__init__()

    def left_rotate(self, x):
        # ==========================================
        # ESTADO INICIAL:
        #      10 (x)
        #        \
        #         20 (y)
        #           \
        #            30
        # ==========================================

        # 1. Isola o herdeiro (y).
        y = getRight(x)

        # 2. Transfere a subárvore esquerda de y para a direita de x,caso ela exista,já que seria menor que y e maior que x
        # No nosso exemplo, a direita do 10 passa a apontar para None.
        x.direita = getLeft(y)
        if getLeft(y) is not None:
            getLeft(y).pai = x

        # ==========================================
        # ESTADO APÓS PASSO 2 (O Corte):
        # O 10 perde a ligação com o 20 e fica isolado.
        #
        #      10 (x)         20 (y)
        #        \              \
        #        None            30
        # ==========================================

        # 3. O nodo 20 copia o ponteiro do pai do nodo 10 (None, pois 10 era raiz). 
        y.pai = getFather(x)

        # 4. Atualiza o ponteiro da árvore para oficializar o novo líder.
        if getFather(x) is None:
            self.root = y
        elif x == getLeft(getFather(x)):
            getFather(x).esquerda = y
        else:
            getFather(x).direita = y

        # ==========================================
        # ESTADO APÓS PASSO 4 (A Promoção):
        # O 20 assume a liderança absoluta da estrutura.
        #
        #    [Nova Raiz] ---> 20 (y)
        #                       \
        #                        30
        #
        #      10 (x) ---> (Flutuando, aguardando religação)
        # ==========================================

        # 5. O rebaixamento final do pivô (A Queda).
        # O 10 é encaixado na vaga esquerda que estava aberta no 20.
        y.esquerda = x
        x.pai = y

        # ==========================================
        # ESTADO FINAL (Rotação Completa):
        #
        #           20 (y)
        #          /      \
        #      10 (x)      30
        # ==========================================

        # O nodo 30, que já era o filho direito do 20 (y.direita), não é afetado por nenhuma dessas linhas e sobe junto com o 20.

    def right_rotate(self, x):
        # ==========================================
        # ESTADO INICIAL (Rotação à Direita):
        # O pivô do giro é o nodo do topo (x).
        # O herdeiro que vai assumir a liderança local vem da esquerda (x).
        #
        #           30 (x)
        #          /
        #      20 (y)
        #      /
        #    10
        # ==========================================

        # 1. Isola o herdeiro (x).
        y = getLeft(x)

        # o filho esquerdo de x irá se tornar o filho direito de y
        x.esquerda = getRight(y)
        # o filho direito de y agora é o filho esquerdo de x
        if getRight(y) is not None:
            getRight(y).pai = x

        # pai de y agora é o pai de x
        y.pai = getFather(x)

        # se o pai de x é none,então ele é raiz
        if getFather(x) is None:
            # atualizando a raiz
            self.root = y
        elif x == getLeft(getFather(x)):  # se x é o filho esquerdo do pai então agora y é o filho esquerdo do pai de x
            getFather(x).esquerda = y
        else:
            # se x é o filho direito do pai,então agora y é o filho direito do pai de x
            getFather(x).direita = y

        # filho direita de y aogra é x
        y.direita = x
        # pai de x agora é y
        x.pai = y

    def inserir(self, valor):
        novo_nodo = NodoRubroNegro(valor)
        y = None
        x = self.root

        # só vai entrar aqui se x não for none,ou seja,se a raiz já existir
        while x is not None:
            # y é o controlador do valor da raiz do nível da interação
            y = x
            # o if else abaixo irá pegar até x for um valor none,e assim sairá do loop
            if getInfo(novo_nodo) < getInfo(x):
                # irá pegar o filho esquerdo de x
                x = getLeft(x)
            else:
                # irá pegar o filho direito de x
                x = getRight(x)

        # seta o valor de y= valor da raiz do nível como pai do novo nodo
        novo_nodo.pai = y

        if y is None:
            # se y estiver como none=então atribui para raiz que não existe ainda
            self.root = novo_nodo
            # se for menor,o valor do filho da esquerda de y é o novo nodo,caso contrário é o filho da direita
        elif getInfo(novo_nodo) < getInfo(y):
            y.esquerda = novo_nodo
        else:
            y.direita = novo_nodo

        self.inserir_fixup(novo_nodo)

    def remover(self, x):

        #caso 3=possui 2 filhos
        if getLeft(x) is not None and getRight(x) is not None:
            nodo_fisico = self.sucessor(x) # Caso 3: O sucessor é arrancado do fundo
        else:
            nodo_fisico = x #Casos 1 e 2: O próprio alvo é arrancado

        # 2. Captura a cor do nó que vai sumir (é ela que define se haverá conserto)
        cor_perdida = getCor(nodo_fisico)
        
        # Guarda a cor original do alvo para o disfarce do Caso 3
        cor_original_x = getCor(x)

        #Delega o trabalho físico e captura onde o buraco ficou
        ponto_de_partida = super().remover(x)

        #Se foi Caso 3, o sucessor subiu. Ele precisa herdar a cor exata do nó que ele substituiu
        if getLeft(x) is not None and getRight(x) is not None:
            nodo_fisico.cor = cor_original_x

        #A árvore só perde o equilíbrio se arrancarmos um nó Preto da memória
        if cor_perdida == "P" and ponto_de_partida is not None:
            self.remover_fixup(ponto_de_partida)

    
    def inserir_fixup(self, nodo):
        # O laço roda enquanto o pai do nodo atual existir e for Vermelho
        while getFather(nodo) is not None and getCor(getFather(nodo)) == "V":
            pai = getFather(nodo)
            avo = getFather(pai)

            # ==========================================
            # LADO ESQUERDO: O pai é o filho esquerdo do avô
            # ==========================================
            if pai == getLeft(avo):
                tio = getRight(avo)

                # ==========================================
                # CASO 1: Tio é Vermelho (Apenas repintura)


                """
                                ANTES (Conflito!)                    DEPOIS (Caso 1)
                                 =================                    =================
                
                                Avô(P)                               Avô(V) <--- O [N] sobe para cá
                                /      \                             /      \
                            Pai(V)    Tio(V)         ====>       Pai(P)    Tio(P)
                            /                                    /
                        [N](V)                                  (V)


                """
                # ==========================================
                if getCor(tio) == "V":
                    pai.cor = "P"
                    tio.cor = "P"
                    avo.cor = "V"
                    nodo = avo  #passa o problema para cima e a recursividade do while irá trabalhar
                
                # ==========================================
                # CASOS DE ROTAÇÃO: Tio é Preto
                # ==========================================
                else:
                    # CASO 2: Topologia em Zigue-Zague (Nó cresce para a direita)
                    """
            ANTES (Zigue-Zague)                  DEPOIS (Transformado em Linha Reta)
      ===================                  ===================================

           Avô(P)                               Avô(P)
          /      \                             /      \
      Pai(V)    Tio(P)         ====>     Pai(V)      Tio(P)  <-- (Antigo nó inserido)
          \                               /
         [N](V)                        [N](V)                <-- (Antigo Pai)
                                 (O ponteiro desceu com a rotação)
                    """


                    if nodo == getRight(pai):
                        nodo = pai
                        self.left_rotate(nodo)
                        
                        # Recalcula ponteiros pois a rotação mudou as posições locais
                        pai = getFather(nodo)
                        avo = getFather(pai)

                    # CASO 3: Topologia em Linha Reta (Nó e pai estão na esquerda)
                    pai.cor = "P" # pai tem que ser preto(esse pai foi o nodo add e o filho agora é o vermelho pai de antes)
                    avo.cor = "V"#define avo como vermelho
                    self.right_rotate(avo)

            # ==========================================
            # LADO DIREITO: O pai é o filho direito do avô (Imagem Espelhada)
            # ==========================================
            else:
                tio = getLeft(avo)
                
                # ==========================================
                # CASO 1: Tio é Vermelho (mesma coisa)



                
                # ==========================================
                if getCor(tio) == "V":
                    pai.cor = "P"
                    tio.cor = "P"
                    avo.cor = "V"
                    nodo = avo
                
                # ==========================================
                # CASOS DE ROTAÇÃO: Tio é Preto
                # ==========================================
                else:
                    # CASO 2: Topologia em Zigue-Zague (Nó cresce para a esquerda)

                    """
                                ANTES (Zigue-Zague)                  DEPOIS (Transformado em Linha Reta)
                            ===================                  ===================================

                                Avô(P)                               Avô(P)
                                /      \                             /      \
                            Pai(V)    Tio(P)         ====>     Pai(V)      Tio(P)  <-- (Antigo nó inserido)
                                \                               /
                                [N](V)                        [N](V)                <-- (Antigo Pai)

                                 (O ponteiro desceu com a rotação)
                    
                 
                    
                    """
                    if nodo == getLeft(pai):
                        nodo = pai
                        self.right_rotate(nodo)
                        
                        # Recalcula ponteiros pois a rotação mudou as posições locais
                        pai = getFather(nodo) #filho antigo 
                        avo = getFather(pai) # avo
                    
                    # CASO 3: Topologia em Linha Reta (Nó e pai estão na direita)
                    pai.cor = "P"
                    avo.cor = "V"
                    self.left_rotate(avo)
                
        # Garantia final: A raiz da árvore deve ser sempre preta
        self.root.cor = "P" 
        
    def remover_fixup(self,x):
        #preciso entender melhor como funciona a remoção
        pass