import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import re

# Esta linha de código desativa as mensagens de aviso (warnings) para evitar que elas apareçam durante a execução do programa. É útil para limpar a saída do aplicativo.
warnings.filterwarnings('ignore')
#Este comando é usado para configurar as opções da página do aplicativo criado com o Streamlit. Ele define o título da página, um ícone para a aba do navegador e o layout da página (neste caso, "wide" para uma largura ampla).
#st.set_page_config(page_title="Renda!!!", page_icon=":bar_chart:",layout="wide")
#page_icon = https://emojipedia.org/most-popular
st.set_page_config(page_title="Renda!!!", page_icon="💲",layout="wide")
#Este comando cria um título para a página do aplicativo. No seu código, ele define o título como "Sample SuperStore EDA" e usa um ícone de gráfico de barras (:bar_chart:).
#st.title(" :bar_chart: Sample SuperStore EDA")
st.title("Verifição da Renda")

#Esta linha de código permite adicionar estilos de CSS personalizados ao aplicativo. No seu caso, ele define um espaço em branco acima de 1rem entre os elementos.
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

"""if "data" not in st.session_state:
    data = pd.read_csv("C:/Users/jefer/Documents/Python Scripts/pyhton_streamlit/Streamlit_teste/renda_pessoas.csv")
    data = data.iloc[:,1:]
    data.classe = data.classe.astype(str)
    data.educacao = data.educacao.astype(str)
    data.Estado_civil = data.Estado_civil.astype(str)
    data.ocupacao = data.ocupacao.astype(str)
    colunas_object = data.select_dtypes(include=['object']).columns
    data[colunas_object] = data[colunas_object].astype(str)
    st.session_state["data"] = data"""
   
data = pd.read_csv('C:/Users/jefer/Documents/Python Scripts/pyhton_streamlit/Streamlit_teste/renda_pessoas.csv')
data = data.iloc[:,1:]
data.classe.replace('?', pd.NA)
data['classe'] = data['classe'].apply(lambda x: pd.NA if re.search(r'\?', str(x)) else x).dropna().astype(str)
data.info()