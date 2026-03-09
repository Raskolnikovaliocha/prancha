# =========================
# PRANCHA DE FIGURAS
# =========================

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import math
import string
import io

st.set_page_config(layout="wide")
st.title("Montador de Prancha de Figuras")

# =========================
# GERAR LETRAS (A,B,...AA,AB)
# =========================
def gerar_letra(i):

    letras = string.ascii_uppercase
    resultado = ""

    while True:
        resultado = letras[i % 26] + resultado
        i = i // 26 - 1

        if i < 0:
            break

    return resultado


# =========================
# CARREGAR FONTE
# =========================
def carregar_fonte(tamanho):

    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", tamanho)
    except:
        return ImageFont.load_default()


# =========================
# CRIAR IMAGEM DA LETRA
# =========================
def criar_letra_img(letra, fonte, tamanho):

    img = Image.new("RGBA", (tamanho*2, tamanho*2), (0,0,0,0))
    draw = ImageDraw.Draw(img)

    # contorno branco
    for dx in [-3,3]:
        for dy in [-3,3]:
            draw.text((tamanho//2+dx, tamanho//2+dy),
                      letra,
                      font=fonte,
                      fill="white")

    # letra preta
    draw.text((tamanho//2, tamanho//2),
              letra,
              font=fonte,
              fill="black")

    return img


# =========================
# POSIÇÃO DA LETRA
# =========================
def calcular_posicao(posicao, x, y, largura, altura, margem):

    if posicao == "Superior esquerdo":
        return x + margem, y + margem

    if posicao == "Superior direito":
        return x + largura - margem*2, y + margem

    if posicao == "Inferior esquerdo":
        return x + margem, y + altura - margem*2

    if posicao == "Inferior direito":
        return x + largura - margem*2, y + altura - margem*2


# =========================
# MONTAR PRANCHA
# =========================
def montar_prancha(imagens,
                   colunas,
                   margem,
                   posicao_letra,
                   proporcao_letra,
                   largura_padrao,
                   altura_padrao):

    imgs = []

    for img in imagens:

        try:
            im = Image.open(img).convert("RGB")
            im = im.resize((largura_padrao, altura_padrao),
                           Image.LANCZOS)

            imgs.append(im)

        except:
            pass

    if len(imgs) == 0:
        return None

    largura = largura_padrao
    altura = altura_padrao

    tamanho_letra = max(20, int(altura * proporcao_letra))
    margem_texto = int(tamanho_letra * 0.4)

    fonte = carregar_fonte(tamanho_letra)

    linhas = math.ceil(len(imgs) / colunas)

    largura_final = colunas * largura + (colunas - 1) * margem
    altura_final = linhas * altura + (linhas - 1) * margem

    prancha = Image.new("RGB",
                        (largura_final, altura_final),
                        "white")

    for i, img in enumerate(imgs):

        linha = i // colunas
        coluna = i % colunas

        x = coluna * (largura + margem)
        y = linha * (altura + margem)

        prancha.paste(img, (x, y))

        letra = gerar_letra(i)

        px, py = calcular_posicao(
            posicao_letra,
            x,
            y,
            largura,
            altura,
            margem_texto
        )

        letra_img = criar_letra_img(letra, fonte, tamanho_letra)

        prancha.paste(letra_img,
                      (int(px), int(py)),
                      letra_img)

    return prancha


# =========================
# UPLOAD
# =========================
imagens = st.file_uploader(
    "Carregue os gráficos",
    type=["png","jpg","jpeg"],
    accept_multiple_files=True
)

# =========================
# INTERFACE
# =========================
if imagens:

    st.subheader("Layout")

    colunas = st.slider("Número de colunas",
                        1,6,2)

    margem = st.slider("Margem entre figuras (px)",
                       0,200,40)

    posicao_letra = st.selectbox(
        "Posição da letra",
        [
            "Superior esquerdo",
            "Superior direito",
            "Inferior esquerdo",
            "Inferior direito"
        ]
    )

    proporcao_letra = st.slider(
        "Tamanho da letra",
        0.03,
        0.20,
        0.08,
        0.01
    )

    st.subheader("Dimensões do painel")

    largura_padrao = st.number_input(
        "Largura (px)",
        400,
        3000,
        1200,
        50
    )

    altura_padrao = st.number_input(
        "Altura (px)",
        400,
        3000,
        1600,
        50
    )

    prancha = montar_prancha(
        imagens,
        colunas,
        margem,
        posicao_letra,
        proporcao_letra,
        largura_padrao,
        altura_padrao
    )

    if prancha:

        st.image(prancha, caption="Prancha final")

        buffer = io.BytesIO()

        prancha.save(buffer,
                     format="PNG",
                     dpi=(300,300))

        st.download_button(
            "Baixar prancha (300 dpi)",
            buffer.getvalue(),
            file_name="prancha.png",
            mime="image/png"
        )
