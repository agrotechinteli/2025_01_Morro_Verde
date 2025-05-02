---
sidebar_position: 2
custom_edit_url: null
---

# Modelo de Dados

**Afinal, o que é um diagrama de banco de dados?**

Um diagrama de banco de dados é uma representação visual da estrutura de um banco de dados. Ele mostra como os dados estão organizados, quais entidades (tabelas) existem, quais atributos (colunas) cada entidade tem e como elas se relacionam entre si.

Modelo de diagrama de banco de dados na aplicação Morro Verde:

![Imagem colada](./Pasted%20image%2020250429160230.png)

Como o modelo de dados suporta as funcionalidades previstas:

1- Preços de fertilizantes de forma histórica e por localização específica (relacionando Produto + Localização + Data).

2- Preços de frete entre origens e destinos (essencial para entender o custo total até o cliente final).

3- Barter Ratios entre insumos (fertilizantes) e safras agrícolas (soja, milho, arroz etc.), permitindo simular trocas.

4- Conversões de moeda (USD ↔ BRL) sem perder a informação original.

5- Análise de tendências de preços, comparação entre produtos, regiões e sazonalidade.
