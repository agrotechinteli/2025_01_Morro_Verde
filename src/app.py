import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

DB_PATH = 'morro_verde.db'
logo_path = "img/logo-morro-verde.png"

def criar_conexao():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def carregar_dados():
    conn = criar_conexao()
    df_precos = pd.read_sql_query('''
        SELECT p.nome AS produto, l.nome AS localizacao, pr.data_preco, pr.preco_brl, pr.preco_usd
        FROM preco pr
        JOIN produto p ON p.id_produto = pr.id_produto
        JOIN localizacao l ON l.id_localizacao = pr.id_localizacao
    ''', conn)

    df_fretes = pd.read_sql_query('''
        SELECT l1.nome AS origem, l2.nome AS destino, f.tipo_transporte, f.preco_brl, f.data_frete
        FROM frete f
        JOIN localizacao l1 ON f.origem = l1.id_localizacao
        JOIN localizacao l2 ON f.destino = l2.id_localizacao
    ''', conn)

    df_barter = pd.read_sql_query('''
        SELECT id_barter, cultura, id_produto, estado, preco_npk, preco_cultura, razao_barter, data
        FROM barter
    ''', conn)


    conn.close()
    return df_precos, df_fretes, df_barter

# --- Layout da Interface ---
st.set_page_config(page_title="Dashboard Morro Verde", layout="wide")

# Carregamento e pré-processamento dos dados (antes dos botões)
df_precos, df_fretes, df_barter = carregar_dados()
df_precos['data_preco'] = pd.to_datetime(df_precos['data_preco'])
df_precos['preco_brl'] = pd.to_numeric(df_precos['preco_brl'], errors='coerce')
df_precos['preco_usd'] = pd.to_numeric(df_precos['preco_usd'], errors='coerce')
df_barter['data'] = pd.to_datetime(df_barter['data'])
df_barter['preco_npk'] = pd.to_numeric(df_barter['preco_npk'], errors='coerce')
df_barter['preco_cultura'] = pd.to_numeric(df_barter['preco_cultura'], errors='coerce')
df_barter['razao_barter'] = pd.to_numeric(df_barter['razao_barter'], errors='coerce')

# Sidebar com botões
with st.sidebar:
    st.image(logo_path, use_container_width=True)
    st.markdown("---")
    st.button("Página Inicial")
    st.button("Previsões")
    st.button("Perfil/Login")

# Título principal
st.title("DASHBOARD - Análise de Concorrência")

# Pop-ups com botão
with st.container():
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("🔍 FILTRAR DADOS"):
            with st.popover("Filtros Disponíveis"):
                st.markdown("### Filtro de Dados")
                produtos = st.multiselect("Produto:", df_precos['produto'].unique(), key="pop_prod")
                locais = st.multiselect("Localização:", df_precos['localizacao'].unique(), key="pop_loc")
                data_ini = st.date_input("Data Inicial:", value=pd.to_datetime(df_precos['data_preco'].min()), key="pop_data_ini")
                data_fim = st.date_input("Data Final:", value=pd.to_datetime(df_precos['data_preco'].max()), key="pop_data_fim")
                if st.button("Aplicar Filtros"):
                    st.session_state['produtos'] = produtos
                    st.session_state['locais'] = locais
                    st.session_state['data_ini'] = data_ini
                    st.session_state['data_fim'] = data_fim

    with col2:
        st.button("📥 IMPORTAR RELATÓRIO")

    with col3:
        if st.button("📝 INPUTAR DADOS"):
            with st.popover("Inserção de Dados"):
                with st.form("form_input"):
                    nome = st.text_input("Nome do Produto")
                    tipo = st.text_input("Tipo do Produto")
                    submitted = st.form_submit_button("Inserir")
                    if submitted and nome and tipo:
                        conn = criar_conexao()
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO produto (nome, tipo) VALUES (?, ?)", (nome, tipo))
                        conn.commit()
                        conn.close()
                        st.success("Produto inserido com sucesso!")

# Aplicar filtros salvos
if 'produtos' in st.session_state:
    if st.session_state['produtos']:
        df_precos = df_precos[df_precos['produto'].isin(st.session_state['produtos'])]
