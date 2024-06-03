#Informando a posição da sequência de Fibonacci que deve ser exibida
n = int(input())
 
#Inicialização dos primeiros números da sequência
f_n1 = 1
f_n2 = 1
f_n = 0
 
#Cálculo da sequência
for i in range(n):
  if(i == n-1): #Verificando se já se encontra na posição informada para então imprimí-lo na tela
    print('O termo na posição %i da sequência de Fibonacci é: %i.' % (n, f_n1)) 
 
  #Atualização dos termos da sequência
  f_n = f_n1+f_n2
  f_n1 = f_n2
  f_n2 = f_n