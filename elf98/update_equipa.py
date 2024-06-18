from sys import argv


def decrypt(data, offset, size):
    ret = ''

    for i in range(offset, offset + size):
        ret += chr((data[i] - data[i - 1]) & 0xff)

    return ret


def encrypt(text):
    out = []

    out.append(len(text))

    for i in range(0, len(text)):
        out.append((ord(text[i]) + out[i]) & 0xff)

    return out


def main(text_input):
    print(f'text to be encrypted: {text_input}')
    encrypted = encrypt(text_input)
    print(f'encrypted text: {' '.join([hex(x) for x in encrypted])}')
    decrypted = decrypt(encrypted, 1, len(encrypted) - 1)
    print(f'decrypted text: {decrypted}')


main(argv[1])
