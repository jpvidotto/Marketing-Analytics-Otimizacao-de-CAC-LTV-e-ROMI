# Marketing Analytics: Otimização de CAC, LTV e ROMI

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Seaborn](https://img.shields.io/badge/Seaborn-7db0ea?style=for-the-badge)

## 📌 Visão Geral do Projeto
Este projeto de Marketing Analytics foca em avaliar a eficiência dos investimentos em marketing digital de uma plataforma. Através da análise de logs de acessos, histórico de pedidos e despesas publicitárias, o objetivo foi calcular as métricas financeiras mais críticas para o negócio: o Custo de Aquisição de Clientes (CAC), o Valor do Tempo de Vida do Cliente (LTV) e o Retorno sobre o Investimento em Marketing (ROMI), utilizando análise de coortes.

## 🎯 Objetivos de Negócio
* **Avaliação de Rentabilidade:** Compreender o comportamento de compra dos clientes ao longo do tempo (Cohort Analysis).
* **Eficiência de Marketing:** Calcular quanto custa trazer um novo cliente (CAC) e quanto valor ele gera para a empresa a longo prazo (LTV).
* **Otimização de Orçamento:** Identificar através do ROMI quais períodos e coortes apresentam os melhores retornos, direcionando estrategicamente os futuros esforços de marketing e vendas.

## 🛠️ Stack Técnica
* **Linguagem:** Python
* **Manipulação e Otimização de Dados:** Pandas, NumPy
* **Visualização de Dados:** Seaborn, Matplotlib (Heatmaps)
* **Estatística:** SciPy

## 📉 Metodologia e Processamento
1. **Engenharia e Otimização de Dados:** Limpeza inicial, padronização de colunas e otimização profunda do uso de memória dos DataFrames (`memory_usage='deep'`) para garantir performance na manipulação de grandes volumes de logs de acesso.
2. **Análise de Coortes (Cohorts):** Agrupamento dos usuários com base no mês da primeira compra para rastrear o comportamento de retenção e geração de receita.
3. **Cálculo de Métricas Unitárias:**
    * **CAC:** Divisão dos custos mensais de marketing pelo número de novos compradores no mesmo período.
    * **LTV:** Cálculo da receita acumulada gerada por cada coorte ao longo dos meses subsequentes.
4. **Cálculo do ROMI:** Aplicação da fórmula `(LTV - CAC) / CAC` para descobrir o retorno real sobre o investimento.
5. **Visualização:** Geração de mapas de calor (Heatmaps) para facilitar a interpretação dos retornos percentuais ao longo da vida útil de cada coorte.

## 🏆 Resultados e Conclusões
* **Retorno Imediato:** A análise de coorte revelou que o melhor mês para o retorno do investimento é o "Mês 0" (o próprio mês da primeira compra). 
* **Eficácia na Aquisição:** O ROMI atinge o seu pico neste período inicial, indicando que as campanhas de marketing são altamente eficientes para gerar a conversão imediata do cliente.
* **Visão Estratégica:** Os dados sugerem que a empresa tem uma excelente estratégia de atração, mas pode desenvolver estratégias adicionais de CRM e vendas para aumentar a retenção e o consumo nos meses subsequentes ao mês de aquisição.

---

### 📂 Estrutura do Repositório
* `sprint8.py`: Script principal em Python contendo o pipeline de análise, desde o processamento até a geração dos gráficos.
* `romi_por_coorte.png`: Mapa de calor gerado pelo script demonstrando o Retorno sobre Investimento.
* `dataframes/`:
  * `visits_log_us.csv`: Logs de acesso e sessões dos utilizadores.
  * `costs_us.csv`: Custos diários de campanhas de marketing.
  * `orders_log_us.csv`: Histórico de compras e faturamento.

---
**João Pedro Vidotto Tavares Dias** *Data Analyst | Especialista em Vendas* [LinkedIn](https://www.linkedin.com/in/joao-vidotto/) | [GitHub](https://github.com/jpvidotto)
