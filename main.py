import string

import PySimpleGUI as sg
from criando_pdf import pdf

sg.theme('Dark Grey 13')  # definindo o tema do layout

"""
Layout certo
"""


def header(cs=None, sre=None, lsre=None, disc=None, tri=None, year=None, aulasd=None, aulasp=None):
    return cs, sre, lsre, disc, tri, year, aulasd, aulasp


def listaNF(nf):
    lnotas = []
    lfaltas = []
    for k, v in nf.items():
        if k[0] == 'n':
            lnotas.append(v)
        if k[0] == 'f':
            lfaltas.append(v)
    return lnotas, lfaltas


def xInRange(num):
    return True if num in range(1, 60) else False


def checkBlankField(vs):
    return any(not value for value in vs.values())


def container(linhas):
    layout1 = [*[[sg.Text(f'{i}')] for i in range(1, linhas + 1)]]
    layout2 = [*[[sg.Input(size=10, key=f"n{j}")] for j in range(1, linhas + 1)]]  #keys adicionadas em notas e faltas
    layout3 = [*[[sg.Input(size=10, key=f"f{k}")] for k in range(1, linhas + 1)]]
    layfinal = [[sg.Column(layout1, key='col1'), sg.Column(layout2, key='col2'), sg.Column(layout3, key='col3')],
                [sg.Push(), sg.Button("Lançar", key="lancar"), sg.Button("Voltar", key="voltar"), sg.Push()]]
    return layfinal


def main_layout():
    return [
        #Curso
        [sg.Text('Curso:'),  # text é o texto mostrado.
         sg.Checkbox("EM", default=False, enable_events=True, key="ckbxEM", disabled=False),
         sg.Checkbox("EF", default=False, enable_events=True, key="ckbxEF", disabled=False),
         #Turma
         sg.Text('Turma:'),
         sg.Combo(['1°', '2°', '3°', '4°', '5°', '6°', '7°', '8°', '9°'], default_value="Ex: 1°, 2°...", size=(5, 10),
                  key='serie', enable_events=True,bind_return_key=True),
         sg.Combo(list(string.ascii_uppercase), default_value="A", size=(5, 10),
                  key='lserie', enable_events=True, bind_return_key=True)
         ],
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


if __name__ == "__main__":
    # STEP 1 definir o layout
    #main_layout =

    # janela principal
    main_window = sg.Window('Gerador de tarjeta', main_layout(),
                            finalize=True)  #window cria a janela. você dá um título e passa o layout montado

    # Variáveis para rastrear o estado anterior das checkboxes
    estado_ckbxEM_anterior = False
    estado_ckbxEF_anterior = False

    janela1 = True
    janela2 = False
    # STEP3 - o loop que mantém o programa aberto.
    while janela1:
        event, values = main_window.read()
        if event == sg.WIN_CLOSED:
            janela1 = False
            break

        """
        Aqui vamos preencher a função header
        """
        #variável "Curso", das Checkbox. Uma dor de cabeça.
        curso = None

        try:
            # Define o valor de curso baseado no estado atual das checkboxes
            if values.get("ckbxEM"):
                curso = "EM"
            elif values.get("ckbxEF"):
                curso = "EF"
            else:
                curso = ''  # Nenhuma das checkboxes está selecionada

            # Verifica mudanças no estado da checkbox "EM"
            if values.get("ckbxEM") != estado_ckbxEM_anterior:
                estado_ckbxEM_anterior = values.get("ckbxEM")
                if estado_ckbxEM_anterior:
                    main_window['ckbxEF'].update(disabled=True)
                    main_window['serie'].update(values=["1°", "2°", "3°"])
                else:
                    main_window['ckbxEF'].update(disabled=False)
                    main_window['serie'].update(values=['1°', '2°', '3°', '4°', '5°', '6°', '7°', '8°', '9°'])

            # Verifica mudanças no estado da checkbox "EF"
            if values.get("ckbxEF") != estado_ckbxEF_anterior:
                estado_ckbxEF_anterior = values.get("ckbxEF")
                if estado_ckbxEF_anterior:
                    main_window['ckbxEM'].update(disabled=True)
                    main_window['serie'].update(values=['1°', '2°', '3°', '4°', '5°', '6°', '7°', '8°', '9°'])
                else:
                    main_window['ckbxEM'].update(disabled=False)
                    main_window['serie'].update(values=["1°", "2°", "3°"])

        except (TypeError, AttributeError):
            pass

        #variavel serie
        serie = None
        if values.get("serie"):
            serie = values["serie"]

        #variavel letradaserie
        lserie = None
        if values.get('lserie'):
            lserie = values.get('lserie')

        #variavel disciplina
        disciplina = None
        if values['disc']:
            disciplina = values['disc']

        #variavel bimestre, trimestre etc
        trimestre = None
        if values['tri']:
            trimestre = values['tri']

        ano = None
        if values['ano']:
            ano = values['ano'][2:]

        aulas_dadas = None
        if values['aulas_dadas']:
            aulas_dadas = values['aulas_dadas']

        aulas_prev = None
        if values['aulas_prev']:
            aulas_prev = values['aulas_prev']

        head = header(curso, serie, lserie, disciplina, trimestre, ano, aulas_dadas, aulas_prev)

        #aqui tem que lançar os dados básicos
        if event == 'continuar':
            # verificando se o input de número de notas é um número válido
            try:
                x = int(values["notas_lancadas"])
                if not xInRange(x):
                    sg.popup_error("Valor Inválido.")
                    continue
                    #a chamada de uma segunda janela quebra a checkbox
                main_window.close()
                main_window = sg.Window("Notas e Faltas", container(x), finalize=True)
                janela1 = False
                janela2 = True
            except ValueError:
                sg.popup("Aviso:", "Campo em branco/Valor Inválido.")

        #usando segundo loop pra evitar KeyError
        while janela2:
            #aqui lança as notas e faltas
            event, values = main_window.read()

            if event == sg.WIN_CLOSED:
                janela2 = False
                break

            if event == "lancar":
                if checkBlankField(values):
                    sg.popup("", "Há espaços em branco no arquivo. Continuaremos com a operação.")
                try:
                    pdf(head, listaNF(values))
                    sg.popup("", "PDF gerado!")
                except Exception:
                    sg.popup("", "Arquivo já existente.")

            if event == "voltar":
                # Fechar o segundo layout e reabrir o primeiro
                main_window.close()
                main_window = sg.Window('Gerador de tarjeta', main_layout(), finalize=True)
                janela2 = False
                janela1 = True
