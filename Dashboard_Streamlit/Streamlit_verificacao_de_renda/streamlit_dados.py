import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import re
import webbrowser

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

if "data" not in st.session_state:
    data = pd.read_csv("C:/Users/jefer/Documents/Python Scripts/pyhton_streamlit/Streamlit_teste/renda_pessoas.csv")
    data = data.iloc[:,1:]
    data['classe'] = data['classe'].apply(lambda x: pd.NA if re.search(r'\?', str(x)) else x).astype(str)
    data = data[data.classe != '<NA>']
    data.Renda = data.Renda.str.replace('<=50K','Menor ou igual a 50 mil').str.replace('>50K','Maior que 50 mil')
    st.session_state["data"] = data
    
data = st.session_state["data"]

#Colocando um link para meu github
st.sidebar.markdown("Produzido por: https://github.com/Jeferson100")

##Colocando um botao
btn = st.button("# Acesse os dados do Kaggle")
if btn:
    webbrowser.open_new_tab("https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data/")


# Create for Selecionador
st.sidebar.header("Escolha um filtro: ")
#Criando_classes
data.Renda = data.Renda.str.replace('<=50K','Menor ou igual a 50 mil').str.replace('>50K','Maior que 50 mil')
renda = st.sidebar.multiselect("Escolha seu nivel de renda", data["Renda"].unique())
#classe_social= st.sidebar.multiselect("Escolha sua classe social", data["classe"].unique())
nivel_educacao= st.sidebar.multiselect("Escolha seu Nivel educacional", data["educacao"].unique())
sexo = st.sidebar.multiselect("Escolha seu Sexo", data["sexo"].unique())
raca = st.sidebar.multiselect("Escolha sua Raça", data["Raca"].unique())

#Combinado selecaos

# Aplicando seleções individuais

filtered_data = data.copy()

if renda:
    filtered_data = filtered_data[filtered_data['Renda'].isin(renda)]    

#if classe_social:
    #filtered_data = filtered_data[filtered_data['classe'].isin(classe_social)]

if nivel_educacao:
    filtered_data = filtered_data[filtered_data['educacao'].isin(nivel_educacao)]

if sexo:
    filtered_data = filtered_data[filtered_data['sexo'].isin(sexo)]

if raca:
    filtered_data = filtered_data[filtered_data['Raca'].isin(raca)]
    

#Media de anos de estudo
media_anos_estudo = round(filtered_data.numero_da_educacao.mean(),2)
col1,col2 = st.columns(2)
#col1.markdown(f"**Media de anos de estudo:** {media_anos_estudo}", unsafe_allow_html=True)
col1.markdown(f"<h2>Média de anos de estudo: {media_anos_estudo}</h2>", unsafe_allow_html=True)


col1, col2 = st.columns((2))
with col1:
    labels = filtered_data.numero_da_educacao.value_counts().sort_index().values
    st.subheader("Distribuição de anos estudados")
    fig = px.histogram(filtered_data, x='numero_da_educacao',
                       labels={'numero_da_educacao': 'Anos de estudo'},
                       template = "seaborn")#, title='Distribuição de anos estudados')
    fig.update_traces(text=labels, textposition='outside')
    fig.update_yaxes(title_text='Frequência')
    st.plotly_chart(fig,use_container_width=True, height = 200)
    
    

with col2:
    st.subheader("Quantidade de raça por renda")
    st.subheader("___")
    if renda:
        renda_raca = data.groupby(['Raca', 'Renda']).size().reset_index(name='Contagem')
    else:
        renda_raca = filtered_data.groupby(['Raca', 'Renda']).size().reset_index(name='Contagem')
        
    pivot_renda_raca = renda_raca.pivot(index='Raca', columns='Renda', values='Contagem').fillna(0)
    pivot_renda_raca.columns = pivot_renda_raca.columns.str.strip()
    # Calcular as porcentagens
    pivot_renda_raca['Porcentagem_maior'] = (pivot_renda_raca['Maior que 50 mil.'] / pivot_renda_raca.sum(axis=1)).round(2).map('{:.2%}'.format)
    pivot_renda_raca['Porcentagem_Menor'] = (pivot_renda_raca['Menor ou igual a 50 mil.'] / pivot_renda_raca.sum(axis=1)).round(2).map('{:.2%}'.format)
    st.dataframe(pivot_renda_raca,
             column_config={
             "Maior que 50 mil.": st.column_config.NumberColumn("Maior que 50 mil"),
             "Menor ou igual a 50 mil.": st.column_config.NumberColumn("Menor ou igual a 50 mil"),
             "Porcentagem_maior": st.column_config.NumberColumn("Maior que 50 mil em %"),
             "Porcentagem_Menor": st.column_config.NumberColumn("Menor ou igual a 50 mil em %")
             },height=300,)
    
    #width ("small", "medium", "large", or None)
    


col1, col2 = st.columns((2))

with col1:
    ocupacao = filtered_data.ocupacao.value_counts().head(10)
    st.subheader("Empregos mais comuns")
    fig = px.bar(x = ocupacao.index, 
                 y = ocupacao.values,
                 color_discrete_sequence=["black"],
                 template = "seaborn",
                 labels={'x': 'Ocupação', 'y': 'Frequência'},
                 text= ocupacao.values)
    fig.update_yaxes(title_text='Frequência')
    st.plotly_chart(fig,use_container_width=True, height = 200)
    #fig = px.bar(category_df, x = "Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],template = "seaborn")
    #st.plotly_chart(fig,use_container_width=True, height = 200)
    
with col2:
    st.subheader("Horas trabalhadas na semana por classe")
    #fig = px.pie(filtered_df, values = "Sales", names = "Region", hole = 0.5)
    #fig.update_traces(text = filtered_df["Region"], textposition = "outside")
    #st.plotly_chart(fig,use_container_width=True)
    cores = px.colors.qualitative.Set3
    classe_horas_trabalhadas = filtered_data.groupby('classe')['horas_por_semana'].mean().sort_values(ascending=False).round(2)
    fig = px.bar(x =classe_horas_trabalhadas.index, 
                 y = classe_horas_trabalhadas.values,
                 color_discrete_sequence=["red"],
                 template = "seaborn",
                 labels={'x': 'Classe Social', 'y': 'Média de Horas Trabalhadas'},
                 text= classe_horas_trabalhadas.values)
    #fig = px.bar(names=classe_horas_trabalhadas.index,values=classe_horas_trabalhadas.values,hole = 0.5)#color_discrete_sequence=cores  # Especifica as cores a serem usada)
    st.plotly_chart(fig,use_container_width=True)
    
    
    
    
col1, col2 = st.columns((2))

with col1:
    st.subheader("Tipos de Relacionamentos")
    #fig = px.pie(filtered_df, values = "Sales", names = "Region", hole = 0.5)
    #fig.update_traces(text = filtered_df["Region"], textposition = "outside")
    #st.plotly_chart(fig,use_container_width=True)
    cores = px.colors.qualitative.Set3
    relacionamentos = filtered_data.Relacionamento.value_counts() 
    fig = px.pie(
        names=relacionamentos.index,
        values=relacionamentos.values,
        hole = 0.5
        #color_discrete_sequence=cores  # Especifica as cores a serem usadas
    )
    fig.update_traces(text = relacionamentos.index , textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)