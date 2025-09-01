from libs.utils import *
from libs.windows import *
import PySimpleGUI as sg 
import subprocess 
from hashlib import sha256


def form_records(user_data: dict) -> list:
    records = []
    for k in list(user_data.keys()):
        num_of_visible_symbols = len(user_data[k])-4 if len(user_data[k]) > 5 else 0
        num_of_hidden_symbols = 4 if len(user_data[k]) > 5 else len(user_data)
        records.append(f"{k}: {USER_DATA[k][:num_of_visible_symbols] + '•'*num_of_hidden_symbols}")
    return records


if __name__ == '__main__':

    THEME = 'Black'
    sg.theme(THEME)
    
    USER_DATA = None
    FILENAME = None

    layout = [
              [sg.Text('Enter keyword to access passwords list: '), sg.Push()],
              [sg.Text('Keyword: '), sg.Push(), sg.Input(size=(25,1), key='-KEY-', password_char='•')],
              [sg.Push(), sg.Button('Submit')]]

    window = sg.Window('PassMan - Authentication window', layout)
    while True:
        event, values = window.read()
        if event == 'Submit':
            BYTES_ENCRYPTER = initBytesEncrypter(values["-KEY-"])
            BYTES_ENCRYPTER.initialize()
            try:
                USER_DATA = loadEncryptedData(BYTES_ENCRYPTER, f'assets/data/{sha256(values["-KEY-"].encode()).hexdigest()}.json')
                FILENAME = f'assets/data/{sha256(values["-KEY-"].encode()).hexdigest()}.json'
                break
            except: sg.popup("You can't open this file from you'r PC.")
        else: exit(0)
    window.close()
    
    RECORDS = form_records(USER_DATA)
    VISIBLE_RECORDS = RECORDS
    FIND_NAME = '' 

    layout = [[sg.Text('Find: '), sg.Push(), sg.Input(size=(54, 1), key='-FIND-', enable_events=True)],
              [sg.Listbox(values=VISIBLE_RECORDS, enable_events=True, size=(60,20), key='RECORDS')],
              [sg.Button('Add', size=(8, 1)), sg.Push(), sg.Button('Remove', size=(8, 1)), sg.Push(), sg.Button('Copy', size=(8, 1))]]

    window = sg.Window('PassMan - Main window', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: break
        elif event == 'RECORDS':
            try:
                INDEX = RECORDS.index(values['RECORDS'][0])
                SELECTED_RECORD = {list(USER_DATA.keys())[INDEX]: USER_DATA[list(USER_DATA.keys())[INDEX]]}
            except: pass
        elif event == '-FIND-':
            if values['-FIND-'] != FIND_NAME:
                FIND_NAME = values['-FIND-']
                VISIBLE_RECORDS = [x for x in RECORDS if FIND_NAME in x.split(': ')[0]]
                window['RECORDS'].update(VISIBLE_RECORDS)
        elif event == 'Add':
            addWindow(BYTES_ENCRYPTER, THEME, FILENAME)
            USER_DATA = loadEncryptedData(BYTES_ENCRYPTER, FILENAME)
            RECORDS = form_records(USER_DATA)
            VISIBLE_RECORDS = [x for x in RECORDS if FIND_NAME in x.split(': ')[0]]
            window['RECORDS'].update(VISIBLE_RECORDS)
        elif event == 'Remove':
            try:  deleteRow(BYTES_ENCRYPTER, SELECTED_RECORD, FILENAME)
            except: sg.popup('Error', 'Select record before removing')
            USER_DATA = loadEncryptedData(BYTES_ENCRYPTER, FILENAME)
            RECORDS = form_records(USER_DATA)
            VISIBLE_RECORDS = [x for x in RECORDS if FIND_NAME in x.split(': ')[0]]
            window['RECORDS'].update(VISIBLE_RECORDS)
        elif event == 'Copy':
            try: subprocess.run("clip", universal_newlines=True, input=SELECTED_RECORD[list(SELECTED_RECORD.keys())[0]])
            except: sg.popup('Error', 'Select record before removing')
    window.close()