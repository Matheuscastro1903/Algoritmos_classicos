class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.pai = None


def getInfo(p):
    return p.valor if p is not None else None

def getLeft(p):
    return p.esquerda if p is not None else None

def getRight(p):
    return p.direita if p is not None else None

def getFather(p):
    return p.pai if p is not None else None


class ArvoreBinaria:
    def __init__(self):
        self.root = None

    def inserir(self, valor):
        novo_nodo = Nodo(valor)
        y = None
        x = self.root

        #só vai entrar aqui se x  não for none,ou seja,se a raiz já existir
        while x is not None:
            #y é o controlador do valor da raiz do nível da interação
            y = x
            #o if else abaixo irá pegar até x for um valor none,e assim sairá do loop
            if getInfo(novo_nodo) < getInfo(x):
                #irá pegar o filho esquerdo de x
                x = getLeft(x)
            else:
                #irá pegar o filho direito de x
                x = getRight(x)
        
        #seta o valor de y= valor da raiz do nível como pai do novo nodo
        novo_nodo.pai = y

        if y is None:
            #se y estiver como none=então atribui para raiz que não existe ainda
            self.root = novo_nodo
            #se for menor,o valor do filho da esquerda de y é o novo nodo,caso contrário é o filho da direita
        elif getInfo(novo_nodo) < getInfo(y):
            y.esquerda = novo_nodo
        else:
            y.direita = novo_nodo

        return novo_nodo

    def minimum(self, x):
    #essa função busca procurar o min a partirr de um nodo específico ou subnodo,não precisando passar sempre a raiz
    # Proteção caso a árvore não tenha sido populada ainda
    #irá descendo até encontrar
        if x is None:
            return None
        
    #vai pegar o filho esquerdo de x até encontrar none
        while getLeft(x) is not None:
            x = getLeft(x)
        
        return x # Retorna o objeto Nodo encontrado

    def maximum(self,x):
        #função irá buscar o max de um nodo específico

        if x is None:
            return None

        while getRight(x) is not None:
            x=getRight(x)

        return x

    def searchBinaria(self,x,k):
        #x(passa o objeto todo)é o nodo de partida e o k é o valor que quer buscar
        #add contador para ver quantas interações devem ser feitas
        # o número de interações máximas deve ser o log da quantidade de elementos da lista na base 2

        contador=0
        

        while x is not None and getInfo(x) != k:
            

            if getInfo(x)>k:
                x=getLeft(x)

            elif getInfo(x)<k:
                x=getRight(x)

            contador+=1

        # Fora do laço, avaliamos o motivo da parada:
        if x is None:
            print(f'-> Não encontrado. Interações={contador}')
        else:
            print(f'-> Encontrado! Interações={contador}')
            
        return x  # Retorna o Nodo ou None

    def sucessor(self,x):

        #caso 1 tem filho na direita e usa a função de minimo até encontrar none
        if getRight(x) is not None:
            #pega o minimo do getright pq na lógica seria o sucessor do seu escolhido,isso se o getright realmente tiver mínimo
            return self.minimum(getRight(x))



        #caso 2: sem filho na direita,então irá subir até o dobrar de esquerda para direita
        y = getFather(x)
        
        #sempre vai ser menor até dobrar para direita
        #sempre vai ser menor até ter um none
        while y is not None and x == getRight(y):
            x = y
            y = getFather(y)
            
        return y


    def antecessor(self,x):
        #caso 1=tem filho na esquerda

        if getLeft(x) is not None:
            #irá pegar o máximo da esquerda
            return self.maximum(getLeft(x))


        #caso 2= não tem filho,irá subir até dobrar da direita para a esquerda
        y=getFather(x)

        while y is not None and x==getLeft(y):
            x=y
            y=getFather(y)

        return y

    def remover(self,x):
        #caso 1-->nodo está na base da árvore(é uma folha)
        #Ação: Basta avisar ao pai desse nodo que ele não tem mais aquele filho, 
        # alterando o ponteiro do pai direto para nulo. O nodo alvo fica isolado e o espaço de memória é liberado.

        if getLeft(x) is None and getRight(x) is None:
            y = getFather(x)
            pai_antigo=getFather(x)
            
            # Proteção: Se a folha não tem pai, ela é a única raiz da árvore
            if y is None:
                self.root = None #reinicia a raiz
                
            #Desconectando a folha da ramificação correta do pai
            elif getLeft(y) == x:
                y.esquerda = None
            else:
                y.direita = None


            #O pai do nodo que foi fisicamente excluído
            return pai_antigo

        #caso 2-->nodo possui exatamente um filho(nodo ponte)
        #Ação: Realizamos um "bypass" estrutural. Desconectamos o nodo alvo e ligamos o pai 
        # dele diretamente ao único neto existente. A árvore se "encolhe" preenchendo o buraco automaticamente.

        #uso de ou exclusivo
        elif (getLeft(x) is not None) ^ (getRight(x) is not None):
            
            #Isola quem é o único neto sobrevivente
            if getLeft(x) is not None:
                filho = getLeft(x)
            else:
                filho = getRight(x)

            #pai de x
            y = getFather(x)
            pai_antigo=getFather(x)
            
            #filho de x agora referencia o avô(pai de x)
            filho.pai = y
            
            #verifica se o pai não é None(evitando que x fosse raiz)
            if y is None:
                #se for o filho vira raiz
                self.root = filho
            elif x == getLeft(y):
                y.esquerda = filho
            else:
                y.direita = filho

            #O pai do nodo que foi fisicamente excluído
            return pai_antigo

    # ==========================================
            # CASO 3: O Nodo completo (possui 2 filhos)
            # Baseado na arquitetura exigida pela literatura[cite: 1]
            # ==========================================
            # ESTADO INICIAL (Exemplo: Removendo o 50):
            #           [50] (x) <-- ALVO DA REMOÇÃO
            #          /    \
            #       [20]    [80] (pai_original_y)
            #              /    \
            #   (y) ->  [60]    [90]
            #             \
            #             [70] (filho_dir_y)
            # ==========================================
        elif getLeft(x) is not None and getRight(x) is not None:
                
                # 1. Encontra o sucessor (y) e o pai original dele
                # O sucessor é matematicamente o menor valor da subárvore direita[cite: 1].
                y = self.sucessor(x)
                pai_original_y = getFather(y)
                pai_antigo=getFather(x)

                # 2. Isola o sucessor (O "Bypass" Interno)
                # Se 'y' não for o filho imediato de 'x', ele precisa ser solto sem perder seu filho direito[cite: 1].
                if pai_original_y != x:
                    filho_dir_y = getRight(y)
                    
                    # O pai original (80) adota o filho direito de y (70)
                    pai_original_y.esquerda = filho_dir_y
                    if filho_dir_y is not None:
                        filho_dir_y.pai = pai_original_y
                    
                    # ==========================================
                    # ESTADO APÓS O BYPASS:
                    #           [50] (x)
                    #          /    \
                    #       [20]    [80] 
                    #              /    \
                    #            [70]   [90]
                    # 
                    #   [60] (y) -> flutuando na memória
                    # ==========================================
                    
                    # O sucessor (60) assume toda a subárvore direita original do alvo (50)[cite: 1]
                    y.direita = getRight(x)
                    y.direita.pai = y

                # ==========================================
                # ESTADO PREPARADO PARA A GRANDE SUBSTITUIÇÃO:
                #           [50] (x)
                #          /    
                #       [20]      [60] (y)
                #                   \
                #                   [80] 
                #                  /    \
                #                [70]   [90]
                # ==========================================

                # 3. A Grande Substituição no Topo
                # O sucessor 'y' (60) assume o braço esquerdo intacto de 'x' (20)[cite: 1]
                y.esquerda = getLeft(x)
                y.esquerda.pai = y
                
                # 'y' se conecta ao teto (ao antigo pai de 'x')[cite: 1]
                pai_x = getFather(x)
                y.pai = pai_x

                # Oficializa o sucessor na posição exata que o alvo ocupava[cite: 1]
                if pai_x is None:
                    self.root = y
                elif x == getLeft(pai_x):
                    pai_x.esquerda = y
                else:
                    pai_x.direita = y
                    
                # ==========================================
                # ESTADO FINAL DA ÁRVORE:
                #           [60] (y) <-- O NOVO LÍDER ASSUME
                #          /    \
                #       [20]    [80] 
                #              /    \
                #            [70]   [90]
                # (O 50 é deletado da memória)
                # ==========================================


                #PARA O CASO 3,RETORNARMOS
                #O pai original do sucessor (ou o próprio sucessor, 
                # caso ele fosse o filho imediato do nodo alvo).
                return pai_original_y if pai_original_y != x else y

        


        

        
        