if 'locais' in st.session_state:
    if st.session_state['locais']:
        df_precos = df_precos[df_precos['localizacao'].isin(st.session_state['locais'])]
if 'data_ini' in st.session_state and 'data_fim' in st.session_state:
    df_precos = df_precos[(df_precos['data_preco'] >= pd.to_datetime(st.session_state['data_ini'])) &
                          (df_precos['data_preco'] <= pd.to_datetime(st.session_state['data_fim']))]

# Gráfico interativo principal
st.subheader("📈 Variação de Preços por Concorrente")
produto_focus = st.selectbox("Produto para análise", df_precos['produto'].unique())
df_focus = df_precos[df_precos['produto'] == produto_focus]
fig = px.line(df_focus.sort_values('data_preco'), x='data_preco', y='preco_brl', color='localizacao',
              title=f'Histórico de Preços (BRL) - {produto_focus}', markers=True)
fig.update_layout(title_font=dict(size=20), margin=dict(t=50, b=10))
st.plotly_chart(fig, use_container_width=True)

# Seção de Avisos Urgentes
st.subheader("⚠️ Avisos Urgentes")
avisos = [
    "Variação abrupta de preço detectada no PR.",
    "Preço médio do frete entre GO e MT aumentou 12%.",
    "Queda no preço da cultura no MS nas últimas semanas.",
    "Alta nos custos de transporte no MT.",
    "Produto importado abaixo da média histórica."
]

# Scroll horizontal para avisos
avisos_html = """<div style='display: flex; overflow-x: auto; gap: 1rem;'>"""
for aviso in avisos:
    avisos_html += f"<div style='min-width: 300px; padding: 1rem; background-color: #FFF3CD; border-left: 5px solid #FFA000; border-radius: 4px;'>⚠️ {aviso}</div>"
avisos_html += "</div>"
st.markdown(avisos_html, unsafe_allow_html=True)

# Gráfico de comparação Permuta
st.subheader("📉 Comparativo Permuta")

culturas_disponiveis = df_barter['cultura'].unique()
cultura_selecionada = st.selectbox("Selecione a Cultura:", culturas_disponiveis)

# Filtrar df_barter pela cultura
filtros_barter = df_barter[df_barter['cultura'] == cultura_selecionada]

# Obter fertilizantes usados nessa cultura
conn = criar_conexao()
produtos_df = pd.read_sql_query("SELECT id_produto, nome FROM produto", conn)
conn.close()

ids_usados = filtros_barter['id_produto'].unique()
nomes_disponiveis = produtos_df[produtos_df['id_produto'].isin(ids_usados)]['nome'].tolist()

fertilizante_selecionado = st.selectbox("Produto (Fertilizante):", nomes_disponiveis)

if fertilizante_selecionado:
    id_fertilizante = produtos_df[produtos_df['nome'] == fertilizante_selecionado]['id_produto'].values[0]
    filtros_barter = filtros_barter[filtros_barter['id_produto'] == id_fertilizante]

    fig_barter = px.line(
        filtros_barter.sort_values("data"),
        x="data",
        y="razao_barter",
        color="estado",
        title=f"Permuta {fertilizante_selecionado} / {cultura_selecionada} - Razão ao longo do tempo"
    )
    st.plotly_chart(fig_barter, use_container_width=True)


# Análises adicionais
st.subheader("📊 Análises Gerais")
col1, col2 = st.columns(2)

# Gráfico 1 - Média de preço por produto
with col1:
    preco_medio = df_precos.groupby("produto")["preco_brl"].mean().reset_index()
    fig1 = px.bar(preco_medio, x='produto', y='preco_brl', title='Preço Médio por Produto', text_auto=True)
    st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2 - Média de preço por local
with col2:
    preco_local = df_precos.groupby("localizacao")["preco_brl"].mean().reset_index()
    fig2 = px.pie(preco_local, names='localizacao', values='preco_brl', title='Distribuição de Preço Médio por Localização')
    st.plotly_chart(fig2, use_container_width=True)

# Tabela de fretes
st.subheader("🚚 Tabela de Fretes Atuais")
st.dataframe(df_fretes.sort_values("data_frete", ascending=False).head(10))
