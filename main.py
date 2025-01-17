import PySimpleGUI as sg

sg.theme('Dark Grey 13')  # definindo o tema do layout

"""
Layout certo
"""


def container(linhas):
    layout1 = [*[[sg.Text(f'{i}')] for i in range(1, linhas+1)]]
    layout2 = [*[[sg.Input(size=10)] for j in range(1, linhas+1)]]
    layout3 = [*[[sg.Input(size=10)] for k in range(1, linhas+1)]]
    layfinal = [[sg.Column(layout1, key='col1'), sg.Column(layout2, key='col2'), sg.Column(layout3, key='col3')]]
    return layfinal


# STEP 1 definir o layout
main_layout = [
    #Curso
    [sg.Text('Curso:'),  # text é o texto mostrado.
     sg.Checkbox("EM", default=False, enable_events=True, key="ckbxEM", disabled=False),
     sg.Checkbox("EF", default=False, enable_events=True, key="ckbxEF", disabled=False),
     #Turma
     sg.Text('Turma:'),
     sg.Combo(['1°', '2°', '3°', '4°', '5°', '6°', '7°', '8°', '9°'], default_value="Ex: 1°, 2°...", size=(10, 10),
              key='série', enable_events=True,
              bind_return_key=True)],
    #Disciplina
    [sg.Text('Disciplina:'), sg.Input(default_text="Ex: Português", size=(10, 10), enable_events=True, key="disc")],
    #Trimestre
    [sg.Text('Trimestre:'),
     sg.Combo(['1°', '2°', '3°', '4°', '5°', '6°'], size=(10, 10), key='tri', enable_events=True,
              bind_return_key=True)],
    #Ano
    [sg.Text('Ano:'), sg.Input(default_text="Ex: 2025", size=(10, 10), enable_events=True, key="ano")],
    # input é a inputbox. ela precisa de pelo menos mais dois parâmetros: enableevents e key, que é o nome que vc
    # usará pra pegá-lo depois
    #aulas dadas e previstas
    [sg.Text('Aulas dadas:'), sg.Input(size=(10, 10), enable_events=True, key="aulas_dadas"),
     sg.Text('Aulas Previstas:'),
     sg.Input(size=(10, 10), enable_events=True, key="aulas_prev")],

    [sg.Text("Notas a lançar:"), sg.Input(size=(10, 10), enable_events=True, key="notas_lancadas")],
    #esse input definirá o número de linhas da window2

    [sg.Push(), sg.Button('Continuar', enable_events=True, key="continuar")]  # button é botão
]

# janela principal
main_window = sg.Window('Gerador de tarjeta', main_layout,
                        finalize=True)  #window cria a janela. você dá um título e passa o layout montado
window2 = None

# STEP3 - o loop que mantém o programa aberto.
while True:
    window, event, values = sg.read_all_windows()  # ler todas as janelas abertas
    # print(window.Title, event, values) if window is not None else None  #ler as janelas desde que não nulas

    if event == 'continuar' and values["notas_lancadas"].strip():  #se o usuário abrir outra janela
        window2 = sg.Window("Notas e Faltas", container(int(values["notas_lancadas"])), finalize=True)
    if event == 'continuar' and not values["notas_lancadas"].strip():  # se o usuário abrir outra janela
        sg.popup("Aviso:", "Você precisa informar a quantidade de notas a lançar.")
    if event == sg.WIN_CLOSED and window == window2:  #se o usuário fechar essa segunda janela
        window2.close()
        window2 = None
    if event == sg.WIN_CLOSED and window == main_window:
        #print("o botão apertado foi da janela 1")
        break

main_window.close() #encerra o programa
if window2:
    window2.close()

