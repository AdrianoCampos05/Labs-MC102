num_of_players = int(input())
random_number = input().split()
interval = input().split()
score = list(range(num_of_players))

for i in range(num_of_players):
    if (i < (num_of_players)/2):
        score[i] = int(random_number[i])*(int(interval[2*i+1]) - int(interval[2*i]))
    else:
        score[i] = int(random_number[i]) + int(interval[2*i+1]) - int(interval[2*i])

for i in range(num_of_players):
    for j in range(num_of_players):
        if(score[i] == score[j] == max(score) and i != j):
            print("Rodada de cerveja para todos os jogadores!") 
            exit()

print("O jogador número %i vai receber o melhor bolo da cidade pois venceu com %i ponto(s)!" % (score.index(max(score)) + 1, max(score)))