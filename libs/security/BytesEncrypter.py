from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from libs.security.PCHashKey import HashGenerator
from base64 import urlsafe_b64encode
from time import time
from libs.security.WMI import getPCInfo


class BytesEncrypter:
    
    def __init__(self, PCHashKey: str = HashGenerator(getPCInfo()).generateHash().encode(), salt: bytes = str(int(time()*10**6)).encode()) -> None:
        self.backend = default_backend()
        self.PCHashKey = PCHashKey
        self.salt = urlsafe_b64encode(salt)
                
    def initialize(self) -> None:
        self.kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                              length=32,
                              salt=self.salt,
                              iterations=2**15,
                              backend=self.backend)                         
        self.key = urlsafe_b64encode(self.kdf.derive(self.PCHashKey))
        self.f = Fernet(self.key)       
    
    @staticmethod
    def insertLetterIntoString(letter: str, text: str, index: int) -> str:
        s1, s2 = text[:index], text[index:]
        return s1 + letter + s2      
    
    def insertSaltIntoContent(self, salt: bytes, content: bytes) -> bytes:
        strSalt, strContent = salt.decode(), content.decode()
        saltLength, contentLength = len(strSalt), len(strContent)
        if contentLength == 0:
            return salt
        blockSize = contentLength // saltLength
        if blockSize > 0:
            for i in range(saltLength):
                strContent = self.insertLetterIntoString(strSalt[i], strContent, i*blockSize+i)
        else:
            return (strSalt+strContent).encode()
        return strContent.encode()
            
    def getSaltFromContent(self, content: bytes) -> bytes:
        strSalt, strContent = '', content.decode()
        saltLength, contentLength = 24, len(strContent)-24
        if contentLength < 24:
            self.salt = strContent[:24].encode()
            return strContent[24:].encode()
        blockSize = contentLength // saltLength
        for i in range(saltLength):
            strSalt = strSalt + strContent[i*blockSize]
            strContent = strContent[:i*blockSize] + strContent[i*blockSize+1:]
        self.salt = strSalt.encode()
        return strContent.encode()
            
    def encrypt(self, content: bytes) -> bytes:
        return self.insertSaltIntoContent(self.salt, self.f.encrypt(content))
    
    def decrypt (self, token: bytes) -> bytes:
        token = self.getSaltFromContent(token)
        self.initialize()
        return self.f.decrypt(token)