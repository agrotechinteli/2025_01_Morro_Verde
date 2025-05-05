---
sidebar_position: 1
custom_edit_url: null
---

# Modelagem da Arquitetura da Solução

## Componentes da Solução Técnica

# Arquitetura da Aplicação

## Frontend

- **Descrição**: Aplicação web interativa desenvolvida com Streamlit, focada em visualização de dados e interação com usuários de forma simples e rápida.
- **Função**: Interface para upload de arquivos (como PDFs), visualização de dashboards interativos e análise gráfica.
- **Comunicação**: Envia requisições HTTP ao backend ou interage diretamente com lógica Python integrada ao Streamlit.

## Backend

- **Descrição**: Backend desenvolvido em Python, responsável pelo processamento de dados, integração com APIs de IA e manipulação de arquivos.
- **Função**: Extração de dados de PDFs usando APIs (como AWS Textract, Google Cloud Vision ou OpenAI), processamento de dados e envio de resultados ao frontend.
- **Comunicação**: APIs RESTful e integração direta com o Streamlit; conexão com o banco de dados PostgreSQL para armazenamento e recuperação de dados.

## APIs

- **Descrição**: Interfaces de integração com serviços externos de IA e OCR.
- **Função**: Realizar a extração automática de informações a partir de documentos (como PDFs escaneados).
- **Exemplos**:
  - AWS Textract
  - Google Cloud Vision
  - OpenAI API
- **Formato de Dados**: JSON

## Banco de Dados

- **Descrição**: Sistema relacional utilizando PostgreSQL.
- **Função**: Armazenamento estruturado e persistente de dados extraídos, análises, relatórios e histórico de interações do usuário.

## Visualização de Dados

- **Descrição**: Gráficos e dashboards gerados com Plotly, Matplotlib e Seaborn.
- **Função**: Exibir dados de forma visual e interativa, facilitando a análise e tomada de decisão.

## Hospedagem

- **Descrição**: A aplicação pode ser hospedada em Heroku ou Streamlit Cloud, permitindo fácil acesso via web.
- **Função**: Disponibilizar a aplicação ao usuário final sem necessidade de infraestrutura própria.

## Fluxo de Dados

1. O usuário acessa a aplicação via navegador (frontend em Streamlit).
2. O usuário envia um arquivo (como um PDF).
3. O backend (Python) processa o arquivo e utiliza APIs externas (AWS Textract, Google Cloud Vision ou OpenAI) para extrair informações.
4. Os dados extraídos são armazenados no PostgreSQL.
5. O backend utiliza bibliotecas de visualização (Plotly, Seaborn, Matplotlib) para gerar gráficos e dashboards.
6. O frontend exibe os resultados de forma interativa ao usuário.
7. Toda a aplicação é hospedada em Heroku ou Streamlit Cloud, acessível via web.
