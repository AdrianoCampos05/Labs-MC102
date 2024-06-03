#variáveis guardam as informações de cada dia
total_fights = []
total_served = []
total_not_served = []
total_unavailable = []

D = int(input())

for i in range(D):  
    M = int(input())
    pairs = []

    #separa os pares de animais que brigam em uma lista
    for j in range(M):
        pairs.append(input().split())
    
    #guarda o tipo e o número de cada procedimento disponível
    #números serão atualizados conforme os procedimentos forem pedidos (linha 56)
    services = input().split()

    Z = int(input())
    
    #guardará pares da forma [animal, procedimento pedido]
    requests = []

    for j in range(Z):
        requests.append(input().split()) 

    fights = 0

    #verifica quantos pares de animais que brigam estarão presentes no dia
    for j in pairs:
        pair_check = 0
        for k in requests:
            if j[0] in k:
                pair_check += 1
            if j[1] in k:
                pair_check += 1
            
        fights += pair_check//2
    
    served = []
    not_served = []
    unavailable = []

    #registra os animais que serão atendidos na lista "served"...
    #e os que pediram um procedimento indisponível na lista "unavailable"
    for j in requests:
        if j[1] in services: 
            available_services = int(services[services.index(j[1]) + 1])       
            for k in services:
                if available_services > 0:
                    if j[1] == k:
                        served.append(j[0])
                        available_services -= 1
                        services[services.index(k)+1] = available_services
                        break
                else:
                    break
        else:
            unavailable.append(j[0])
    
    #registra os animais que pediram procedimentos já esgotados na lista "not_served"
    for j in requests:
        if not (j[0] in served or j[0] in unavailable):
            not_served.append(j[0])

    #informações do dia atual são registradas na respectiva lista com informações de todos os dias
    total_fights.append(fights)
    total_served.append(served)
    total_not_served.append(not_served)
    total_unavailable.append(unavailable)

#imprime as informações coletadas de todos os dias
for i in range(D):    
    print("Dia:", i+1)
    print("Brigas:", total_fights[i])

    #comando "pop()" remove os elementos das listas conforme eles são impressos
    if len(total_served[i]) > 0:
        print("Animais atendidos:", end = " ")
        while len(total_served[i]) > 1:
            print(total_served[i][0], end = ", ")
            total_served[i].pop(0)
        print(total_served[i][0])

    if len(total_not_served[i]) > 0:
        print("Animais não atendidos:", end = " ")
        while len(total_not_served[i]) > 1:
            print(total_not_served[i][0], end = ", ")
            total_not_served[i].pop(0)
        print(total_not_served[i][0])

    for j in total_unavailable[i]:
        print("Animal", j, "solicitou procedimento não disponível.")
    print()