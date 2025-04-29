---
sidebar_position: 2
custom_edit_url: null
---

# Modelo de Dados

[Produto]

- id_produto (PK)
- nome
- tipo (ex: Ureia, MAP, etc.)

[Localizacao]

- id_localizacao (PK)
- nome
- tipo (Porto, Estado, País)

[Preco]

- id_preco (PK)
- id_produto (FK)
- id_localizacao (FK)
- data_preco
- preco_usd
- preco_brl
- tipo_preco (FOB, CIF, FOT, EXW)

[Frete]

- id_frete (PK)
- origem (FK para Localizacao)
- destino (FK para Localizacao)
- tipo_transporte (ex: Marítimo, Rodoviário)
- preco_usd
- preco_brl
- data_frete

[Barter]

- id_barter (PK)
- cultura (ex: soja, milho, algodão)
- id_produto (FK)
- estado
- preco_npk (usd/t)
- preco_cultura (por saca)
- razao_barter (sacas/tonelada NPK)
- data

Como o modelo de dados suporta as funcionalidades previstas:

1- Preços de fertilizantes de forma histórica e por localização específica (relacionando Produto + Localização + Data).
2- Preços de frete entre origens e destinos (essencial para entender o custo total até o cliente final).
3- Barter Ratios entre insumos (fertilizantes) e safras agrícolas (soja, milho, arroz etc.), permitindo simular trocas.
4- Conversões de moeda (USD ↔ BRL) sem perder a informação original.
5- Análise de tendências de preços, comparação entre produtos, regiões e sazonalidade.