#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Arquivo principal da aplicacao.
    Desafio passado em 10/04/2019 pela iClinic para avaliacao de habilidades
    
    DESCRIÇÃO DO TESTE:
    - Imagine que você é responsável pelo setor de importação de dados, você 
        não deve de maneira nenhuma importar os dados direto no banco de 
        produção.
    - Deve ser criado uma camada de abstração a seu critério (SQL, XLS e etc),
        com os dados das 3 fontes. Nossa API irá consumir esses dados.
    
    Segue link do sheets:
    - https://docs.google.com/spreadsheets/d/1N6JFMIQR71HF5u5zkWthqbgpA8WYz_0ufDGadeJnhlo/edit#gid=0
    
    INSTRUÇÃO DO TESTE:
    - Quando os dados estivem em branco, importar em branco;
    - O telefone deve ser +55DDDNUMERO. Ex: (+5516981773421);
    - O Valor deve ser formatado como dinheiro (real). Ex: 999,00;
    - O valor_com_desconto deve ser calculado com o valor_total - desconto%;
    - Datas no formato TIMESTAMP;
    - Relacionar a tabela dependentes com usuários;
    
    O QUE ESTÁ SENDO AVALIADO:
    - Chamada de Apis (chamar api do google sheets);
    - Analise, leitura e manipulação de dados;
    - Cálculos;
    - Git;
    - Reaproveitamento de código;
    - Performance;
    - Clean Code;
    - Capacidade de abstração;
    
    Estrutura de saída usuários:
    id, nome, email, telefone, valor_total, valor_com_desconto;
    
    Estrutura de saída dependentes:
    id, usuario_id, dependente_de_id; (edited)    
    
    -- FIM --        
    
    Esta aplicacao acessa SpreadSheet do GoogleDocs remotamente

