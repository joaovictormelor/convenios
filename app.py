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

# Carregando a planilha TED
file_id = "1KLmqRbECQwOUvOpU3v60PKWQsfVrpmau5yDKcVkOXMw"
url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv&gid=0"

def tratar_datas(df):
    df['INÍCIO DA VIGÊNCIA'] = pd.to_datetime(df['INÍCIO DA VIGÊNCIA'], format='%d/%m/%Y', errors='coerce')
    df['FIM DA VIGÊNCIA'] = pd.to_datetime(df['FIM DA VIGÊNCIA'], format='%d/%m/%Y', errors='coerce')
    return df

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
            'Status': ['Atualmente vigentes', 'Vencidos no ano', 'Iniciados no ano'],
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
            'Status': ['Atualmente Vigentes', 'Vencidos no ano', 'Celebrados no ano'],
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

    # Título do aplicativo
    st.title("Acompanhamento de TEDs UFT")

    # Carregar e processar os dados
    df = pd.read_csv(url, header=2, nrows=86)
    df.columns = df.columns.str.replace('\n', ' ', regex=True).str.replace('  ', ' ').str.strip()

    # Conversão de datas
    df['INÍCIO DA VIGÊNCIA'] = pd.to_datetime(df['INÍCIO DA VIGÊNCIA'], errors='coerce', dayfirst=True)
    df['FIM DA VIGÊNCIA'] = pd.to_datetime(df['FIM DA VIGÊNCIA'], errors='coerce', dayfirst=True)
    df['DATA FINAL PARA ENCAMINHAMENTO'] = pd.to_datetime(df['DATA FINAL PARA ENCAMINHAMENTO'], errors='coerce', dayfirst=True)

    # Data atual
    current_date = datetime.now()

    # Cálculos de contagem
    teds_firmados_total = df[df['INÍCIO DA VIGÊNCIA'].notna()].shape[0]
    teds_finalizados_total = df[df['FIM DA VIGÊNCIA'] < current_date].shape[0]
    teds_vigentes_total = df[df['FIM DA VIGÊNCIA'] >= current_date].shape[0]
    teds_vigentes_calculado = teds_firmados_total - teds_finalizados_total

    # Exibir resumo das contagens
    st.subheader("Resumo das Contagens")
    st.write(f"Total de TEDs Firmados: {teds_firmados_total}")
    st.write(f"Total de TEDs Finalizados: {teds_finalizados_total}")
    st.write(f"Total de TEDs Vigentes: {teds_vigentes_calculado}")
    # st.write(f"Total de TEDs Vigentes (diretamente contado): {teds_vigentes_total}")

    # Contagem de TEDs por ano
    firmados_por_ano = df['INÍCIO DA VIGÊNCIA'].dt.year.value_counts().sort_index()
    finalizados_por_ano = df[df['FIM DA VIGÊNCIA'] < current_date]['FIM DA VIGÊNCIA'].dt.year.value_counts().sort_index()
    tabela_ano = pd.DataFrame({
        "Ano": firmados_por_ano.index.astype(str),
        "TEDs Firmados": firmados_por_ano.values,
        "TEDs Finalizados": finalizados_por_ano.reindex(firmados_por_ano.index, fill_value=0).values
    })
    tabela_ano = tabela_ano.sort_values(by="Ano", ascending=False)
    st.subheader("TEDs por Ano")
    st.dataframe(tabela_ano, hide_index=True)

    # Status atual de TEDs
    teds_prestacao_contas = df[(df['FIM DA VIGÊNCIA'] < current_date) & 
                            (df['DATA FINAL PARA ENCAMINHAMENTO'] > current_date)].shape[0]
    tabela_status = pd.DataFrame({
     "Status": ["TEDs Vigentes", "TEDs no Período de Prestação"],
    "Quantidade": [
        teds_vigentes_total,  # Quantidade de TEDs vigentes (supondo que esta já esteja correta)
        # Use a contagem correta aqui:
        df[(df['SITUAÇÃO DO ENCAMINHAMENTO'] == 'Fazer prestação de contas')].shape[0]]
    })
    st.subheader("Status Atual de TEDs")
    st.dataframe(tabela_status, hide_index=True)

    # Filtrar TEDs no período de prestação de contas e selecionar as colunas específicas
    teds_prestacao_contas_lista = df[
        df['SITUAÇÃO DO ENCAMINHAMENTO'] == 'Fazer prestação de contas'
    ][['TED/ANO', 'DATA FINAL PARA ENCAMINHAMENTO', 'TÍTULO/OBJETO']]

    # Converter a coluna 'DATA FINAL PARA ENCAMINHAMENTO' para o padrão brasileiro
    teds_prestacao_contas_lista['DATA FINAL PARA ENCAMINHAMENTO'] = teds_prestacao_contas_lista['DATA FINAL PARA ENCAMINHAMENTO'].dt.strftime('%d/%m/%Y')

    # Exibir a lista no Streamlit
    st.subheader("TEDs no Período de Prestação de Contas")
    st.dataframe(teds_prestacao_contas_lista, hide_index=True)
