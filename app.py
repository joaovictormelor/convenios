import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Data atual
data_atual = datetime.now().date()

# Menu de navegação
pagina = st.sidebar.radio(
    "Selecione o tipo de convênio:",
    ["Início", "TED", "Com recurso", "Sem recurso"]
)


#if st.button("🔄 Atualizar dados"):
 #   st.cache_data.clear()


##carregando a tabela Com Recurso
@st.cache_data
def load_dataCR():
    url = "https://docs.google.com/spreadsheets/d/1WyWOO_JqN44h2suO69nBSmuklV8DQka6/export?format=csv&gid=385902901"
    df = pd.read_csv(url, engine='python', header=1)
    df.columns = df.columns.str.strip()
    return df

#carregando a tabela Sem Recurso filtrando apenas pelos CELEBRADOS
@st.cache_data
def load_dataSR():
    url = "https://docs.google.com/spreadsheets/d/1WyWOO_JqN44h2suO69nBSmuklV8DQka6/export?format=xlsx&gid=765747999"
    df = pd.read_excel(url, engine="openpyxl", header=0)
    df.columns = df.columns.str.strip()
    condicao = df['Situação'].str.strip().str.lower() == 'celebrado'

    df_filtrado = df[condicao.fillna(False)]

    return df_filtrado

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
if pagina == "Com recurso":
    st.title("Com Recursos")
    df1 = tratar_datas(load_dataCR())

    df1_vigencia = df1[(df1['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df1['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
    df1_fimV = df1[df1['FIM DA VIGÊNCIA'].dt.date < data_atual]
    total_vigencia = df1_vigencia.shape[0]
    total_fimV = df1_fimV.shape[0]

    filtro = st.selectbox("Filtrar:", ["Todos", "Em vigência", "Vencidos", "Ano", "Finalidade"])

    if filtro == "Em vigência":
        st.markdown(f"## Total: **{total_vigencia}**")
        st.dataframe(df1_vigencia[['ANO','FINALIDADE', 'CONTRATO/CONVÊNIO', 'PARTES', 'PROCESSO', 'PROJETO', 'VALOR GERAL', 'NOME COORDENADOR', 'INÍCIO DA VIGÊNCIA', 'FIM DA VIGÊNCIA']], hide_index=True)

    elif filtro == "Vencidos":
        st.markdown(f"## Total: **{total_fimV}**")
        st.dataframe(df1_fimV[['ANO','FINALIDADE', 'CONTRATO/CONVÊNIO', 'PARTES', 'PROCESSO', 'PROJETO', 'VALOR GERAL', 'NOME COORDENADOR', 'INÍCIO DA VIGÊNCIA', 'FIM DA VIGÊNCIA']], hide_index=True)

    elif filtro == "Ano":
        ano_selecionado = st.selectbox('Selecione o ano', sorted(df1['ANO'].dropna().unique(), reverse=True))

        #tabla com os contratos iniciados no ano selecioando
        df1_ano = df1[df1['ANO'] == ano_selecionado]
        st.markdown(f"### Dados do ano {ano_selecionado}:")
        st.dataframe(df1_ano[['ANO','FINALIDADE', 'CONTRATO/CONVÊNIO', 'PARTES', 'PROCESSO', 'PROJETO', 'VALOR GERAL', 'NOME COORDENADOR', 'INÍCIO DA VIGÊNCIA', 'FIM DA VIGÊNCIA']], hide_index=True)

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


        #tabela resumo do ano
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
        st.dataframe(df1[['ANO','FINALIDADE', 'CONTRATO/CONVÊNIO', 'PARTES', 'PROCESSO', 'PROJETO', 'VALOR GERAL', 'NOME COORDENADOR', 'INÍCIO DA VIGÊNCIA', 'FIM DA VIGÊNCIA']], hide_index=True)

        #st.title("Convênios")
        #st.markdown(f"### Em vigência: **{total_vigencia}**")
        #st.markdown(f"### Vencidos: **{total_fimV}**")
        #grafico_pizza(['em vigência', 'vencidos'], [total_vigencia, total_fimV], "Distribuição")

        st.markdown("## Total anual")
        acordos_por_ano = df1['ANO'].value_counts().reset_index()
        acordos_por_ano.columns = ['ANO', 'Quantidade de Acordos']
        acordos_por_ano = acordos_por_ano.sort_values(by='ANO', ascending=False)
        st.dataframe(acordos_por_ano, hide_index=True)

# Página "sem recurso"
elif pagina == "Sem recurso":
    st.title("Sem Recursos")
    df2 = tratar_datas(load_dataSR())
    df2_vigencia = df2[(df2['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df2['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
    df2_fimV = df2[df2['FIM DA VIGÊNCIA'].dt.date < data_atual]
    total_vigencia = df2_vigencia.shape[0]
    total_fimV = df2_fimV.shape[0]

    filtro = st.selectbox("Filtrar:", ["Todos", "Em vigência", "Vencidos", "Ano", "Finalidade"])

    if filtro == "Em vigência":
        st.markdown(f"## Total: **{total_vigencia}**")
        st.dataframe(df2_vigencia[["Ano", "ACORDO/\nCONVÊNIO", "PARTES", "PROCESSO", "TITULO", "NOME \nCOORDENADOR", "Situação", "INÍCIO DA VIGÊNCIA", "FIM DA VIGÊNCIA"]], hide_index=True)

    elif filtro == "Vencidos":
        st.markdown(f"## Total: **{total_fimV}**")
        st.dataframe(df2_fimV[["Ano", "ACORDO/\nCONVÊNIO", "PARTES", "PROCESSO", "TITULO", "NOME \nCOORDENADOR", "Situação", "INÍCIO DA VIGÊNCIA", "FIM DA VIGÊNCIA"]], hide_index=True)

    elif filtro == "Ano":
        ano_selecionado = st.selectbox('Selecione o ano', sorted(df2['Ano'].dropna().unique(), reverse=True))

        #tabla com os contratos iniciados no ano selecioando
        df2_ano = df2[df2['Ano'] == ano_selecionado]
        st.markdown(f"### Dados do ano {ano_selecionado}:")
        st.dataframe(df2_ano[["Ano", "ACORDO/\nCONVÊNIO", "PARTES", "PROCESSO", "TITULO", "NOME \nCOORDENADOR", "Situação", "INÍCIO DA VIGÊNCIA", "FIM DA VIGÊNCIA"]], hide_index=True)

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
        st.dataframe(resumo_df, hide_index=True)

    elif filtro == "Finalidade":
        st.markdown("🛠️ Em construção")

    else:
        total = df2.shape[0]
        st.markdown(f"## Total: **{total}**")
        st.dataframe(df2[["Ano", "ACORDO/\nCONVÊNIO", "PARTES", "PROCESSO", "TITULO", "NOME \nCOORDENADOR", "Situação", "INÍCIO DA VIGÊNCIA", "FIM DA VIGÊNCIA"]], hide_index=True)


        st.markdown("## Total anual")
        acordos_por_ano = df2['Ano'].value_counts().reset_index()
        acordos_por_ano.columns = ['ANO', 'Quantidade de Acordos']
        acordos_por_ano = acordos_por_ano.sort_values(by='ANO', ascending=False)
        st.dataframe(acordos_por_ano, hide_index=True)


# Página "home"
elif pagina == "Início":
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


# Página TED
elif pagina == "TED":
    st.markdown("ted aq. trazer o app ted ja feito  pra ca")
