class Vec(list):
    '''Lista de inteiros com adição redefinida e uma função extra
    '''
    def __add__(self, other):
        '''Retorna o vetor soma entrada por entrada
        '''
        return Vec([i + j for i, j in zip(self, other)])


    def is_in_range(self, *args: int) -> bool:
        '''Verifica se todos os componentes estão entre 0 e valores dados (inclusive)
        Parâmetros:
        args: int
            limites superiores para cada entrada do vetor
        '''
        for i, j in zip(self, args):
            if i < 0 or i > j:
                return False 
        return True


class Room:
    '''Classe que representa o cômodo com o robô

    Atributo fornecido pelo usuário:
        grid: list[list[int]]
            A matriz do cômodo
        
    Atributos definidos dentro da classe:
        height: int
            O número de linhas
        width: int
            O número de colunas
        pos: Vec
            A posição atual do robô
        last_pos: Vec
            Ultima posição antes do robô entrar no modo limpeza
        target: Vec
            A posição alvo do robô
        last_target: Vec
            O último alvo do robô antes de entrar no modo limpeza
        end: Vec
            O destino final do robô
        on_path: bool
            Guarda se o robô está ou não no caminho "normal"
        cleaning: bool
            Guarda se o robô está no modo limpeza
            Modo retorno é considerado parte do modo limpeza
        almost_done: bool
            Guarda se o robô já passou no canto inferior direito
            Só ativa se o robô não estiver no modo limpeza
        done: bool
            Guarda se o robô acabou toda a limpeza
        left, up, right, down: vec
            Vetores correspondentes às quatro direções
    '''

    def __init__(self, grid: list[list[str]]):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        
        # Os vetores são da forma [linha, coluna]
        self.pos = Vec([0, 0])
        self.last_pos = Vec([0, 0])
        self.target = Vec([0, 0])
        self.last_target = Vec([0, 0])
        self.end = Vec([self.height - 1, self.width - 1])
        self.on_path = True
        self.cleaning = False
        self.almost_done = False
        self.done = False
        
        # Vetores com direções
        self.left = Vec([0, -1])
        self.up = Vec([-1, 0])
        self.right = Vec([0, 1])
        self.down = Vec([1, 0])


    def __str__(self):
        name = ''
        for i in self.grid:
            name += ' '.join(i) + '\n'
        name = name.removesuffix('\n')  # Impede quebra de linha no final da string
        return name
    

    def move(self) -> None:
        '''Move o robô para na direção de target
        Altera a grid e já imprime o resultado
        '''
        if self.pos != self.target:  # Impede que o mesmo layout seja impresso duas vezes
            self.grid[self.pos[0]][self.pos[1]] = '.'
            self.grid[self.target[0]][self.target[1]] = 'r'
            self.pos = self.target
            print()
            print(self)


    def scan_one_way(self, direction: Vec) -> None:
        '''Verifica se há sujeito na direção indicada
        Se houver, ativa o modo limpeza e muda o alvo do robô

        Parâmetro:
            direction: Vec
                A direção escaneada
        '''
        scan_target = self.pos + direction

        if scan_target.is_in_range(*self.end):
            if self.grid[scan_target[0]][scan_target[1]] == 'o':
                self.cleaning = True
                self.target = scan_target         


    def scan_around(self) -> None:
        '''Escaneia o ambiente e define o alvo do robô
        '''

        if self.on_path:
            self.last_target = self.default_target()
            self.last_pos = self.pos
            
        self.scan_one_way(self.down)
        self.scan_one_way(self.right)
        self.scan_one_way(self.up)
        self.scan_one_way(self.left)
        
        if self.pos == self.target:  # Só entra se nenhuma nenhuma sujeira for detectada
            if self.cleaning:
                if self.pos == self.last_pos or self.pos == self.last_target:
                    self.cleaning = False
                    self.on_path = True
                    self.target = self.default_target()
                else:
                    self.go_back()
            else:
                self.target = self.default_target()

        if self.target != self.default_target():
            self.on_path = False

    
    def go_back(self) -> None:
        '''Define o alvo do robô no modo retorno
        '''
        if self.pos[1] < self.last_pos[1]:
            self.target = self.pos + self.right
        elif self.pos[1] > self.last_pos[1]:
            self.target = self.pos + self.left
        elif self.pos[0] < self.last_pos[0]:
            self.target = self.pos + self.down
        elif self.pos[0] > self.last_pos[0]:
            self.target = self.pos + self.up


    def default_target(self) -> Vec:
        '''Calcula o alvo "normal" do robô
        
        Retorna: Vec
            O alvo calculado
        '''
        self.almost_done_check()

        if not self.almost_done and self.pos[0] % 2 == 1:
            target = self.pos + self.left
        else:
            target = self.pos + self.right

        if not target.is_in_range(*self.end):
            if self.almost_done and self.pos == self.end:
                self.done = True
            else:
                target = self.pos + self.down

        return target


    def almost_done_check(self) -> None:
        '''Verifica se o robô passou pelo canto inferior esquerdo
        atribui o resultado ao atributo almost_done
        '''
        if not self.almost_done:
            if self.pos == Vec([self.height - 1, 0]) and not self.cleaning:
                self.almost_done = True


def main():
    grid = [input().split() for _ in range(int(input()))]
    room = Room(grid)
    print(room)
    room.scan_around()
    while not room.done:
        room.move()
        room.scan_around()

if __name__ == '__main__':
    main()
