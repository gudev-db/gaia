import streamlit as st
import pandas as pd
import json

def classificar_ansiedade(pontuacao):
    if pontuacao <= 5:
        return "Não ansioso"
    elif pontuacao <= 10:
        return "Levemente ansioso"
    elif pontuacao <= 15:
        return "Moderadamente Ansioso"
    elif pontuacao <= 19:
        return "Severamente Ansioso"
    else:
        return "Extremamente ansioso"

def filtrar_por_ansiedade(df, grau_ansiedade):
    return df[df["classificacao"] == grau_ansiedade][['Nome', 'classificacao','Setor']]

def carregar_dados(uploaded_file):
    df = pd.read_csv(uploaded_file)
    
    # Verifica se o valor na coluna 'nome' é uma string antes de aplicar o parsing do JSON
    df['nome'] = df['nome'].apply(lambda x: json.loads(x)["first"] + " " + json.loads(x)["last"] if isinstance(x, str) else x)
    
    df['Setor'] = df['Setor'].str.capitalize()
    return df

def mapear_respostas(df):
    mapeamento_respostas = {
        "Não": 0,
        "Um pouco": 1,
        "Sim": 2,
        "Bastante": 3
    }
    df.replace(mapeamento_respostas, inplace=True)
    return df

def gerar_graficos(df, selected_setor):
    st.subheader(f"Análise para o Setor: {selected_setor}")

    # Gerando gráfico para a variável 'classificacao'
    st.subheader("Classificação")
    classificacao_data = df["classificacao"].value_counts().sort_index()
    st.bar_chart(classificacao_data)

def distribuicao_classificacoes(df):
    st.sidebar.markdown("---")
    st.sidebar.subheader("Distribuição de Classificações")
    classificacao_data = df["classificacao"].value_counts()
    

def pontuacao_por_setor(df):
    st.sidebar.markdown("---")
    st.sidebar.subheader("Pontuação Total por Setor")
    pontuacao_por_setor = df.groupby("Setor")["pontuacao"].sum()
    st.sidebar.bar_chart(pontuacao_por_setor)

def estatisticas_por_setor(df):
    st.sidebar.markdown("---")
    st.sidebar.subheader("Estatísticas de Pontos por Setor")
    estatisticas_por_setor = df.groupby("Setor")["pontuacao"].agg(['mean', lambda x: x.mode().iloc[0], lambda x: x.median(), 'std'])
    estatisticas_por_setor.columns = ['Média', 'Moda', 'Mediana', 'Desvio Padrão']
    st.sidebar.table(estatisticas_por_setor)


def pontuacao_por_setor(df):
    st.sidebar.markdown("---")
    st.sidebar.subheader("Nível de ansiedade por setor (Bruto)")
    
    # Calculando a pontuação total por setor
    pontuacao_por_setor = df.groupby("Setor")["pontuacao"].sum().sort_values(ascending=False)

    # Gráfico de barras para visualização da pontuação por setor
    st.sidebar.bar_chart(pontuacao_por_setor)

def pontuacao_por_setor2(df):
    st.sidebar.markdown("---")
    st.sidebar.subheader("Nível de ansiedade por setor")
    
    # Calculando a pontuação total por setor
    pontuacao_por_setor = df.groupby("Setor")["pontuacao"].sum().sort_values(ascending=False)
    
    # Exibindo os nomes dos setores em ordem decrescente de pontuação
    for setor, pontuacao in pontuacao_por_setor.items():
        st.sidebar.write(f"{setor}: {pontuacao}")

def pontuacao_projetada_por_setor(df):
    st.sidebar.markdown("---")
    st.sidebar.subheader("Nível de ansiedade por setor (Proporcional)")

    # Calculando a pontuação total por setor
    pontuacao_por_setor = df.groupby("Setor")["pontuacao"].sum().sort_values(ascending=False)

    # Calculando o número de empregados em cada setor
    numero_empregados_por_setor = df["Setor"].value_counts().sort_index()

    # Calculando a pontuação projetada por número de empregados em cada setor
    pontuacao_projetada_por_empregado = pontuacao_por_setor / numero_empregados_por_setor

    # Gráfico de barras para visualização da pontuação projetada por número de empregados em cada setor
    st.sidebar.bar_chart(pontuacao_projetada_por_empregado)

    # Exibindo os nomes dos setores e suas pontuações projetadas por empregado
    for setor, pontuacao_projetada in pontuacao_projetada_por_empregado.items():
        st.sidebar.write(f"{setor}: {pontuacao_projetada:.2f} (Pontuação Projetada por Empregado)")


# Configurações Streamlit
st.title("Dashboard - Análise de Ansiedade Setorial")
uploaded_file = st.file_uploader("Faça o upload do seu arquivo CSV aqui:", type=["csv"])

if uploaded_file is not None:
    df = carregar_dados(uploaded_file)
    cols_to_keep = ['nome', 'Setor', 'acalmar', 'bocaseca', 'nervoso', 'respiracao', 'reacao', 'tremor', 'panico']
    df = df[cols_to_keep]
    df = mapear_respostas(df)
    
    df["pontuacao"] = df.iloc[:, 2:].sum(axis=1)
    df["classificacao"] = df["pontuacao"].apply(classificar_ansiedade)
    
    setores = df["Setor"].unique()
    selected_setor = st.sidebar.selectbox("Selecione um setor ou Global:", list(setores) + ["Global"])
    
    df.rename(columns={
        'nome': 'Nome',
        'Setor': 'Setor',
        'acalmar': 'Dificuldade em se acalmar',
        'bocaseca': 'Apresenta boca seca',
        'nervoso': 'Se sente nervoso',
        'respiracao': 'Dificuldade em respirar',
        'reacao': 'Exagero nas reações',
        'tremor': 'Apresenta tremores',
        'panico': 'Sente Pânico'
    }, inplace=True)

    if selected_setor == "Global":
        filtered_df = df
    else:
        filtered_df = df[df["Setor"] == selected_setor]
    
    pontuacao_projetada_por_setor(df)
    pontuacao_por_setor(df)
    gerar_graficos(filtered_df, selected_setor)
    #pontuacao_por_setor2(df)
    #distribuicao_classificacoes(filtered_df)
    estatisticas_por_setor(df)
    

    
    
    # Função para filtrar nomes com base no grau de ansiedade
    st.header('Filtrar funcionários por grau de ansiedade')
    grau_ansiedade = st.selectbox("Selecione o grau de ansiedade para filtrar:", df['classificacao'].unique())
    if grau_ansiedade:
        filtered_by_ansiedade = filtrar_por_ansiedade(df, grau_ansiedade)
        st.write(f"Pessoas com grau de ansiedade: {grau_ansiedade}")
        st.write(filtered_by_ansiedade)

