def fix_parameters(parameters):
    '''Adequa cada um dos parâmetros fornecidos
    Strings de inteiros continuam sendo strings, mas valores muito altos são reduzidos ao valor máximo aceito
    Demais strings recebem aspas extras (importantes para o comando exec())
    '''
    new_parameters = []
    for i in parameters:
        try:
            int(i)
        except ValueError:
            new_parameter_i = ('"' + i + '"')
        else:        
            if int(i) > len(gene):
                new_parameter_i = str(len(gene))
            else:
                new_parameter_i = i
        finally:
            new_parameters.append(new_parameter_i)
    return new_parameters

def format_command(command):
    '''Formata o comando inserido de forma que ele possa ser executado
    '''
    func = command[0] + "("
    parameters = fix_parameters(command[1::])
    parameters = ",".join(parameters) + ")"
    return func + parameters

#if/else necessário porque o slice não funciona da forma desejada quando i == 0
def reverter(i,j):
    global gene
    if i != 0:
        gene = gene[:i] + gene[j:i-1:-1] + gene[j+1:]
    else:
        gene = gene[j::-1] + gene[j+1:]
        

def transpor(i,j,k):
    global gene
    gene = gene[:i] + gene[j+1:k+1] + gene[i:j+1] + gene[k+1:]
    
def combinar(g,i):
    global gene
    gene = gene[:i] + g + gene[i:]

def concatenar(g):
    global gene
    gene += g

def remover(i,j):
    global gene
    gene = gene[:i] + gene[j+1:]

def transpor_e_reverter(i,j,k):
    global gene
    if i != 0:
        gene = gene[:i] + gene[j:i-1:-1] + gene[k:j:-1] + gene[k+1:]
    else:
        gene = gene[j::-1] + gene[k:j:-1] + gene[k+1:]

def buscar(g):
    print(gene.count(g))

def buscar_bidirecional(g):
    print(gene.count(g) + gene.count(g[::-1]))

def mostrar():
    print(gene)

def sair():
    exit()

def main():
    global gene
    gene = input()
    
    while True:
        last_command = input().split()
        last_command = format_command(last_command)
        exec(last_command)

if __name__ == "__main__":
    main()
    