import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Menu de navegação
pagina = st.sidebar.radio(
    "Selecione o tipo de convenio:",
    ["com recurso", "sem recurso"]
)

# Página 1
if pagina == "com recurso":

    def load_data():
        csv_url = "https://docs.google.com/spreadsheets/d/1lKmtydv3EFVuZ-ddTqKqrJNb59KaQ4GL/export?format=csv&gid=385902901"
        df1 = pd.read_csv(csv_url, engine='python', header=0)
        # Converter as colunas de data para o tipo datetime
        if 'Unnamed: 11' in df1.columns and 'Unnamed: 12' in df1.columns:
            df1['INÍCIO DA VIGÊNCIA'] = pd.to_datetime(df1['Unnamed: 11'], format='%d/%m/%Y', errors='coerce')
            df1['FIM DA VIGÊNCIA'] = pd.to_datetime(df1['Unnamed: 12'], format='%d/%m/%Y', errors='coerce')
        return df1

    df1 = load_data()

    #print(df1.columns)

    data_atual = datetime.now().date()

    if 'INÍCIO DA VIGÊNCIA' in df1.columns and 'FIM DA VIGÊNCIA' in df1.columns:
        df1_vigencia = df1[(df1['INÍCIO DA VIGÊNCIA'].dt.date <= data_atual) & (df1['FIM DA VIGÊNCIA'].dt.date >= data_atual)]
        total_vigencia = df1_vigencia.shape[0]

    if 'FIM DA VIGÊNCIA' in df1.columns:
        df1_fimV = df1[df1['FIM DA VIGÊNCIA'].dt.date < data_atual]
        total_fimV = df1_fimV.shape[0]

    #grafico
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
        st.dataframe(df1_vigencia)

    elif status_vigencia == "Vencidos":
        st.markdown(f"## Total de convênios ({status_vigencia}): **{total_fimV}**")
        st.dataframe(df1_fimV)
 
    else:
        df1_filtrado = df1
        total = df1.shape[0]

    st.markdown(f"## Total de convênios ({status_vigencia}): **{total}**")
    st.dataframe(df1_filtrado)





# Página 2
elif pagina == "sem recurso":
    st.title("Planilha 2 📈")
    url2 = "https://docs.google.com/spreadsheets/d/1lKmtydv3EFVuZ-ddTqKqrJNb59KaQ4GL/edit?gid=765747999#gid=765747999"  # Substitua pelo link público
    df2 = pd.read_csv(url2)
    st.dataframe(df2)

    import streamlit as st

    mensagem = st.text_area("Digite sua mensagem")
    st.write("Sua mensagem foi:", mensagem)


    
