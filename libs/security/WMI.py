from win32com.client import GetObject
from os import listdir


class WMIClassesLoader:

    def __init__(self, folder: str) -> None:
        self.folder = folder
        self.filenames = listdir(self.folder)
        self.file_extension = '.' + self.filenames[0].split('.')[-1]
        self.classes = [filename.replace(self.file_extension, '') for filename in self.filenames]
        self.fields = [[] for _ in self.classes]        
    
    def load_fields(self) -> None:
        for i in range(len(self.classes)):
            with open(f'{self.folder}/{self.classes[i]}{self.file_extension}', 'r') as f:
                for line in f:
                    if (';' in line) and ('}' not in line):
                        self.fields[i].append(line.split(' ')[-1].split(';')[0].split('[')[0])
    
    def return_data(self) -> tuple:
        return self.classes, self.fields
 
class WMIInfoRetriever:

    def __init__(self, classes: list, fields: list) -> None:
        self.wmi = GetObject("winmgmts:root\cimv2")
        self.classes = classes
        self.fields = fields
        self._dict = {}
        
        for attr in self.classes:
            setattr(self, attr, self.wmi.ExecQuery("Select * from " + attr))
        
        for i in range(len(self.classes)):
            arr = getattr(self, self.classes[i])
            for j in range(len(arr)):
                for k in range(len(self.fields[i])):
                    try:
                        value = getattr(arr[j], self.fields[i][k])
                        if value not in [None, 'Error']:
                            self._dict[f"{self.classes[i]}.{self.fields[i][k]}[{j}]"] = value
                    except:
                        pass
    
    def get_dict(self):
        return self._dict
    
def getPCInfo() -> list:
    loader = WMIClassesLoader("libs/security/WMI_Classes")
    loader.load_fields()
    classes, fields = loader.return_data()
    retriever = WMIInfoRetriever(classes, fields)
    _dict = retriever.get_dict()
    return [item[-1] for item in _dict.items()]