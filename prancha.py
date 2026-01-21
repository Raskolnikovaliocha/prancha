# =========================
# PRANCHA DE FIGURAS – VERSÃO FINAL
# =========================

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import math
import string

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
def carregar_fonte(tamanho):
    # Fonte garantida no PIL / Streamlit Cloud
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", tamanho)
    except:
        return ImageFont.load_default()


def calcular_posicao_texto(posicao, x_img, y_img, largura, altura, margem):
    if posicao == "Superior esquerdo":
        return (x_img + margem, y_img + margem), "la"

    elif posicao == "Superior direito":
        return (x_img + largura - margem, y_img + margem), "ra"

    elif posicao == "Inferior esquerdo":
        return (x_img + margem, y_img + altura - margem), "ld"

    else:  # Inferior direito
        return (x_img + largura - margem, y_img + altura - margem), "rd"


def montar_prancha(imagens, n_col, margem, posicao_letra, proporcao_letra, largura_padrao, altura_padrao):
    imgs = [
    Image.open(img)
    .convert("RGB")
    .resize((largura_padrao, altura_padrao), Image.LANCZOS)
    for img in imagens]


    largura_max = max(img.width for img in imgs)
    altura_max = max(img.height for img in imgs)

    # 🔥 TAMANHO REAL DA LETRA (PROPORCIONAL À FIGURA)
    tamanho_letra = int(altura_max * proporcao_letra)
    margem_texto = int(tamanho_letra * 0.3)

    fonte = carregar_fonte(tamanho_letra)

    n_linhas = math.ceil(len(imgs) / n_col)

    largura_final = n_col * largura_max + (n_col - 1) * margem
    altura_final = n_linhas * altura_max + (n_linhas - 1) * margem

    prancha = Image.new("RGB", (largura_final, altura_final), "white")
    draw = ImageDraw.Draw(prancha)

    letras = list(string.ascii_uppercase)

    for i, img in enumerate(imgs):
        linha = i // n_col
        coluna = i % n_col

        x = coluna * (largura_max + margem)
        y = linha * (altura_max + margem)

        prancha.paste(img, (x, y))

        letra = letras[i]

        pos, anchor = calcular_posicao_texto(
            posicao_letra,
            x,
            y,
            largura_max,
            altura_max,
            margem_texto
        )

        draw.text(
            pos,
            letra,
            fill="black",
            font=fonte,
            anchor=anchor
        )

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

    proporcao_letra = st.slider(
        "Tamanho da letra (proporção da altura da figura)",
        min_value=0.001,#0.05
        max_value=0.50,
        value=0.18,
        step=0.01
    )

    st.caption("Ex.: 0.20 → letra ocupa ~20% da altura da figura")

    st.subheader("Configurações do layout")

    st.subheader("Dimensões dos painéis")

    largura_padrao = st.number_input(
        "Largura do painel (px)",
        min_value=400,
        max_value=3000,
        value=1200,
        step=50
    )
    
    altura_padrao = st.number_input(
        "Altura do painel (px)",
        min_value=400,
        max_value=3000,
        value=1600,
        step=50
    )



    

    prancha = montar_prancha(
        imagens,
        n_col,
        margem,
        posicao_letra,
        proporcao_letra, 
        largura_padrao,
        altura_padrao
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
