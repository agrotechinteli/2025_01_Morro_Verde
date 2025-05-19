
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta, date
import io
import os
import PyPDF2  # Para manipulação de PDFs

DB_PATH = 'morro_verde.db'
logo_path = "img/logo-morro-verde.png"
UPLOAD_FOLDER = "uploads"

# Criar pasta de uploads se não existir
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def criar_conexao():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def carregar_dados():
    conn = criar_conexao()
    
    # Carregar a estrutura de preços combinando as colunas de USD e BRL
    df_precos = pd.read_sql_query('''
    SELECT 
        p.nome AS produto, 
        l.nome AS localizacao, 
        pr.data_preco,
        pr.preco,
        pr.moeda
    FROM preco pr
    JOIN produto p ON p.id_produto = pr.id_produto
    JOIN localizacao l ON l.id_localizacao = pr.id_localizacao
''', conn)


    # Carregar fretes da mesma forma
    df_fretes = pd.read_sql_query('''
        SELECT 
            l1.nome AS origem, 
            l2.nome AS destino, 
            f.tipo_transporte, 
            CASE 
                WHEN f.preco_usd IS NOT NULL THEN f.preco_usd
                ELSE f.preco_brl
            END AS preco,
            CASE 
                WHEN f.preco_usd IS NOT NULL THEN 'USD'
                ELSE 'BRL'
            END AS moeda,
            f.data_frete
        FROM frete f
        JOIN localizacao l1 ON f.origem = l1.id_localizacao
        JOIN localizacao l2 ON f.destino = l2.id_localizacao
    ''', conn)

    # Carregar dados de permuta (barter)
    df_barter = pd.read_sql_query('''
        SELECT 
            id_barter, 
            cultura, 
            id_produto, 
            estado, 
            preco_npk AS preco_fertilizante, 
            preco_cultura, 
            razao_barter, 
            data
        FROM barter
    ''', conn)
    
    # Informações de referência
    df_produtos = pd.read_sql_query("SELECT id_produto, nome, tipo FROM produto", conn)
    df_localizacoes = pd.read_sql_query("SELECT id_localizacao, nome, tipo FROM localizacao", conn)
    df_fertilizantes = pd.read_sql_query("SELECT id, nome, preco, fornecedor, data_atualizacao FROM fertilizantes", conn)
    df_acordos = pd.read_sql_query("SELECT * FROM acordos_barter", conn)
    df_produtores = pd.read_sql_query("SELECT id, nome FROM produtores", conn)

    # Obter todas as tabelas do banco para o input de dados
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    return df_precos, df_fretes, df_barter, df_produtos, df_localizacoes, df_fertilizantes, df_acordos, df_produtores, tabelas

# Função para salvar PDF
def salvar_pdf(uploaded_file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}_{uploaded_file.name}")
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

# Função para extrair texto de um PDF
def extrair_texto_pdf(file_path):
    texto = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_paginas = len(reader.pages)
            
            for i in range(num_paginas):
                pagina = reader.pages[i]
                texto += pagina.extract_text()
                
    except Exception as e:
        texto = f"Erro ao extrair texto: {str(e)}"
    
    return texto

# Função para obter esquema da tabela
def obter_esquema_tabela(tabela):
    conn = criar_conexao()
    cursor = conn.cursor()
    
    # Obter informações sobre as colunas da tabela
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = cursor.fetchall()
    
    conn.close()
    
    # Formatar informações das colunas (cid, name, type, notnull, dflt_value, pk)
    esquema = [{"nome": col[1], "tipo": col[2], "pk": col[5] == 1} for col in colunas]
    return esquema

