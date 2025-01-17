import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


# Parâmetros: um canva, x e y como posições, o texto e opcionalmente o tamanho da fonte.
def rodarTexto90(c, a, b, message, fonte=8):
    # Cria um TextObject
    text = c.beginText()
    # Define a posição inicial do TextObject. irrelevante aqui.
    text.setTextOrigin(100, 100)
    # Aplica a matriz de transformação para rotacionar o texto
    # Rotação de 90 graus
    angle = 90
    rotation_matrix = \
        [
            math.cos(math.radians(angle)), math.sin(math.radians(angle)),  # a, b
            -math.sin(math.radians(angle)), math.cos(math.radians(angle)),  # c, d
            a, b  # e, f (deslocamento)
        ]
    text.setTextTransform(*rotation_matrix)
    # Define o texto e o estilo
    text.setFont("Helvetica", fonte)
    text.textLine(message)
    # Adiciona o TextObject ao canvas
    c.drawText(text)

# Funcionando
# pdf = canvas.Canvas("métodofinal.pdf", pagesize=A4)

# rodarTexto90(pdf, 200, 200, "Números")
# pdf.showPage()
# pdf.save()
