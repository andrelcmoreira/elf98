from sys import argv
from dataclasses import dataclass


@dataclass
class Player:

    name: str
    position: str
    country: str

    def __repr__(self):
        return f'{self.position}: {self.name} - {self.country}'


# https://www.espn.com.br/futebol/time/elenco/_/id/2026/bra.sao_paulo
PLAYERS = [
    Player(name='Rafael', position='G', country='BRA'),
    Player(name='Jandrei', position='G', country='BRA'),
    Player(name='Igor', position='Z', country='BRA'),
    Player(name='Diego Costa', position='Z', country='BRA'),
    Player(name='Robert Arboleda', position='Z', country='EQU'),
    Player(name='Wellington', position='Z', country='BRA'),
    Player(name='Alan Franco', position='Z', country='ARG'),
    Player(name='Michel Araújo', position='M', country='URU'),
    Player(name='Giuliano Galoppo', position='M', country='ARG'),
    Player(name='Rodrigo Nestor', position='M', country='BRA'),
    Player(name='Luiz Gustavo', position='M', country='BRA'),
    Player(name='Lucas Moura', position='A', country='BRA'),
    Player(name='Jonathan Calleri', position='A', country='ARG'),
    Player(name='Luciano', position='A', country='BRA'),
    Player(name='Ferreira', position='A', country='BRA'),
    Player(name='Juan', position='A', country='BRA'),
    Player(name='Erick', position='A', country='BRA'),
]


def decrypt(data, offset, size):
    ret = ''

    for i in range(offset, offset + size):
        ret += chr((data[i] - data[i - 1]) & 0xff)

    return ret


def to_pos_code(pos):
    match pos:
        case 'G': return 0
        case 'Z': return 1
        case 'M': return 2
        case 'A': return 3


def encrypt(text):
    out = []

    out.append(len(text))

    for i in range(0, len(text)):
        out.append((ord(text[i]) + out[i]) & 0xff)

    return out


def encrypt_players():
    for player in PLAYERS:
        pass # TODO


def main(text_input):
    print(f'text to be encrypted: {text_input}')
    encrypted = encrypt(text_input)
    print(f'encrypted text: {' '.join([hex(x) for x in encrypted])}')
    decrypted = decrypt(encrypted, 1, len(encrypted) - 1)
    print(f'decrypted text: {decrypted}')


main(argv[1])
