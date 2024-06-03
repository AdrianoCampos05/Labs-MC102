#lista de "cola" com resultado de cada jogo já calculado 
#i-ésima lista correponde à escolha de Reginaldo, j-ésima entrada de cada lista corresponde à jogada de Sheila
#1 = sheila ganha; -1 = reginaldo ganha; 0 = empate
results = [[0,1,-1,-1,1],[-1,0,1,1,-1],[1,-1,0,-1,1],[1,-1,1,0,-1],[-1,1,-1,1,0]]
plays = ["pedra","papel","tesoura","lagarto","spock"]

sheila_str = input()
reginaldo_str = input()

for i in range(5):
    if sheila_str == plays[i]:
        sheila_int = i
    if reginaldo_str == plays[i]:
        reginaldo_int = i

if results[reginaldo_int][sheila_int] == 1:
    print("Interestelar")
elif results[reginaldo_int][sheila_int] == -1:
    print("Jornada nas Estrelas")
else:
    print("empate")