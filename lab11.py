class Entity:
    '''Classe mãe de Character e Enemy

    Atributos:
        _hp: int
            a vida do ser
        _atk: int
            o poder de ataque do ser
        _current_pos: tuple[int]
            a posição atual do ser
    '''
    def __init__(self, hp: int, atk: int, start_pos: tuple[int]):
        self._hp = hp
        self._atk = atk
        self._current_pos = start_pos

    @property
    def atk(self):
        if self.is_dead():
            return 0  # Mortos não dão dano
        else:    
            return self._atk
    
    @atk.setter
    def atk(self, value: int):
        if value >= 1: 
            self._atk = value
        else:
            self._atk = 1
    
    @property
    def current_pos(self):
        return self._current_pos


    def change_hp(self, value: int) -> int:
        '''Adiciona um valor ao hp do objeto
        Se a vida final for negativa, então define hp = 0
        Retorna o dano tomado

        Parâmetro:
            value: int
                o valor adicionado ao hp (pode ser negativo)
        
        Retorna: int
            o dano tomado (negativo caso o objeto ganhe hp)
        '''
        new_hp = self._hp + value
        effective_dmg = -value
        
        if new_hp < 0:
            effective_dmg = self._hp
            self._hp = 0
        else:
            self._hp = new_hp
            
        return effective_dmg
                        
    
    def is_dead(self) -> bool:
        return self._hp <= 0


    def change_pos(self, target: tuple[int]) -> None:
        self._current_pos = target


class Character(Entity):
    '''Classe que representa um personagem (no caso, apenas o Link)

    Atributos:
        _end_pos: tuple[int]
            o destino final do personagem
        _has_gone_down: bool
            se o personagem já chegou na parte de baixo da masmorra
        todos os atributos herdados da classe Entity
    '''
    def __init__(self, hp: int, atk: int, start_pos: tuple[int], end_pos: tuple[int]):
        super().__init__(hp, atk, start_pos)
        self._end_pos = end_pos
        self._has_gone_down = False

    @property
    def hp(self):
        return self._hp

    
    def __str__(self):
        if self.is_dead():
            return 'X'
        return 'P'

    def get_target(self, dungeon: 'Dungeon') -> tuple[int]:
        '''Encontra a posição para a qual o personagem deve se mover

        Parâmetro:
            dungeon: Dungeon
                a masmorra
        
        Retorna: tuple[int]
            a posição alvo
        '''
        pos = self._current_pos
        
        if not self._has_gone_down:
            target = (pos[0] + 1, pos[1])
            if not dungeon.has_pos(target):
                self._has_gone_down = True
            else:
                return target

        if pos[0] % 2 == 0:
            target = (pos[0], pos[1] - 1)
        else:
            target = (pos[0], pos[1] + 1)
        
        if not dungeon.has_pos(target):
            target = (pos[0] - 1, pos[1])

        return target


class Enemy(Entity):
    '''Classe que representa um inimigo

    Atributos:
        _kind: str
            o tipo de inimigo
        todos os atributos herdados da classe Entity
    '''
    def __init__(self, hp: int, atk: int, kind: str, start_pos: tuple[int]):
        super().__init__(hp, atk, start_pos)
        self._kind = kind

    
    def __str__(self):
        return self._kind

    
    def get_target(self, dungeon: 'Dungeon') -> tuple[int]:
        '''Encontra a posição para a qual o personagem deve se mover

        Parâmetro:
            dungeon: Dungeon
                a masmorra

        Retorna: tuple[int]
            a posição alvo
        '''
        pos = self._current_pos
        
        
        if self._kind == 'U':
            target = (pos[0] - 1, pos[1])
        elif self._kind == 'D':
            target = (pos[0] + 1, pos[1])
        elif self._kind == 'L':
            target = (pos[0], pos[1] - 1)
        else:
            target = (pos[0], pos[1] + 1)
        
        if not dungeon.has_pos(target):
            target = pos
        
        return target



class Item:
    '''Classe que representa um item

    Atributos:
        _name: str
            o nome do item
        _kind: str
            o tipo de item (v ou d)
        _pos: tuple[int]
            a posição do item na masmorra
        _value: int
            o valor do item
    '''
    def __init__(self, name: str, kind: str, pos: tuple[int], value: int):
        self._name = name
        self._kind = kind
        self._pos = pos
        self._value = value


    def __str__(self):
        return self._kind

    
    def use(self, character: Character) -> None:
        '''Modifica o atributo adequado do personagem e imprime a notificação de coleta
        Se o atributo _kind do item não for 'v' nem 'd', o atributo modificado é o atk

        Atributo:
            character: Character
                o personagem que coletou o item
        '''
        if character.is_dead():
            return

        if self._kind == 'v':
            character.change_hp(self._value)
        else:
            character.atk += self._value

        print(f'[{self._kind}]Personagem adquiriu o objeto {self._name} com status de {self._value}')


