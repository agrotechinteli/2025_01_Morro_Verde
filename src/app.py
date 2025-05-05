import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import criar_tabela, inserir_fertilizante, consultar_fertilizantes

# Criar banco e tabela se necessário
criar_tabela()

# Função para gerar gráfico de preços de fertilizantes
def gerar_grafico(dados):
    df = pd.DataFrame(dados, columns=['ID', 'Nome', 'Preço', 'Fornecedor', 'Data'])
    fig, ax = plt.subplots()
    ax.bar(df['Nome'], df['Preço'])
    ax.set_xlabel('Fertilizantes')
    ax.set_ylabel('Preço')
    ax.set_title('Preço de Fertilizantes')
    st.pyplot(fig)

# Função para o Streamlit renderizar a interface
def app():
    # Cabeçalho
    st.title('Dashboard Inteligente Morro Verde')

    # Seção de Inserção Manual de Dados
    st.header('Inserir Dados de Fertilizantes')
    
    nome = st.text_input("Nome do Fertilizante")
    preco = st.number_input("Preço do Fertilizante", min_value=0.0, format="%.2f")
    fornecedor = st.text_input("Fornecedor")
    data_atualizacao = st.date_input("Data de Atualização")

    if st.button("Inserir Dados"):
        if nome and preco and fornecedor and data_atualizacao:
            inserir_fertilizante(nome, preco, fornecedor, str(data_atualizacao))
            st.success("Dados inseridos no banco com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos.")

    # Seção para visualizar os dados inseridos no banco
    st.header('Dados de Fertilizantes')
    dados = consultar_fertilizantes()
    if dados:
        st.write("Tabela de Fertilizantes")
        df = pd.DataFrame(dados, columns=['ID', 'Nome', 'Preço', 'Fornecedor', 'Data'])
        st.dataframe(df)

        # Gerar gráfico dos preços
        gerar_grafico(dados)
    else:
        st.write("Ainda não há dados disponíveis.")

# Rodar o app Streamlit
if __name__ == '__main__':
    app()
