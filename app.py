import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Data atual
data_atual = datetime.now().date()

# Função para carregar o CSS de um arquivo externo
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Carrega o CSS personalizado
load_css("style.css")


# Menu de navegação
pagina = st.sidebar.radio(
    "Selecione o tipo de convênio:",
    ["home", "com recurso", "sem recurso"]
)


# Funções para carregamento dos dados e armazenamene em cache
@st.cache_data
def load_dataCR():
    url = "https://docs.google.com/spreadsheets/d/1WyWOO_JqN44h2suO69nBSmuklV8DQka6/export?format=csv&gid=385902901"
    df = pd.read_csv(url, engine='python', header=1)
    df.columns = df.columns.str.strip()
    return df

@st.cache_data
def load_dataSR():
    url = "https://docs.google.com/spreadsheets/d/1WyWOO_JqN44h2suO69nBSmuklV8DQka6/export?format=xlsx&gid=765747999"
    df = pd.read_excel(url, engine="openpyxl", header=0)
    df.columns = df.columns.str.strip()
    return df

def tratar_datas(df):
    df['INÍCIO DA VIGÊNCIA'] = pd.to_datetime(df['INÍCIO DA VIGÊNCIA'], format='%d/%m/%Y', errors='coerce')
    df['FIM DA VIGÊNCIA'] = pd.to_datetime(df['FIM DA VIGÊNCIA'], format='%d/%m/%Y', errors='coerce')
    return df

def grafico_pizza(labels, values, titulo):
    st.markdown(f"### {titulo}")
    # A facecolor do plot será um branco suave para contrastar com o novo fundo da página
    fig, ax = plt.subplots(facecolor='#F5F5F5') 
    # Definindo cores mais atraentes para o gráfico de pizza
    colors = ['#4CAF50', '#FFC107', '#2196F3', '#FF5722', '#9C27B0']
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors[:len(labels)],
            textprops={'color': '#333333'}) # Cor do texto da porcentagem
    ax.axis('equal')
    st.pyplot(fig)

