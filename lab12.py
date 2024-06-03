class Card:
    '''Classe que representa uma carta

    Atributos:
        _name: str
            o nome da carta
        _suit: str
            o naipe da carta
        _rank: str
            o número/letra da carta
        _rank_dict: dict[str: int]
            os valores relativos de cada número/letra
        _suit_dict: dict[str: int]
            os valores relativos de cada naipe
    '''
    def __init__(self, name: str):
        self._name = name
        self._suit = name[-1]
        self._rank = name.removesuffix(self._suit)
        
        rank_order = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
        self._rank_dict = {i: j for i, j in zip(rank_order, range(13))}

        suit_order = ('O', 'E', 'C', 'P')
        self._suit_dict = {i: j for i, j in zip(suit_order, range(4))}

    @property
    def rank(self):
        return self._rank


    def __str__(self):
        return self._name

    
    def __repr__(self):  #usado apenas para debugging
        return f'Card({self._name})'


    def __eq__(self, other):
        '''Se other for do tipo Card, ambos os objetos precisam ter o mesmo nome
        Se other for do tipo str, other deve ser igual à letra/ ao número da carta
        '''
        if type(other) == Card:
            return self._name == other._name
        elif type(other) == str:
            return self._rank == other
        else:
            return NotImplemented

    def __lt__(self, other):
        rank_dict = self._rank_dict
        suit_dict = self._suit_dict
        
        if type(other) == Card:
            if self._rank == other._rank:
                return suit_dict[self._suit] < suit_dict[other._suit]
            else:
                return rank_dict[self._rank] < rank_dict[other._rank]
        
        if type(other) == str:
            return rank_dict[self._rank] < rank_dict[other]
        
        return NotImplemented

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)


class Hand:
    '''Classe que representa uma mão de cartas

    Atributos:
        _player: int
            o número do jogador com a mão
        _cards: list[card]
            as cartas da mão
        _bluffing: bool
            se o jogador blefou na última jogada
    '''
    def __init__(self, player: int, cards: list[Card]):
        self._player = player
        self._cards = cards
        self._bluffing = False

    @property
    def bluffing(self):
        return self._bluffing    


    def sort_cards(self) -> None:
        self._cards = sort(self._cards)


    def __str__(self):
        string = 'Mão:'
        for i in self._cards[::-1]:
            string += ' ' + str(i)
        return string 


    def draw(self, cards: list[Card]) -> None:
        '''Adiciona uma lista de cartas à mão
        Ordena a mão
        '''
        self._cards += cards
        self.sort_cards()


    def play(self, rank: str) -> list[list[Card], str, int]:
        '''Remove e retorna todas as cartas que o jogador possui com um dado valor

        Parâmetro:
            rank: str
                o número/letra jogado
        
        Retorna: list[list[Card], str, int]
            a lista de cartas jogadas; o número/letra jogado; o número de cartas

        '''
        counter = 0
        cards = []
        index = search_higher_card(rank, self._cards)
        current_card = rank

        while current_card == rank:
            current_card = self._cards.pop(index)
            cards.append(current_card)
            counter += 1
            if len(self._cards) <= index:
                break
            current_card = self._cards[index]

        return [cards, rank, counter]


    def bluff(self, last_rank: str) -> list[list[Card], str, int]:
        '''Joga as cartas mais fracas da mão
        ativa o parâmetro _bluffing

        Parâmetro:
            last_rank: str
                o número/letra da última carta jogada
        
        Retorna: list[list[Card], str, int]
            as cartas jogadas; o número/letra da rodada anterior; o número de cartas
        '''
        self._bluffing = True
        real_rank = self._cards[0].rank
        real_play = self.play(real_rank)
        return [real_play[0], last_rank, real_play[2]]


    def choose_card(self, last_rank: str) -> list[list[Card], str, int]:
        '''Determina o que o jogador fará na rodada

        Parâmetro:
            last_rank: str
                o número/letra da última carta jogada
        
        Retorna:
            as cartas jogadas; o número/letra jogado (alterado em caso de blefe); o número de cartas
        '''
        self._bluffing = False
        index = search_higher_card(last_rank, self._cards)
        if index == None:
            return self.bluff(last_rank)
        else:
            return self.play(self._cards[index].rank)


    def check_for_win(self) -> None:
        '''Verifica se a mão está vazia
        Caso esteja, imprime a mensagem de vitória e encerra o programa
        '''
        if self._cards == []:
            print(f'Jogador {self._player + 1} é o vencedor!')
            exit()
        

def sort(cards: list[Card]) -> list[Card]:
    '''Uma implementação do insertion sort
    Retorna uma cópia ordenada lista 
    '''
    l = cards.copy()
    for i in range(1, len(l)):
        ith_card = l[i]
        j = i - 1
        while j >= 0 and l[j] > ith_card:
            l[j + 1] = l[j]
            j -= 1
        l[j + 1] = ith_card
    return l


def search_higher_card(rank: str, sorted_list: list[Card]) -> int:
    '''Encontra o índice da primeira carta de valor maior ou igual a rank
    '''
    start = 0
    end = len(sorted_list) - 1
    while start <= end:
        mid = (start + end) // 2
        if sorted_list[mid] >= rank:
            end = mid - 1
        else:
            start = mid + 1

    if start >= len(sorted_list):
        return None

    return start
    

def print_hands(players: dict[int: Hand]):
    '''Imprime a mão de todos os jogadores
    '''
    for i, j in players.items():
        print(f'Jogador {i + 1}')
        print(j)


def print_pile(pile: list[Card]) -> None:
    '''Imprime a pilha de descarte
    '''
    string = 'Pilha:'
    for i in pile:
        string += ' ' + str(i)
    print(string)


def main():
    no_of_players = int(input())
    players = {}
    for i in range(no_of_players):
        cards = [Card(j) for j in input().split(', ')]
        hand = Hand(i, cards)
        hand.sort_cards()
        players[i] = hand

    pile = []
    call_gap = int(input())  # Número de rodadas entre dúvidas

    print_hands(players)
    print_pile(pile)

    round_counter = 0
    last_rank = 'A'
    
    while True:
        round_counter += 1
        current_player = round_counter % no_of_players
        if current_player == 0:
            current_player = no_of_players

        played_cards = players[current_player - 1].choose_card(last_rank)
        pile.extend(played_cards[0])
        
        last_rank = played_cards[1]
        print(f'[Jogador {current_player}] {played_cards[2]} carta(s) {last_rank}')
        print_pile(pile)

        if round_counter % call_gap == 0:
            next_player = current_player + 1
            if next_player > no_of_players:
                next_player = 1

            print(f'Jogador {next_player} duvidou.')
            
            if players[current_player - 1].bluffing:
                players[current_player - 1].draw(pile)
            else:
                players[next_player - 1].draw(pile)

            pile = []

            print_hands(players)
            print_pile(pile)

            last_rank = 'A'
        
        players[current_player - 1].check_for_win()


if __name__ == '__main__':
    main()
