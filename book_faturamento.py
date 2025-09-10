import pandas as pd

def consolidar_planilhas(arquivo1, arquivo2, arquivo3, arquivo_saida="consolidacao.xlsx"):
    
    # Carregar as planilhas
    df_cadastrais = pd.read_excel(arquivo1)
    df_ferias = pd.read_excel(arquivo2)
    df_demitidos = pd.read_excel(arquivo3)

    # Padronizar nomes para maiúsculas
    df_cadastrais['Nome'] = df_cadastrais['Nome'].str.upper()
    df_ferias['Profissional'] = df_ferias['Profissional'].str.upper()
    df_demitidos['Nome'] = df_demitidos['Nome'].str.upper()

    # Mesclar os dados
    df_consolidado = (
        df_cadastrais
        .merge(
            df_ferias[['Profissional', 'Primeiro dia', 'Ultimo dia']],
            left_on='Nome', right_on='Profissional',
            how='left'
        )
        .merge(
            df_demitidos[['Nome', 'Data de Situação']],
            on='Nome',
            how='left'
        )
    )

    # Remover a coluna duplicada 'Profissional' se não precisar dela
    df_consolidado = df_consolidado.drop(columns=['Profissional'])

    # Criar a estrutura da planilha final
    df_final = pd.DataFrame()

    # Preencher colunas consolidadas
    df_final['QTDE DE EMPREGADOS'] = range(1, len(df_consolidado) + 1)
    df_final['MATRÍCULA'] = df_consolidado['Matrícula']
    df_final['NOME COMPLETO DO EMPREGADOR'] = df_consolidado['Nome']
    df_final['Nº CPF'] = df_consolidado['Número de CPF']
    df_final['ADMISSÃO (dd.mm.aaaa)'] = pd.to_datetime(
        df_consolidado['Data de Admissão'], errors="coerce"
    ).dt.strftime('%d.%m.%Y')
    df_final['FUNÇÃO'] = df_consolidado['Nome Cargo']
    df_final['PREFIXO'] = ''
    df_final['SB'] = ''
    df_final['LOCAL DA PRESTAÇÃO DO SERVIÇO'] = df_consolidado['Nome Local Trab.']
    df_final['UF DE ATENDIMENTO'] = 'DF'

    # Extrair horários
    horarios = df_consolidado['Desc. Horário'].astype(str).str.findall(r'\b\d{1,2}:\d{2}\b')
    df_final['HORÁRIO DA JORNADA (entrada)'] = horarios.apply(
        lambda x: min(x, key=lambda t: (int(t.split(':')[0]), int(t.split(':')[1]))) if x else ''
    )
    df_final['HORÁRIO DA JORNADA (saída)'] = horarios.apply(
        lambda x: max(x, key=lambda t: (int(t.split(':')[0]), int(t.split(':')[1]))) if x else ''
    )

    # Formatar valores monetários
    df_final['SALÁRIO (R$)'] = 'R$ ' + df_consolidado['Salário'].map('{:,.2f}'.format).str.replace('.', '#').str.replace(',', '.').str.replace('#', ',')
    df_final['AUXÍLIO TRANSPORTE (R$)'] = 'R$ ' + df_consolidado['Valor de Auxílio (Tipo de Modalidade)'].map('{:,.2f}'.format).str.replace('.', '#').str.replace(',', '.').str.replace('#', ',')
    df_final['AUXÍLIO ALIMENTAÇÃO (R$)'] = 'R$ ' + df_consolidado['Remuneração Variável (Benefícios)'].map('{:,.2f}'.format).str.replace('.', '#').str.replace(',', '.').str.replace('#', ',')

    df_final['SALDO DO FGTS (R$)'] = 'R$ '

    # Férias
    df_final['FÉRIAS (início)'] = pd.to_datetime(df_consolidado['Primeiro dia'], errors='coerce').dt.strftime('%d.%m.%Y')
    df_final['FÉRIAS (fim)'] = pd.to_datetime(df_consolidado['Ultimo dia'], errors='coerce').dt.strftime('%d.%m.%Y')

    df_final['FALTAS (quantidade)'] = ''
    df_final['HORAS EXTRAS (quantidade)'] = ''
    df_final['LOCAL DA HORA EXTRA'] = ''
    
    # Demissão
    df_final['DEMISSÃO (dd.mm.aaaa)'] = pd.to_datetime(df_consolidado['Data de Situação_y'], errors='coerce').dt.strftime('%d.%m.%Y')

    # Salvar planilha consolidada
    df_final.to_excel(arquivo_saida, index=False)
    return df_final
