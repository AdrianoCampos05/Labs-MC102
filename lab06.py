def expand(v1: list[int], v2: list[int], n1: int, n2: int) -> None:
    '''Se v2 é maior, extende v1 com n1
    Se v1 é maior, extende v2 com n2
    '''
    size_dif = len(v2) - len(v1)
    if size_dif >= 0:
        v1 += [n1]*size_dif
    else:
        v2 += [n2]*(-size_dif)


def soma_vetores(v1: list[int], v2: list[int]) -> list[int]:
    '''Soma os vetores v1 e v2
    '''
    expand(v1, v2, 0, 0)
    new_vec = [v1[i] + v2[i] for i in range(len(v1))]
    return new_vec


def subtrai_vetores(v1: list[int], v2: list[int]) -> list[int]:
    '''Subtrai v2 de v1
    '''
    expand(v1, v2, 0, 0)
    new_vec = [v1[i] - v2[i] for i in range(len(v1))]
    return new_vec


def multiplica_vetores(v1: list[int], v2: list[int]) -> list[int]:
    '''Multiplica v1 e v2
    '''
    expand(v1, v2, 1, 1)
    new_vec = [v1[i] * v2[i] for i in range(len(v1))]
    return new_vec


def divide_vetores(v1: list[int], v2: list[int]) -> list[int]:
    '''Divide v1 por v2
    '''
    expand(v1, v2, 0, 1)
    new_vec = [v1[i] // v2[i] for i in range(len(v1))]
    return new_vec


def multiplicacao_escalar(v: list[int], e: int) -> list[int]:
    '''Multiplica v por e
    '''
    new_vec = [e * i for i in v]
    return new_vec


def n_duplicacao(v: list[int], n: int) -> list[int]:
    '''Duplica v n vezes
    '''
    new_vec = v * n
    return new_vec


def soma_elementos(v: list[int]) -> int:
    '''Soma os elementos de v
    '''
    sum = 0
    for i in v:
        sum += i
    return sum


def produto_interno(v1: list[int], v2: list[int]) -> int:
    '''Calcula o produto interno de v1 e v2
    '''
    expand(v1, v2, 1, 1)
    product = 0
    for i in range(len(v1)):
        product += v1[i] * v2[i]
    return product


def multiplica_todos(v1: list[int], v2: list[int]) -> list[int]:
    '''Multiplica cada entrada de v1 e v2
    '''
    new_vec = []
    for i in v1:
        product = 0
        for j in v2:
            product += i * j
        new_vec.append(product)
    return new_vec


def correlacao_cruzada(v: list[int], mask: list[int]) -> list[int]:
    '''Calcula a correlação_cruzada de v com mask
    '''
    new_vec = []
    for i in range(len(v) - len(mask) + 1):
        product = 0
        for j in range(len(mask)):
            product += v[i+j] * mask[j]
        new_vec.append(product)
    return new_vec


def make_vec(obj: object) -> list[int]:
    '''Transforma obj em um vetor se obj for str ou int
    '''
    if type(obj) == str:
        if type(eval(obj)) == tuple:
            return list(eval(obj))
        else:
            return [eval(obj)]
    elif type(obj) == list:
        return obj
    elif type(obj) == int:
        return [obj]
    else:
        return []


def main() -> None:
    vector = make_vec(input())
    given_func = input()
    while given_func != "fim":
        if given_func == "soma_elementos":
            vector = [soma_elementos(vector)]
        elif given_func == 'multiplicacao_escalar':
            vector = multiplicacao_escalar(vector, int(input()))
        elif given_func == "n_duplicacao":
            vector = n_duplicacao(vector, int(input()))
        else:
            vector = make_vec(eval(given_func)(vector, make_vec(input())))
        print(vector)
        given_func = input()


if __name__ == "__main__":
    main()
