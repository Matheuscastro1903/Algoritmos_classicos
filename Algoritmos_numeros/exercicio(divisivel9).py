def divisivel_nove(n):
    if n==9 or n==0:
        return "É divisível"
    if n<9 and n!=0:
        #caso o valor da soma seja menor que 9,então já sabemos que não é divisível
        return "Não é divisível"
    else:
        lista_numeros=[]
        #para transformar um número inteiro em lista precisa interar com um for,transformando primeiro a 
        #entrada em string e retransformando em inteiro no loop
        
        for i in str(n):
            i=int(i)
            lista_numeros.append(i)

        soma=sum(lista_numeros)
        
        #return serve para parar a execução por um tempo e e você não colocasse o return, 
        # a função chamaria a próxima execução mas não retornaria o valor final para a chamada anterior
        return divisivel_nove(soma)
    

print(divisivel_nove(543643))
