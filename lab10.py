class Entity:
    '''Classe genérica, mãe de Player e Enemy

    Parâmetros:
        _max_hp: int 
            a vida máxima
        _hp: int
            a vida atual
    '''
    def __init__(self, max_hp: int):
        self._max_hp = max_hp
        self._hp = max_hp


    def take_damage(self, dmg: int) -> None:
        '''Subtrai dmg da vida do objeto
        '''
        self._hp -= dmg


    def is_alive(self) -> bool:
        '''Retorna True se o objeto tem mais de 0 hp, False do contrário
        '''
        if self._hp <= 0:
            return False
        else:
            return True


class Player(Entity):
    '''Classe que representa um personagem (no caso, apenas Aloy)

    Atributos:
        _arrows: dict[str: int]
            os tipos de flecha e suas quantidades atuais
        max_arrows: dict[str: int]
            os tipos de flecha e suas quantidades máximas
    '''
    def __init__(self, max_hp: int, arrows: dict[str: int]):
        super().__init__(max_hp)
        self._arrows = arrows  # Os tipos de flecha e suas quantidades atuais
        self.max_arrows = arrows.copy()  # Os tipos de flecha e suas quantidades máximas


    @property  # Preciso mesmo criar propriedades em casos assim? A Sandra falou pra fazer.
    def hp(self):
        return self._hp
    

    def heal(self) -> None:
        '''Recupera metade da vida máxima
        '''
        self._hp += self._max_hp // 2
        if self._hp > self._max_hp:
            self._hp = self._max_hp


    def use_arrow(self, arrow_type: str) -> None:
        '''Se tiver flechas do tipo, subtrai 1 do número de flechas disponíveis
        '''
        if self._arrows[arrow_type] > 0:
            self._arrows[arrow_type] -= 1

    
    def get_used_arrows(self):
        '''Devolve um dicionário com os tipos de flecha e as quantidades usadas
        Tipos de flecha que não foram usados na rodada não são incluídos 
        '''
        used_arrows = {}
        for i in self._arrows:
            number_used = self.max_arrows[i] - self._arrows[i]
            if number_used > 0:
                used_arrows[i] = number_used
        return used_arrows


    def check_for_arrows(self) -> None:
        '''Verifica se Aloy ainda tem flechas
        Se estiver sem flechas, chama a função que termina o jogo
        '''
        for i in self._arrows.values():
            if i > 0:
                return
        end_game('arrows', self.hp)


    def retrieve_arrows(self) -> None:
        '''Recupera todas as flechas de Aloy
        '''
        self._arrows = self.max_arrows.copy()


class BodyPart:
    '''Classe que representa uma parte do corpo de um inimigo

    Atributos:
        _name: str
            o nome da parte
        _weakness: str
            o tipo de fraqueza
        _max_dmg: int
            o dano máximo
        _pos: tuple[int]
            as coordenadas do ponto fraco
    '''
    def __init__(self, name: str, weakness: str, max_dmg: int, pos: tuple[int]):
        self._name = name
        self._weakness = weakness
        self._max_dmg = max_dmg
        self._pos = pos


    @property
    def name(self):
        return self._name


    def damage(self, hit_pos: tuple[int], arrow_type: str) -> int:
        '''Calcula o dano tomado pela parte do corpo.

        Parâmetros:
            hit_pos: tuple[int]
                as coordenadas atingidas
            arrow_type: str
                o tipo de flecha que atingiu a parte

        Retorna: int
            o dano tomado
        '''
        weakness = self._weakness
        distance = abs(self._pos[0] - hit_pos[0]) + abs(self._pos[1] - hit_pos[1])
        dmg = self._max_dmg - distance
        if weakness != 'todas' and weakness != arrow_type:
            dmg //= 2
        if dmg < 0:  # Aloy pode mirar mal, mas isso não faz ela curar os monstros
            dmg = 0
        return dmg


class Enemy(Entity):
    '''Classe que representa um inimigo

    Atributos:
        _max_hp: int
            a vida máxima
        _hp: int
            a vida atual
        _atk: int
            o poder de ataque
        _body_parts: tuple[BodyPart]
            as partes do corpo
    '''
    def __init__(self, max_hp: int, atk: int, *body_parts: BodyPart):
        self._max_hp = max_hp  # Vida máxima
        self._hp = max_hp  # Vida atual
        self._atk = atk  # Poder de ataque
        self._body_parts = body_parts  # Pontos fracos


    @property
    def body_parts(self):
        return self._body_parts

    @property
    def atk(self):
        return self._atk

def create_enemies(no_of_enemies) -> dict[int: Enemy]:
    '''Cria um dicionário com os inimigos
    Parâmetro
    no_of_enemies:
        o número de inimigos criados

    Retorna: dict[int: Enemy]
        dicionário com os inimigos
        a chave de cada inimigo é seu número correspondente
    '''
    enemies = {}
    for i in range(no_of_enemies):
        enemy_stats = [int(i) for i in input().split()]
        all_body_parts = []

        for _ in range(enemy_stats[2]):
            body_part = input().split(', ')
            name = body_part.pop(0)
            weakness = body_part.pop(0)
            
            body_part = [int(i) for i in body_part]  # Strings já foram removidas
            max_dmg = body_part.pop(0)
            pos = tuple(body_part)

            all_body_parts.append(BodyPart(name, weakness, max_dmg, pos))
        
        enemy = Enemy(enemy_stats[0], enemy_stats[1], *all_body_parts)
        enemies.update({i: enemy})
    return enemies


