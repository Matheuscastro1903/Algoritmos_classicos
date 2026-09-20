from ..semana1.arvorebinaria import (
    ArvoreBinaria,
    Nodo,
    getInfo,
    getLeft,
    getRight,
    getFather,
)



class ArvoreBinariaAVL(ArvoreBinaria):
    def __init__(self):
        # Aciona o construtor da classe pai para criar o self.root
        super().__init__()
        
    # ==========================================
    # MÓDULOS EXCLUSIVOS DA AVL
    # ==========================================
    # def altura(self, nodo): ...
    # def fator_balanceamento(self, x): ...
    # def left_rotate(self, x): ...
    # def right_rotate(self, x): ...
    # def balancear(self, nodo): ...
    # def varrer_e_consertar(self, nodo): ...

    def inserir(self, valor):
        #Delega o trabalho para a classe pai
        # A classe pai insere o valor e já devolve a identidade física do nodo
        novo_nodo = super().inserir(valor)

    # A AVL aciona a sua matemática exclusiva de balanceamento
        if novo_nodo is not None:
            self.varrer_e_consertar(novo_nodo)
        
    def remover(self, x):
        # TODO: Descobrir o ponto de partida do conserto
        #ponto de partida seria no caso 1 e 2(o pai do nodo excluido) e no caso 3(o pai do sucessor 
        #nodo excluido)
        ponto_de_partida = super().remover(x)
        
        # Se a árvore não ficou completamente vazia, inicia o conserto de baixo para cima
        if ponto_de_partida is not None:
            self.varrer_e_consertar(ponto_de_partida)


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
    #       None             30
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
        
    # 5. O rebaixamento final do pivô.
    # O 10 é empurrado para baixo, tornando-se oficialmente o filho esquerdo do 20.
        
    
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

        #o filho esquerdo de x irá se tornar o filho direito de y
        x.esquerda=getRight(y)
        #o filho direito de y agora é o filho esquerdo de x
        if getRight(y) is not None:
            getRight(y).pai=x

        #pai de y agora é o pai de x
        y.pai = getFather(x)
            
        #se o pai de x é none,então ele é raiz
        if getFather(x) is None:
            #atualizando a raiz
            self.root = y
        elif x == getLeft(getFather(x)): #se x é o filho esquerdo do pai então agora y é o filho esquerdo do pai de x
            getFather(x).esquerda = y
        else:
            #se x é o filho direito do pai,então agora y é o filho direito do pai de x
            getFather(x).direita = y

        #filho direita de y aogra é x
        y.direita=x
        #pai de x agora é y
        x.pai=y

    def altura(self, nodo):
        #esse aqui é o ponto de parada para identificar quando for uma folha
        #o algoritmo não consegue saber quando é folha,então mesmo assim chama a função recursiva
        #quando encontrar o máximo,caso ambos os caso sejam de folha,o resultado será 0 já que será -1 +1
        if nodo is None:
            return -1

        #(Explorando todas as rotas internas simultaneamente)
        # O algoritmo pausa neste nodo e manda inspeções para a esquerda e para a direita.
        altura_esq = self.altura(getLeft(nodo))
        altura_dir = self.altura(getRight(nodo))

    # 3. A Resposta Matemática
    # Ao receber o relatório dos dois lados, ele escolhe o caminho mais longo e soma 1 (contando a si mesmo).
        return max(altura_esq, altura_dir) + 1

    def fator_balanceamento(self,x):
        #fator de balanceamento é a diferença de duas alturas
        filhoesq=getLeft(x)
        filhodir=getRight(x)

        return self.altura(filhodir)-self.altura(filhoesq)

    def balancear(self, nodo):
        fb = self.fator_balanceamento(nodo)

    # Cenário A: Peso excessivo à Direita (+2)
        if fb > 1:
        # Avalia o filho direito para descobrir a topologia
            fb_filho = self.fator_balanceamento(getRight(nodo))
        
        # Se o filho pende para a esquerda (-1), é um Zigue-Zague
            if fb_filho < 0:
                self.right_rotate(getRight(nodo)) # 1º Passo: Desdobra a articulação
        
        # 2º Passo: Rotação corretiva final no nodo pai
            self.left_rotate(nodo)

    # Cenário B: Peso excessivo à Esquerda (-2)
        elif fb < -1:
        # Avalia o filho esquerdo para descobrir a topologia
            fb_filho = self.fator_balanceamento(getLeft(nodo))
        
        # Se o filho pende para a direita (+1), é um Zigue-Zague
            if fb_filho > 0:
                self.left_rotate(getLeft(nodo)) # 1º Passo: Desdobra a articulação
        
        # 2º Passo: Rotação corretiva final no nodo pai
            self.right_rotate(nodo)

    def varrer_e_consertar(self, nodo):
        # A subida que você imaginou, engatilhada logo após conectar o novo nodo
        atual = nodo
        while atual is not None:
            self.balancear(atual)
            atual = getFather(atual)


    
    


