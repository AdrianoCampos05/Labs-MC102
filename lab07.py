def main() -> None:
    global dict
    dict = {
        # Dicionário com definiçoes de vogal, consoante e número
        # Inclui apenas letras minúsculas
        'vogal': ['a', 'e', 'i', 'o', 'u'],
        'consoante': [chr(i) for i in range(98, 123)
                      if chr(i) not in ['a', 'e', 'i', 'o', 'u']],
        'numero': [str(i) for i in range(10)]
    }

    operation = input()
    operand_1 = input()
    operand_2 = input()
    line_count = int(input())
    message = []  # Lista com caracteres da mensagem
    split_message = []  # Lista com linhas da mensagem
    for i in range(line_count):
        line = input()
        message.extend(line)
        split_message.append(line)

    key = find_key(message, operand_1, operand_2, operation)
    solved_message = decipher(split_message, key)
    print(key)
    for i in solved_message:
        print(i)


def find_key_half(message: list[str], operand_str: str) -> int:
    '''Calcula a parte da chave determinada por apenas um dos operandos
    '''
    try:
        operand = dict[operand_str]
    except KeyError:
        return message.index(operand_str)
    else:
        for i in message:
            if i.lower() in operand:
                return message.index(i)


def find_key(message: list[str], op_1: str, op_2: str, operation: str) -> int:
    '''Encontra a chave dada a mensagem, os operandos e a operação
    '''
    key_1 = find_key_half(message, op_1)
    key_2 = key_1 + find_key_half(message[key_1:], op_2)
    key = eval(str(key_1) + operation + str(key_2))
    return key


def decipher(message: list[str], key: int) -> list[str]:
    '''Decifra a mensagem com a chave
    Retorna a mensagem decifrada separada por linhas
    '''
    new_message = []
    for i in message:
        new_line = ''
        for j in i:
            new_line += ascii_loop(ord(j) + key)
        new_message.append(new_line)
    return new_message


def ascii_loop(ordinal: int) -> str:
    '''Converte o ordinal em caracter
    Faz com que os ordinais "loopem" quando passarem de 126
    '''
    return chr((ordinal - 32) % 95 + 32)


if __name__ == "__main__":
    main()
