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

    def montar_prancha(imagens, n_col, margem):
        imgs = [Image.open(img).convert('RGB') for img in imagens]# conversaão das imagens em RGB

        #largura máxima e altura máxima das fotos plotadas:
        largura_max =  max(img.width for img in imgs)
        altura_max = max(img.height for img in imgs )

        #Número de linhas:
        n_linhas = math.ceil(len(imgs)/n_col)
        largura_final = n_col*largura_max + (n_col-1)*margem
        altura_final = n_linhas * altura_max + (n_linhas - 1) * margem


        # NESSA PARTE VAMOS FOPRMAR UM QUADRO BRANCO 
        prancha = Image.new("RGB", (largura_final, altura_final), "white")
        for i, img in enumerate(imgs):
            linha = i // n_col
            coluna = i % n_col

            x = coluna * (largura_max + margem)
            y = linha * (altura_max + margem)

            prancha.paste(img, (x, y))

        return prancha



    prancha = montar_prancha(imagens, n_col, margem)

    st.image(prancha, caption="Prancha final", use_container_width=True)

    prancha.save("prancha_final.png", dpi=(300, 300))

    with open("prancha_final.png", "rb") as f:
        st.download_button(
            "Baixar prancha (PNG 300 dpi)",
            f,
            file_name="prancha_final.png",
            mime="image/png"
        )


    


