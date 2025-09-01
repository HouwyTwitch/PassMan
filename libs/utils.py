from libs.security.BytesEncrypter import BytesEncrypter
from libs.security.PCHashKey import generatePCHashKey
from os.path import exists
import json
from hashlib import sha256
from libs.security.PCHashKey import HashGenerator
from libs.security.WMI import getPCInfo


def initBytesEncrypter(keyword: str) -> BytesEncrypter:
    if exists('assets/licence.key'):
        with open('assets/licence.key', 'r', encoding='utf-8', errors='ignore') as f:
            return BytesEncrypter(PCHashKey = (sha256((f.read()+keyword).encode()).hexdigest().encode()))
    with open('assets/licence.key', 'w', encoding='utf-8', errors='ignore') as f: f.write(generatePCHashKey())
    return BytesEncrypter(PCHashKey=sha256(HashGenerator(getPCInfo()).generateHash()+keyword).hexdigest().encode())

def saveEncryptedData(bytesEncrypter: BytesEncrypter, _dict: dict, filename: str) -> bool:
    with open(filename, 'wb') as f: f.write(bytesEncrypter.encrypt(str(_dict).encode()))

def loadEncryptedData(bytesEncrypter: BytesEncrypter, filename: str) -> dict:
    try:
        with open(filename, 'rb') as f: token = f.read()
        return json.loads(bytesEncrypter.decrypt(token).decode().replace("'", '"'))
    except FileNotFoundError:
        saveEncryptedData(bytesEncrypter, {}, filename)
        return {}

def addRow(bytesEncrypter: BytesEncrypter, row: dict, filename: str) -> None:
    data = loadEncryptedData(bytesEncrypter, filename)
    data[list(row.keys())[0]] = row[list(row.keys())[0]]
    saveEncryptedData(bytesEncrypter, data, filename)

def deleteRow(bytesEncrypter: BytesEncrypter, row: dict, filename: str) -> None:
    data = loadEncryptedData(bytesEncrypter, filename)
    if list(row.keys())[0] in data: del data[list(row.keys())[0]]
    saveEncryptedData(bytesEncrypter, data, filename)