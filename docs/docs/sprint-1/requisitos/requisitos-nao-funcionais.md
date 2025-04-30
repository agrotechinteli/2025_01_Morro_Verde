---
sidebar_position: 2
custom_edit_url: null
---

# Requisitos Não Funcionais

Segundo Marcelo Fantinato, professor da Universidade Virtual do Estado de São Paulo, os requisitos não funcionais (RNFs) definem as formas e maneiras como a solução executará os comportamentos declarados nos requisitos funcionais, delimitando os atributos de qualidade e restrições do sistema. Apesar de não terem ligação direta com as funcionalidades específicas, os RNFs são essenciais para avaliar quão bem o produto atende às necessidades do usuário final e mantém seu padrão de qualidade.

Os RNFs deste projeto seguem a norma **ISO 25010**, estabelecida pela *International Organization for Standardization* em 2011, que define um modelo de qualidade para software com base em oito aspectos principais:

- **Adequação Funcional**: Capacidade de atender às funções especificadas.
- **Desempenho**: Eficiência no uso de recursos e tempo de resposta.
- **Compatibilidade**: Capacidade de operar com outros sistemas ou tecnologias.
- **Usabilidade**: Facilidade de uso e aprendizado.
- **Confiabilidade**: Capacidade de operar corretamente sob condições especificadas.
- **Segurança**: Proteção contra acessos não autorizados.
- **Manutenibilidade**: Facilidade de correção e atualização.
- **Portabilidade**: Capacidade de operar em diferentes ambientes.

Neste projeto, os aspectos de "Acessibilidade" e "Capacitação" foram incluídos como extensões contextuais da norma ISO 25010. "Acessibilidade" está relacionada à disponibilidade do sistema para os usuários (mapeada como subcaracterística de Desempenho e Usabilidade), enquanto "Capacitação" refere-se ao treinamento necessário para adoção eficiente (mapeada como subcaracterística de Usabilidade).

## Requisitos Não Funcionais

Os RNFs abaixo foram definidos com métricas quantificáveis para garantir clareza, mensurabilidade e alinhamento com os objetivos do parceiro Morro Verde, que busca maior agilidade na precificação e análise de mercado de fertilizantes.

| **RNF#** | **Descrição** | **Aspecto de qualidade** |
|----------|---------------|--------------------------|
| RNF01 | O dashboard deve ser intuitivo, alcançando uma pontuação de usabilidade mínima de 80/100 em testes com a equipe comercial, com tempo médio de aprendizado de 2 horas. | Usabilidade |
| RNF02 | O dashboard deve operar em tempo real, fornecendo dados atualizados a cada 5 minutos para cotações cambiais e a cada 1 semana para relatórios de mercado. | Desempenho |
| RNF03 | O dashboard deve ser acessível em tempo real pela equipe comercial via interface web, com disponibilidade durante o horário comercial (8h às 18h). | Acessibilidade |
| RNF04 | O sistema deve garantir previsões de preços com precisão mínima de 85% em testes com dados históricos dos últimos 12 meses. | Confiabilidade |
| RNF05 | As integrações de dados (APIs e relatórios) devem ser eficazes, com taxa de erro inferior a 1% em 1000 chamadas de API ou uploads de relatórios. | Confiabilidade |
| RNF06 | O sistema deve permitir ajustes com base em feedback, implementando melhorias solicitadas em até 3 dias úteis. | Manutenibilidade |
| RNF07 | O sistema deve incluir documentação completa, com pelo menos 90% de cobertura das funcionalidades. | Manutenibilidade |
| RNF08 | O sistema deve consolidar dados dispersos em um único ambiente, suportando até 10.000 registros de dados por mês sem degradação de desempenho. | Escalabilidade |
| RNF09 | O sistema deve ser compatível com Python, SQL e bibliotecas de visualização (Matplotlib, Plotly, Seaborn). | Compatibilidade |
| RNF10 | O sistema deve incluir treinamento, com 100% dos usuários da equipe comercial capacitados. | Capacitação |

### Justificativa das Métricas

As métricas foram definidas para agregar valor ao parceiro, garantindo que o dashboard atenda às expectativas de desempenho, usabilidade e confiabilidade. Abaixo, a justificativa para as principais métricas:

