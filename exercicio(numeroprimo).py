def verificar_primo(n):
    if n<=1:
        return "Não é primo"
    else:
        for i in range(2,int(n**0.5)+1):
             #esse for não irá percorrer todos os elementos,apenas até a raiz quadrada,pois
             #se não existiu nenhum divisor até a raiz quadrada,então é primo
            if n%i==0:
                return "Não é primo"
             
        return "É primo"




print(verificar_primo(49))





