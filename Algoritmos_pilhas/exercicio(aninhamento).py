"""
Analisar a complexidade de tempo de execução de um algoritmo é uma tarefa muito importante
para a criação de programas eficientes. Um algoritmo que executa em tempo linear é geralmente
muito mais rápido que um algoritmo que necessita de tempo exponencial para a mesma tarefa.

Geralmente, o tempo de execução de um algoritmo é definido de acordo com o tamanho N da
entrada, onde N pode ser a quantidade de elementos a serem ordenados, o número de pontos de
determinado polígono e assim por diante.

Descobrir uma fórmula para o tempo de execução em função de N não é uma tarefa simples e seria
muito bom se isso fosse automatizado. Infelizmente, isto em geral não é possível, mas neste
exercício você irá considerar programas de natureza simples e poderá determinar a quantidade de
operações de um programa com precisão.

Exercício:

Considere que um analista traduziu um programa anotando a quantidade de repetições dos loops e
que ele decidiu contar somente algumas instruções mais custosas com relação à quantidade de
tempo que cada operação (instrução) necessita. As instruções custosas consideradas pelo analista
foram as listadas a seguir:
IO (instrução de entrada e saída: 30 unidades de tempo),
MEM (acesso à memória: 10 unidades de tempo),
PROCSUM (instrução de processamento: 1 unidade de tempo),
PROCMULT (instrução de processamento: 10 unidades de tempo)
LOOP X (instrução de repetição de um bloco de comandos, repete X vezes todas as
instruções que estivem entre o LOOP e o respectivo FIMLOOP).

Seu programa deverá considerar as anotações do analista de acordo com a descrição abaixo e
calcular a complexidade total em unidades de tempo:
A entrada deverá iniciar com a palavra INICIO e terminar com a palavra FIM;
A entrada poderá ter instruções custosas e loops;
A entrada poderá usar estruturas de repetição (loop) para repetir um bloco de comandos internos por determinada quantidade de vezes, e este bloco de comandos pode ter outros loops internos até 2 níveis de profundidade (isto é, somente haverá 2 níveis de aninhamento de loops). Um loop deverá iniciar com a palavra LOOP seguida de um número inteiro indicando a quantidade de vezes que ele repetirá o bloco de comandos interno. Portanto, logo após o número haverá um bloco de comandos com instruções custosas (que podem incluir outros loops) e o loop será finalizado com a palavra FIMLOOP. Observe o exemplo abaixo:
INICIO
IO
LOOP 2
    MEM
    PROCMULT
FIMLOOP
PROCSUM
LOOP 4
    IO
FIMLOOP
PROCMULT
LOOP 3
    MEM
FIMLOOP
IO
FIM


4. O programa também pode ter outros loops no mesmo nível, desde que estejam após o fechamento do loop anterior.

REGRA GERAL: 
Você deverá utilizar python 3. Sempre que um novo loop for fechado, a quantidade de operações custosas que foi somada dentro dele deverá ser multiplicada pela quantidade de vezes que o loop executou e este valor deverá ser adicionado a uma variável somadora geral.

Formato de Entrada do seu programa:
A entrada contém um pseudo código que é construído de acordo com as regras acima. Espaços em
branco, tabulações (\t) e quebras de linha (\r e \n) podem aparecer em qualquer local do programa e
devem ser desconsiderados. Por questões técnicas da plataforma de testes, toda a entrada será lida
em uma única linha (sem “enter”).
Formato de Saída do seu programa:
A saída deverá exibir o tempo de execução total como um número inteiro. Este total considera o
somatório de todas as operações custosas do programa de entrada.


"""





import sys

entrada = sys.stdin.read()

valores = entrada.split()

valores.pop(0)
valores.pop(-1)



pilha = []
#a pilha funcionará como uma lista de dicionários


total = 0
i = 0



while i < len(valores):   # vou usar while aqui só pra ilustrar os pulos
    valor_atual = valores[i]

    if valor_atual == "IO":
        custo = 30
        
        if pilha: #se a pilha estiver com algo
            
            pilha[-1]["custo"] += custo
        
        else: #caso contrário,se a pilha estiver vazia,somará ao valor total 
            total += custo
        i += 1

    elif valor_atual == "MEM":
        custo = 10
        if pilha:
            pilha[-1]["custo"] += custo
        else:
            total += custo
        i += 1

    elif valor_atual == "PROCSUM":
        custo = 1
        if pilha:
            pilha[-1]["custo"] += custo
        else:
            total += custo
        i += 1

    elif valor_atual == "PROCMULT":
        custo = 10
        if pilha:
            pilha[-1]["custo"] += custo
        else:
            total += custo
        i += 1

    elif valor_atual == "LOOP":
        valor_loop = int(valores[i + 1])  # pega o próximo
        pilha.append({"valor_loop": valor_loop, "custo": 0})
        i += 2   # pula LOOP e o número

    elif valor_atual == "FIMLOOP":
        bloco = pilha.pop() #pega o último elemento da lista(o último loop)
        #pega os valores dos dicionário de custo e valor loop e multiplica
        custo_total_bloco = bloco["custo"] * bloco["valor_loop"]

        if pilha: #caso ainda exista algum loop,vai somar o valor do custo total do bloco como valor do custo do último loop da lista
            pilha[-1]["custo"] += custo_total_bloco
        else:
            #caso contrário,já soma com o valor total mesmo
            total += custo_total_bloco
        i += 1

print(total)