---
sidebar_position: 2
custom_edit_url: null
---

# Requisitos Não Funcionais

&emsp;Segundo Marcelo Fantinato, professor da Universidade Virtual do Estado de São Paulo, os requisitos não funcionais são as formas e maneiras como a solução executará os comportamentos declarados nos requisitos funcionais e delimitam as atribuições de qualidade e restrições do sistema. Nesse contexto, apesar de os requisitos não funcionais não terem impacto ou ligação direta com as funcionalidades da solução, são importantes e necessários para avaliar quão bem o produto atende as necessidades do usuário final e mantém seu padrão de qualidade.

&emsp;Além disso, os requisitos não funcionais seguem algumas normas de padronização, como a norma ISO25010, a qual será utilizada e seguida na documentação desse projeto. A ISO25010 é um conjunto de regras cunhadas pela _International Organization for Standardization_ em 2011 e que descrevem um modelo para a qualidade de um software, ou seja, quais características e comportamentos um software deve ter para declarar que ele possui qualidade. A ISO25010 avalia e compara 8 aspectos principais das soluções de software:

- Adequação Funcional
- Desempenho
- Compatibilidade
- Usabilidade
- Confiabilidade 
- Segurança
- Manutenibilidade
- Portabilidade


&emsp;Abaixo estão descritos os requisito não funcionais da solução:

| **RNF#** | **Descrição** | **Aspecto de qualidade** | 
|----------|----------|----------|
|RNF01|O dashboard deve ser intuitivo, com feedback positivo da equipe comercial sobre usabilidade.|Usabilidade|
|RNF02|O dashboard deve operar em tempo real para fornecer dados atualizados instantaneamente.|Desempenho|
|RNF03|O dashboard deve ser acessível em tempo real pela equipe comercial via interface web. |Acessibilidade|
|RNF04| O sistema deve garantir previsões precisas para embasar decisões estratégicas. |Confiabilidade|
|RNF05| As integrações de dados (APIs e relatórios) devem ser eficazes e livres de erros. | Confiabilidade |
|RNF06| O sistema deve permitir ajustes com base em feedback da equipe comercial. |Manutenibilidade|
|RNF07| O sistema deve incluir documentação completa para facilitar manutenção futura. | Manutenibilidade |
|RNF08| O sistema deve consolidar dados dispersos em um único ambiente, suportando volumes crescentes de dados. | Escalabilidade |
|RNF09| O sistema deve ser compatível com Python, SQL e bibliotecas de visualização (Matplotlib, Plotly, Seaborn).| Compatibilidade |
|RNF10| O sistema deve incluir treinamento para garantir adoção eficiente pelos usuários. | Capacitação
