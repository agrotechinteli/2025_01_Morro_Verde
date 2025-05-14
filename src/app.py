import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from db import criar_tabelas, inserir_fertilizante, consultar_fertilizantes, filtrar_fertilizantes, consultar_frete

# Criar banco de dados e tabelas
criar_tabelas()

st.set_page_config(layout="wide")  # Use a tela toda

with st.sidebar :
    st.image("../docs/static/img/logo-morro-verde.png", width=150) 

# Título central
st.markdown("<h1 style='text-align: center;'>DASHBOARD</h1>", unsafe_allow_html=True)

# Linha de botões superiores
btn_col_upload, btn_col_input, = st.columns([2, 12])
with btn_col_upload:
    st.button("UPLOAD RELATÓRIO")

    with btn_col_input:
        if st.button("INPUT DADOS"):
            st.session_state['mostrar_formulario'] = True

# Se o botão foi clicado, mostrar o formulário como um "pop-up"
if st.session_state.get('mostrar_formulario', False):
    with st.expander("Inserir Dados de Fertilizantes", expanded=True):
        nome = st.text_input("Nome do Fertilizante")
        preco = st.number_input("Preço do Fertilizante", min_value=0.0, format="%.2f")
        fornecedor = st.text_input("Fornecedor")
        data_atualizacao = st.date_input("Data de Atualização")

        form_col_salvar, form_col_fechar = st.columns([2, 20])

        with form_col_salvar:
            if st.button("Salvar Dados"):
                if nome and preco and fornecedor and data_atualizacao:
                    inserir_fertilizante(nome, preco, fornecedor, str(data_atualizacao))
                    st.success("Dados inseridos com sucesso!")
                    st.session_state['mostrar_formulario'] = False
                else:
                    st.error("Preencha todos os campos.")

        with form_col_fechar:
            if st.button("Fechar"):
                st.session_state["mostrar_formulario"] = False


# Área principal da análise
st.markdown("### Análise Concorrentes")
st.markdown("<div style='height: 300px; background-color: #e0e0e0; display: flex; align-items: center; justify-content: center;'>Área de análise</div>", unsafe_allow_html=True)

st.markdown("---")

# Tabela 1 + Tabela 2 + Gráfico 1 + Gráfico 2
col_left, col_right, = st.columns([3, 1.5])

# COLUNA DA TABELA
with col_left:
    st.subheader("Fertilizantes Cadastrados")
    tabela_fertilizantes = consultar_fertilizantes()
    tabela_frete = consultar_frete()

    if tabela_fertilizantes:
        # Cabeçalho da tabela com botão ao lado
        cabecalho_col1, cabecalho_col2 = st.columns([6, 1])
        with cabecalho_col1:
            st.write("Tabela de Fertilizantes")
            df = pd.DataFrame(tabela_fertilizantes, columns=['ID', 'Nome', 'Preço', 'Fornecedor', 'Data'])
        st.dataframe(df.set_index('ID'))  # Apenas uma exibição, com ID como índice

        with cabecalho_col2:
             st.button("FILTRAR", key="filtro_fertilizante")
                

  #      # Exibir tabela
    if tabela_frete :
        # Cabeçalho da tabela com botão ao lado
        cabecalho_col1, cabecalho_col2 = st.columns([6, 1])
        with cabecalho_col1:
              st.write("#### Tabela de Frete")
        df_frete = pd.DataFrame(tabela_frete, columns=['ID', 'Origem', 'Destino','Tipo de Transporte ','Preco USD', 'Preco R$','Data'])
        st.dataframe(df_frete.set_index('ID'))

        with cabecalho_col2:
             st.button("FILTRAR", key="filtro_frete")
               


    else:
        st.write("Sem dados cadastrados.")

# COLUNA DO GRÁFICO
with col_right:
    st.subheader("Gráfico 1")
    grafico_fertilizantes = consultar_fertilizantes()
    grafico_frete = consultar_frete()
    
    if grafico_fertilizantes:
        df = pd.DataFrame(grafico_fertilizantes, columns=['ID', 'Nome', 'Preço', 'Fornecedor', 'Data'])
        fig, ax = plt.subplots()
        ax.bar(df['Nome'], df['Preço'])
        ax.set_xlabel('Fertilizantes')
        ax.set_ylabel('Preço')
        st.pyplot(fig)
    else:
        st.write("Sem dados ainda.")

    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

    if grafico_frete:
        df = pd.DataFrame(grafico_frete, columns=['ID', 'Origem', 'Destino', 'Tipo de Transporte ', 'Preco USD', 'Preco R$', 'Data'])
        
        # Ordenar o DataFrame por preço em R$ (coluna 'Preco R$')
        df = df.sort_values(by='Preco R$', ascending=True)

        fig, ax = plt.subplots()
        ax.bar(df['Destino'], df['Preco R$'])
        ax.set_xlabel('Destino')
        ax.set_ylabel('Preço R$')
        ax.set_title('Preço de Frete por Destino (Ordem Crescente)')
        plt.xticks(rotation=45)  # Gira os rótulos para evitar sobreposição, se necessário
        st.pyplot(fig)
   
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

        
        df_usd = df.sort_values(by='Preco USD', ascending=True)
        fig2, ax2 = plt.subplots()
        ax2.bar(df_usd['Destino'], df_usd['Preco USD'])
        ax2.set_xlabel('Destino')
        ax2.set_ylabel('Preço USD')
        ax2.set_title('Preço de Frete por Destino (USD - Ordem Crescente)')
        plt.xticks(rotation=45)
        st.pyplot(fig2)

   
   
   
    else:
        st.write("Sem dados ainda.")


        