# Função para inserir dados em uma tabela
def inserir_dados(tabela, dados):
    conn = criar_conexao()
    cursor = conn.cursor()
    
    # Obter colunas da tabela excluindo a PK autoincrement
    esquema = obter_esquema_tabela(tabela)
    colunas = [col["nome"] for col in esquema if not col["pk"] or col["nome"] in dados.keys()]
    
    # Construir query de inserção
    placeholders = ", ".join(["?" for _ in colunas])
    query = f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({placeholders})"
    
    # Valores a serem inseridos
    valores = [dados.get(col, None) for col in colunas]
    
    try:
        cursor.execute(query, valores)
        conn.commit()
        sucesso = True
        mensagem = "Dados inseridos com sucesso!"
    except Exception as e:
        conn.rollback()
        sucesso = False
        mensagem = f"Erro ao inserir dados: {str(e)}"
    finally:
        conn.close()
    
    return sucesso, mensagem

# --- Layout da Interface ---
st.set_page_config(page_title="Dashboard Morro Verde", layout="wide")

# Inicializar estados da sessão se não existirem
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = 'dashboard'
if 'mostrar_filtros' not in st.session_state:
    st.session_state.mostrar_filtros = False
if 'mostrar_importar' not in st.session_state:
    st.session_state.mostrar_importar = False
if 'mostrar_inputar' not in st.session_state:
    st.session_state.mostrar_inputar = False

# Funções para alterar o estado dos botões
def toggle_filtros():
    st.session_state.mostrar_filtros = not st.session_state.mostrar_filtros
    st.session_state.mostrar_importar = False
    st.session_state.mostrar_inputar = False

def toggle_importar():
    st.session_state.mostrar_importar = not st.session_state.mostrar_importar
    st.session_state.mostrar_filtros = False
    st.session_state.mostrar_inputar = False

def toggle_inputar():
    st.session_state.mostrar_inputar = not st.session_state.mostrar_inputar
    st.session_state.mostrar_filtros = False
    st.session_state.mostrar_importar = False

def mudar_pagina(pagina):
    st.session_state.pagina_atual = pagina

# Carregamento e pré-processamento dos dados
df_precos, df_fretes, df_barter, df_produtos, df_localizacoes, df_fertilizantes, df_acordos, df_produtores, tabelas = carregar_dados()
df_precos['data_preco'] = pd.to_datetime(df_precos['data_preco'])
df_precos['preco'] = pd.to_numeric(df_precos['preco'], errors='coerce')
df_barter['data'] = pd.to_datetime(df_barter['data'])
df_barter['preco_fertilizante'] = pd.to_numeric(df_barter['preco_fertilizante'], errors='coerce')
df_barter['preco_cultura'] = pd.to_numeric(df_barter['preco_cultura'], errors='coerce')
df_barter['razao_barter'] = pd.to_numeric(df_barter['razao_barter'], errors='coerce')

# Sidebar com botões
with st.sidebar:
    st.image(logo_path, use_container_width=True)
    st.markdown("---")
    
    if st.button("Página Inicial", use_container_width=True):
        mudar_pagina('dashboard')
    
    if st.button("Previsões", use_container_width=True):
        mudar_pagina('previsoes')
    
    if st.button("Perfil/Login", use_container_width=True):
        mudar_pagina('perfil')

# Título principal
st.title("DASHBOARD - Análise de Concorrência")

# Botões de funcionalidade
with st.container():
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("🔍 FILTRAR DADOS", use_container_width=True, key="btn_filtrar"):
            toggle_filtros()
        
    with col2:
        if st.button("📥 IMPORTAR RELATÓRIO", use_container_width=True, key="btn_importar"):
            toggle_importar()

    with col3:
        if st.button("📝 INPUTAR DADOS", use_container_width=True, key="btn_inputar"):
            toggle_inputar()

