import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

#data
data_atual = datetime.now().date()

# Menu de navegação
pagina = st.sidebar.radio(
    "Selecione o tipo de convenio:",
    ["home","com recurso", "sem recurso"]
)


#faz conexão com a tabela de convenios Com Repasse
def load_dataCR():
    csv_url = "https://docs.google.com/spreadsheets/d/1lKmtydv3EFVuZ-ddTqKqrJNb59KaQ4GL/export?format=csv&gid=385902901"
    df1 = pd.read_csv(csv_url, engine='python', header=1)
    return df1

#Sem Repasse
def load_dataSR():
    # Link correto para o download direto do Google Sheets
    url = "https://docs.google.com/spreadsheets/d/1lKmtydv3EFVuZ-ddTqKqrJNb59KaQ4GL/export?format=xlsx&gid=765747999"
    df2 = pd.read_excel(url, engine="openpyxl", header=0)
    return df2


# Página 1
if pagina == "com recurso":
    st.title("Com Recursos 📈")

    df1 = load_dataCR()

    #filtro vigencia
    df1['INÍCIO DA VIGÊNCIA'] = pd.to_datetime(df1['INÍCIO DA VIGÊNCIA'], format='%d/%m/%Y', errors='coerce')
    df1['FIM DA VIGÊNCIA'] = pd.to_datetime(df1['FIM DA VIGÊNCIA'], format='%d/%m/%Y', errors='coerce')

    print(df1.columns)

    if 'INÍCIO DA VIGÊNCIA' in df1.columns and 'FIM DA VIGÊNCIA' in df1.columns:
        df1_vigencia = df1[(df1['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df1['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
        total_vigencia = df1_vigencia.shape[0]

    if 'FIM DA VIGÊNCIA' in df1.columns:
        df1_fimV = df1[df1['FIM DA VIGÊNCIA'].dt.date < data_atual]
        total_fimV = df1_fimV.shape[0]


    filtro = st.selectbox(
        "Filtrar:",
        options=["Todos", "Em vigência", "Vencidos", "Ano", "Finalidade"]
    )


    if filtro == "Em vigência":
        st.markdown(f"## Total de convênios ({filtro}): **{total_vigencia}**")
        st.dataframe(df1_vigencia)

    elif filtro == "Vencidos":
        st.markdown(f"## Total de convênios ({filtro}): **{total_fimV}**")
        st.dataframe(df1_fimV)

    elif filtro == "Ano":
        # Filtro de ano
        ano_selecionado = st.selectbox('Selecione o ano', df1['ANO'].unique())
        # Filtrando os dados
        df1_filtrado = df1[df1['ANO'] == ano_selecionado]

        # Exibir os dados filtrados
        st.write(f"Dados do ano {ano_selecionado}:", df1_filtrado)        


        # Contar a quantidade de acordos por ano
        acordos_por_ano = df1['ANO'].value_counts().reset_index()

        # Renomear as colunas para algo mais descritivo
        acordos_por_ano.columns = ['ANO', 'Quantidade de Acordos']

        # Exibir os resultados como uma tabela
        st.dataframe(acordos_por_ano)
    elif filtro == "Finalidade":
        st.markdown('aguma coisa aqui')
 
    else:
        df1_filtrado = df1
        total = df1.shape[0]
        st.markdown(f"## Total de convênios ({filtro}): **{total}**")
        st.dataframe(df1_filtrado)

        #grafico
        st.title("Convênios")
        labels = ['em vigencia', 'finalizados']
        values = [total_vigencia, total_fimV]
        st.markdown(f"### Em vigencia: **{total_vigencia}**")
        st.markdown(f"### Vencidos: **{total_fimV}**")
        # Gera o gráfico se os valores forem maiores que zero
        if sum(values) > 0:
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%')
            ax.axis('equal')  # Deixa o gráfico redondo
            st.pyplot(fig)

            st.markdown("## Total anual")
                    # Contar a quantidade de acordos por ano
            acordos_por_ano = df1['ANO'].value_counts().reset_index()

            # Renomear as colunas para algo mais descritivo
            acordos_por_ano.columns = ['ANO', 'Quantidade de Acordos']
            # Ordenar os anos em ordem decrescente
            acordos_por_ano = acordos_por_ano.sort_values(by='ANO', ascending=False)
            # Exibir os resultados como uma tabela
            st.dataframe(acordos_por_ano)

            # Criar o gráfico
            fig, ax = plt.subplots()
            ax.bar(acordos_por_ano['ANO'].astype(str), acordos_por_ano['Quantidade de Acordos'])

            # Adicionar título e rótulos
            ax.set_title('Quantidade de Acordos por Ano')
            ax.set_xlabel('Ano')
            ax.set_ylabel('Quantidade de Acordos')

            # Exibir o gráfico no Streamlit
            st.pyplot(fig)






# Página 2
elif pagina == "sem recurso":
    st.title("Sem Recursos 📈")

    
    df2 = load_dataSR()
    # Converter as colunas de data para o tipo datetime
    df2['INÍCIO DA VIGÊNCIA'] = pd.to_datetime(df2['INÍCIO DA VIGÊNCIA'], format='%d/%m/%Y', errors='coerce')
    df2['FIM DA VIGÊNCIA'] = pd.to_datetime(df2['FIM DA VIGÊNCIA'], format='%d/%m/%Y', errors='coerce')

    #print(df2.columns)

    if 'INÍCIO DA VIGÊNCIA' in df2.columns and 'FIM DA VIGÊNCIA' in df2.columns:
        df2_vigencia = df2[(df2['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df2['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
        total_vigencia = df2_vigencia.shape[0]

    if 'FIM DA VIGÊNCIA' in df2.columns:
        df2_fimV = df2[df2['FIM DA VIGÊNCIA'].dt.date < data_atual]
        total_fimV = df2_fimV.shape[0]

    #grafico
    #apresentar o valor total de projetos com e sem repasse
    st.title("Gráfico")
    

    # Nomes e dados
    labels = ['em vigencia', 'finalizados']
    values = [total_vigencia, total_fimV]

    # Gera o gráfico se os valores forem maiores que zero
    if sum(values) > 0:
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.axis('equal')  # Deixa o gráfico redondo
        st.pyplot(fig)



    status_vigencia = st.selectbox(
        "Filtrar por vigência:",
        options=["Todos", "Em vigência", "Vencidos"]
    )


    if status_vigencia == "Em vigência":
        st.markdown(f"## Total de convênios ({status_vigencia}): **{total_vigencia}**")
        st.dataframe(df2_vigencia)

    elif status_vigencia == "Vencidos":
        st.markdown(f"## Total de convênios ({status_vigencia}): **{total_fimV}**")
        st.dataframe(df2_fimV)
 
    else:
        df1_filtrado = df2
        total = df2.shape[0]

    st.markdown(f"## Total de convênios ({status_vigencia}): **{total}**")
    st.dataframe(df1_filtrado)

 


elif pagina == "home":
 
        st.markdown("acesse a barra lateral para ver mais dados")
        df1 = load_dataCR()
        df2 = load_dataSR()

        #com repasse
        df1['INÍCIO DA VIGÊNCIA'] = pd.to_datetime(df1['INÍCIO DA VIGÊNCIA'], format='%d/%m/%Y', errors='coerce')
        df1['FIM DA VIGÊNCIA'] = pd.to_datetime(df1['FIM DA VIGÊNCIA'], format='%d/%m/%Y', errors='coerce')

        if 'INÍCIO DA VIGÊNCIA' in df1.columns and 'FIM DA VIGÊNCIA' in df1.columns:
            df1_vigencia = df1[(df1['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df1['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
            total_vigenciaCR = df1_vigencia.shape[0]

        #para o sem repasse
        df2['INÍCIO DA VIGÊNCIA'] = pd.to_datetime(df2['INÍCIO DA VIGÊNCIA'], format='%d/%m/%Y', errors='coerce')
        df2['FIM DA VIGÊNCIA'] = pd.to_datetime(df2['FIM DA VIGÊNCIA'], format='%d/%m/%Y', errors='coerce')

        if 'INÍCIO DA VIGÊNCIA' in df2.columns and 'FIM DA VIGÊNCIA' in df2.columns:
            df2_vigencia = df2[(df2['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df2['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
            total_vigenciaSR = df2_vigencia.shape[0]

        
        #grafico
        #apresentar o valor total de projetos com e sem repasses
        st.title("Convênios vigentes")
        

        # Nomes e dados
        labels = ['com repasse', 'sem repasse']
        values = [total_vigenciaCR, total_vigenciaSR]

        st.markdown(f"### Com repasse: **{total_vigenciaCR}**")
        st.markdown(f"### Sem repasse: **{total_vigenciaSR}**")
        # Gera o gráfico se os valores forem maiores que zero
        if sum(values) > 0:
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%')
            ax.axis('equal')  # Deixa o gráfico redondo
            st.pyplot(fig)


            
