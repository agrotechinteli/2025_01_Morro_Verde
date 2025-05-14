import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from db import criar_tabelas, inserir_fertilizante, consultar_fertilizantes, filtrar_fertilizantes, consultar_frete


st.set_page_config(layout="wide")

with st.sidebar :
    st.image("../docs/static/img/logo-morro-verde.png", width=150) 


# ===== Título central =====
st.markdown("<h1 style='text-align: center;'>Previsões de Preços</h1>", unsafe_allow_html=True)

# ===== Indicadores principais =====
col1, col2, col3 = st.columns([3, 2, 3])
with col1:
    st.metric("Aumento dos Preços", "00")
with col2:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.metric("Preço Médio", "00")
with col3:
    st.markdown("#####")
    st.markdown("##### MÊS")
    data_selecionada = st.date_input("Escolha o mês", format="DD/MM/YYYY")

# ===== Filtro =====
st.button("FILTRAR")

# ===== Gráficos (grade) =====
# Linha 1 com dois gráficos
graf_col1, graf_col2 = st.columns(2)
with graf_col1:
    st.markdown("##### Gráfico 1")
    fig, ax = plt.subplots()
    ax.bar(["A", "B", "C"], [10, 20, 15])
    st.pyplot(fig)

with graf_col2:
    st.markdown("##### Gráfico 2")
    fig, ax = plt.subplots()
    ax.bar(["A", "B", "C"], [15, 25, 10])
    st.pyplot(fig)

# Linha 2 com três gráficos
graf_col3, graf_col4, graf_col5 = st.columns(3)
with graf_col3:
    st.markdown("##### Gráfico 3")
    fig, ax = plt.subplots()
    ax.bar(["X", "Y", "Z"], [5, 10, 15])
    st.pyplot(fig)

with graf_col4:
    st.markdown("##### Gráfico 4")
    fig, ax = plt.subplots()
    ax.bar(["X", "Y", "Z"], [8, 12, 18])
    st.pyplot(fig)

with graf_col5:
    st.markdown("##### Gráfico 5")
    fig, ax = plt.subplots()
    ax.bar(["X", "Y", "Z"], [12, 8, 20])
    st.pyplot(fig)