if __name__ == "__main__":
    print("=====================================================")
    print(" INICIANDO BATERIA DE TESTES - ÁRVORE AVL ")
    print("=====================================================\n")

    # ==========================================
    # TESTE 1: Inserção - Rotação Simples à Direita (Peso à Esquerda)
    # Cenário: Inserir 30, 20, 10 (Linha reta caindo para a esquerda)
    # ==========================================
    avl_esq = ArvoreBinariaAVL()
    avl_esq.inserir(30)
    avl_esq.inserir(20)
    avl_esq.inserir(10) # Causa desbalanceamento no 30 (-2)
    
    assert getInfo(avl_esq.root) == 20
    assert getInfo(getLeft(avl_esq.root)) == 10
    assert getInfo(getRight(avl_esq.root)) == 30
    print("✅ TESTE 1 PASSOU: Rotação Simples à Direita funcionou.")


    # ==========================================
    # TESTE 2: Inserção - Rotação Simples à Esquerda (Peso à Direita)
    # Cenário: Inserir 10, 20, 30 (Linha reta subindo para a direita)
    # ==========================================
    avl_dir = ArvoreBinariaAVL()
    avl_dir.inserir(10)
    avl_dir.inserir(20)
    avl_dir.inserir(30) # Causa desbalanceamento no 10 (+2)
    
    assert getInfo(avl_dir.root) == 20
    assert getInfo(getLeft(avl_dir.root)) == 10
    assert getInfo(getRight(avl_dir.root)) == 30
    print("✅ TESTE 2 PASSOU: Rotação Simples à Esquerda funcionou.")


    # ==========================================
    # TESTE 3: Inserção - Rotação Dupla (Zigue-Zague Esquerda-Direita)
    # Cenário: Inserir 30, 10, 20
    # ==========================================
    avl_zig_esq = ArvoreBinariaAVL()
    avl_zig_esq.inserir(30)
    avl_zig_esq.inserir(10)
    avl_zig_esq.inserir(20) # Causa desbalanceamento no 30 (-2), mas 10 pende para a direita (+1)
    
    assert getInfo(avl_zig_esq.root) == 20
    assert getInfo(getLeft(avl_zig_esq.root)) == 10
    assert getInfo(getRight(avl_zig_esq.root)) == 30
    print("✅ TESTE 3 PASSOU: Rotação Dupla (Esquerda-Direita) funcionou.")


    # ==========================================
    # TESTE 4: Remoção - Caso 1 (Folha) Acionando Balanceamento
    # Cenário: Inserir 20, 10, 30, 40. Remover 10.
    # O nodo 20 ficará desbalanceado (+2) e forçará uma rotação à esquerda.
    # ==========================================
    avl_rem_folha = ArvoreBinariaAVL()
    for v in [20, 10, 30, 40]:
        avl_rem_folha.inserir(v)
    
    # Remove a folha 10 (Caso 1)
    avl_rem_folha.remover(avl_rem_folha.searchBinaria(avl_rem_folha.root, 10))
    
    # A raiz original (20) desbalanceou. O 30 deve assumir a raiz.
    assert getInfo(avl_rem_folha.root) == 30
    assert getInfo(getLeft(avl_rem_folha.root)) == 20
    assert getInfo(getRight(avl_rem_folha.root)) == 40
    print("✅ TESTE 4 PASSOU: Remoção (Caso 1) acionou rebalanceamento perfeito.")


    # ==========================================
    # TESTE 5: Remoção - Caso 3 (Dois Filhos) e Validação de Ponteiros
    # Cenário: Inserir 50, 30, 70, 20, 40, 60, 80.
    # Remover 50 (a raiz). O sucessor 60 deve assumir e a árvore não deve quebrar.
    # ==========================================
    avl_rem_raiz = ArvoreBinariaAVL()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        avl_rem_raiz.inserir(v)
        
    # Remove a raiz 50 (Caso 3)
    avl_rem_raiz.remover(avl_rem_raiz.root)
    
    nova_raiz = avl_rem_raiz.root
    assert getInfo(nova_raiz) == 60
    assert getInfo(getLeft(nova_raiz)) == 30
    assert getInfo(getRight(nova_raiz)) == 70
    
    # Valida se o 70 perdeu o filho 60 que subiu (o bypass do sucessor imediato)
    assert getInfo(getLeft(getRight(nova_raiz))) is None
    print("✅ TESTE 5 PASSOU: Remoção da Raiz (Caso 3) funcionou.")


    # ==========================================
    # TESTE 6: Proteção contra Árvore Vazia
    # Cenário: Remover a última folha existente na árvore
    # ==========================================
    avl_vazia = ArvoreBinariaAVL()
    avl_vazia.inserir(100)
    avl_vazia.remover(avl_vazia.root)
    
    assert avl_vazia.root is None
    print("✅ TESTE 6 PASSOU: Árvore limpa com sucesso sem gerar erros.")

    print("\n=====================================================")
    print(" TODOS OS TESTES PASSARAM! A ÁRVORE AVL ESTÁ ESTÁVEL. ")
    print("=====================================================")