class Dungeon:
    '''Classe que representa uma masmorra

    Atributos:
        _height: int
            o número de linhas
        _width: int
            o número de colunas
        _grid: list[list[list[object]]]
            a matriz da masmorra
            cada posição é uma lista de objetos
    '''
    def __init__(self, height: int, width: int):
        self._height = height
        self._width = width
        self._grid = [[[] for _ in range(width)] for _ in range(height)] 

    
    def __str__(self):
        string = ''
        for i in self._grid:
            line = [str(self.priority(*j)) for j in i]
            string += ' '.join(line) + '\n'

        return string
    
    
    @staticmethod
    def priority(*args: object) -> object:
        '''Decide qual argumento tem prioridade de impressão
        
        Parâmetros:
            args: object
                os objetos sendo comparados
            
        Retorna: object
            o objeto com maior prioridade
        '''
        priority_order = (Character, str, Enemy, Item)
        for i in priority_order:
            for j in args:
                if isinstance(j, i):
                    return j
        return '.'


    def place_obj(self, obj: object, pos: tuple[int]) -> None:
        '''Insere um objeto na grid

        Parâmetros:
            obj: object
                o objeto a ser inserido
            pos: tuple[int]
                a posição da grid onde obj será inserido

        '''
        self._grid[pos[0]][pos[1]].insert(0, obj)

    
    def remove_obj(self, obj: object, pos: tuple[int]) -> None:
        '''Remove um objeto da grid

            Parâmetros:
                obj: object
                    o objeto a ser inserido
                pos: tuple[int]
                    a posição da grid onde obj será inserido
        '''
        self._grid[pos[0]][pos[1]].remove(obj)


    def check_for_fight(self, character: Character) -> None:
        '''Controla a ocorrência de combates:
        Verifica se eles devem ocorrer;
        Chama a função de combate quando necessário;
        Remove os inimigos da masmorra caso ele morram

        Atributo:
            character: Character
                o personagem
        '''
        character_pos = character.current_pos
        grid_pos = self._grid[character_pos[0]][character_pos[1]]
        for i in grid_pos[::-1]:
            if isinstance(i, Enemy):
                fight(character, i)
                if i.is_dead():
                    self.remove_obj(i, i.current_pos)


    def check_for_items(self, character: Character) -> None:
        '''Controla a coleta de itens:
        Verifica se há itens na posição do personagem
        Usa e remove os itens da masmorra quando necessário
        '''
        character_pos = character.current_pos
        grid_pos = self._grid[character_pos[0]][character_pos[1]]
        for i in grid_pos[::-1]:
            if isinstance(i, Item):
                i.use(character)
                self.remove_obj(i, character_pos)

    
    def has_pos(self, pos: tuple[int]) -> bool:
        '''Verifica se a posição informada faz parte da masmorra
        '''
        return (self._height > pos[0] >= 0 and self._width > pos[1] >= 0)

                
def fight(character: Character, enemy: Enemy) -> None:
    '''Altera o hp do personagem e do monstro
    imprime o resultado do combate

    Atributos:
        character: Character
            o personagem
        enemy: Enemy
            o inimigo
    '''
    if character.is_dead() or enemy.is_dead():
        return
    
    damage = enemy.change_hp(-character.atk)
    print(f'O Personagem deu {damage} de dano ao monstro na posicao {character.current_pos}')

    if enemy.is_dead():
        return
    
    damage = character.change_hp(-enemy.atk)
    print(f'O Monstro deu {damage} de dano ao Personagem. Vida restante = {character.hp}')


def move(ent, dungeon: Dungeon, target: tuple[int]) -> None:
    '''Movimenta o ser na masmorra
    Altera tanto o atributo current_pos do ser quanto sua posição na matriz da masmorra

    Atributos:
        ent: Character | Enemy
            o ser que será movimentado
        dungeon: Dungeon
            a masmorra
        target: tuple[int]
            a nova posição do ser
    '''
    old_pos = ent.current_pos
    dungeon.remove_obj(ent, old_pos)
    ent.change_pos(target)
    dungeon.place_obj(ent, target)


def main():
    hp, atk = input().split()
    height, width = input().split()

    dungeon = Dungeon(int(height), int(width))
    
    start_pos = input().split(',')
    start_pos = (int(start_pos[0]), int(start_pos[1]))

    end_pos = input().split(',')
    end_pos = (int(end_pos[0]), int(end_pos[1]))

    # Vou chamar o Link de zelda e ningúem pode me impedir mwahaha
    zelda = Character(int(hp), int(atk), start_pos, end_pos)

    dungeon.place_obj(zelda, start_pos)
    dungeon.place_obj('*', end_pos)

    enemies = []
    no_of_enemies = int(input())

    for _ in range(no_of_enemies):
        enemy_info = input().split()
        hp = int(enemy_info[0])
        atk = int(enemy_info[1])
        kind = enemy_info[2]
        pos = tuple([int(i) for i in enemy_info[3].split(',')])

        enemy = Enemy(hp, atk, kind, pos)
        enemies.append(enemy)
        dungeon.place_obj(enemy, pos)

    
    no_of_items = int(input())

    for _ in range(no_of_items):
        item_info = input().split()
        name = item_info[0]
        kind = item_info[1]
        pos = tuple([int(i) for i in item_info[2].split(',')])
        value = int(item_info[3])
        
        item = Item(name, kind, pos, value)
        dungeon.place_obj(item, pos)


    while True:
        print(dungeon)
        
        if 'X' in str(dungeon):
            exit()

        if '*' not in str(dungeon):
            break
        
        move(zelda, dungeon, zelda.get_target(dungeon))
        
        # A segunda verificação impede que haja combate na última rodada
        if '*' not in str(dungeon):
            print(dungeon)
            break

        for i in enemies:
            move(i, dungeon, i.get_target(dungeon))
        
        dungeon.check_for_items(zelda)
        dungeon.check_for_fight(zelda)

        for i in enemies:
            if i.is_dead():
                enemies.remove(i)
        
    print('Chegou ao fim!')


if __name__ == '__main__':
    main()
