import pandas as pd
    import streamlit as st
    import plotly.express as px
    from sqlalchemy import create_engine, text

    # Lê o arquivo CSV (sem cabeçalho)
    df = pd.read_csv('iot_temperature.csv', header=None, names=['temperature'])

    # Configurações do banco de dados (usaremos um banco de dados em memória para este exemplo)
    engine = create_engine('sqlite:///:memory:')

    # Insere os dados no banco de dados
    df.to_sql('temperature_readings', engine, if_exists='replace', index=False)

    # Views SQL adaptadas (usando uma conexão e sqlalchemy.text)
    with engine.connect() as connection:
        sql_text = text('''
        CREATE VIEW avg_temp AS
        SELECT AVG(temperature) as avg_temp
        FROM temperature_readings;
        ''')
        connection.execute(sql_text)

    # Função para carregar dados de uma view
    def load_data(view_name):
        return pd.read_sql(f"SELECT * FROM {view_name}", engine)

    # Título do dashboard
    st.title('Dashboard de Temperaturas IoT')

    # Gráfico 1: Média de temperatura geral
    st.header('Média de Temperatura Geral')
    df_avg_temp = load_data('avg_temp')
    fig1 = px.bar(df_avg_temp, x=['Média'], y='avg_temp')
    st.plotly_chart(fig1)

    # Informações adicionais
    st.write("Este dashboard exibe a média geral de temperatura.")