#hi
import streamlit as st 
from PIL import Image
import math
st.header('Construção de prancha')
#1 inserindo dados de entrada:
imagens = st.file_uploader('Carregue os gráficos (PNG de preferência)', type=['png','jpg','jpeg '], accept_multiple_files = True)

if len(imagens) > 0 : # me refiro ao número de imagens
    n_col = st.slider('Número de colunas', 1,5, 2)
    margem = st.slider ('Margem entre figuras (px)',0,100,20)

    posicao_letra = st.selectbox(
    "Posição das letras",
    ["Superior esquerdo", "Superior direito",
     "Inferior esquerdo", "Inferior direito"]
)

    tamanho_letra = st.slider("Tamanho da letra", 20, 80, 40)

    def calcular_posicao_texto(posicao, x_img, y_img, largura, altura, offset=10):
        if posicao == "Superior esquerdo":
            return x_img + offset, y_img + offset
        elif posicao == "Superior direito":
            return x_img + largura - offset, y_img + offset
        elif posicao == "Inferior esquerdo":
            return x_img + offset, y_img + altura - offset
        else:  # Inferior direito
            return x_img + largura - offset, y_img + altura - offset



    

    def montar_prancha(imagens, n_col, margem, posicao_letra, tamanho_letra):
        imgs = [Image.open(img).convert("RGB") for img in imagens]
    
        largura_max = max(img.width for img in imgs)
        altura_max = max(img.height for img in imgs)
    
        n_linhas = math.ceil(len(imgs) / n_col)
    
        largura_final = n_col * largura_max + (n_col - 1) * margem
        altura_final = n_linhas * altura_max + (n_linhas - 1) * margem
    
        prancha = Image.new("RGB", (largura_final, altura_final), "white")
    
        draw = ImageDraw.Draw(prancha)
        letras = list(string.ascii_uppercase)
    
        try:
            fonte = ImageFont.truetype("arial.ttf", tamanho_letra)
        except:
            fonte = ImageFont.load_default()
    
        for i, img in enumerate(imgs):
            linha = i // n_col
            coluna = i % n_col
    
            x = coluna * (largura_max + margem)
            y = linha * (altura_max + margem)
    
            prancha.paste(img, (x, y))
    
            # --- LETRA ---
            letra = letras[i]
    
            x_texto, y_texto = calcular_posicao_texto(
                posicao_letra,
                x, y,
                largura_max,
                altura_max
            )
    
            draw.text((x_texto, y_texto), letra, fill="black", font=fonte)

        return prancha


   prancha = montar_prancha(
    imagens,
    n_col,
    margem,
    posicao_letra,
    tamanho_letra
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


    