- **RNF01 (Usabilidade)**: A pontuação de 80/100 no System Usability Scale (SUS) é um padrão reconhecido para sistemas intuitivos. O tempo de aprendizado de 2 horas é viável para a equipe comercial.
- **RNF02 (Desempenho)**: Atualizações a cada 5 minutos para cotações cambiais refletem a volatilidade do mercado, enquanto atualizações semanais para relatórios de mercado alinham-se com a revisão de preços em 2 meses.
- **RNF03 (Acessibilidade)**: A disponibilidade durante o horário comercial (8h às 18h) atende ao uso típico da equipe comercial, com margem para pequenas manutenções fora desse período.
- **RNF04 (Confiabilidade)**: A precisão de 85% em previsões é alcançável com modelos de séries temporais, considerando variáveis como pluviosidade e endividamento, e um período de 12 meses cobre ciclos sazonais.
- **RNF05 (Confiabilidade)**: Uma taxa de erro inferior a 1% em integrações é padrão para APIs modernas e uploads validados, garantindo operações confiáveis.
- **RNF06 e RNF07 (Manutenibilidade)**: Prazos de 3 dias para ajustes e 90% de cobertura na documentação são realistas para sprints quinzenais e facilitam manutenção futura.
- **RNF08 (Escalabilidade)**: Suportar 10.000 registros por mês é conservador para um sistema de fertilizantes, garantindo desempenho com Streamlit e SQL.
- **RNF09 (Compatibilidade)**: A compatibilidade com Python, SQL e bibliotecas específicas assegura integração com tecnologias modernas.
- **RNF10 (Capacitação)**: Capacitar 100% dos usuários em sessões práticas de 4 horas garante adoção eficiente.

## Regras de Negócios Vinculadas

As Regras de Negócios (RNs) abaixo foram definidas para suportar os RNFs, garantindo que o sistema atenda aos objetivos do projeto e os aspectos de qualidade da ISO 25010. Cada RN está vinculada a um ou mais RNFs, reforçando a qualidade da solução.

| **RN#** | **Descrição** | **RNFs Suportados** | **Aspecto de Qualidade** |
|---------|---------------|---------------------|--------------------------|
| RN01 | O dashboard deve exibir indicadores de precificação (ex.: preço do dólar, custo de importação, preços de concorrentes) consolidados em uma única interface para facilitar a revisão da política de preços. | RNF01, RNF08 | Usabilidade, Escalabilidade |
| RN02 | A revisão da política de preços deve ser realizada em até 2 meses, utilizando os dados e previsões do dashboard. | RNF02, RNF04 | Desempenho, Confiabilidade |
| RN03 | O dashboard deve permitir o upload manual de relatórios em formatos predefinidos (ex.: CSV, Excel, PDF) e extrair automaticamente os principais indicadores para a base de dados. | RNF01, RNF05 | Usabilidade, Confiabilidade |
| RN04 | O sistema deve integrar APIs externas para coletar dados em tempo real, como cotações cambiais e históricos de precificação de fertilizantes. | RNF02, RNF03, RNF05 | Desempenho, Acessibilidade, Confiabilidade |
| RN05 | O modelo de machine learning deve prever tendências de preços com base em séries temporais, utilizando dados históricos e variáveis como pluviosidade e endividamento dos produtores. | RNF01, RNF04 | Usabilidade, Confiabilidade |
| RN06 | O dashboard deve incluir gráficos que permitam comparar preços de concorrentes e identificar oportunidades de mercado. | RNF01, RNF04 | Usabilidade, Confiabilidade |
| RN07 | Alterações no dashboard (ex.: novas funcionalidades, ajustes na interface) devem ser implementadas com base em feedback coletado da equipe comercial. | RNF01, RNF06 | Usabilidade, Manutenibilidade |
| RN08 | O sistema deve ser entregue com documentação detalhada, incluindo guias de uso, descrições técnicas e instruções de manutenção. | RNF07, RNF10 | Manutenibilidade, Capacitação |
| RN09 | O treinamento dos usuários deve ser realizado na Sprint 5, com sessões práticas para garantir que a equipe comercial utilize o dashboard eficientemente. | RNF01, RNF10 | Usabilidade, Capacitação |
| RN10 | O sistema deve ser desenvolvido utilizando Python, SQL e bibliotecas de visualização compatíveis, com versionamento de código via Git. | RNF06, RNF09 | Manutenibilidade, Compatibilidade |

### Benefícios das Regras de Negócios

As RNs foram projetadas para:
- **Agilizar a precificação**: RN01, RN02 e RN06 reduzem o ciclo de revisão de preços de 6 para 2 meses, conforme objetivo do projeto.
- **Garantir confiabilidade**: RN04, RN05 e RN06 asseguram dados precisos e atualizados, essenciais para decisões estratégicas.
- **Facilitar adoção**: RN03, RN07 e RN09 tornam o sistema intuitivo e acessível, com treinamento eficiente.
- **Suportar manutenção**: RN08 e RN10 garantem documentação e versionamento para atualizações futuras.

## Conclusão

Os RNFs e RNs apresentados foram definidos para atender às necessidades da Morro Verde, alinhando-se à norma ISO 25010 e incorporando métricas quantificáveis que agregam valor ao parceiro. A vinculação entre RNs e RNFs garante que os aspectos de qualidade, como usabilidade, desempenho e confiabilidade, sejam alcançados, resultando em um dashboard funcional, eficiente e adotável pela equipe comercial.