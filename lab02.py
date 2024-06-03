def VoidError():
    print("Opção inválida, recomece o questionário.")

desafios_str = "Suas escolhas te levaram a um caminho repleto de desafios, para você recomendamos as distribuições: "
motivacao_str = "Você passará pelo caminho daqueles que decidiram abandonar sua zona de conforto, as distribuições recomendadas são: "
aprendizado_str = "Ao trilhar esse caminho, um novo guru do Linux irá surgir, as distribuições que servirão de base para seu aprendizado são: "

print("Este é um sistema que irá te ajudar a escolher a sua próxima Distribuição Linux. Responda a algumas poucas perguntas para ter uma recomendação.")
print("Seu SO anterior era Linux?" + "\n" + "(0) Não" "\n" "(1) Sim")

latest_ans = input()

if latest_ans == "0":
    print("Seu SO anterior era um MacOS?" + "\n" + "(0) Não" + "\n" + "(1) Sim")

    latest_ans = input()

    if latest_ans == "0":
       print(motivacao_str + "Ubuntu Mate, Ubuntu Mint, Kubuntu, Manjaro.") 
    elif latest_ans == "1":  
        print(motivacao_str + "ElementaryOS, ApricityOS.")     
    else:
        VoidError()         
elif latest_ans == "1":
    print("É programador/ desenvolvedor ou de áreas semelhantes?" + "\n" + "(0) Não" + "\n" + "(1) Sim" + "\n" + "(2) Sim, realizo testes e invasão de sistemas") 
    
    latest_ans = input()

    if latest_ans == "2":
        print(aprendizado_str + "Kali Linux, Black Arch.")
    elif latest_ans == "0":
        print(aprendizado_str + "Ubuntu Mint, Fedora.")
    elif latest_ans == "1":
        print("Gostaria de algo pronto para uso ao invés de ficar configurando o SO?" + "\n" + "(0) Não" + "\n" + "(1) Sim")

        latest_ans = input()

        if latest_ans == "0":
            print("Já utilizou Arch Linux?" + "\n" + "(0) Não" + "\n" + "(1) Sim")

            latest_ans = input()

            if latest_ans == "0":
                print(aprendizado_str + "Antergos, Arch Linux.")
            elif latest_ans == "1":
                print(desafios_str + "Gentoo, CentOS, Slackware.")
            else:
                VoidError()
        elif latest_ans == "1":
            print("Já utilizou Debian ou Ubuntu?" + "\n" + "(0) Não" + "\n" + "(1) Sim")

            latest_ans = input()

            if latest_ans == "0":
                print(aprendizado_str + "OpenSuse, Ubuntu Mint, Ubuntu Mate, Ubuntu.")
            elif latest_ans == "1":
                print(desafios_str + "Manjaro, ApricityOS.")
            else:
                VoidError()
        else:
            VoidError()       
    else:
        VoidError()
else:
    VoidError()