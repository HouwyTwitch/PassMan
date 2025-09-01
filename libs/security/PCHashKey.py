from urllib.parse import quote
from base64 import b64encode
from hashlib import sha256
from time import time
from libs.security.WMI import getPCInfo


class HashGenerator:

    def __init__(self, arr: list) -> None:
        self.data = arr
    
    @staticmethod
    def twoLayerEncoding(text: str) -> str:
        try:
            return b64encode(quote(text).encode()).decode()
        except:
            return 'NONE'
    
    def encodeEachVariable(self) -> None:
        for i in range(len(self.data)):
            self.data[i] = self.twoLayerEncoding(self.data[i])
    
    @staticmethod
    def mergeStrings(arr: list) -> str:
        result = ''
        for i in range(max([len(item) for item in arr])):
            for k in range(len(arr)):
                result = result + arr[k][i%len(arr[k])]
        return result
    
    @staticmethod
    def count_letters_in_a_row(text, index):
        count = 0
        for letter in text[index:]:
            if letter == text[index]:
                count += 1
            else:
                break
        return count
    
    def compressHash(self, text):
        for letter in list(dict.fromkeys([letter for letter in text])):
            text_len = len(text)
            while letter*2 in text:
                count = self.count_letters_in_a_row(text, text.index(letter*2))
                if str(count) == letter:
                    text = text.replace(letter*count, f"{letter}{count-1}+1")
                else:
                    text = text.replace(letter*count, f"{letter}{count}")
        return text
    
    def generateHash(self) -> str:
        self.encodeEachVariable()
        self.hash_result = self.mergeStrings(self.data)
        self.hash_result = self.compressHash(self.hash_result)
        self.hash_result = sha256(self.hash_result.encode()).hexdigest()
        return self.hash_result
            

def generatePCHashKey() -> str:
    return HashGenerator(getPCInfo()).generateHash()