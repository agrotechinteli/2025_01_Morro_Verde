 import streamlit as st
# import sqlite3
# import pandas as pd
# import plotly.express as px
# from datetime import datetime, timedelta
# import io

# DB_PATH = 'morro_verde.db'
# logo_path = "img/logo-morro-verde.png"

# def criar_conexao():
#     conn = sqlite3.connect(DB_PATH)
#     conn.execute('PRAGMA foreign_keys = ON')
#     return conn

# def carregar_dados():
#     conn = criar_conexao()
#     df_precos = pd.read_sql_query('''
#         SELECT p.nome AS produto, l.nome AS localizacao, pr.data_preco, pr.preco, pr.moeda
#         FROM preco pr
#         JOIN produto p ON p.id_produto = pr.id_produto
#         JOIN localizacao l ON l.id_localizacao = pr.id_localizacao
#     ''', conn)

#     df_fretes = pd.read_sql_query('''
#         SELECT l1.nome AS origem, l2.nome AS destino, f.tipo_transporte, f.preco, f.moeda, f.data_frete
#         FROM frete f
#         JOIN localizacao l1 ON f.origem = l1.id_localizacao
#         JOIN localizacao l2 ON f.destino = l2.id_localizacao
#     ''', conn)

#     df_barter = pd.read_sql_query('''
#         SELECT id_barter, cultura, id_produto, estado, preco_fertilizante, preco_cultura, razao_barter, data
#         FROM barter
#     ''', conn)
    
#     df_produtos = pd.read_sql_query("SELECT id_produto, nome FROM produto", conn)
#     df_localizacoes = pd.read_sql_query("SELECT id_localizacao, nome FROM localizacao", conn)

#     conn.close()
#     return df_precos, df_fretes, df_barter, df_produtos, df_localizacoes

# # --- Layout da Interface ---
# st.set_page_config(page_title="Dashboard Morro Verde", layout="wide")

# # Inicializar estados da sessão se não existirem
# if 'pagina_atual' not in st.session_state:
#     st.session_state.pagina_atual = 'dashboard'
# if 'mostrar_filtros' not in st.session_state:
#     st.session_state.mostrar_filtros = False
# if 'mostrar_importar' not in st.session_state:
#     st.session_state.mostrar_importar = False
# if 'mostrar_inputar' not in st.session_state:
#     st.session_state.mostrar_inputar = False

# # Funções para alterar o estado dos botões
# def toggle_filtros():
#     st.session_state.mostrar_filtros = not st.session_state.mostrar_filtros
#     st.session_state.mostrar_importar = False
#     st.session_state.mostrar_inputar = False

# def toggle_importar():
#     st.session_state.mostrar_importar = not st.session_state.mostrar_importar
#     st.session_state.mostrar_filtros = False
#     st.session_state.mostrar_inputar = False

# def toggle_inputar():
#     st.session_state.mostrar_inputar = not st.session_state.mostrar_inputar
#     st.session_state.mostrar_filtros = False
#     st.session_state.mostrar_importar = False

# def mudar_pagina(pagina):
#     st.session_state.pagina_atual = pagina

# # Carregamento e pré-processamento dos dados
# df_precos, df_fretes, df_barter, df_produtos, df_localizacoes = carregar_dados()
# df_precos['data_preco'] = pd.to_datetime(df_precos['data_preco'])
# df_precos['preco'] = pd.to_numeric(df_precos['preco'], errors='coerce')
# df_barter['data'] = pd.to_datetime(df_barter['data'])
# df_barter['preco_fertilizante'] = pd.to_numeric(df_barter['preco_fertilizante'], errors='coerce')
# df_barter['preco_cultura'] = pd.to_numeric(df_barter['preco_cultura'], errors='coerce')
# df_barter['razao_barter'] = pd.to_numeric(df_barter['razao_barter'], errors='coerce')

# # Sidebar com botões
# with st.sidebar:
#     st.image(logo_path, use_container_width=True)
#     st.markdown("---")
    
#     if st.button("Página Inicial", use_container_width=True):
#         mudar_pagina('dashboard')
    
#     if st.button("Previsões", use_container_width=True):
#         mudar_pagina('previsoes')
    
#     if st.button("Perfil/Login", use_container_width=True):
#         mudar_pagina('perfil')

# # Título principal
# st.title("DASHBOARD - Análise de Concorrência")

# # Botões de funcionalidade
# with st.container():
#     col1, col2, col3 = st.columns([1, 1, 1])