# Página "com recurso"
if pagina == "com recurso":
    st.title("Convênios com Recurso") # Adicionei um emoji de dinheiro
    df1 = tratar_datas(load_dataCR())

    df1_vigencia = df1[(df1['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df1['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
    df1_fimV = df1[df1['FIM DA VIGÊNCIA'].dt.date < data_atual]
    total_vigencia = df1_vigencia.shape[0]
    total_fimV = df1_fimV.shape[0]

    # Usando st.columns para melhor layout dos totais
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Em Vigência", value=total_vigencia, delta_color="normal")
    with col2:
        st.metric(label="Vencidos", value=total_fimV, delta_color="inverse")

    st.markdown("---") # Linha divisória

    filtro = st.selectbox("Filtrar dados:", ["Todos", "Em vigência", "Vencidos", "Ano", "Finalidade"])

    if filtro == "Em vigência":
        st.markdown(f"### Detalhes: Em Vigência")
        st.dataframe(df1_vigencia, use_container_width=True) # Ocupa a largura total do contêiner

    elif filtro == "Vencidos":
        st.markdown(f"### Detalhes: Vencidos")
        st.dataframe(df1_fimV, use_container_width=True)

    elif filtro == "Ano":
        ano_selecionado = st.selectbox('Selecione o Ano', sorted(df1['ANO'].dropna().unique(), reverse=True))

        df1_ano = df1[df1['ANO'] == ano_selecionado]
        st.markdown(f"### Dados do Ano {ano_selecionado}:")
        st.dataframe(df1_ano, use_container_width=True)

        total_iniciados_ano = df1_ano.shape[0]
        df1_vencidos_ano = df1[df1['FIM DA VIGÊNCIA'].dt.year == ano_selecionado]
        total_vencidos_ano = df1_vencidos_ano.shape[0]

        df1_vigentes_no_ano = df1[
            (df1['INÍCIO DA VIGÊNCIA'].dt.year <= ano_selecionado) &
            (df1['FIM DA VIGÊNCIA'].dt.year >= ano_selecionado) &
            (df1['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) &
            (df1['FIM DA VIGÊNCIA'].dt.date >= data_atual)
        ]
        total_vigentes_no_ano = df1_vigentes_no_ano.shape[0]

        resumo_df = pd.DataFrame({
            'Status': ['Vigentes', 'Vencidos no Ano', 'Iniciados no Ano'],
            'Quantidade': [total_vigentes_no_ano, total_vencidos_ano, total_iniciados_ano]
        })
        st.markdown(f"### Resumo do Ano {ano_selecionado}:")
        st.dataframe(resumo_df, use_container_width=True)


    elif filtro == "Finalidade":
        st.info("filtro 'finalidade' a ver") # Use st.info para mensagens
        # Para futura implementação de finalidade, você poderia fazer algo como:
        # finalidade_selecionada = st.selectbox('Selecione a Finalidade', df1['FINALIDADE'].dropna().unique())
        # df1_finalidade = df1[df1['FINALIDADE'] == finalidade_selecionada]
        # st.dataframe(df1_finalidade)


    else: # Filtro "Todos"
        total = df1.shape[0]
        st.markdown(f"### Todos os Convênios")
        st.dataframe(df1, use_container_width=True)

        st.markdown("## Distribuição Anual")
        acordos_por_ano = df1['ANO'].value_counts().reset_index()
        acordos_por_ano.columns = ['ANO', 'Quantidade de Acordos']
        acordos_por_ano = acordos_por_ano.sort_values(by='ANO', ascending=False)
        st.dataframe(acordos_por_ano, use_container_width=True)

        fig, ax = plt.subplots(facecolor='#E0E0E0') # Cor de fundo do gráfico combinando com o fundo da página
        ax.bar(acordos_por_ano['ANO'].astype(str), acordos_por_ano['Quantidade de Acordos'], color='#00796B') # Cor para as barras
        ax.set_title('Quantidade de Acordos por Ano', color='#333333')
        ax.set_xlabel('Ano', color='#333333')
        ax.set_ylabel('Quantidade', color='#333333')
        plt.xticks(rotation=45, color='#333333')
        plt.yticks(color='#333333')
        st.pyplot(fig)


# Página "sem recurso"
elif pagina == "sem recurso":
    st.title("Convênios sem Recurso") # Adicionei um emoji de nota
    df2 = tratar_datas(load_dataSR())
    df2_vigencia = df2[(df2['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df2['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
    df2_fimV = df2[df2['FIM DA VIGÊNCIA'].dt.date < data_atual]
    total_vigencia = df2_vigencia.shape[0]
    total_fimV = df2_fimV.shape[0]

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Em Vigência", value=total_vigencia, delta_color="normal")
    with col2:
        st.metric(label="Vencidos", value=total_fimV, delta_color="inverse")

    st.markdown("---")

    filtro = st.selectbox("Filtrar dados:", ["Todos", "Em vigência", "Vencidos", "Ano", "Finalidade"])

    if filtro == "Em vigência":
        st.markdown(f"### Detalhes: Em Vigência")
        st.dataframe(df2_vigencia, use_container_width=True)

    elif filtro == "Vencidos":
        st.markdown(f"### Detalhes: Vencidos")
        st.dataframe(df2_fimV, use_container_width=True)

    elif filtro == "Ano":
        ano_selecionado = st.selectbox('Selecione o Ano', sorted(df2['Ano'].dropna().unique(), reverse=True))

        df2_ano = df2[df2['Ano'] == ano_selecionado]
        st.markdown(f"### Dados do Ano {ano_selecionado}:")
        st.dataframe(df2_ano, use_container_width=True)

        total_iniciados_ano = df2_ano.shape[0]
        df2_vencidos_ano = df2[df2['FIM DA VIGÊNCIA'].dt.year == ano_selecionado]
        total_vencidos_ano = df2_vencidos_ano.shape[0]

        df2_vigentes_no_ano = df2[
            (df2['INÍCIO DA VIGÊNCIA'].dt.year <= ano_selecionado) &
            (df2['FIM DA VIGÊNCIA'].dt.year >= ano_selecionado) &
            (df2['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) &
            (df2['FIM DA VIGÊNCIA'].dt.date >= data_atual)
        ]
        total_vigentes_no_ano = df2_vigentes_no_ano.shape[0]

        resumo_df = pd.DataFrame({
            'Status': ['Vigentes', 'Vencidos no Ano', 'Iniciados no Ano'],
            'Quantidade': [total_vigentes_no_ano, total_vencidos_ano, total_iniciados_ano]
        })
        st.markdown(f"### Resumo do Ano {ano_selecionado}:")
        st.dataframe(resumo_df, use_container_width=True)

    elif filtro == "Finalidade":
        st.info("🛠️ Funcionalidade 'Finalidade' em construção. Volte em breve!") # Use st.info para mensagens
        # Para futura implementação de finalidade, você poderia fazer algo como:
        # finalidade_selecionada = st.selectbox('Selecione a Finalidade', df2['FINALIDADE'].dropna().unique())
        # df2_finalidade = df2[df2['FINALIDADE'] == finalidade_selecionada]
        # st.dataframe(df2_finalidade)

    else: # Filtro "Todos"
        total = df2.shape[0]
        st.markdown(f"### Todos os Convênios")
        st.dataframe(df2, use_container_width=True)

        st.markdown("## Distribuição Anual")
        acordos_por_ano = df2['Ano'].value_counts().reset_index()
        acordos_por_ano.columns = ['ANO', 'Quantidade de Acordos']
        acordos_por_ano = acordos_por_ano.sort_values(by='ANO', ascending=False)
        st.dataframe(acordos_por_ano, use_container_width=True)

        fig, ax = plt.subplots(facecolor='#E0E0E0') # Cor de fundo do gráfico combinando com o fundo da página
        ax.bar(acordos_por_ano['ANO'].astype(str), acordos_por_ano['Quantidade de Acordos'], color='#FF8F00') # Outra cor para sem recurso
        ax.set_title('Quantidade de Acordos por Ano', color='#333333')
        ax.set_xlabel('Ano', color='#333333')
        ax.set_ylabel('Quantidade', color='#333333')
        plt.xticks(rotation=45, color='#333333')
        plt.yticks(color='#333333')
        st.pyplot(fig)


# Página "home"
elif pagina == "home":
    st.title("Visualização de convênios")
    st.markdown("Use a barra lateral à esquerda para navegar entre os tipos de convênio e explorar os dados.")

    df1 = tratar_datas(load_dataCR())
    df2 = tratar_datas(load_dataSR())

    df1_vigencia = df1[(df1['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df1['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
    df2_vigencia = df2[(df2['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df2['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
    total_vigenciaCR = df1_vigencia.shape[0]
    total_vigenciaSR = df2_vigencia.shape[0]

    st.markdown("---")
    st.header("Visão Geral de Convênios Vigentes")
    colA, colB = st.columns(2)
    with colA:
        st.metric(label="Convênios com Recurso (Vigentes)", value=total_vigenciaCR, delta_color="normal")
    with colB:
        st.metric(label="Convênios sem Recurso (Vigentes)", value=total_vigenciaSR, delta_color="normal")

    st.markdown("### Distribuição dos Convênios Vigentes por Tipo")
    grafico_pizza(['Com Recurso', 'Sem Recurso'], [total_vigenciaCR, total_vigenciaSR], "")

