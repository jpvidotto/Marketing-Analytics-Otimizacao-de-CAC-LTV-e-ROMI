import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats as st

visit_logs = pd.read_csv('dataframes/visits_log_us.csv', dtype={'Device': 'category', 'Source Id': 'category'}, parse_dates=['Start Ts', 'End Ts'])
costs = pd.read_csv('dataframes/costs_us.csv', parse_dates=['dt'])
orders_log = pd.read_csv('dataframes/orders_log_us.csv', parse_dates=['Buy Ts'])

visit_logs.columns = visit_logs.columns.str.lower().str.replace(' ', '_')
costs.columns = costs.columns.str.lower().str.replace(' ', '_')
orders_log.columns = orders_log.columns.str.lower().str.replace(' ', '_')

visit_logs.info(memory_usage='deep')
#costs.info(memory_usage='deep')
#orders_log.info(memory_usage='deep')

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


## Voltar para conferir
acessos_por_dia = visit_logs.groupby(visit_logs['start_ts'].dt.date)['uid'].count()
plt.figure(figsize=(12, 6))
sns.lineplot(x=acessos_por_dia.index, y=acessos_por_dia.values)
plt.title('Número de Acessos por Dia')
plt.xlabel('Data')
plt.ylabel('Número de Acessos')
plt.xticks(rotation=45)
plt.savefig('acessos_por_dia.png')
plt.close()

duracao_visitas = (visit_logs['end_ts'] - visit_logs['start_ts']).dt.total_seconds() / 60
plt.figure(figsize=(12, 6))
sns.histplot(duracao_visitas, bins=70, kde=True)
plt.title('Duração das Visitas (em minutos)')
plt.xlabel('Duração (minutos)')
plt.ylabel('Frequência')
plt.savefig('duracao_visitas.png')
plt.close()

return_rate = visit_logs.groupby(visit_logs['start_ts'].dt.date)['uid'].nunique() / visit_logs.groupby(visit_logs['start_ts'].dt.date)['uid'].count()
print(return_rate)

