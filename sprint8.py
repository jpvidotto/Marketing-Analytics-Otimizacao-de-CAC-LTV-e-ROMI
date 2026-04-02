import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats as st

visit_logs = pd.read_csv('dataframes/visits_log_us.csv', dtype={'Device': 'category', 'Source Id': 'category'}, parse_dates=['Start Ts', 'End Ts'])
costs = pd.read_csv('dataframes/costs_us.csv', parse_dates=['dt'], dtype={'source_id': 'category'})
orders_log = pd.read_csv('dataframes/orders_log_us.csv', parse_dates=['Buy Ts'])

# Renomeando as colunas para facilitar o acesso e a manipulação dos dados
visit_logs.columns = visit_logs.columns.str.lower().str.replace(' ', '_')
costs.columns = costs.columns.str.lower().str.replace(' ', '_')
orders_log.columns = orders_log.columns.str.lower().str.replace(' ', '_')


#  Analisando o uso de memória dos DataFrames para garantir que eles estão otimizados para análise.
visit_logs.info(memory_usage='deep')
costs.info(memory_usage='deep')
orders_log.info(memory_usage='deep')

#Iniciando o 2 passo
#Respondendo a 1 etapa.

#Vamos analisar a tendência de usuários ao longo do tempo, agrupando os dados por dia, semana e mês. Para isso, utilizaremos a coluna 'start_ts' para extrair as datas e calcular o número de usuários únicos para cada período. Em seguida, geraremos gráficos de linha para visualizar essas tendências.
usuarios_por_dia = visit_logs.groupby(visit_logs['start_ts'].dt.date)['uid'].nunique()
plt.figure(figsize=(12, 6))
sns.lineplot(x=usuarios_por_dia.index, y=usuarios_por_dia.values)
plt.title('Número de Usuários por Dia')
plt.xlabel('Data')
plt.ylabel('Número de Usuários')
plt.xticks(rotation=45)
plt.savefig('usuarios_por_dia.png')
plt.close()
usuarios_por_semana = visit_logs.groupby(visit_logs['start_ts'].dt.to_period('W'))['uid'].nunique()
plt.figure(figsize=(12, 6))
sns.lineplot(x=usuarios_por_semana.index.astype(str), y=usuarios_por_semana.values)
plt.title('Número de Usuários por Semana')
plt.xlabel('Semana')
plt.ylabel('Número de Usuários')
plt.xticks(rotation=45)
plt.savefig('usuarios_por_semana.png')
plt.close()
usuarios_por_mes = visit_logs.groupby(visit_logs['start_ts'].dt.to_period('M'))['uid'].nunique()
plt.figure(figsize=(12, 6))
sns.lineplot(x=usuarios_por_mes.index.astype(str), y=usuarios_por_mes.values)
plt.title('Número de Usuários por Mês')
plt.xlabel('Mês')
plt.ylabel('Número de Usuários')
plt.xticks(rotation=45)
plt.savefig('usuarios_por_mes.png')
plt.close()


# Vamos analisar o número de acessos por dia, agrupando os dados por dia e contando o número total de sessões (acessos) e o número de usuários únicos para cada dia. Em seguida, geraremos um gráfico de linha para visualizar a tendência dos acessos ao longo do tempo.
acessos_por_dia = visit_logs.groupby(visit_logs['start_ts'].dt.date)['uid'].agg(['count', 'nunique'])
acessos_por_dia.columns = ['n_sessions', 'n_users']

plt.figure(figsize=(12, 6))
sns.lineplot(x=acessos_por_dia.index, y=acessos_por_dia['n_sessions'])
plt.title('Número de Acessos por Dia')
plt.xlabel('Data')
plt.ylabel('Número de Acessos')
plt.xticks(rotation=45)
plt.savefig('acessos_por_dia.png')
plt.close()

#Vamos analisar a duração das visitas dos usuários. Para isso, calcularemos a diferença entre as colunas 'end_ts' e 'start_ts' para obter a duração de cada visita em minutos. Em seguida, geraremos um histograma para visualizar a distribuição das durações das visitas.
duracao_visitas = (visit_logs['end_ts'] - visit_logs['start_ts']).dt.total_seconds() / 60
plt.figure(figsize=(12, 6))
sns.histplot(duracao_visitas, bins=70, kde=True)
plt.title('Duração das Visitas (em minutos)')
plt.xlabel('Duração (minutos)')
plt.ylabel('Frequência')
plt.savefig('duracao_visitas.png')
plt.close()


# # --- Com que frequência os usuários voltam?  

# # Determinando o mês de aquisição de cada usuário (primeira sessão)
visit_logs['acquisition_month'] = visit_logs.groupby('uid')['start_ts'].transform('min').dt.to_period('M')