#     with col1:
#         if st.button("🔍 FILTRAR DADOS", use_container_width=True, key="btn_filtrar"):
#             toggle_filtros()
        
#     with col2:
#         if st.button("📥 IMPORTAR RELATÓRIO", use_container_width=True, key="btn_importar"):
#             toggle_importar()

#     with col3:
#         if st.button("📝 INPUTAR DADOS", use_container_width=True, key="btn_inputar"):
#             toggle_inputar()

# # Interface para Filtros
# if st.session_state.mostrar_filtros:
#     with st.expander("Filtros Avançados", expanded=True):
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             data_inicio = st.date_input("Data Início", 
#                                         value=datetime.now() - timedelta(days=90),
#                                         max_value=datetime.now())
            
#         with col2:
#             data_fim = st.date_input("Data Fim", 
#                                     value=datetime.now(),
#                                     max_value=datetime.now())
            
#         with col3:
#             todos_produtos = ["Todos"] + list(df_precos['produto'].unique())
#             filtro_produto = st.selectbox("Produto", todos_produtos)
            
#         col4, col5, col6 = st.columns(3)
        
#         with col4:
#             todas_localizacoes = ["Todas"] + list(df_precos['localizacao'].unique())
#             filtro_localizacao = st.selectbox("Localização", todas_localizacoes)
            
#         with col5:
#             todas_moedas = ["Todas"] + list(df_precos['moeda'].unique())
#             filtro_moeda = st.selectbox("Moeda", todas_moedas)
            
#         with col6:
#             st.write("")
#             st.write("")
#             if st.button("Aplicar Filtros", use_container_width=True):
#                 st.success("Filtros aplicados com sucesso!")

# # Interface para Importar Relatório
# if st.session_state.mostrar_importar:
#     with st.expander("Importar Relatório", expanded=True):
#         col1, col2 = st.columns(2)
        
#         with col1:
#             tipo_importacao = st.selectbox("Tipo de Importação", 
#                                           ["Preços", "Fretes", "Barter (Permuta)"])
#             arquivo = st.file_uploader("Selecione um arquivo CSV ou Excel", 
#                                       type=["csv", "xlsx", "xls"])
            
#         with col2:
#             st.info("Formatos aceitos: CSV, XLS, XLSX")
#             st.markdown("""
#             **Colunas necessárias:**
#             - Para Preços: produto, localizacao, data_preco, preco, moeda
#             - Para Fretes: origem, destino, tipo_transporte, preco, moeda, data_frete
#             - Para Barter: cultura, produto, estado, preco_fertilizante, preco_cultura, data
#             """)
            
#         if arquivo is not None:
#             if st.button("Processar Importação", use_container_width=True):
#                 st.success(f"Arquivo importado com sucesso! (Simulação)")
#                 # Aqui você implementaria a lógica real de importação

# # Interface para Inputar Dados
# if st.session_state.mostrar_inputar:
#     with st.expander("Inputar Novos Dados", expanded=True):
#         tipo_input = st.selectbox("Tipo de Dados", ["Preço", "Frete", "Barter (Permuta)"])
        
#         if tipo_input == "Preço":
#             col1, col2 = st.columns(2)
#             with col1:
#                 prod_input = st.selectbox("Produto", df_produtos['nome'].unique())
#                 loc_input = st.selectbox("Localização", df_localizacoes['nome'].unique())
                
#             with col2:
#                 preco_input = st.number_input("Preço", min_value=0.0, step=0.01)
#                 moeda_input = st.selectbox("Moeda", ["BRL", "USD", "EUR"])
#                 data_input = st.date_input("Data", value=datetime.now())
                
#             if st.button("Salvar Preço", use_container_width=True):
#                 st.success("Preço registrado com sucesso! (Simulação)")
#                 # Aqui você implementaria a lógica real de salvar no banco de dados
        
#         elif tipo_input == "Frete":
#             col1, col2 = st.columns(2)
#             with col1:
#                 origem_input = st.selectbox("Origem", df_localizacoes['nome'].unique())
#                 destino_input = st.selectbox("Destino", df_localizacoes['nome'].unique())
                
#             with col2:
#                 tipo_transp = st.selectbox("Tipo de Transporte", ["Rodoviário", "Ferroviário", "Marítimo"])
#                 preco_frete = st.number_input("Valor do Frete", min_value=0.0, step=0.01)
#                 moeda_frete = st.selectbox("Moeda Frete", ["BRL", "USD", "EUR"])
#                 data_frete = st.date_input("Data do Frete", value=datetime.now())
                
#             if st.button("Salvar Frete", use_container_width=True):
#                 st.success("Frete registrado com sucesso! (Simulação)")
                
#         elif tipo_input == "Barter (Permuta)":
#             col1, col2 = st.columns(2)
#             with col1:
#                 cultura_input = st.selectbox("Cultura", df_barter['cultura'].unique())
#                 produto_input = st.selectbox("Produto/Fertilizante", df_produtos['nome'].unique())
#                 estado_input = st.selectbox("Estado", df_barter['estado'].unique())
                
#             with col2:
#                 preco_fert = st.number_input("Preço do Fertilizante", min_value=0.0, step=0.01)
#                 preco_cult = st.number_input("Preço da Cultura", min_value=0.0, step=0.01)
#                 data_barter = st.date_input("Data", value=datetime.now())
                
#             if preco_cult > 0:
#                 razao = preco_fert / preco_cult
#                 st.info(f"Razão de permuta calculada: {razao:.2f}")
                
#             if st.button("Salvar Permuta", use_container_width=True):
#                 st.success("Dados de permuta registrados com sucesso! (Simulação)")

# # Conteúdo principal com base na página atual
# if st.session_state.pagina_atual == 'dashboard':
#     # Gráfico interativo principal
#     st.subheader("📈 Variação de Preços por Concorrente")

#     # Seleção de produto e moeda
#     produto_focus = st.selectbox("Produto para análise", df_precos['produto'].unique())
#     moeda_focus = st.selectbox("Moeda:", df_precos['moeda'].unique())

#     # Filtrar por produto e moeda
#     df_focus = df_precos[
#         (df_precos['produto'] == produto_focus) &
#         (df_precos['moeda'] == moeda_focus)
#     ]

#     # Verifica se há dados disponíveis
#     if not df_focus.empty:
#         fig = px.line(
#             df_focus.sort_values('data_preco'),
#             x='data_preco',
#             y='preco',
#             color='localizacao',
#             title=f'Histórico de Preços ({moeda_focus}) - {produto_focus}',
#             markers=True
#         )
#         fig.update_layout(
#             title_font=dict(size=20), 
#             margin=dict(t=50, b=10),
#             legend_title="Localização"
#         )
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.warning("Nenhum dado encontrado para o produto e moeda selecionados.")

#     # Seção de Avisos Urgentes - Melhorado o contraste
#     st.subheader("⚠️ Avisos Urgentes")
#     avisos = [
#         "Variação abrupta de preço detectada no PR.",
#         "Preço médio do frete entre GO e MT aumentou 12%.",
#         "Queda no preço da cultura no MS nas últimas semanas.",
#         "Alta nos custos de transporte no MT.",
#         "Produto importado abaixo da média histórica."
#     ]

#     # Cards para avisos com melhor contraste
#     cols_avisos = st.columns(len(avisos))
#     for i, aviso in enumerate(avisos):
#         with cols_avisos[i]:
#             st.markdown(
#                 f"""
#                 <div style='background-color: #FFA000; color: #000000; padding: 1rem; 
#                 border-radius: 5px; height: 100%; font-weight: 500; text-align: center;'>
#                 ⚠️ {aviso}
#                 </div>
#                 """, 
#                 unsafe_allow_html=True
#             )

#     # Gráfico de comparação Permuta
#     st.subheader("📉 Comparativo Permuta")

#     culturas_disponiveis = df_barter['cultura'].unique()
#     cultura_selecionada = st.selectbox("Selecione a Cultura:", culturas_disponiveis)

#     # Filtrar df_barter pela cultura
#     filtros_barter = df_barter[df_barter['cultura'] == cultura_selecionada]

#     # Obter fertilizantes usados nessa cultura
#     ids_usados = filtros_barter['id_produto'].unique()
#     fertilizantes_disponiveis = df_produtos[df_produtos['id_produto'].isin(ids_usados)]['nome'].tolist()

#     if fertilizantes_disponiveis:
#         fertilizante_selecionado = st.selectbox("Produto (Fertilizante):", fertilizantes_disponiveis)

#         if fertilizante_selecionado:
#             id_fertilizante = df_produtos[df_produtos['nome'] == fertilizante_selecionado]['id_produto'].values[0]
#             filtros_barter = filtros_barter[filtros_barter['id_produto'] == id_fertilizante]

#             fig_barter = px.line(
#                 filtros_barter.sort_values("data"),
#                 x="data",
#                 y="razao_barter",
#                 color="estado",
#                 title=f"Permuta {fertilizante_selecionado} / {cultura_selecionada} - Razão ao longo do tempo"
#             )
#             fig_barter.update_layout(legend_title="Estado")
#             st.plotly_chart(fig_barter, use_container_width=True)
#     else:
#         st.warning(f"Não há dados de permuta disponíveis para a cultura {cultura_selecionada}")

#     # Análises adicionais
#     st.subheader("📊 Análises Gerais")
#     col1, col2 = st.columns(2)

#     # Gráfico 1 - Média de preço por produto (em BRL)
#     with col1:
#         preco_medio = df_precos[df_precos['moeda'] == 'BRL'].groupby("produto")["preco"].mean().reset_index()
#         preco_medio = preco_medio.sort_values("preco", ascending=False)
#         fig1 = px.bar(
#             preco_medio, 
#             x='produto', 
#             y='preco', 
#             title='Preço Médio por Produto (BRL)', 
#             text_auto=True,
#             color='produto'
#         )
#         fig1.update_layout(showlegend=False)
#         st.plotly_chart(fig1, use_container_width=True)

#     # Gráfico 2 - Média de preço por local (em BRL)
#     with col2:
#         preco_local = df_precos[df_precos['moeda'] == 'BRL'].groupby("localizacao")["preco"].mean().reset_index()
#         fig2 = px.pie(
#             preco_local, 
#             names='localizacao', 
#             values='preco', 
#             title='Distribuição de Preço Médio por Localização (BRL)',
#             hole=0.4
#         )
#         st.plotly_chart(fig2, use_container_width=True)

#     # Tabela de fretes
#     st.subheader("🚚 Tabela de Fretes Atuais")
#     st.dataframe(
#         df_fretes.sort_values("data_frete", ascending=False).head(10),
#         use_container_width=True,
#         column_config={
#             "origem": "Origem",
#             "destino": "Destino",
#             "tipo_transporte": "Tipo de Transporte",
#             "preco": st.column_config.NumberColumn("Preço", format="R$ %.2f"),
#             "moeda": "Moeda",
#             "data_frete": st.column_config.DateColumn("Data", format="DD/MM/YYYY")
#         }
#     )

# elif st.session_state.pagina_atual == 'previsoes':
#     st.header("Previsões de Mercado")
#     st.info("Esta página está em desenvolvimento. Em breve você poderá visualizar previsões e tendências de mercado.")
    
#     # Placeholder para mockup de previsões
#     st.subheader("Tendências Previstas (Mockup)")
#     tendencias_data = {
#         'Produto': ['MAP', 'KCL', 'Ureia', 'TSP', 'SSP'],
#         'Tendência': [1, -1, 1, 0, -1],
#         'Previsão (%)': [12, -8, 5, 0, -3]
#     }
    
#     tendencias_df = pd.DataFrame(tendencias_data)
    
#     # Criar indicadores de tendência
#     def formatar_tendencia(val):
#         if val == 1:
#             return "↗️ Alta"
#         elif val == -1:
#             return "↘️ Queda"
#         else:
#             return "→ Estável"
    
#     tendencias_df['Indicador'] = tendencias_df['Tendência'].apply(formatar_tendencia)
    
#     # Mostrar tabela com tendências
#     st.dataframe(
#         tendencias_df[['Produto', 'Indicador', 'Previsão (%)']],
#         use_container_width=True,
#         hide_index=True
#     )

# elif st.session_state.pagina_atual == 'perfil':
#     st.header("Perfil do Usuário")
    
#     # Simulação de perfil
#     col1, col2 = st.columns([1, 2])
    
#     with col1:
#         st.markdown("""
#         <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 10px; text-align: center;'>
#             <img src="https://i.pravatar.cc/150?img=68" style='border-radius: 50%; width: 150px; height: 150px;' alt='Foto de perfil'>
#             <h2>João Silva</h2>
#             <p>Analista de Mercado</p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("### Detalhes da Conta")
#         st.markdown("**Email:** joao.silva@morroverde.com.br")
#         st.markdown("**Departamento:** Comercial")
#         st.markdown("**Último acesso:** Hoje às 10:45")
        
#         st.markdown("### Atividades Recentes")
#         atividades = [
#             "Importou relatório de preços - 2 horas atrás",
#             "Atualizou permuta de KCL - Ontem",
#             "Gerou relatório trimestral - 3 dias atrás"
#         ]
        
#         for atividade in atividades:
#             st.markdown(f"- {atividade}")
    
#     st.button("Editar Perfil", use_container_width=False)
#     st.button("Sair", use_container_width=False)