"""
#a soma só irá começar a ser feita quando o valor for none
A Altura do nodo 40 é o comprimento topológico da maior rota abaixo dele (3 conexões de distância até chegar ao fundo).

O Fator de Balanceamento (FB) é a subtração executada após as alturas serem reveladas: Altura da Direita (2) menos Altura da Esquerda (0).
                40(x)
              /      \
            20       60 
                    /      \
                50        80
                              \
                               90

#explicando interações de baixo para cima


#LADO ESQUERDO
- os filhos de 20 são none,tendo como retorno igual a 0,não iremos usar esse lado até o outro chegar no mesmo floor

#LADO DIREITO
- os filhos de 90 são none retornando 0
- os filhos de 80 são 0 e -1(já que um deles é none),tendo como resultado final +1 já que 0 seria maior e no fim somamos +1
- os filhos de 60 retornam 0 do lado do 50 e +1 do lado do 80-->resultando em +2  no final


#comparação final
- agora iremos comparar o filho esquerdo do 40(resultado igual a 0) e o filho direito(resultado igual a +2)
-escolhendo o máximo,resulta em +2,entretanto ainda faltaria soma +1


#COMO IDENTIFICAR QUANDO USAR ROTAÇÂO A ESQUERDA OU A DIREITA

Quando o nodo pai acusa o colapso estrutural (retornando +2 ou -2), você simplesmente chama o 
fator_balanceamento novamente, mas desta vez passando o nodo filho correspondente. O choque entre os sinais 
matemáticos (positivo e negativo) revela exatamente para qual lado a ramificação dobrou.

Mapeamento das Rotações via Sinais

Pai (+2) e Filho Direito (+1 ou 0): As duas gerações pendem para o lado direito, 
formando uma linha reta. Exige uma Rotação Simples à Esquerda no nodo pai.

Pai (+2) e Filho Direito (-1): O pai pende para a direita, 
mas o peso do filho dobra de volta para a esquerda, formando o zigue-zague. Exige a Rotação Dupla (primeiro um giro à direita no filho, depois um giro à esquerda no pai).

Pai (-2) e Filho Esquerdo (-1 ou 0): Ambas as gerações pendem para a esquerda (linha reta). 
Exige uma Rotação Simples à Direita no nodo pai.

Pai (-2) e Filho Esquerdo (+1): O pai pende para a esquerda, mas o filho dobra para a direita (zigue-zague). 
Exige a Rotação Dupla (primeiro um giro à esquerda no filho, depois um giro à direita no pai).


O processo de balanceamento de uma árvore AVL não é uma varredura de manutenção periódica que 
avalia a estrutura inteira de uma só vez. Ele atua como um sistema de reação instantânea focado 
exclusivamente no trajeto que acabou de sofrer uma alteração física, baseando-se nos fundamentos teóricos do seu material de algoritmos.

A Estabilidade Prévia

Antes de qualquer nova ação, a árvore inteira já está perfeitamente equilibrada. 
Não existe a necessidade de procurar e recalcular os outros lados da estrutura, pois a topologia dos galhos distantes permanece intacta.

O Gatilho de Partida
O potencial colapso estrutural ocorre no exato segundo em que o seu método inserir conecta um novo valor no final de um galho.

É esse nodo recém-adicionado (e exclusivamente ele) que é injetado diretamente na função varrer_e_consertar(novo_nodo).

A Rota Única de Inspeção

A varredura corretiva não procura por outras folhas perdidas na estrutura. 
Ela utiliza os ponteiros pai para escalar uma única rota contínua: do nodo que acabou de nascer direto para o topo da raiz.

Apenas os ancestrais diretos desse novo nodo podem ter sofrido um acúmulo de peso lateral. 
O resto da árvore é sumariamente ignorado, o que garante a velocidade de processamento exigida pela estrutura.

Para realizar o conserto, o algoritmo reage apenas ao evento imediato na trilha específica afetada


"""