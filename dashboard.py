import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.set_page_config(layout="wide")

uploaded_file = st.sidebar.file_uploader("Escolha um arquivo Excel", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
else:
    st.warning("Por favor, faça o upload de um arquivo Excel.")

st.title("Dashboard de Verificação de Fake News")

st.sidebar.subheader("Filtros")
start_date = st.sidebar.date_input("Data inicial", df["Data_Verificação"].min())
end_date = st.sidebar.date_input("Data final", df["Data_Verificação"].max())
filtered_data = df[(df["Data_Verificação"] >= pd.to_datetime(start_date)) & (df["Data_Verificação"] <= pd.to_datetime(end_date))]

category = st.sidebar.selectbox("Selecione a Categoria de Conteúdo", options=["Todas"] + list(df["Categoria_Conteudo"].unique()))
if category != "Todas":
    filtered_data = filtered_data[filtered_data["Categoria_Conteudo"] == category]

source = st.sidebar.selectbox("Selecione a Fonte de Informação", options=["Todas"] + list(df["Fonte_Informação"].unique()))
if source != "Todas":
    filtered_data = filtered_data[filtered_data["Fonte_Informação"] == source]

st.header("Métricas Resumidas")
total_verificacoes = len(filtered_data)
media_verificacoes_dia = filtered_data.resample('D', on='Data_Verificação').size().mean()

col1, col2 = st.columns(2)
col1.metric("Total de Verificações", total_verificacoes)
col2.metric("Média de Verificações por Dia", f"{media_verificacoes_dia:.2f}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Verificações por Categoria de Conteúdo")
    fig, ax = plt.subplots(figsize=(6, 4))
    
    category_counts = filtered_data["Categoria_Conteudo"].value_counts().reset_index()
    category_counts.columns = ["Categoria_Conteudo", "Quantidade"]
    sns.barplot(data=category_counts, x="Categoria_Conteudo", y="Quantidade", ax=ax, palette="Set2")
    
    ax.set_xlabel("Categoria de Conteúdo")
    ax.set_ylabel("Quantidade de Verificações")
    st.pyplot(fig)

with col2:
    st.subheader(f"Fonte de Informação {' - ' + category if category != 'Todas' else ''}")
    fig, ax = plt.subplots(figsize=(6, 4))
    filtered_data.set_index('Data_Verificação').resample('D').size().plot(ax=ax)
    ax.set_xlabel("Data")
    ax.set_ylabel("Quantidade de Verificações")
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.markdown("---")

st.subheader(f"Fonte de Informação {' - ' + source if source != 'Todas' else ''}")
fig, ax = plt.subplots(figsize=(6, 4))
result_counts = filtered_data["Fonte_Informação"].value_counts()

wedges, texts, autotexts = ax.pie(result_counts, labels=result_counts.index, autopct='%1.1f%%', startangle=30, textprops={'fontsize': 12})

for text in texts:
    text.set_fontsize(14)
for autotext in autotexts:
    autotext.set_fontsize(12)

ax.axis("equal")
st.pyplot(fig)

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(filtered_data)

st.download_button(
    label="Baixar dados filtrados em CSV",
    data=csv,
    file_name='dados_filtrados.csv',
    mime='text/csv',
)

