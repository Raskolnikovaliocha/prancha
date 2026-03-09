import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import math
import string
import io

st.title("Montador de Prancha")

def gerar_letra(i):

    letras = string.ascii_uppercase
    resultado = ""

    while True:
        resultado = letras[i % 26] + resultado
        i = i // 26 - 1
        if i < 0:
            break

    return resultado


def carregar_fonte(tamanho):

    try:
        return ImageFont.truetype("arial.ttf", tamanho)
    except:
        return ImageFont.load_default()


imagens = st.file_uploader(
    "Carregue imagens",
    accept_multiple_files=True
)

if imagens:

    colunas = st.slider("Colunas",1,6,2)
    margem = st.slider("Margem",0,200,40)

    largura = st.number_input("Largura",800,3000,1200)
    altura = st.number_input("Altura",800,3000,1600)

    proporcao_letra = st.slider("Tamanho letra",0.03,0.2,0.08)

    tamanho_letra = int(altura * proporcao_letra)

    fonte = carregar_fonte(tamanho_letra)

    imgs = []

    for img in imagens:

        im = Image.open(img).convert("RGB")
        im = im.resize((largura,altura))
        imgs.append(im)

    linhas = math.ceil(len(imgs)/colunas)

    prancha = Image.new(
        "RGB",
        (
            colunas*largura+(colunas-1)*margem,
            linhas*altura+(linhas-1)*margem
        ),
        "white"
    )

    draw = ImageDraw.Draw(prancha)

    for i,img in enumerate(imgs):

        linha = i//colunas
        coluna = i%colunas

        x = coluna*(largura+margem)
        y = linha*(altura+margem)

        prancha.paste(img,(x,y))

        letra = gerar_letra(i)

        px = x + 30
        py = y + 30

        for dx in [-3,-2,-1,1,2,3]:
            for dy in [-3,-2,-1,1,2,3]:

                draw.text(
                    (px+dx,py+dy),
                    letra,
                    font=fonte,
                    fill="white"
                )

        draw.text(
            (px,py),
            letra,
            font=fonte,
            fill="black"
        )

    st.image(prancha)

    buffer = io.BytesIO()

    prancha.save(buffer,
                 format="PNG",
                 dpi=(300,300))

    st.download_button(
        "Baixar",
        buffer.getvalue(),
        "prancha.png"
    )
