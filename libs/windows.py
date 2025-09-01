import PySimpleGUI as sg
from libs.utils import addRow


def addWindow(bytesEncrypter, theme: str, filename: str):
    sg.theme(theme)

    layout = [[sg.Text('Name/Link: '), sg.Push(), sg.Input(size=(25,1), key='-NAME-')],
              [sg.Text('Password: '), sg.Push(), sg.Input(size=(25,1), key='-PASS-', password_char='•')],
              [sg.Push(), sg.Button('Add')]]

    window = sg.Window('PassMan - Add window', layout)
    event, values = window.read()
    if event == 'Add': addRow(bytesEncrypter, {values['-NAME-']: values['-PASS-']}, filename)
    window.close()