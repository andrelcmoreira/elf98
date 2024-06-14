from sys import argv


def decrypt(data, offset, size):
    ret = ''

    for i in range(offset, offset + size):
        char = (int.from_bytes(data[i]) - int.from_bytes(data[i - 1])) & 0xff
        ret += chr(char)

    return ret


def encrypt(text):
    out = []

    out.append(int.to_bytes(len(text)))

    for i in range(0, len(text)):
        ret = int.to_bytes((ord(text[i]) + int.from_bytes(out[i])) & 0xff)
        out.append(ret)

    return out


def main(text_input):
    print(f'text to be encrypted: {text_input}')
    encrypted = encrypt(text_input)
    print(f'encrypted text: {' '.join([x.hex() for x in encrypted])}')
    decrypted = decrypt(encrypted, 1, len(encrypted) - 1)
    print(f'decrypted text: {decrypted}')


main(argv[1])
