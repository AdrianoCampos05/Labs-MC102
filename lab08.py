class Movie:
    '''Classe que representa um filme     
    ...
    Atributos
    ---------
    categories: list[str]
        lista de categorias para as quais o filme foi indicado (com repetição)
    scores: list[int]
        lista das notas recebidas pelo filme
    win_count: int
        número de categorias simples vencidas pelo filme
    total_score: float
        soma das médias obtidas pelo filme em cada categoria
    '''
    def __init__(self):
        self.categories = []
        self.scores = []
        self.win_count = 0
        self.total_score = 0.0  


def avg_score(title: Movie, category: str) -> float:
    '''Calcula a nota média de um filme em uma dada categoria
    ...
    Parâmetros
    ----------
    title: Movie
        filme cuja média será calculada
    category: str
        categoria em que o filme está sendo avaliado

    Retorna
    -------
    float
        nota média do filme na categoria
    '''
    added_score = 0
    counter = 0
    for i, j in zip(title.categories, title.scores):
        if i == category:
            added_score += j
            counter += 1

    try:
        return added_score / counter
    except ZeroDivisionError:
        return 0


def category_winner(category: str, nominees: dict[str, Movie]) -> str:
    '''Determina o vencedor de uma categoria simples
    Adiciona a média na categoria ao atributo 'total_score' de cada filme
    ...
    Parâmetros
    ----------
    category: str
        categoria sendo disputada
    nominees: dict[str, Movie]
        dicionário com todos os filmes

    Retorna
    -------
    float
        nome do vencedor da categoria
    '''
    current_leader = ''
    high_score = 0
    for i in nominees:
        average = avg_score(nominees[i], category)
        nominees[i].total_score += average

        if average > high_score:
            current_leader = i
            high_score = average
        elif average == high_score and current_leader != '':  # Desempate
            leader_vote_count = nominees[current_leader].categories.count(category)
            i_vote_count = nominees[i].categories.count(category)
            if i_vote_count > leader_vote_count:
                current_leader = i
                high_score = average

    return current_leader


def simple_winners(nominees: dict[str, Movie]) -> dict[str, str]:
    '''Determina os vencedores de todas as categorias simples
    Adiciona 1 ao atributo 'win_count' de filmes vencedores (1 por vitória)
    ...
    Parâmetros
    ----------
    nominees: dict[str, Movie]:
        dicionário com todos os filmes

    Retorna
    -------
    dict[str, str]
        dicionário com os nomes das categorias e os respectivos vencedores
    '''
    simple_winners = {
        'filme que causou mais bocejos': '',
        'filme que foi mais pausado': '',
        'filme que mais revirou olhos': '',
        'filme que não gerou discussão nas redes sociais': '',
        'enredo mais sem noção': ''
    }

    for i in simple_winners:
        winner = category_winner(i, nominees)
        simple_winners[i] = winner
        nominees[winner].win_count += 1

    return simple_winners


def special_winners(nominees: dict[str, list[Movie]]) -> dict[str, list[str]]:
    '''Determina os vencedores das categorias especiais
    ...
    Parâmetros
    ----------
    nominees: dict[str, Movie]:
        dicionário com todos os filmes
    
    Retorna
    -------
    dict[str, list[str]]
        dicionário com as categorias e as listas de vencedores
    '''
    winners = {
        'prêmio pior filme do ano': [],
        'prêmio não merecia estar aqui': []
    }

    for i in nominees:
        if nominees[i].total_score < 1:  # 1 é a menor média possível
            winners['prêmio não merecia estar aqui'].append(i)

    awards_won = [i.win_count for i in nominees.values()]
    max_wins = max(awards_won)
    for i, j in zip(awards_won, nominees):
        if i == max_wins:
             winners['prêmio pior filme do ano'].append(j)
    
    if winners['prêmio não merecia estar aqui'] == []:
        winners['prêmio não merecia estar aqui'] = ['sem ganhadores']

    contenders = winners['prêmio pior filme do ano']
    if len(contenders) > 1:  # Desempate 
        total_scores = [nominees[i].total_score for i in contenders]
        max_score = max(total_scores)
        for i, j in zip(total_scores, contenders):
            if i == max_score:
                winners['prêmio pior filme do ano'] = [j]
                break

    return winners


def main():
    nominees = {}  # Dicionário com filmes indicados e seus respectivos objetos
    for _ in range(int(input())):
        title = input()
        nominees.update({title: Movie()})

    for _ in range(int(input())):
        nomination = input().split(', ')
        score = int(nomination.pop())
        title = nomination.pop()
        category = nomination.pop()
        
        nominees[title].categories.append(category)
        nominees[title].scores.append(score)

    winners_1 = simple_winners(nominees)
    winners_2 = special_winners(nominees)
    
    print('#### abacaxi de ouro ####')
    print('\ncategorias simples')
    for i in winners_1:
        print('categoria:', i)
        print('-', winners_1[i])
    print('\ncategorias especiais')
    for i in winners_2:
        print(i)
        print('-', end= ' ')
        print(*winners_2[i], sep= ', ')

if __name__ == '__main__':
    main()