visit_logs['session_month'] = visit_logs['start_ts'].dt.to_period('M')

# # Calculando a "idade" do coorte para cada sessão
visit_logs['cohort_lifetime'] = (visit_logs['session_month'] - visit_logs['acquisition_month']).apply(lambda x: x.n)

# # Tabela de coortes (pivot table)
cohorts = visit_logs.groupby(['acquisition_month', 'cohort_lifetime'])['uid'].nunique().reset_index()
cohorts_pivot = cohorts.pivot_table(index='acquisition_month', columns='cohort_lifetime', values='uid')

# # Calculando a retenção em percentual
cohort_size = cohorts_pivot.iloc[:, 0]
retention_matrix = cohorts_pivot.divide(cohort_size, axis=0)

# # Gerando o mapa de calor de retenção
sns.heatmap(retention_matrix, annot=True, fmt='.0%', cmap='YlGnBu')
plt.title('Matriz de Retenção por Coorte')
plt.xlabel('Meses desde a Aquisição')
plt.ylabel('Mês de Aquisição')
plt.savefig('matriz_retenção.png')
plt.close()

#Respondendo a 2 etapa.

# # --- Quando as pessoas começam a comprar?

# # Encontrando a primeira visita de cada usuário
first_visit = visit_logs.groupby('uid')['start_ts'].min().reset_index()
first_visit.columns = ['uid', 'first_visit_ts']

# # Encontrando a primeira compra de cada usuário
first_order = orders_log.groupby('uid')['buy_ts'].min().reset_index()
first_order.columns = ['uid', 'first_buy_ts']

# # Unindo informações
conversion_data = pd.merge(first_visit, first_order, on='uid')


conversion_data['time_to_conversion'] = (conversion_data['first_buy_ts'] - conversion_data['first_visit_ts']).dt.days

# # Gráfico
plt.figure(figsize=(12, 6))
sns.barplot(x=conversion_data['time_to_conversion'], y=conversion_data['uid'])
plt.title('Tempo para Conversão (Dias)')
plt.xlabel('Dias para a Primeira Compra')
plt.ylabel('Usuários')
plt.savefig('tempo_para_conversao.png')
plt.close()

print(f"Tempo mediano para a primeira compra: {conversion_data['time_to_conversion'].median():.1f} dias")

#Vamos analisar o comportamento dos compradores em comparação com os visitantes que não realizaram compras. Para isso, identificaremos os usuários que realizaram compras e compararemos suas atividades no site, como número de visitas, duração das visitas e fontes de tráfego.
# # --- Quantos pedidos os clientes fazem? 


# # Encontrando o mês da primeira compra de cada cliente (este será o coorte)
first_order_month = orders_log.groupby('uid')['buy_ts'].min().dt.to_period('M')
first_order_month.name = 'acquisition_month'

# # Juntando a informação do coorte de volta ao dataframe de pedidos
orders_with_cohort = orders_log.join(first_order_month, on='uid')

# # Mês de cada pedido
orders_with_cohort['order_month'] = orders_with_cohort['buy_ts'].dt.to_period('M')

# # Calculando 'idade' do coorte para cada pedido (em meses desde a 1ª compra)
orders_with_cohort['cohort_age'] = (orders_with_cohort['order_month'] - orders_with_cohort['acquisition_month']).apply(lambda x: x.n)

# # Criando uma tabela pivot com o número total de pedidos por coorte e por idade
orders_by_cohort = orders_with_cohort.pivot_table(
 index='acquisition_month',
 columns='cohort_age',
 values='uid',
 aggfunc='count'
 )

# # Obtendo o tamanho de cada coorte (número de clientes únicos que compraram pela 1ª vez em cada mês)
cohort_size = orders_with_cohort.groupby('acquisition_month')['uid'].nunique()

# # Dividindo o número de pedidos pelo tamanho do coorte para obter a média
avg_orders_pivot = orders_by_cohort.divide(cohort_size, axis=0)

# # Mapa heatmap
sns.heatmap(avg_orders_pivot, annot=True, fmt='.2f', cmap='YlGnBu')
plt.title('Média de Pedidos por Cliente por Coorte e Idade do Coorte')
plt.xlabel('Meses desde a Primeira Compra')
plt.ylabel('Mês da Primeira Compra')
plt.savefig('media_pedidos_por_coorte.png')
plt.close()

#Vamos calcular a receita média por mês e a receita total por cliente (LTV - Lifetime Value) para os usuários que realizaram compras. Para isso, agruparemos os dados de compras por mês e por cliente, e calcularemos as métricas correspondentes.
average_check = orders_log['revenue'].mean()
print(f"O ticket médio geral é: ${average_check:.2f}")

