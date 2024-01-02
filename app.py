import streamlit as st
import pandas as pd


# Leitura dos dados a partir do arquivo CSV
file_path = "bd.csv"  # Substitua pelo caminho correto, se necessário
df = pd.read_csv(file_path)

# Mapear respostas para valores numéricos
mapeamento_respostas = {
    "Não": 0,
    "Um pouco": 1,
    "Sim": 2,
    "Bastante": 3
}

# Mapear variáveis para descrições correspondentes
variavel_descricao = {
    "acalmar": "Dificuldade em se acalmar",
    "bocaseca": "Apresenta boca seca",
    "nervoso": "Sente-se nervoso mais que o normal",
    "respiracao": "Sente dificuldade em respirar",
    "exagero": "Tem tido reações exageradas ultimamente",
    "tremor": "Tem sentido tremores"
}

# Aplicar mapeamento para respostas
df.replace(mapeamento_respostas, inplace=True)

# Calcular pontuação para cada usuário
df["pontuacao"] = df.iloc[:, 2:].sum(axis=1)

# Adicionar coluna de classificação
def classificar_ansiedade(pontuacao):
    if pontuacao <= 3:
        return "Não ansioso"
    elif pontuacao <= 9:
        return "Levemente ansioso"
    elif pontuacao <= 15:
        return "Ansioso"
    else:
        return "Bastante ansioso"

df["classificacao"] = df["pontuacao"].apply(classificar_ansiedade)

# Configurações Streamlit
st.title("Análise de Variáveis por Setor")
setores = df["Setor"].unique()

# Sidebar para selecionar o setor ou "Global"
selected_setor = st.sidebar.selectbox("Selecione um setor ou Global:", list(setores) + ["Global"])

# Filtrar DataFrame com base no setor selecionado
if selected_setor == "Global":
    filtered_df = df
else:
    filtered_df = df[df["Setor"] == selected_setor]

# Gráficos para cada variável no setor selecionado
st.subheader(f"Análise para o Setor: {selected_setor}")
for variavel, descricao in variavel_descricao.items():
    st.subheader(descricao)
    chart_data = filtered_df[variavel].value_counts()
    st.bar_chart(chart_data)




# Gráfico de distribuição de classificações por setor
st.sidebar.markdown("---")
st.sidebar.subheader("Distribuição de Classificações")
classificacao_data = filtered_df["classificacao"].value_counts()
st.sidebar.bar_chart(classificacao_data)

# Mostrar a pontuação total de cada setor
st.sidebar.markdown("---")
st.sidebar.subheader("Pontuação Total por Setor")
pontuacao_por_setor = df.groupby("Setor")["pontuacao"].sum()
st.sidebar.bar_chart(pontuacao_por_setor)



# Tabela com moda, média, mediana, primeiro quartil, terceiro quartil e desvio padrão dos pontos por setor
st.sidebar.markdown("---")
st.sidebar.subheader("Estatísticas de Pontos por Setor")
estatisticas_por_setor = df.groupby("Setor")["pontuacao"].agg(['mean', lambda x: x.mode().iloc[0], lambda x: x.median(),'std'])
estatisticas_por_setor.columns = ['Média', 'Moda', 'Mediana','Desvio Padrão']
st.sidebar.table(estatisticas_por_setor)