# Interface para Filtros
if st.session_state.mostrar_filtros:
    with st.expander("Filtros Avançados", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            data_inicio = st.date_input("Data Início", 
                                        value=datetime.now() - timedelta(days=90),
                                        max_value=datetime.now())
            
        with col2:
            data_fim = st.date_input("Data Fim", 
                                    value=datetime.now(),
                                    max_value=datetime.now())
            
        with col3:
            todos_produtos = ["Todos"] + list(df_precos['produto'].unique())
            filtro_produto = st.selectbox("Produto", todos_produtos)
            
        col4, col5, col6 = st.columns(3)
        
        with col4:
            todas_localizacoes = ["Todas"] + list(df_precos['localizacao'].unique())
            filtro_localizacao = st.selectbox("Localização", todas_localizacoes)
            
        with col5:
            todas_moedas = ["Todas"] + list(df_precos['moeda'].unique())
            filtro_moeda = st.selectbox("Moeda", todas_moedas)
            
        with col6:
            st.write("")
            st.write("")
            if st.button("Aplicar Filtros", use_container_width=True):
                st.success("Filtros aplicados com sucesso!")

# Interface para Importar Relatório
if st.session_state.mostrar_importar:
    with st.expander("Importar Relatório (PDF)", expanded=True):
        st.info("Faça upload do relatório em PDF recebido do cliente.")
        
        uploaded_file = st.file_uploader("Selecione o arquivo PDF", type=["pdf"])
        
        if uploaded_file is not None:
            # Exibir informações do arquivo
            file_details = {
                "Nome do arquivo": uploaded_file.name,
                "Tipo de arquivo": uploaded_file.type,
                "Tamanho": f"{uploaded_file.size / 1024:.2f} KB"
            }
            
            st.json(file_details)
            
            # Visualização prévia e processamento
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Visualizar conteúdo", use_container_width=True):
                    # Salvar o PDF temporariamente
                    temp_path = salvar_pdf(uploaded_file)
                    
                    # Extrair texto do PDF
                    texto = extrair_texto_pdf(temp_path)
                    
                    # Exibir prévia do texto
                    st.text_area("Prévia do conteúdo", texto[:500] + "...", height=300)
            
            with col2:
                cliente = st.text_input("Cliente")
                data_relatorio = st.date_input("Data do relatório", value=datetime.now())
                notas = st.text_area("Observações", height=150)
                
                if st.button("Salvar relatório", use_container_width=True):
                    if cliente:
                        # Salvar o relatório definitivamente
                        file_path = salvar_pdf(uploaded_file)
                        st.success(f"Relatório '{uploaded_file.name}' salvo com sucesso!")
                        st.info(f"Caminho do arquivo: {file_path}")
                    else:
                        st.warning("Por favor, informe o nome do cliente.")

# Interface para Inputar Dados
if st.session_state.mostrar_inputar:
    with st.expander("Inputar Dados no Banco", expanded=True):
        # Selecionar tabela para inserção
        tabela_selecionada = st.selectbox("Selecione a tabela para inserção de dados", tabelas)
        
        if tabela_selecionada:
            # Obter esquema da tabela selecionada
            esquema = obter_esquema_tabela(tabela_selecionada)
            
            st.subheader(f"Inserir dados na tabela: {tabela_selecionada}")
            
            # Criar campos de entrada baseados no esquema da tabela
            dados_form = {}
            colunas_por_linha = 2
            
            colunas_nao_pk = [col for col in esquema if not col["pk"]]
            
            # Organizar em linhas com duas colunas
            for i in range(0, len(colunas_nao_pk), colunas_por_linha):
                cols = st.columns(colunas_por_linha)
                
                for j in range(colunas_por_linha):
                    if i + j < len(colunas_nao_pk):
                        coluna = colunas_nao_pk[i + j]
                        nome_coluna = coluna["nome"]
                        tipo_coluna = coluna["tipo"].upper()
                        
                        with cols[j]:
                            # Criar campo de entrada apropriado para o tipo de dado
                            if "INT" in tipo_coluna:
                                dados_form[nome_coluna] = st.number_input(
                                    f"{nome_coluna} ({tipo_coluna})", 
                                    step=1
                                )
                            elif "REAL" in tipo_coluna or "FLOAT" in tipo_coluna or "DOUBLE" in tipo_coluna:
                                dados_form[nome_coluna] = st.number_input(
                                    f"{nome_coluna} ({tipo_coluna})", 
                                    step=0.01
                                )
                            elif "DATE" in tipo_coluna:
                                dados_form[nome_coluna] = st.date_input(
                                    f"{nome_coluna} ({tipo_coluna})", 
                                    value=datetime.now()
                                )
                            else:  # Tipo TEXT ou outros
                                # Verificar se é um campo que requer seleção de valores existentes
                                if nome_coluna == "id_produto" and tabela_selecionada in ["preco", "barter"]:
                                    opcoes = df_produtos.set_index("id_produto")["nome"].to_dict()
                                    id_selecionado = st.selectbox(
                                        f"{nome_coluna} (Produto)", 
                                        options=list(opcoes.keys()),
                                        format_func=lambda x: f"{x} - {opcoes[x]}"
                                    )
                                    dados_form[nome_coluna] = id_selecionado
                                    
                                elif nome_coluna == "id_localizacao" or nome_coluna == "origem" or nome_coluna == "destino":
                                    opcoes = df_localizacoes.set_index("id_localizacao")["nome"].to_dict()
                                    id_selecionado = st.selectbox(
                                        f"{nome_coluna} (Localização)", 
                                        options=list(opcoes.keys()),
                                        format_func=lambda x: f"{x} - {opcoes[x]}"
                                    )
                                    dados_form[nome_coluna] = id_selecionado
                                    
                                elif nome_coluna == "cultura" and tabela_selecionada == "barter":
                                    culturas_unicas = df_barter["cultura"].unique()
                                    dados_form[nome_coluna] = st.selectbox(
                                        f"{nome_coluna}", 
                                        options=[""] + list(culturas_unicas)
                                    )
                                    
                                elif nome_coluna == "estado" and tabela_selecionada == "barter":
                                    estados_unicos = df_barter["estado"].unique()
                                    dados_form[nome_coluna] = st.selectbox(
                                        f"{nome_coluna}", 
                                        options=[""] + list(estados_unicos)
                                    )
                                    
                                elif nome_coluna == "tipo_transporte" and tabela_selecionada == "frete":
                                    dados_form[nome_coluna] = st.selectbox(
                                        f"{nome_coluna}", 
                                        options=["Rodoviário", "Ferroviário", "Marítimo", "Aéreo"]
                                    )
                                    
                                elif nome_coluna == "fornecedor" and tabela_selecionada == "fertilizantes":
                                    fornecedores = df_fertilizantes["fornecedor"].unique() if not df_fertilizantes.empty else []
                                    dados_form[nome_coluna] = st.text_input(
                                        f"{nome_coluna}", 
                                        key=f"input_{tabela_selecionada}_{nome_coluna}"
                                    )
                                    if fornecedores.size > 0:
                                        st.selectbox(
                                            "Fornecedores existentes", 
                                            options=[""] + list(fornecedores),
                                            key=f"select_{tabela_selecionada}_{nome_coluna}"
                                        )
                                    
                                else:
                                    dados_form[nome_coluna] = st.text_input(
                                        f"{nome_coluna} ({tipo_coluna})", 
                                        key=f"input_{tabela_selecionada}_{nome_coluna}"
                                    )
            
            # Campos especiais que requerem cálculos
            if tabela_selecionada == "barter" and "preco_npk" in dados_form and "preco_cultura" in dados_form:
                try:
                    preco_npk = float(dados_form["preco_npk"]) if dados_form["preco_npk"] else 0
                    preco_cultura = float(dados_form["preco_cultura"]) if dados_form["preco_cultura"] else 0
                    
                    if preco_cultura > 0:
                        razao = preco_npk / preco_cultura
                        st.info(f"Razão de permuta calculada: {razao:.2f}")
                        dados_form["razao_barter"] = str(round(razao, 2))
                except:
                    pass
            
            # Botão para salvar os dados
            if st.button("Salvar dados", use_container_width=True):
                # Validar dados (implementação simples)
                campos_vazios = [nome for nome, valor in dados_form.items() if not valor and valor != 0]
                
                if campos_vazios:
                    st.warning(f"Por favor, preencha os seguintes campos: {', '.join(campos_vazios)}")
                else:
                    # Converter datas para string no formato ISO
                    for nome, valor in dados_form.items():
                        if isinstance(valor, datetime) or isinstance(valor, date):
                            dados_form[nome] = valor.isoformat()
                    
                    # Tentar inserir os dados no banco
                    sucesso, mensagem = inserir_dados(tabela_selecionada, dados_form)
                    
                    if sucesso:
                        st.success(mensagem)
                        # Recarregar dados para refletir as alterações
                        if st.button("Recarregar dados"):
                            st.experimental_rerun()
                    else:
                        st.error(mensagem)

# Conteúdo principal com base na página atual
if st.session_state.pagina_atual == 'dashboard':
    # Gráfico interativo principal
    st.subheader("📈 Variação de Preços por Concorrente")

    # Seleção de produto e moeda
    produto_focus = st.selectbox("Produto para análise", df_precos['produto'].unique())
    moeda_focus = st.selectbox("Moeda:", df_precos['moeda'].unique())

    # Filtrar por produto e moeda
    df_focus = df_precos[
        (df_precos['produto'] == produto_focus) &
        (df_precos['moeda'] == moeda_focus)
    ]

    # Verifica se há dados disponíveis
    if not df_focus.empty:
        fig = px.line(
            df_focus.sort_values('data_preco'),
            x='data_preco',
            y='preco',
            color='localizacao',
            title=f'Histórico de Preços ({moeda_focus}) - {produto_focus}',
            markers=True
        )
        fig.update_layout(
            title_font=dict(size=20), 
            margin=dict(t=50, b=10),
            legend_title="Localização"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado para o produto e moeda selecionados.")

    # Seção de Avisos Urgentes - Melhorado o contraste
    st.subheader("⚠️ Avisos Urgentes")
    avisos = [
        "Variação abrupta de preço detectada no PR.",
        "Preço médio do frete entre GO e MT aumentou 12%.",
        "Queda no preço da cultura no MS nas últimas semanas.",
        "Alta nos custos de transporte no MT.",
        "Produto importado abaixo da média histórica."
    ]

    # Cards para avisos com melhor contraste
    cols_avisos = st.columns(len(avisos))
    for i, aviso in enumerate(avisos):
        with cols_avisos[i]:
            st.markdown(
                f"""
                <div style='background-color: #FFA000; color: #000000; padding: 1rem; 
                border-radius: 5px; height: 100%; font-weight: 500; text-align: center;'>
                ⚠️ {aviso}
                </div>
                """, 
                unsafe_allow_html=True
            )

    # Gráfico de comparação Permuta
    st.subheader("📉 Comparativo Permuta")

    culturas_disponiveis = df_barter['cultura'].unique()
    cultura_selecionada = st.selectbox("Selecione a Cultura:", culturas_disponiveis)

    # Filtrar df_barter pela cultura
    filtros_barter = df_barter[df_barter['cultura'] == cultura_selecionada]

    # Obter fertilizantes usados nessa cultura
    ids_usados = filtros_barter['id_produto'].unique()
    fertilizantes_disponiveis = df_produtos[df_produtos['id_produto'].isin(ids_usados)]['nome'].tolist()

    if fertilizantes_disponiveis:
        fertilizante_selecionado = st.selectbox("Produto (Fertilizante):", fertilizantes_disponiveis)

        if fertilizante_selecionado:
            id_fertilizante = df_produtos[df_produtos['nome'] == fertilizante_selecionado]['id_produto'].values[0]
            filtros_barter = filtros_barter[filtros_barter['id_produto'] == id_fertilizante]

            fig_barter = px.line(
                filtros_barter.sort_values("data"),
                x="data",
                y="razao_barter",
                color="estado",
                title=f"Permuta {fertilizante_selecionado} / {cultura_selecionada} - Razão ao longo do tempo"
            )
            fig_barter.update_layout(legend_title="Estado")
            st.plotly_chart(fig_barter, use_container_width=True)
    else:
        st.warning(f"Não há dados de permuta disponíveis para a cultura {cultura_selecionada}")

    # Análises adicionais
    st.subheader("📊 Análises Gerais")
    col1, col2 = st.columns(2)

    # Gráfico 1 - Média de preço por produto (em BRL)
    with col1:
        preco_medio = df_precos[df_precos['moeda'] == 'BRL'].groupby("produto")["preco"].mean().reset_index()
        preco_medio = preco_medio.sort_values("preco", ascending=False)
        fig1 = px.bar(
            preco_medio, 
            x='produto', 
            y='preco', 
            title='Preço Médio por Produto (BRL)', 
            text_auto=True,
            color='produto'
        )
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2 - Média de preço por local (em BRL)
    with col2:
        preco_local = df_precos[df_precos['moeda'] == 'BRL'].groupby("localizacao")["preco"].mean().reset_index()
        fig2 = px.pie(
            preco_local, 
            names='localizacao', 
            values='preco', 
            title='Distribuição de Preço Médio por Localização (BRL)',
            hole=0.4
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Tabela de fretes
    st.subheader("🚚 Tabela de Fretes Atuais")
    st.dataframe(
        df_fretes.sort_values("data_frete", ascending=False).head(10),
        use_container_width=True,
        column_config={
            "origem": "Origem",
            "destino": "Destino",
            "tipo_transporte": "Tipo de Transporte",
            "preco": st.column_config.NumberColumn("Preço", format="R$ %.2f"),
            "moeda": "Moeda",
            "data_frete": st.column_config.DateColumn("Data", format="DD/MM/YYYY")
        }
    )

elif st.session_state.pagina_atual == 'previsoes':
    st.header("Previsões de Mercado")
    st.info("Esta página está em desenvolvimento. Em breve você poderá visualizar previsões e tendências de mercado.")
    
    # Placeholder para mockup de previsões
    st.subheader("Tendências Previstas (Mockup)")
    tendencias_data = {
        'Produto': ['MAP', 'KCL', 'Ureia', 'TSP', 'SSP'],
        'Tendência': [1, -1, 1, 0, -1],
        'Previsão (%)': [12, -8, 5, 0, -3]
    }
    
    tendencias_df = pd.DataFrame(tendencias_data)
    
    # Criar indicadores de tendência
    def formatar_tendencia(val):
        if val == 1:
            return "↗️ Alta"
        elif val == -1:
            return "↘️ Queda"
        else:
            return "→ Estável"
    
    tendencias_df['Indicador'] = tendencias_df['Tendência'].apply(formatar_tendencia)
    
    # Mostrar tabela com tendências
    st.dataframe(
        tendencias_df[['Produto', 'Indicador', 'Previsão (%)']],
        use_container_width=True,
        hide_index=True
    )

elif st.session_state.pagina_atual == 'perfil':
    st.header("Perfil do Usuário")
    
    
    # Simulação de perfil
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        **Nome:** João da Silva  
        **Cargo:** Analista de Dados Agrícolas  
        **Organização:** Morro Verde  
        **Último acesso:** 19/05/2025  
        """)

    with col2:
        st.markdown("""
        ### Sobre você  
        Você está utilizando o sistema de monitoramento de preços, fretes e permutas para tomar decisões estratégicas no agronegócio.  
        Aqui você poderá acompanhar seus relatórios importados, inserir novos dados e acessar dashboards interativos.  
        """)