# # Análise do Ticket Médio ao longo do tempo
orders_log['order_month'] = orders_log['buy_ts'].dt.to_period('M')
monthly_avg_check = orders_log.groupby('order_month')['revenue'].mean()

plt.figure(figsize=(12, 6))
sns.lineplot(x=monthly_avg_check.index.astype(str), y=monthly_avg_check.values)
plt.title('Ticket Médio por Mês')
plt.xlabel('Mês')
plt.ylabel('Ticket Médio')
plt.xticks(rotation=45)
plt.savefig('ticket_medio_por_mes.png')
plt.close()

# # --- Quanto dinheiro eles trazem para a empresa (LTV)?


# # Definindo o mês de aquisição (primeira compra) como o coorte
orders_log['acquisition_month'] = orders_log.groupby('uid')['buy_ts'].transform('min').dt.to_period('M')

# # Calculando a idade do coorte para cada pedido
orders_log['cohort_lifetime'] = ((orders_log['order_month'] - orders_log['acquisition_month']).apply(lambda x: x.n))

# # Calculando a receita por coorte e por idade
cohorts_revenue = orders_log.groupby(['acquisition_month', 'cohort_lifetime'])['revenue'].sum().reset_index()

# # Obtendo o tamanho de cada coorte (número de clientes únicos)
cohort_sizes = orders_log.groupby('acquisition_month')['uid'].nunique().reset_index()
cohort_sizes.columns = ['acquisition_month', 'n_buyers']

# # Unindo os dados de receita e tamanho do coorte
cohorts_data = pd.merge(cohorts_revenue, cohort_sizes, on='acquisition_month')

# # LTV
cohorts_data['ltv'] = cohorts_data['revenue'] / cohorts_data['n_buyers']

# # Tabela pivot para o LTV
ltv_pivot = cohorts_data.pivot_table(index='acquisition_month',
                                    columns='cohort_lifetime',
                                    values='ltv',
                                    aggfunc='sum').cumsum(axis=1)

# # Heatmap do LTV
plt.figure(figsize=(12, 6))
sns.heatmap(ltv_pivot, annot=True, fmt='.2f', cmap='YlGnBu')
plt.title('LTV por Coorte e Idade do Coorte')
plt.xlabel('Meses desde a Primeira Compra')
plt.ylabel('Mês da Primeira Compra')
plt.savefig('ltv_por_coorte.png')
plt.close()



#Respondendo a 3 etapa.

# # --- Quanto dinheiro foi gasto?



# # Adicionando uma coluna de mês para agrupar os custos
costs['month'] = costs['dt'].dt.to_period('M')

# # Criar uma tabela dinâmica (pivot) para organizar os dados para o gráfico
# # Onde o índice é o mês, as colunas são as fontes e os valores são os custos
costs_pivot = costs.pivot_table(
index='month',
columns='source_id',
values='costs',
aggfunc='sum'
 ).fillna(0) 

# # Plotando o gráfico de linhas a partir da tabela dinâmica
plt.figure(figsize=(12, 6))
sns.lineplot(data=costs, x='month', y='costs', hue='source_id')
plt.title('Custos por Fonte ao Longo do Tempo')
plt.xlabel('Mês')
plt.ylabel('Custos Totais')
plt.xticks(rotation=45)
plt.legend(title='Fonte de Aquisição')
plt.savefig('custos_por_fonte.png')
plt.close()



# # --- Quanto custou a aquisição de clientes (CAC)? 


# # Adiciando uma coluna de mês aos custos
costs['month'] = costs['dt'].dt.to_period('M')

# # Encontrando a primeira visita de cada usuário para obter a fonte de aquisição
first_visits = visits.sort_values('start_ts').drop_duplicates('uid')
first_visits = first_visits[['uid', 'source_id']]

# # Encontrando o mês da primeira compra de cada cliente
first_orders = orders.sort_values('buy_ts').drop_duplicates('uid')
first_orders['acquisition_month'] = first_orders['buy_ts'].dt.to_period('M')
first_orders = first_orders[['uid', 'acquisition_month']]

# # Unindo as informações para saber a fonte e o mês de aquisição de cada cliente
buyers = pd.merge(first_orders, first_visits, on='uid')

# # Calculando o número de clientes adquiridos por mês e por fonte
buyers_by_month_source = buyers.groupby(['acquisition_month', 'source_id'])['uid'].nunique().reset_index()
buyers_by_month_source.columns = ['month', 'source_id', 'n_buyers']

# # Formanto os custos mensais por fonte
costs_by_month_source = costs.groupby(['month', 'source_id'])['costs'].sum().reset_index()