def update_crits(enemy_key: int, hit_pos: tuple[int], body_part: BodyPart, crit_dict: dict) -> None:
    '''Atualiza o dicionário fornecido caso um ponto crítico seja atingido
    Parâmetros:
        enemy_key: int
            a chave do inimigo
        hit_pos: tuple[int]
            as coordenadas atingidas
        body_part: BodyPart
            a parte do corpo do inimigo atingida
        crit_dict: dict[int: dict[tuple[int]: int]]
            o dicionário com os inimigos, os pontos críticos e os números de acertos
            é modificado pela função
    '''
    weak_pos = body_part._pos
    if weak_pos == hit_pos:
        crit_dict[enemy_key][weak_pos] += 1


def print_crits(crit_dict: dict, ref_dict: dict) -> None:
    '''Imprime o dicionário de pontos críticos no formato adequado

    Parâmetro:
        crit_dict: dict[int: dict[tuple[int]: int]]
            o dicionário de pontos críticos
        ref_dict: dict[int: dict[tuple[int]: int]]
            o dicionário de referência (com as quantidades de críticos todas iguais a 0)
    '''
    if crit_dict != ref_dict:
        print('Críticos acertados:')
        for enemy_key, part_dict in crit_dict.items():
            if part_dict != ref_dict[enemy_key]:
                print(f'Máquina {enemy_key}:')
                for pos, hits in part_dict.items():
                    if hits != 0:
                        print(f'- {pos}: {hits}x')


def end_game(ending: str, hp= 0) -> None:
    '''Imprime as informações finais e encerra o jogo
    
    Parâmetros:
        ending: str
            o tipo de final obtido
        hp: int (opcional)
            a vida de aloy no final do jogo
            só é necessário caso Aloy fique sem flechas
        

    '''
    match ending:
        case 'died':
            print(f'Vida após o combate = {hp}')
            print('Aloy foi derrotada em combate e não retornará a tribo.')
        case 'arrows':
            print(f'Vida após o combate = {hp}')
            print('Aloy ficou sem flechas e recomeçará sua missão mais preparada.')
        case 'won':
            print('Aloy provou seu valor e voltou para sua tribo.')
    exit()


def main():
    hp = int(input())
    arrows = input().split()
    arrows = {arrows[2*i]: int(arrows[2*i+1]) for i in range(len(arrows)//2)}

    aloy = Player(hp, arrows)

    enemies_left = int(input())  # Número de inimigos que estão vivos
    combat_counter = 0  #  A rodada de combate atual
    
    while enemies_left > 0:
        engaged_enemy_no = int(input())  # Número de inimigos sendo enfrentados
        engaged_enemies = create_enemies(engaged_enemy_no)  # Inimigos sendo enfrentados

        # Dicionário com dicionários
        # Tem a forma {chave do inimigo: {posição: número de acertos}}
        crits = {i: {j: 0 for j in [k._pos for k in engaged_enemies[i].body_parts]} for i in engaged_enemies}
        
        # Usado para verificar se o dicionário original foi alterado
        crit_reference = {i: j.copy() for i, j in crits.items()}
        
        print(f'Combate {combat_counter}, vida = {aloy.hp}')
        
        combat_counter += 1
        arrow_counter = 0  # Número de flechas consecutivas
        while engaged_enemies != {}:
            aloy.check_for_arrows()
            
            command = input().split(', ')
            target_enemy_key = int(command[0])
            target_enemy = engaged_enemies[target_enemy_key]
            name = command[1]
            arrow_type = command[2]
            hit_pos = (int(command[3]), int(command[4]))

            for part in target_enemy.body_parts:
                if part.name == name:
                    target_enemy.take_damage(part.damage(hit_pos, arrow_type))
                    update_crits(target_enemy_key, hit_pos, part, crits)
                    aloy.use_arrow(arrow_type)

            if not target_enemy.is_alive():
                print(f'Máquina {target_enemy_key} derrotada')
                del engaged_enemies[target_enemy_key]
                enemies_left -= 1

            if arrow_counter >= 2:
                for i in engaged_enemies.values():
                    aloy.take_damage(i.atk)
                arrow_counter = 0
            else:
                arrow_counter += 1

            if not aloy.is_alive():
                end_game('died')
        
        print(f'Vida após o combate = {aloy.hp}')
        print('Flechas utilizadas:')
        used_arrows = aloy.get_used_arrows()
        for i in used_arrows:

            # Aqui eu acessei o atributo max_arrows diretamente, sem usar o decorador de propriedade
            # Isso é inadequado?
            print(f'- {i}: {used_arrows[i]}/{aloy.max_arrows[i]}')
        print_crits(crits, crit_reference)
        
        aloy.retrieve_arrows()
        aloy.heal()
    
    end_game('won')


if __name__ == '__main__':
    main()