if __name__ == "__main__":
    arvore = ArvoreBinaria()
    
    # 1. Inserindo a raiz
    arvore.inserir(15)
    print(f"Raiz da árvore: {getInfo(arvore.root)}")
    
    arvore.inserir(6)
    arvore.inserir(3)
    arvore.inserir(7)
    arvore.inserir(18)
    arvore.inserir(17)
    arvore.inserir(20)
    
    # 4. Validando se as conexões de ponteiros deram certo
    raiz = arvore.root
    filho_esq = getLeft(raiz)
    filho_dir = getRight(raiz)
    
    print(f"Filho esquerdo da raiz (esperado 6): {getInfo(filho_esq)}")
    print(f"Filho direito da raiz (esperado 18): {getInfo(filho_dir)}")
    
    # 5. Validando se o ponteiro de volta (pai) funcionou
    pai_do_esq = getFather(filho_esq)
    print(f"Pai do nodo 6 (esperado 15 - raiz): {getInfo(pai_do_esq)}")
    
    # 6. Validando um "neto" (filho direito do nodo 6)
    neto = getRight(filho_esq)
    print(f"Filho direito do nodo 6 (esperado 7): {getInfo(neto)}")

    # ==========================================
    # NOVOS TESTES: MÍNIMO E MÁXIMO
    # ==========================================
    print("\n--- Testes de Mínimo e Máximo ---")
    
    # 7. Testando o mínimo da árvore inteira (partindo da raiz)
    minimo_total = arvore.minimum(arvore.root)
    print(f"Mínimo da árvore inteira (esperado 3): {getInfo(minimo_total)}")
    
    # 8. Testando o máximo da árvore inteira (partindo da raiz)
    maximo_total = arvore.maximum(arvore.root)
    print(f"Máximo da árvore inteira (esperado 20): {getInfo(maximo_total)}")
    
    # 9. Testando mínimo de uma sub-árvore (partindo do nodo 18)
    minimo_sub = arvore.minimum(filho_dir)
    print(f"Mínimo da sub-árvore direita (esperado 17): {getInfo(minimo_sub)}")
    
    # 10. Testando máximo de uma sub-árvore (partindo do nodo 6)
    maximo_sub = arvore.maximum(filho_esq)
    print(f"Máximo da sub-árvore esquerda (esperado 7): {getInfo(maximo_sub)}")


    # ==========================================
    # NOVOS TESTES: BUSCA BINÁRIA
    # ==========================================
    print("\n--- Testes de Busca ---")
    
    # 11. Testando busca por um número que EXISTE na árvore
    print("Teste A: Buscando o número 18 (deve encontrar)")
    nodo_encontrado = arvore.searchBinaria(arvore.root, 18)
    if nodo_encontrado is not None:
        print(f"Sucesso: O objeto Nodo retornado contém o valor {getInfo(nodo_encontrado)}")
    
    # 12. Testando busca por um número que NÃO EXISTE na árvore
    print("\nTeste B: Buscando o número 99 (não deve encontrar)")
    nodo_nao_encontrado = arvore.searchBinaria(arvore.root, 99)
    if nodo_nao_encontrado is None:
        print("Sucesso: A função retornou None corretamente para um valor inexistente")

    # ==========================================
    # NOVOS TESTES: SUCESSOR E ANTECESSOR
    # ==========================================
    print("\n--- Testes de Sucessor e Antecessor ---")

    # 13. Sucessor com filho direito: mínimo da sub-árvore direita
    sucessor_com_filho = arvore.sucessor(filho_esq)
    assert getInfo(sucessor_com_filho) == 7
    print(f"Sucessor de 6 (esperado 7): {getInfo(sucessor_com_filho)}")

    # 14. Sucessor sem filho direito: sobe até encontrar um pai maior
    nodo_7 = getRight(filho_esq)
    sucessor_subindo = arvore.sucessor(nodo_7)
    assert getInfo(sucessor_subindo) == 15
    print(f"Sucessor de 7 (esperado 15): {getInfo(sucessor_subindo)}")

    # 15. Maior nodo da árvore: não possui sucessor
    nodo_20 = getRight(filho_dir)
    sucessor_maximo = arvore.sucessor(nodo_20)
    assert sucessor_maximo is None
    print(f"Sucessor de 20 (esperado None): {getInfo(sucessor_maximo)}")

    # 16. Antecessor com filho esquerdo: máximo da sub-árvore esquerda
    antecessor_com_filho = arvore.antecessor(filho_dir)
    assert getInfo(antecessor_com_filho) == 17
    print(f"Antecessor de 18 (esperado 17): {getInfo(antecessor_com_filho)}")

    # 17. Antecessor sem filho esquerdo: sobe até encontrar um pai menor
    nodo_17 = getLeft(filho_dir)
    antecessor_subindo = arvore.antecessor(nodo_17)
    assert getInfo(antecessor_subindo) == 15
    print(f"Antecessor de 17 (esperado 15): {getInfo(antecessor_subindo)}")

    # 18. Menor nodo da árvore: não possui antecessor
    nodo_3 = getLeft(filho_esq)
    antecessor_minimo = arvore.antecessor(nodo_3)
    assert antecessor_minimo is None
    print(f"Antecessor de 3 (esperado None): {getInfo(antecessor_minimo)}")

    # ==========================================
    # NOVOS TESTES: REMOÇÃO - CASOS 1 E 2
    # ==========================================
    print("\n--- Testes de Remoção ---")

    # 19. Caso 1: remoção de uma folha à esquerda
    arvore_remocao_folha = ArvoreBinaria()
    arvore_remocao_folha.inserir(10)
    arvore_remocao_folha.inserir(5)
    arvore_remocao_folha.remover(getLeft(arvore_remocao_folha.root))
    assert getLeft(arvore_remocao_folha.root) is None
    print("Caso 1: folha removida corretamente")

    # 20. Caso 1: remoção da única raiz, que também é uma folha
    arvore_remocao_raiz = ArvoreBinaria()
    arvore_remocao_raiz.inserir(10)
    arvore_remocao_raiz.remover(arvore_remocao_raiz.root)
    assert arvore_remocao_raiz.root is None
    print("Caso 1: raiz removida corretamente")

    # 21. Caso 2: nó com um filho à esquerda
    arvore_um_filho_esq = ArvoreBinaria()
    arvore_um_filho_esq.inserir(10)
    arvore_um_filho_esq.inserir(5)
    arvore_um_filho_esq.inserir(3)
    arvore_um_filho_esq.remover(getLeft(arvore_um_filho_esq.root))
    assert getInfo(getLeft(arvore_um_filho_esq.root)) == 3
    assert getFather(getLeft(arvore_um_filho_esq.root)) is arvore_um_filho_esq.root
    print("Caso 2: nó com filho esquerdo removido e filho reconectado")

    # 22. Caso 2: nó com um filho à direita
    arvore_um_filho_dir = ArvoreBinaria()
    arvore_um_filho_dir.inserir(10)
    arvore_um_filho_dir.inserir(15)
    arvore_um_filho_dir.inserir(20)
    arvore_um_filho_dir.remover(getRight(arvore_um_filho_dir.root))
    assert getInfo(getRight(arvore_um_filho_dir.root)) == 20
    assert getFather(getRight(arvore_um_filho_dir.root)) is arvore_um_filho_dir.root
    print("Caso 2: nó com filho direito removido e filho reconectado")

    # 23. Caso 2: remoção da raiz com um único filho
    arvore_raiz_um_filho = ArvoreBinaria()
    arvore_raiz_um_filho.inserir(10)
    arvore_raiz_um_filho.inserir(5)
    arvore_raiz_um_filho.remover(arvore_raiz_um_filho.root)
    assert getInfo(arvore_raiz_um_filho.root) == 5
    assert getFather(arvore_raiz_um_filho.root) is None
    print("Caso 2: raiz substituída pelo único filho")




    # ==========================================
    # TESTE 1: Caso 3 na Raiz com sucessor "enterrado"
    # O 50 sai. O 60 (sucessor) sobe. O buraco físico fica onde o 60 estava.
    # O pai original do 60 era o 80. Logo, o retorno deve ser o 80.
    # ==========================================
    arvore_caso3_bypass = ArvoreBinaria()
    for v in [50, 20, 80, 60, 90, 70]:
        arvore_caso3_bypass.inserir(v)
        
    ponto_partida_1 = arvore_caso3_bypass.remover(arvore_caso3_bypass.root)
    
    # Validações da nova coroa
    assert getInfo(arvore_caso3_bypass.root) == 60
    assert getInfo(getLeft(arvore_caso3_bypass.root)) == 20
    assert getInfo(getRight(arvore_caso3_bypass.root)) == 80
    assert getFather(arvore_caso3_bypass.root) is None
    
    # Validação do Bypass
    nodo_80 = getRight(arvore_caso3_bypass.root)
    assert getInfo(getLeft(nodo_80)) == 70
    
    # Validação da Modularização (O retorno aponta para o lugar certo?)
    assert getInfo(ponto_partida_1) == 80
    print("Caso 3 (Teste 1): Raiz removida. Retorno correto aponta para o nodo 80.")


    # ==========================================
    # TESTE 2: Caso 3 na Raiz com sucessor sendo o filho imediato
    # O 50 sai. O 70 (sucessor e filho imediato) sobe.
    # Como o 70 assumiu o lugar e o buraco era o antigo braço direito dele próprio, o retorno deve ser o 70.
    # ==========================================
    arvore_caso3_imediato = ArvoreBinaria()
    for v in [50, 20, 70, 80]:
        arvore_caso3_imediato.inserir(v)
        
    ponto_partida_2 = arvore_caso3_imediato.remover(arvore_caso3_imediato.root)
    
    # Validações estruturais
    assert getInfo(arvore_caso3_imediato.root) == 70
    assert getInfo(getLeft(arvore_caso3_imediato.root)) == 20
    assert getInfo(getRight(arvore_caso3_imediato.root)) == 80
    
    # Validação da Modularização
    assert getInfo(ponto_partida_2) == 70
    print("Caso 3 (Teste 2): Raiz removida. Retorno correto aponta para o nodo 70.")


    # ==========================================
    # TESTE 3: Caso 3 em um Nodo Interno (Galho esquerdo)
    # Alvo: 50. Sucessor: 60. Pai original do 60: 80.
    # ==========================================
    arvore_caso3_interno = ArvoreBinaria()
    for v in [100, 50, 150, 20, 80, 60, 90, 70]:
        arvore_caso3_interno.inserir(v)
        
    alvo_interno = getLeft(arvore_caso3_interno.root) # Captura o nodo 50
    ponto_partida_3 = arvore_caso3_interno.remover(alvo_interno)
    
    # Validações estruturais
    novo_filho_esq_raiz = getLeft(arvore_caso3_interno.root)
    assert getInfo(novo_filho_esq_raiz) == 60
    assert getInfo(getLeft(novo_filho_esq_raiz)) == 20
    assert getInfo(getRight(novo_filho_esq_raiz)) == 80
    
    # Validação da Modularização
    assert getInfo(ponto_partida_3) == 80
    print("Caso 3 (Teste 3): Nodo interno removido. Retorno correto aponta para o nodo 80.")