@author:    MuriloCunha
@email:     mcscunha@yahoo.com.br
@criacao:   13/04/2019
"""

import os
import sys
import csv
from datetime import datetime
from pprint import pprint
from fun_google_api_sheets import SpreadSheetsGoogle
from fun_csv import ArquivoCsv
from fun_xml import ArquivoXml
from fun_geral import verificarExistenciaArquivo, corrigirTelefone
from fun_geral import corrigirValor, calcularValorTotalComDesconto

# Se modificar o SCOPO, deve-se deletar o arquivo token.pickle
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# https://docs.google.com/spreadsheets/d/1N6JFMIQR71HF5u5zkWthqbgpA8WYz_0ufDGadeJnhlo/edit#gid=0
SPREADSHEET_ID = '1N6JFMIQR71HF5u5zkWthqbgpA8WYz_0ufDGadeJnhlo'
RANGE = 'usuarios!A1:F100'
ARQCSV = 'dataApr-1-2019.csv'
ARQXML = 'dataApr-1-2019 2.xml'


def recuperarConteudoSpreadSheet(strIDSpreadSheet, strRangeSheet):
    '''
        Acessar o conteudo do sheet no GoogleDocs e disponibilizar na memoria
    '''
    lstCelulas = None

    # Acessa planilha no GoogleDocs
    spreadSheet = SpreadSheetsGoogle(SCOPES,
                                     r'../token.pickle',
                                     r'../credentials.json'
                                     )
    
    # Valida as credenciais
    creds = spreadSheet.logarContaGoogleDocs()

    # Pega os dados da planilha definida nos parametros
    planilha = spreadSheet.obterPlanilhaGoogleDocs(creds,
                                                   strIDSpreadSheet,
                                                   strRangeSheet
                                                   )
    
    # Pega o conteudo da planilha e guarda em uma lista de lista
    if planilha:
        lstCelulas = spreadSheet.obterCelulasDaPlanilha(planilha)

    # Se encontrar uma planilha vazia, informe ao usuario
    if not lstCelulas:
        print('Nenhuma informação encontrada.')

    # Retorne o resultado do acesso
    return lstCelulas
    
    
def exibirConteudoSpreadSheet():
    lstLinhasSheet = recuperarConteudoSpreadSheet(SPREADSHEET_ID, RANGE)
    
    for row in lstLinhasSheet:
        print('{0}'.format(row))


def recuperarConteudoCsv(strArquivoCsv):
    '''
        Acessar o conteudo do arquivo CSV e enviar para memoria
    '''
    lstLinhasCsv = None

    if verificarExistenciaArquivo(strArquivoCsv):
        arqCsv = ArquivoCsv(strArquivoCsv, ';')
        lstLinhasCsv = arqCsv.obterConteudoCsv()
    else:
        print('Arquivo não encontrado OU com erro ao abrir, talvez encoding')
    
    return lstLinhasCsv

def exibirConteudoCSV():
    '''
        Exibir o conteudo do arquivo CSV na tela
    '''
    lstLinhas = recuperarConteudoCsv(ARQCSV)
    if lstLinhas:
        line_count = 0
        for row in lstLinhas:
            if line_count == 0:
                print('Colunas encontradas:\n\t{}'.format(row))
                print('Dados...')
            else:
                print('\t{}'.format(row))
            line_count += 1
        print('Linhas processadas: {}'.format(line_count))


def recuperarConteudoXml(strArquivoXml, strNoComDados):
    '''
        Acessar o conteudo do arquivo XML e enviar para memoria
    '''
    lstLinhasXml = None

    if verificarExistenciaArquivo(strArquivoXml):
        arqXml = ArquivoXml(strArquivoXml)  # Criar classe
        xmlNoRaiz = arqXml.carregarXml()    # Abrir o arquivo
        lstLinhasXml = arqXml.obterConteudoXml(xmlNoRaiz, strNoComDados) # Por dados na memoria
    else:
        print('Arquivo XML não encontrado.')

    return lstLinhasXml
    
    
def exibirConteudoXML():
    '''
        Exibir o conteudo do XML em linhas, mais facil de conferir o conteudo
    '''
    lstLinhas = recuperarConteudoXml(ARQXML, 'record')
    pprint(lstLinhas)


def alterarArquivoSpreadSheet():
    '''
        Para trocar o ID que o sistema vai acessar, assim, não será usado
    apenas para um documento
    '''
    global SPREADSHEET_ID
    arq = input('Qual a ID referente ao documento no GoogleDocs?\n')
    SPREADSHEET_ID = arq
    print('ID alterado com sucesso')


def alterarArquivoCsv():
    '''
        Para trocar o arquivo CSV que o sistema vai acessar, assim, será usado
    para mais documentos
    '''
    global ARQCSV
    arq = input('Qual o caminho + nome do arquivo CSV fonte de dados?\n')
    ARQCSV = arq
    print('Fonte de dados CSV alterado com sucesso')
    


def alterarArquivoXml():
    '''
        Para trocar o arquivo XML que o sistema vai acessar, assim, será usado
    para mais documentos
    '''
    global ARQXML
    arq = input('Qual o caminho + nome do arquivo XML fonte de dados?\n')
    ARQXML = arq
    print('Fonte de dados XML alterado com sucesso')


def juntarTresArquivosEmCsv():
    from time import time
    reaTempoInicial = time()

    # Carregando os dados em memoria
    #
    '''
    lstLinhasSheetUsu = [ ['LIBERAR', 'CARREGAMENTO', 'DA', 'LISTA', 'CINCO', 'SEIS'],
                          ['AAA', 'BBB', 'CCC', 'DDD', '5', '10'] ]
    lstLinhasSheetDep = [ ['LIBERAR', 'CARREGAMENTO', 'DA', 'LISTA'],
                          ['111', '222', '333', '444', '555', ''] ]
    '''
    lstLinhasSheetUsu = recuperarConteudoSpreadSheet(SPREADSHEET_ID, RANGE)
    lstLinhasCsv = recuperarConteudoCsv(ARQCSV)
    lstLinhasXml = recuperarConteudoXml(ARQXML, 'record')
    RANGE_DEP = 'dependentes!A1:D18'
    lstLinhasSheetDep = recuperarConteudoSpreadSheet(SPREADSHEET_ID, RANGE_DEP)
    print('[1 / 7] - Fonte de dados iniciais carregados... OK')
    
    # Eliminar o cabecalho das colunas, este cabecalho será definido no fim
    #
    lstLinhasSheetUsu.pop(0)
    lstLinhasCsv.pop(0)
    lstLinhasXml.pop(0)
    lstLinhasSheetDep.pop(0)
    
    # Alterando os dados
    #  
    lstComValorTotal = []
    for idx, linha in enumerate(lstLinhasSheetUsu):
        lstLinhasSheetUsu[idx][3] = corrigirTelefone(linha[3])
        lstLinhasSheetUsu[idx][4] = corrigirValor(linha[4])
        # CURIOSIDADE
        #
        # a = 3.456    (a   = tipo float)
        # b = list(a)  (ERRO: Float object is not iterable)
        # b = [a]      (OK  : Neste caso, é dado um "APPEND" em uma lista 
        #                     vazia. Por isso a variavel VTCD abaixo é 
        #                     calculada separada e depois acrescentada dentro
        #                     de uma lista no APPEND)
        #                     
        vtcd = calcularValorTotalComDesconto(
                lstLinhasSheetUsu[idx][4], lstLinhasSheetUsu[idx][5])
        lstComValorTotal.append(linha + [vtcd])
    
    print('[2 / 7] - Correção dos dados da fonte Sheets... OK')
    
    for idx, linha in enumerate(lstLinhasCsv):
        lstLinhasCsv[idx][3] = corrigirTelefone(linha[3])
        vtcd = calcularValorTotalComDesconto(
                lstLinhasCsv[idx][4], lstLinhasCsv[idx][5])
        lstComValorTotal.append(linha + [vtcd])
    
    print('[3 / 7] - Correção dos dados da fonte CSV... OK')

    for idx, linha in enumerate(lstLinhasXml):
        lstLinhasXml[idx][3] = corrigirTelefone(linha[3])
        vtcd = calcularValorTotalComDesconto(lstLinhasXml[idx][4], '0')
        lstComValorTotal.append(linha + [0] + [vtcd])
                
    print('[4 / 7] - Correção dos dados da fonte XML... OK')

    for idx, linha in enumerate(lstLinhasSheetDep):
        if len(linha) == 4: 
            datahora = lstLinhasSheetDep[idx][3]
            datahora = datetime.strptime(datahora, '%d/%m/%Y %H:%M:%S')
            lstLinhasSheetDep[idx][3] = datetime.strftime(
                    datahora, '%d/%m/%Y %H:%M:%S')
        else:
            lstLinhasSheetDep[idx].append('')
                
    print('[5 / 7] - Correção dos dados da fonte Dependentes... OK')

    #
    # Resultado das 3 fontes acima:
    # -------------------------------------------------------------------------------------------------
    # ID        : 0        , 1       , 2           , 3           , 4            , 5       , 6
    # -------------------------------------------------------------------------------------------------
    # Sheet     : id       , nome    , email       , telefone    , valor        , desconto, valor_total
    # CSV       : client_id, username, email_client, phone_client, product_value, discount, valor_total
    # XML       : user_id  , name    , email_user  , phone       , buy_value    , 0       , valor_total
    # -------------------------------------------------------------------------------------------------
    # CSVsaida  : id       , nome    , email       , telefone    , valor_total  , valor_com_desconto
    # -------------------------------------------------------------------------------------------------
    lstComValorTotal.insert(0, ['id',
                                'nome',
                                'email',
                                'telefone',
                                'valor_total',
                                'COL_APAGAR',   # Apenas para facilitar abaixo
                                'valor_com_desconto'])
    lstLinhasSheetDep.insert(0, ['id',
                                 'usuario_id',
                                 'dependente_de_id',
                                 'data'])
    
    # Gravando os arquivos CSV
    #
    with open('usuarios.csv', 'w', encoding='UTF-8', newline='') as csv_file:
        file = csv.writer(csv_file, delimiter=';', quoting=csv.QUOTE_NONE)
        #file.writerows(lstComValorTotal)
        for linha in lstComValorTotal:
            linha.pop(5)
            file. writerows( [linha] )
    
    print('[6 / 7] - Gravação do arquivo de saida: ususarios.csv... OK')
    
    with open('dependentes.csv', 'w', encoding='UTF-8', newline='') as csv_file:
        file = csv.writer(csv_file, delimiter=';', quoting=csv.QUOTE_NONE)
        for linha in lstLinhasSheetDep:
            file.writerows( [linha] )
  
    print('[7 / 7] - Gravação do arquivo de saida: dependentes.csv... OK')

    reaTempoFinal = time()
    print('\nTempo total de processamento: {:.3f} segundos'.format(
            reaTempoFinal - reaTempoInicial))

def menu():
    # Limpar a tela nao importando o SO
    os.system('cls' if os.name == 'nt' else 'clear')

    print('DESAFIO iCLINIC - 10/04/2019 - MuriloCunha')
    print('\n')
    print('[ 1 ] Exibir o conteudo do SpreadSheet (GoogleDocs) ({})'.
          format(SPREADSHEET_ID))
    print('[ 2 ] Exibir o conteudo do arquivo CSV ({})'.format(ARQCSV))
    print('[ 3 ] Exibir o conteudo do arquivo XML ({})'.format(ARQXML))
    print('')
    print('[ 4 ] Definir arquivo SpreadSheet')
    print('[ 5 ] Definir arquivo CSV')
    print('[ 6 ] Definir arquivo XML')
    print('')
    print('[ 7 ] Consolidar info das três fontes em arquivo CSV')
    print('')
    print('[ 0 ] Sair do sistema')
    print('')

    op = int(input('Qual opção deseja executar?\n'))

    while True:
        if op == 0:
            break
        elif op == 1:
            exibirConteudoSpreadSheet()
        elif op == 2:
            exibirConteudoCSV()
        elif op == 3:
            exibirConteudoXML()
        elif op == 4:
            alterarArquivoSpreadSheet()
        elif op == 5:
            alterarArquivoCsv()
        elif op == 6:
            alterarArquivoXml()
        elif op == 7:
            juntarTresArquivosEmCsv()
        else:
            print("Por favor, somente numeros entre 0 e 7. Tente novamente\n")
        
        input('\nTecle [ENTER] para continuar...')
        menu()

    print('Encerrando o sistema... OK')
    # Usar o EXIT de SYS por causa de problemas com o console IPython
    sys.exit(0)


if __name__ == '__main__':
    menu()
