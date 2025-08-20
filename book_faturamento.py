# %%
import pandas as pd
from datetime import datetime
import re

# %%
# Carregar as planilhas
df_cadastrais = pd.read_excel('/content/PLANILHAS/dados_cadastrais.xlsx')
df_ferias = pd.read_excel('/content/PLANILHAS/ferias.xlsx')
df_demitidos = pd.read_excel('/content/PLANILHAS/demitidos.xlsx')

# %%
# Padronizar nomes para maiúsculas em todas as planilhas
df_cadastrais['Nome'] = df_cadastrais['Nome'].str.upper()
df_ferias['nome'] = df_ferias['nome'].str.upper()
df_demitidos['Nome'] = df_demitidos['Nome'].str.upper()

# %%
# Renomear colunas para padronização
df_ferias = df_ferias.rename(columns={'nome': 'Nome'})
df_demitidos = df_demitidos.rename(columns={'Nome': 'Nome'})

# %%
# Mesclar os dados das planilhas
df_consolidado = df_cadastrais.merge(
    df_ferias[['Nome', 'INICIO', 'FIM']],
    on='Nome',
    how='left'
).merge(
    df_demitidos[['Nome', 'Data de Situação']],
    on='Nome',
    how='left'
)

# %%
# Criar a estrutura da planilha final
df_final = pd.DataFrame()

# Preencher as colunas consolidadas
df_final['QTDE DE EMPREGADOS'] = range(1, len(df_consolidado) + 1)
df_final['MATRÍCULA'] = df_consolidado['Matrícula']
df_final['NOME COMPLETO DO EMPREGADOR'] = df_consolidado['Nome']
df_final['Nº CPF'] = df_consolidado['Número de CPF']
df_final['ADMISSÃO (dd.mm.aaaa)'] = pd.to_datetime(df_consolidado['Data de Admissão']).dt.strftime('%d.%m.%Y')
df_final['FUNÇÃO'] = df_consolidado['Nome Cargo']
df_final['PREFIXO'] = ''
df_final['SB'] = ''
df_final['LOCAL DA PRESTAÇÃO DO SERVIÇO'] = df_consolidado['Nome Local Trab.']
df_final['UF DE ATENDIMENTO'] = 'DF'

# Extrair todos os horários da coluna 'Desc. Horário'
horarios = df_consolidado['Desc. Horário'].str.findall(r'\b\d{1,2}:\d{2}\b')

# Calcula o menor horário da jornada
df_final['HORÁRIO DA JORNADA (entrada)'] = horarios.apply(
    lambda x: min(x, key=lambda t: (int(t.split(':')[0]), int(t.split(':')[1]))) if x else ''
)

#Calcula o maior horário da jornada
df_final['HORÁRIO DA JORNADA (saída)'] = horarios.apply(
    lambda x: max(x, key=lambda t: (int(t.split(':')[0]), int(t.split(':')[1]))) if x else ''
)

df_final['SALÁRIO (R$)'] = 'R$ ' + df_consolidado['Salário'].map('{:,.2f}'.format).str.replace('.', '#').str.replace(',', '.').str.replace('#', ',')
df_final['AUXÍLIO TRANSPORTE (R$)'] = 'R$ ' + df_consolidado['Valor de Auxílio (Tipo de Modalidade)'].map('{:,.2f}'.format).str.replace('.', '#').str.replace(',', '.').str.replace('#', ',')
df_final['AUXÍLIO ALIMENTAÇÃO (R$)'] = 'R$ ' + df_consolidado['Remuneração Variável (Benefícios)'].map('{:,.2f}'.format).str.replace('.', '#').str.replace(',', '.').str.replace('#', ',')
df_final['SALDO DO FGTS (R$)'] = 'R$ '

# Férias
df_final['FÉRIAS (início)'] = pd.to_datetime(df_consolidado['INICIO'], errors='coerce').dt.strftime('%d.%m.%Y')
df_final['FÉRIAS (fim)'] = pd.to_datetime(df_consolidado['FIM'], errors='coerce').dt.strftime('%d.%m.%Y')

df_final['FALTAS (quantidade)'] = ''
df_final['HORAS EXTRAS (quantidade)'] = ''
df_final['LOCAL DA HORA EXTRA'] = ''

# Formatar data de demissão
df_final['DEMISSÃO (dd.mm.aaaa)'] = pd.to_datetime(df_consolidado['Data de Situação_y'], errors='coerce').dt.strftime('%d.%m.%Y')


# %%
# Salvar a planilha consolidada
df_final.to_excel('/content/PLANILHAS/consolidacao.xlsx', index=False)
print(f"Planilha consolidada salva com sucesso!")


