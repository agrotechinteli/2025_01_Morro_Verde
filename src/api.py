import fitz  # PyMuPDF
import sqlite3
import google.generativeai as genai
import json
import os
from datetime import datetime

# ======================= CONFIGURAÇÃO =======================
GEMINI_API_KEY = "SUA_API_KEY"
CAMINHO_PDF = "relatorios/relatorio.pdf"
NOME_ARQUIVO = os.path.basename(CAMINHO_PDF)

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# ======================= ETAPA 1: LER PDF =======================
def ler_pdf(caminho_pdf):
    texto = ""
    with fitz.open(caminho_pdf) as doc:
        for pagina in doc:
            texto += pagina.get_text()
    return texto

# ======================= ETAPA 2: EXTRAIR DADOS COM IA =======================


# ======================= ETAPA 3: INSERIR NO BANCO =======================


# ======================= EXECUÇÃO =======================

