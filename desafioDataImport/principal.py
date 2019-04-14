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
from pprint import pprint
from fun_google_api_sheets import SpreadSheetsGoogle
from fun_csv import ArquivoCsv
from fun_xml import ArquivoXml
from fun_geral import verificarExistenciaArquivo

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


def recuperarConteudoCsv():
    '''
        Acessar o conteudo do arquivo CSV e enviar para memoria
    '''
    lstLinhasCsv = None

    if verificarExistenciaArquivo(ArquivoCsv):
        arqCsv = ArquivoCsv(ARQCSV, ';')
        lstLinhasCsv = arqCsv.obterConteudoCsv()
    else:
        print('Arquivo não encontrado OU com erro ao abrir, talvez encoding')
    
    return lstLinhasCsv

def exibirConteudoCSV():
    '''
        Exibir o conteudo do arquivo CSV na tela
    '''
    lstLinhas = recuperarConteudoCsv()
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


def recuperarConteudoXml():
    '''
        Acessar o conteudo do arquivo XML e enviar para memoria
    '''
    lstLinhasXml = None

    if verificarExistenciaArquivo(ARQXML):
        arqXml = ArquivoXml(ARQXML)
        lstLinhasXml = arqXml.carregarXml()
    else:
        print('Arquivo XML não encontrado.')

    return lstLinhasXml
    
    
def exibirConteudoXML():
    '''
        Exibir o conteudo do XML em linhas, mais facil de conferir o conteudo
    '''
    lstLinhas = recuperarConteudoXml()
    if lstLinhas:
        lstLinha = []
        lstValor = []
        
        # Conhecendo a estrutura do arquivo XML...
        for dado in lstLinhas.findall('record'):
            lstValor.append(dado.find('user_id').text)
            lstValor.append(dado.find('name').text)
            lstValor.append(dado.find('email_user').text)
            lstValor.append(dado.find('phone').text)
            lstValor.append(dado.find('buy_value').text)
            
            lstLinha.append(lstValor[:])
            lstValor.clear()
        
        pprint(lstLinha)


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
    lstCsvResultado = []
    lstTotalComDesconto = ['valor_com_desconto']
    
    lstLinhasSheetUsu = recuperarConteudoSpreadSheet(SPREADSHEET_ID, RANGE)
    RANGE = 'dependentes!A1:D18'
    lstLinhasSheetDep = recuperarConteudoSpreadSheet(SPREADSHEET_ID, RANGE)
    
    for idx, linha in enumerate(lstLinhasSheetUsu):

        #
        # Correcao nos telefones da planilha do GoogleDocs
        #
        if idx > 0:   # ignorar a linha de cabecalho
            telefone = linha[3]
            for carac in ('(', ')', ' ', '-'):
                telefone = telefone.replace(carac, '')
            if len(telefone) < 12:
                lstLinhasSheetUsu[idx][3] = '+55{}{}'.format(telefone[:2],
                              telefone[2:]) if len(telefone) > 0 else ''
            else:
                lstLinhasSheetUsu[idx][3]= '+{}'.format(telefone[:])
        
            #
            # Correcao da coluna VALOR - Formatado como dinheiro
            #
            valor = linha[4]
            #for carac in ('R$',):
            valor = valor.replace('R$', '')
            valor = valor.replace(',', '.')
            lstLinhasSheetUsu[idx][4] = '{:.2f}'.format(float(valor))

            #
            # Adicao da coluna (Valor_Total - Desconto)
            #
            desconto = linha[5]
            desconto = desconto.replace('-', '0')
            valorTotalDesc = float(lstLinhasSheetUsu[idx][4]) * (1 - (float(desconto)/100))
            lstTotalComDesconto.append('{:.2f}'.format(valorTotalDesc))
            print('{:.2f}'.format(valorTotalDesc))
            

    #
    # Trabalhando na segunda aba (dependentes)
    #
    for idx, linha in enumerate(lstLinhasSheetDep):

        if idx > 0:   # ignorar a linha de cabecalho
            
        
        
    pprint(lstLinhasSheetUsu)
    


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
    print('[ 8 ] Consolidar info das três fontes em arquivo CSV')
    print('')
    print('[ 0 ] Sair do sistema')
    print('')

    try:
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
                print("Por favor, somente numeros entre 0 e 8. Tente novamente\n")
            
            input('\nTecle [ENTER] para continuar...')
            menu()


    except ValueError:
        print("Isso não é um número OU houve um erro na rotina chamada.\n")
        input('\n')
        menu()    
    

    print('Encerrando o sistema... OK')
    # Usar o EXIT de SYS por causa de problemas com o console IPython
    sys.exit(0)


if __name__ == '__main__':
    menu()
