from sys import setrecursionlimit
setrecursionlimit(4000)

class Image:
    '''Classe que representa uma imagem

    Atributos:
        _height: int
            o número de pixels por coluna
        _width: int
            o número de pixels por linha
        _max_value: int
            a intensidade máxima de um pixel
        _grid: list[list[int]]
            a matriz com a intensidade de cada pixel
            nota: o pixel (x, y) corresponde à entrada [y][x] da matriz
    '''
    def __init__(self, height, width, max_value, grid):
        self._height = height
        self._width = width
        self._max_value = max_value
        self._grid = grid


    def __str__(self):
        string = ''
        for i in self._grid:
            for j in i:
                string += f'{j} '
            
            string = string.strip()
            string += '\n'

        string = string.strip('\n')
        return string


    def neighbors(self, x: int, y: int) -> list[tuple[int]]:
        '''Devolve uma lista com as coordenadas dos pixels adjacentes ao pixel (x y)
        '''
        pixels = []
        
        for i in (-1, 1, 0):
            new_x = x + i
            if 0 <= new_x < self._width:
                for j in (-1, 1, 0):
                    new_y = y + j
                    if 0 <= new_y < self._height:
                        pixels.append((new_x, new_y))

        pixels.pop()  # O último pixel é o pixel original
        return pixels


    def close_enough(self, x: int, y: int, value: int, threshold: int) -> bool:
        '''Determina se o pixel (x, y) está dentro do limiar de tolerância
        '''
        delta = abs(self._grid[y][x] - value)
        return delta <= threshold


    def expand_region(self, x: int, y: int, threshold: int, value, region) -> None:
        '''Adiciona o pixel (x, y) à região.
        Chama a mesma função para todos os vizinhos de (x, y) que estiverem dentro do limiar
        '''
        region.append((x, y))

        for i in self.neighbors(x, y):
            if (i[0], i[1]) in region:
                continue

            if self.close_enough(i[0], i[1], value, threshold):
                self.expand_region(i[0], i[1], threshold, value, region)


    def get_region(self, x: int, y: int, threshold: int) -> list[tuple[int]]:
        '''Retorna a região conectada ao pixel (x, y)
        '''
        region = []
        value = self._grid[y][x]
        self.expand_region(x, y, threshold, value, region)
        return region


    def bucket(self, value: int, threshold: int, x: int, y: int):
        '''Altera o valor de todos os pixels da região conectada a (x, y) para o valor dado
        '''
        region = self.get_region(x, y, threshold)
        for i in region:
            self._grid[i[1]][i[0]] = value

    
    def negative(self, threshold: int, x: int, y: int):
        '''Inverte o valor de todos os pixels da região conectada a (x, y)
        '''
        region = self.get_region(x, y, threshold)
        for i in region:
            self._grid[i[1]][i[0]] = self._max_value - self._grid[i[1]][i[0]]
    

    def cmask(self, threshold: int, x: int, y: int):
        '''Altera o valor de todos os pixels conectados a (x, y) para 0
        Altera o valor dos demais pixels para 255
        '''
        region = self.get_region(x, y, threshold)
        for i in range(self._width):
            for j in range(self._height):
                if (i, j) in region:
                    self._grid[j][i] = 0
                else:
                    self._grid[j][i] = 255


def main():
    in_file = open(input())
    version = in_file.readline().strip('\n')
    in_file.readline()  # Inútil
    width, height = in_file.readline().split()
    width, height = int(width), int(height)
    max_value = int(in_file.readline())

    grid = []
    
    for _ in range(height):
        line = in_file.readline().split()
        line = [int(i) for i in line]
        grid.append(line)

    in_file.close()
    image = Image(height, width, max_value, grid)

    for _ in range(int(input()) - 1):
        command = input().split()
        function = command.pop(0)

        parameters = [int(i) for i in command]
        if function == 'bucket':
            image.bucket(*parameters)
        elif function == 'negative':
            image.negative(*parameters)
        elif function == 'cmask':
            image.cmask(*parameters)
        print(image)

    
    print(f'{version}')
    print('# Imagem criada pelo lab13')
    print(f'{width} {height}')
    print(f'{max_value}')
    print(image)


if __name__ == '__main__':
    main()
        