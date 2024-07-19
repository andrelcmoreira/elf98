
class Serializer:

    @staticmethod
    def encrypt(text):
        out = bytearray()

        out.append(len(text))
        for i in range(0, len(text)):
            out.append((ord(text[i]) + out[i]) & 0xff)

        return out
