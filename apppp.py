import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Data atual
data_atual = datetime.now().date()

# Menu de navegação
pagina = st.sidebar.radio(
    "Selecione o tipo de convênio:",
    ["home", "com recurso", "sem recurso"]
)


#if st.button("🔄 Atualizar dados"):
 #   st.cache_data.clear()


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
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)

# Página "com recurso"
if pagina == "com recurso":
    st.title("Com Recursos")
    df1 = tratar_datas(load_dataCR())

    df1_vigencia = df1[(df1['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df1['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
    df1_fimV = df1[df1['FIM DA VIGÊNCIA'].dt.date < data_atual]
    total_vigencia = df1_vigencia.shape[0]
    total_fimV = df1_fimV.shape[0]

    filtro = st.selectbox("Filtrar:", ["Todos", "Em vigência", "Vencidos", "Ano", "Finalidade"])

    if filtro == "Em vigência":
        st.markdown(f"## Total: **{total_vigencia}**")
        st.dataframe(df1_vigencia)

    elif filtro == "Vencidos":
        st.markdown(f"## Total: **{total_fimV}**")
        st.dataframe(df1_fimV)

    elif filtro == "Ano":
        ano_selecionado = st.selectbox('Selecione o ano', sorted(df1['ANO'].dropna().unique(), reverse=True))

        #tabla com os contratos iniciados no ano selecioando
        df1_ano = df1[df1['ANO'] == ano_selecionado]
        st.markdown(f"### Dados do ano {ano_selecionado}:")
        st.dataframe(df1_ano[['ANO','FINALIDADE', 'CONTRATO/CONVÊNIO', 'FONTE RECURSO', 'PARTES', 'PROCESSO', 'PROJETO', 'VALOR GERAL', 'NOME COORDENADOR', 'INÍCIO DA VIGÊNCIA', 'FIM DA VIGÊNCIA']], hide_index=True)

        # Contratos iniciados no ano (coluna ANO)
        total_iniciados_ano = df1_ano.shape[0]

        # FIM DA VIGÊNCIA no ano selecionado
        df1_vencidos_ano = df1[df1['FIM DA VIGÊNCIA'].dt.year == ano_selecionado]
        total_vencidos_ano = df1_vencidos_ano.shape[0]

        # Contratos vigentes hoje E que abrangem o ano selecionado
        df1_vigentes_no_ano = df1[
            (df1['INÍCIO DA VIGÊNCIA'].dt.year <= ano_selecionado) &
            (df1['FIM DA VIGÊNCIA'].dt.year >= ano_selecionado) &
            (df1['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) &
            (df1['FIM DA VIGÊNCIA'].dt.date >= data_atual)
        ]
        total_vigentes_no_ano = df1_vigentes_no_ano.shape[0]


        #tabela resumo
        resumo_df = pd.DataFrame({
            'Status': ['Vigentes', 'Vencidos no ano', 'Iniciados no ano'],
            'Quantidade': [total_vigentes_no_ano, total_vencidos_ano, total_iniciados_ano]
        })
        st.markdown(f"### Resumo do ano {ano_selecionado}:")
        st.dataframe(resumo_df)



    elif filtro == "Finalidade":
        st.markdown("🛠️ Em construção")

    else:
        total = df1.shape[0]
        st.markdown(f"## Total: **{total}**")
        st.dataframe(df1)

        #st.title("Convênios")
        #st.markdown(f"### Em vigência: **{total_vigencia}**")
        #st.markdown(f"### Vencidos: **{total_fimV}**")
        #grafico_pizza(['em vigência', 'vencidos'], [total_vigencia, total_fimV], "Distribuição")

        st.markdown("## Total anual")
        acordos_por_ano = df1['ANO'].value_counts().reset_index()
        acordos_por_ano.columns = ['ANO', 'Quantidade de Acordos']
        acordos_por_ano = acordos_por_ano.sort_values(by='ANO', ascending=False)
        st.dataframe(acordos_por_ano)

        fig, ax = plt.subplots()
        ax.bar(acordos_por_ano['ANO'].astype(str), acordos_por_ano['Quantidade de Acordos'])
        ax.set_title('Quantidade de Acordos por Ano')
        ax.set_xlabel('Ano')
        ax.set_ylabel('Quantidade')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    

# Página "sem recurso"
elif pagina == "sem recurso":
    st.title("Sem Recursos")
    df2 = tratar_datas(load_dataSR())
    df2_vigencia = df2[(df2['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df2['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
    df2_fimV = df2[df2['FIM DA VIGÊNCIA'].dt.date < data_atual]
    total_vigencia = df2_vigencia.shape[0]
    total_fimV = df2_fimV.shape[0]

    filtro = st.selectbox("Filtrar:", ["Todos", "Em vigência", "Vencidos", "Ano", "Finalidade"])

    if filtro == "Em vigência":
        st.markdown(f"## Total: **{total_vigencia}**")
        st.dataframe(df2_vigencia)

    elif filtro == "Vencidos":
        st.markdown(f"## Total: **{total_fimV}**")
        st.dataframe(df2_fimV)

    elif filtro == "Ano":
        ano_selecionado = st.selectbox('Selecione o ano', sorted(df2['Ano'].dropna().unique(), reverse=True))

        #tabla com os contratos iniciados no ano selecioando
        df2_ano = df2[df2['Ano'] == ano_selecionado]
        st.markdown(f"### Dados do ano {ano_selecionado}:")
        st.dataframe(df2_ano)

        # Contratos iniciados no ano (coluna ANO)
        total_iniciados_ano = df2_ano.shape[0]

        # FIM DA VIGÊNCIA no ano selecionado
        df2_vencidos_ano = df2[df2['FIM DA VIGÊNCIA'].dt.year == ano_selecionado]
        total_vencidos_ano = df2_vencidos_ano.shape[0]

        # Contratos vigentes hoje E que abrangem o ano selecionado
        df2_vigentes_no_ano = df2[
            (df2['INÍCIO DA VIGÊNCIA'].dt.year <= ano_selecionado) &
            (df2['FIM DA VIGÊNCIA'].dt.year >= ano_selecionado) &
            (df2['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) &
            (df2['FIM DA VIGÊNCIA'].dt.date >= data_atual)
        ]
        total_vigentes_no_ano = df2_vigentes_no_ano.shape[0]


        #tabela resumo
        resumo_df = pd.DataFrame({
            'Status': ['Vigentes', 'Vencidos no ano', 'Iniciados no ano'],
            'Quantidade': [total_vigentes_no_ano, total_vencidos_ano, total_iniciados_ano]
        })
        st.markdown(f"### Resumo do ano {ano_selecionado}:")
        st.dataframe(resumo_df)

    elif filtro == "Finalidade":
        st.markdown("🛠️ Em construção")

    else:
        total = df2.shape[0]
        st.markdown(f"## Total: **{total}**")
        st.dataframe(df2)

        #st.title("Convênios")
        #st.markdown(f"### Em vigência: **{total_vigencia}**")
        #st.markdown(f"### Vencidos: **{total_fimV}**")
        #grafico_pizza(['em vigência', 'vencidos'], [total_vigencia, total_fimV], "Distribuição")

        st.markdown("## Total anual")
        acordos_por_ano = df2['Ano'].value_counts().reset_index()
        acordos_por_ano.columns = ['ANO', 'Quantidade de Acordos']
        acordos_por_ano = acordos_por_ano.sort_values(by='ANO', ascending=False)
        st.dataframe(acordos_por_ano)

        fig, ax = plt.subplots()
        ax.bar(acordos_por_ano['ANO'].astype(str), acordos_por_ano['Quantidade de Acordos'])
        ax.set_title('Quantidade de Acordos por Ano')
        ax.set_xlabel('Ano')
        ax.set_ylabel('Quantidade')
        plt.xticks(rotation=45)
        st.pyplot(fig)


# Página "home"
elif pagina == "home":
    st.markdown("Acesse a barra lateral para ver mais dados")
    df1 = tratar_datas(load_dataCR())
    df2 = tratar_datas(load_dataSR())

    df1_vigencia = df1[(df1['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df1['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
    df2_vigencia = df2[(df2['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df2['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
    total_vigenciaCR = df1_vigencia.shape[0]
    total_vigenciaSR = df2_vigencia.shape[0]

    st.title("Convênios vigentes")
    st.markdown(f"### Com repasse: **{total_vigenciaCR}**")
    st.markdown(f"### Sem repasse: **{total_vigenciaSR}**")
    grafico_pizza(['com repasse', 'sem repasse'], [total_vigenciaCR, total_vigenciaSR], "")