# # Unindo custos e número de compradores por mês e fonte
cac_monthly_data = pd.merge(costs_by_month_source, buyers_by_month_source, on=['month', 'source_id'])

# # CAC mensal para cada fonte
# # (Lidar com a divisão por zero caso haja custos sem compradores, embora improvável com o merge)
cac_monthly_data = cac_monthly_data[cac_monthly_data['n_buyers'] > 0]
cac_monthly_data['cac'] = cac_monthly_data['costs'] / cac_monthly_data['n_buyers']

# # Tabela dinâmica (pivot) para a plotagem
cac_pivot = cac_monthly_data.pivot_table(
index='month',
columns='source_id',
values='cac'
 )

# # Gráfico de linhas
plt.figure(figsize=(12, 6))
sns.lineplot(data=cac_pivot)
plt.title('CAC por Fonte ao Longo do Tempo')
plt.xlabel('Mês')
plt.ylabel('CAC (Custo por Aquisição)')
plt.xticks(rotation=45)
plt.legend(title='Fonte de Aquisição')
plt.savefig('cac_por_fonte.png')
plt.close()





# # --- Os investimentos valeram a pena? 

# # LTV acumulado por coorte
orders_log['acquisition_month'] = orders_log.groupby('uid')['buy_ts'].transform('min').dt.to_period('M')
orders_log['order_month'] = orders_log['buy_ts'].dt.to_period('M')
orders_log['cohort_lifetime'] = (orders_log['order_month'] - orders_log['acquisition_month']).apply(lambda x: x.n)
cohorts_revenue = orders_log.groupby(['acquisition_month', 'cohort_lifetime'])['revenue'].sum().reset_index()
cohort_sizes = orders_log.groupby('acquisition_month')['uid'].nunique().reset_index()
cohort_sizes.columns = ['acquisition_month', 'n_buyers']
cohorts_data = pd.merge(cohorts_revenue, cohort_sizes, on='acquisition_month')
cohorts_data['ltv'] = cohorts_data['revenue'] / cohorts_data['n_buyers']
ltv_pivot = cohorts_data.pivot_table(index='acquisition_month', columns='cohort_lifetime', values='ltv').cumsum(axis=1)

# # CAC por coorte (mês de aquisição)
costs['month'] = costs['dt'].dt.to_period('M')
first_orders = orders_log.sort_values('buy_ts').drop_duplicates('uid')
first_orders['acquisition_month'] = first_orders['buy_ts'].dt.to_period('M')
n_buyers_by_cohort = first_orders.groupby('acquisition_month')['uid'].nunique().reset_index()
n_buyers_by_cohort.columns = ['month', 'n_buyers']
costs_by_cohort = costs.groupby('month')['costs'].sum().reset_index()
cac_by_cohort = pd.merge(costs_by_cohort, n_buyers_by_cohort, on='month')
cac_by_cohort['cac'] = cac_by_cohort['costs'] / cac_by_cohort['n_buyers']
cac_by_cohort = cac_by_cohort[['month', 'cac']]
cac_by_cohort.columns = ['acquisition_month', 'cac']

# # ROMI (LTV - CAC) / CAC
# # Juntando o CAC com a tabela de LTV
 report = pd.merge(ltv_pivot.reset_index(), cac_by_cohort, on='acquisition_month')
report = report.set_index('acquisition_month')

# # Obtendo a coluna de CAC e as colunas de LTV
cac_values = report['cac']
ltv_values = report.drop(columns=['cac'])

# # Calculando o ROMI para cada mês da vida do coorte
romi_pivot = ltv_values.subtract(cac_values, axis=0).divide(cac_values, axis=0)

# # Mapa de calor do ROMI
sns.heatmap(romi_pivot, annot=True, fmt='.2f', cmap='YlGnBu')
plt.title('ROMI por Coorte e Idade do Coorte')
plt.xlabel('Meses desde a Primeira Compra')
plt.ylabel('Mês da Primeira Compra')
plt.savefig('romi_por_coorte.png')
plt.close()

## O melhor mês para investir foi o mês 0 (mês da primeira compra), onde o ROMI é mais alto, indicando que o retorno sobre o investimento foi mais significativo nesse período. Isso sugere que os esforços de aquisição de clientes foram mais eficazes em gerar valor imediato para a empresa. No entanto, é importante considerar que o ROMI pode variar ao longo do tempo, e a análise de coortes ajuda a entender como o valor dos clientes evolui após a aquisição. Portanto, embora o mês 0 seja o melhor para investir, é crucial monitorar o desempenho das coortes ao longo do tempo para otimizar as estratégias de marketing e retenção.