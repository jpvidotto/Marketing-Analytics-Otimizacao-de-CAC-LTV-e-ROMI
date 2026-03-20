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
mean_total_revenue = orders_log['revenue'].mean()
#print(f"Receita média por mês: {mean_total_revenue:.2f}")

#Calculando a receita total por cliente (LTV)
ltv_por_cliente = orders_log.groupby('uid')['revenue'].sum()
ltv_medio = ltv_por_cliente.mean()
#print(f"Receita total por cliente: {ltv_medio:.2f}")

#Respondendo a 3 etapa.

#Calculando o valor gasto em marketing por origem de tráfego. Para isso, agruparemos os dados de custos por 'source_id' e calcularemos a soma dos custos para cada origem de tráfego.
custo_por_origem = costs.groupby('source_id')['costs'].sum().reset_index()
#print("Valor gasto em marketing por origem de tráfego:")
#print(custo_por_origem)

#Calculando o valor gasto em marketing por mês. Para isso, agruparemos os dados de custos por mês e calcularemos a soma dos custos para cada mês.
custo_por_mes = costs.groupby(costs['dt'].dt.to_period('M'))['costs'].sum()
#print("Valor gasto em marketing por mês:")
#print(custo_por_mes)

#Calculando o valor gasto em marketing em todo o período. Para isso, somaremos todos os custos registrados no dataset de custos.
custo_total = costs['costs'].sum()
#print(f"Valor gasto em marketing em todo o período: {custo_total:.2f}")

#Calculando o gasto foi gasto em aquisição de clientes para cada origem de tráfego. Para isso, identificaremos os usuários que realizaram compras e suas respectivas origens de tráfego, e depois calcularemos o custo por aquisição (CPA) para cada origem.

clients_por_origem = visit_logs.groupby(['source_id', 'device'])['uid'].nunique().reset_index()

cac_por_origem = custo_por_origem.merge(clients_por_origem, on='source_id', how='left')
cac_por_origem['cac'] = cac_por_origem['costs'] / cac_por_origem['uid']
cac_por_origem = cac_por_origem[['source_id', 'cac']].sort_values(by='cac')
plt.figure(figsize=(12, 6))
sns.barplot(x='source_id', y='cac', data=cac_por_origem)
plt.title('Custo por Aquisição (CPA) por Origem de Tráfego')
plt.xlabel('Origem de Tráfego')
plt.ylabel('Custo por Aquisição (CPA)')
plt.xticks(rotation=45)
plt.savefig('cac_por_origem.png')
plt.close()

cac_by_device = visit_logs.groupby(['device', 'source_id'])['uid'].nunique().reset_index()
cac_by_device = cac_by_device.merge(cac_por_origem, on='source_id', how='left')
cac_by_device['total_price'] = cac_by_device['uid'] * cac_by_device['cac']
plt.figure(figsize=(12, 6))
sns.barplot(x='device', y='total_price', data=cac_by_device)
plt.title('Custo Total por Dispositivo')
plt.xlabel('Dispositivo')
plt.ylabel('Custo Total')
plt.xticks(rotation=45)
plt.savefig('cac_por_dispositivo.png')
plt.close()

#Verificando as informações obtidas nas análises as origens mais eficazes em termos de aquisição de clientes, comparando o custo por aquisição (CPA) para cada origem de tráfego. Para isso, identificaremos as origens com os menores CPA e analisaremos suas características para entender por que são mais eficazes.


