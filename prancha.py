# =========================
# PRANCHA DE FIGURAS
# =========================

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import math
import string
import os

st.set_page_config(layout="wide")
st.header("Construção de prancha")

# =========================
# UPLOAD
# =========================
imagens = st.file_uploader(
    "Carregue os gráficos (PNG de preferência)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# =========================
# FUNÇÕES
# =========================
def calcular_posicao_texto(posicao, x_img, y_img, largura, altura, offset):
    if posicao == "Superior esquerdo":
        return x_img + offset, y_img + offset

    elif posicao == "Superior direito":
        return x_img + largura - offset, y_img + offset

    elif posicao == "Inferior esquerdo":
        return x_img + offset, y_img + altura - offset

    else:  # Inferior direito
        return x_img + largura - offset, y_img + altura - offset


def carregar_fonte(nome_fonte, tamanho):
    fontes = {
        "Arial": "arial.ttf",
        "Times New Roman": "times.ttf",
        "Courier New": "cour.ttf"
    }

    try:
        return ImageFont.truetype(fontes[nome_fonte], tamanho)
    except:
        return ImageFont.load_default()


def montar_prancha(imagens, n_col, margem, posicao_letra, proporcao_letra, fonte_nome):
    imgs = [Image.open(img).convert("RGB") for img in imagens]

    largura_max = max(img.width for img in imgs)
    altura_max = max(img.height for img in imgs)

    # TAMANHO REAL DA LETRA (PROPORCIONAL!)
    tamanho_letra = int(altura_max * proporcao_letra)
    offset = int(tamanho_letra * 0.4)

    n_linhas = math.ceil(len(imgs) / n_col)

    largura_final = n_col * largura_max + (n_col - 1) * margem
    altura_final = n_linhas * altura_max + (n_linhas - 1) * margem

    prancha = Image.new("RGB", (largura_final, altura_final), "white")
    draw = ImageDraw.Draw(prancha)

    letras = list(string.ascii_uppercase)
    fonte = carregar_fonte(fonte_nome, tamanho_letra)

    for i, img in enumerate(imgs):
        linha = i // n_col
        coluna = i % n_col

        x = coluna * (largura_max + margem)
        y = linha * (altura_max + margem)

        prancha.paste(img, (x, y))

        letra = letras[i]

        x_texto, y_texto = calcular_posicao_texto(
            posicao_letra,
            x,
            y,
            largura_max,
            altura_max,
            offset
        )

        draw.text((x_texto, y_texto), letra, fill="black", font=fonte)

    return prancha

# =========================
# INTERFACE
# =========================
if imagens:

    st.subheader("Configurações do layout")

    n_col = st.slider("Número de colunas", 1, 6, 2)
    margem = st.slider("Margem entre figuras (px)", 0, 150, 30)

    posicao_letra = st.selectbox(
        "Posição das letras",
        [
            "Superior esquerdo",
            "Superior direito",
            "Inferior esquerdo",
            "Inferior direito"
        ]
    )

    fonte_nome = st.selectbox(
        "Fonte da letra",
        ["Arial", "Times New Roman", "Courier New"]
    )

    proporcao_letra = st.slider(
        "Tamanho da letra (proporção da figura)",
        min_value=0.05,
        max_value=0.25,
        value=0.12,
        step=0.01
    )

    st.markdown(
        "📌 **Exemplo:** 0.10 = letra ocupa ~10% da altura da figura"
    )

    prancha = montar_prancha(
        imagens,
        n_col,
        margem,
        posicao_letra,
        proporcao_letra,
        fonte_nome
    )

    st.image(prancha, caption="Prancha final", use_container_width=True)

    # =========================
    # DOWNLOAD
    # =========================
    prancha.save("prancha_final.png", dpi=(300, 300))

    with open("prancha_final.png", "rb") as f:
        st.download_button(
            "📥 Baixar prancha (PNG – 300 dpi)",
            f,
            file_name="prancha_final.png",
            mime="image/png"
        )
