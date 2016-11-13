"""Создать декораторы для шифрования и дешифрования строковых литералов в качестве возвращаемого значения и параметра \
соответственно. Для шифрования использовать перестановочный шифр, в котором тест делится на блоки, которые \
перемешиваются и в каждом блоке перемешиваются элементы"""

class TurningEncryption(object):
    text = ""
    text_len = 0
    blocks_sequence = ""  # sequence of blocks in message
    block_len = 0
    elements_sequence = ""  # sequence of elements in block
    list_letters = list()  # string is being built here

    def __init__(self, message, blocks_seq, elements_seq):
        self.text = message
        self.text_len = len(message)
        self.blocks_sequence = list(map(int, blocks_seq.split()))
        self.elements_sequence = list(map(int, elements_seq.split()))
        self.block_len = len(self.elements_sequence)

        # check if we can divide text into blocks of assigned length
        if (self.text_len <= len(self.blocks_sequence) * len(self.elements_sequence)):
            self.text += " " * (len(self.blocks_sequence) * len(self.elements_sequence) - self.text_len)
        else:
            raise Exception("Can't divide message on blocks")

    def encrypt(self):  #O(n)
        self.list_letters.clear()
        for gr_num in self.blocks_sequence:
            for el_num in self.elements_sequence:
                pos = self.block_len * gr_num + el_num  # getting a position of current symbol to input in result
                self.list_letters.append(self.text[pos])  # decided to avoid string concatenation (memory issues)
        return ''.join(self.list_letters) # getting string from list

    def decrypt(self):  #O(n)
        self.list_letters.clear()
        for i in range(0, self.text_len // self.block_len):  # creating empty list to store blocks and elements [[],[]]
            temp = list()
            for k in range(0, self.block_len):
                temp.append(k)
            self.list_letters.append(temp)

        el_counter = 0  # counter for current element
        for gr_num in self.blocks_sequence:
            for el_num in self.elements_sequence:
                # write symbol with current position in needed cell
                self.list_letters[gr_num][el_num] = self.text[el_counter]
                el_counter += 1
            self.list_letters[gr_num] = ''.join(self.list_letters[gr_num]) # decided to avoid string concatenation
        return ''.join(self.list_letters)



def encrypt_decorator(groups, elements):
    print("encrypt_decorator")
    def encryption(function_to_decorate):
        print("encryption")
        def wrapper(*args, **kwargs):
            text = function_to_decorate(*args, **kwargs)
            enc = TurningEncryption(text, groups, elements)
            return enc.encrypt()
        return wrapper
    return encryption

def decrypt_decorator(groups, elements):
    print("decrypt_decorator")
    def decryption(function_to_decorate):
        print("decryption")
        def wrapper(str):
            decrypt = TurningEncryption(str, groups, elements)
            str = decrypt.decrypt()
            return function_to_decorate(str)
        return wrapper
    return decryption


@encrypt_decorator("2 1 0 3", "1 0 2")
def my_text_gen(bla):
    return "hello world"

@decrypt_decorator("2 1 0 3", "1 0 2")
def get_text(dec):
    print(dec)

crypt = my_text_gen(453)
print(crypt)
get_text(crypt)

