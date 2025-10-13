print("LISTA DE COMANDOS\n" \
"1-escrever\n" 
"2-mostrar\n"
"3-retirar\n" 
"4-refazer\n" 
"5-parar\n")

pedido=input("Aparte ENTER para iniciarmos")

frase_final=[]
desfeitos=[]



def pegar_elementos(lista_pedido):
    
    #aqui irá tratar a lista e retornará apenas depois do comando inicial
        return lista_pedido[1:]

while pedido not in ["parou","para","parar","paro"]:
    
    try:
        print("ESCREVA OS COMANDOS:")
        print()
        pedido=input().strip().lower()
        lista_pedido=pedido.split()
    
        i=0
        leitura_lista=len(lista_pedido)
        elemento=lista_pedido[0]

        if elemento in ["stop","parar","para","paro"]:
            break

        if elemento in ["escrever","mostrar","retirar","refazer"]:
        
            if elemento=="escrever":
                texto=pegar_elementos(lista_pedido)
                for z in texto:
                    frase_final.append(z)
                print("-"*30)
            elif elemento=="mostrar":
                texto_final=" ".join(frase_final)
                print(texto_final)
                print("-"*30)
            elif elemento=="retirar":
                if not frase_final:
                    print("PARA RETIRAR VOCÊ PRECISA ESCREVER ALGO ANTES")
                else:
                    retirado=frase_final.pop(-1)
                    desfeitos.append(retirado)
                print("-"*30)
            elif elemento=="refazer":
                if not desfeitos:
                    print("NÃO EXISTE ELEMENTOS PARA REFAZER")
                    print("-"*30)
                else:
                    refeito=desfeitos.pop(-1)
                    frase_final.append(refeito)
                    print("-"*30)
        else:
            print("Comando inválido")
    except:
        print("COMANDO INVÁLIDO")
        
