from PIL import Image, ImageDraw, ImageFont
from unidecode import unidecode
import json, os

def criar_hu(titulo, texto):
    # Abrir a imagem de fundo
    fundo = Image.open("imgs/hu_template.png").convert("RGBA")
    largura, altura = fundo.size

    desenho = ImageDraw.Draw(fundo)
    
    # Adicionar o título
    fonte_titulo = ImageFont.truetype("fonts/Roboto-Bold.ttf", 100)
    desenho.text((20, 20), titulo, font=fonte_titulo, fill=(0, 0, 0, 255))
    
    # Adicionar o texto
    fonte_texto = ImageFont.truetype("fonts/Roboto-Regular.ttf", 64)
    desenho.text((20, 365), texto, font=fonte_texto, fill=(0, 0, 0, 255))
    
    return fundo

def formatar_nome(nome):
    return unidecode(nome.replace(" ", "_").replace("\n", "").lower())


def dividir_string(string, limite):
    palavras = string.split()
    texto = ""
    parte_atual = ""

    for palavra in palavras:
        if len(parte_atual) + len(palavra) + 1 <= limite:
            if parte_atual:
                parte_atual += " "
            parte_atual += palavra
        else:
            texto += f"{parte_atual}\n"
            parte_atual = palavra

    texto += f"{parte_atual}\n"

    return texto


def gerar_hus(index, param):

    dados = json.load(open('json/tcc_hus.json', 'r', encoding='utf-8'))

    for hus_usuario in dados[index]['hus']:

        titulo = hus_usuario['titulo']
        texto = hus_usuario['texto']

        hu = criar_hu(dividir_string(titulo,20), dividir_string(texto,30))

        caminho = f"hus/{param}/{formatar_nome(titulo)}"
        if not os.path.exists(caminho):
            os.makedirs(caminho)


        hu.save(f"{caminho}/hu-{formatar_nome(titulo)}.png")

        for subs_usuario in hus_usuario['subs']:
            subs_titulo = subs_usuario['titulo']
            subs_texto = subs_usuario['texto']
            
            subs_hu = criar_hu(dividir_string(subs_titulo,20), dividir_string(subs_texto,30))
            subs_hu.save(f"{caminho}/husub-{formatar_nome(subs_titulo)}.png")

gerar_hus(0, "usuario")


# titulo = "Disponibilização de informações sobre cooperativas"
# texto = "Como membro de uma cooperativa, eu quero poder disponibilizar informações sobre a minha cooperativa, como histórico, missão, visão e valores, para que minha cooperativa tenha uma maior transparência e engajamento com o público."
# 
# hu = criar_hu(dividir_string(titulo, 20), dividir_string(texto, 30))
# hu.save(f"debug.png")
