
class BaseParser:

    def get_field(self, data, offset, size):
        return data[offset:offset + size]

    def decrypt_field(self, data, offset, size):
        ret = ''

        for i in range(offset, offset + size):
            ret += chr((data[i] - data[i - 1]) & 0xff) # picking only the 8 less
                                                       # significant bits

        return ret
