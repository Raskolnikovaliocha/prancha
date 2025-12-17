import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import math
import string

st.header("Construção de prancha")

# ===============================
# Upload das imagens
# ===============================
imagens = st.file_uploader(
    "Carregue os gráficos (PNG de preferência)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# ===============================
# Funções auxiliares
# ===============================
def calcular_posicao_texto(posicao, x_img, y_img, largura, altura, offset=10):
    if posicao == "Superior esquerdo":
        return x_img + offset, y_img + offset
    elif posicao == "Superior direito":
        return x_img + largura - offset, y_img + offset
    elif posicao == "Inferior esquerdo":
        return x_img + offset, y_img + altura - offset
    else:  # Inferior direito
        return x_img + largura - offset, y_img + altura - offset


def carregar_fonte(nome, estilo, tamanho):
    try:
        if nome == "Arial":
            if estilo == "Negrito":
                return ImageFont.truetype("arialbd.ttf", tamanho)
            elif estilo == "Itálico":
                return ImageFont.truetype("ariali.ttf", tamanho)
            else:
                return ImageFont.truetype("arial.ttf", tamanho)

        elif nome == "Times New Roman":
            if estilo == "Negrito":
                return ImageFont.truetype("timesbd.ttf", tamanho)
            elif estilo == "Itálico":
                return ImageFont.truetype("timesi.ttf", tamanho)
            else:
                return ImageFont.truetype("times.ttf", tamanho)

    except:
        # fallback seguro (especialmente no Streamlit Cloud)
        return ImageFont.load_default()


def montar_prancha(
    imagens,
    n_col,
    margem,
    posicao_letra,
    proporcao_letra,
    fonte_nome,
    estilo_fonte
):
    imgs = [Image.open(img).convert("RGB") for img in imagens]

    largura_max = max(img.width for img in imgs)
    altura_max = max(img.height for img in imgs)

    n_linhas = math.ceil(len(imgs) / n_col)

    largura_final = n_col * largura_max + (n_col - 1) * margem
    altura_final = n_linhas * altura_max + (n_linhas - 1) * margem

    prancha = Image.new("RGB", (largura_final, altura_final), "white")
    draw = ImageDraw.Draw(prancha)

    letras = list(string.ascii_uppercase)

    # tamanho da letra proporcional à imagem
    tamanho_letra_px = int(altura_max * (proporcao_letra / 100))
    fonte = carregar_fonte(fonte_nome, estilo_fonte, tamanho_letra_px)

    for i, img in enumerate(imgs):
        linha = i // n_col
        coluna = i % n_col

        x = coluna * (largura_max + margem)
        y = linha * (altura_max + margem)

        prancha.paste(img, (x, y))

        if i < len(letras):
            letra = letras[i]
        else:
            letra = f"({i+1})"

        x_texto, y_texto = calcular_posicao_texto(
            posicao_letra, x, y, largura_max, altura_max
        )

        draw.text((x_texto, y_texto), letra, fill="black", font=fonte)

    return prancha


# ===============================
# Interface do usuário
# ===============================
if imagens:
    n_col = st.slider("Número de colunas", 1, 5, 2)
    margem = st.slider("Margem entre figuras (px)", 0, 100, 20)

    posicao_letra = st.selectbox(
        "Posição das letras",
        [
            "Superior esquerdo",
            "Superior direito",
            "Inferior esquerdo",
            "Inferior direito",
        ],
    )

    proporcao_letra = st.slider(
        "Tamanho da letra (% da altura da figura)",
        3.0,
        15.0,
        6.0,
        step=0.5,
    )

    fonte_nome = st.selectbox(
        "Fonte da letra",
        ["Arial", "Times New Roman"]
    )

    estilo_fonte = st.selectbox(
        "Estilo da fonte",
        ["Normal", "Negrito", "Itálico"]
    )

    prancha = montar_prancha(
        imagens,
        n_col,
        margem,
        posicao_letra,
        proporcao_letra,
        fonte_nome,
        estilo_fonte
    )

    st.image(prancha, caption="Prancha final", use_container_width=True)

    prancha.save("prancha_final.png", dpi=(300, 300))

    with open("prancha_final.png", "rb") as f:
        st.download_button(
            "Baixar prancha (PNG 300 dpi)",
            f,
            file_name="prancha_final.png",
            mime="image/png"
        )


