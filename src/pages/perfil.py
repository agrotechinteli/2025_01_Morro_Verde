import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from db import criar_tabelas, inserir_fertilizante, consultar_fertilizantes, filtrar_fertilizantes, consultar_frete

# DEVE SER A PRIMEIRA CHAMADA DO STREAMLIT
st.set_page_config(layout="wide")

# Agora os outros comandos Streamlit
img = "../docs/static/img/mock_foto_perfil.png"

with st.sidebar:
    st.image("../docs/static/img/logo-morro-verde.png", width=150)

# ===== Título central =====
st.markdown("<h1 style='text-align: center;'>Perfil</h1>", unsafe_allow_html=True)

col1, img_col, col3 = st.columns([4, 4, 4])


with img_col:
    
    st.image(img, width=350)

    st.markdown("<p style='font-size:30px;'>Nome:</p>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:30px;'>Sobrenome:</p>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:30px;'>Cargo:</p>", unsafe_allow_html=True)