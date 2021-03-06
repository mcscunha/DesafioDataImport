#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Arquivo contendo funcoes e metodos para manipulacao geral

@author:    MuriloCunha
@email:     mcscunha@yahoo.com.br
@criacao:   13/04/2019
"""


from os import path


def verificarExistenciaArquivo(strArquivo):
    resp = True
    if not path.exists(str(strArquivo)):
        resp = False
    return resp


def corrigirTelefone(strTelefone):
    '''
    Correcao nos telefones passados. 
    Mascara: +55DDDNumerotelefone
    Formato final: +551699112233
    '''
    for carac in ('(', ')', ' ', '-'):
        strTelefone = strTelefone.replace(carac, '')
    if len(strTelefone) < 12:
        if len(strTelefone) > 0:
            telefone = '+55{}{}'.format(strTelefone[:2], strTelefone[2:])
        else:
            telefone = ''
    else:
        telefone = '+{}'.format(strTelefone[:])
    
    return telefone
    

def corrigirValor(strValor):
    '''
        Correcao dos numeros floats passados como STRING para a funcao, devolvendo
    como uma STRING formatada com duas casas decimais e ponto como separador
        Elimina alguns caracteres literais invalidos, troca virgula por ponto e
    formata com duas casas decimais
        Formato Final: "250.00"
    '''
    for carac in ('R$', '-'):
        strValor = strValor.replace(carac, '')
        
    valor = strValor.replace(',', '.')
    return '{:.2f}'.format(float(valor) if valor != '' else 0)


def calcularValorTotalComDesconto(strValor, strDesconto):
    '''
    Calcula a coluna Valor_Total_Com_Desconto
    Formato Final: Valor_Total * (1 - (Desconto/100))
    '''
    if strDesconto == '':
        strDesconto = 0
    else:
        strDesconto = corrigirValor(strDesconto)
    return '{:.2f}'.format(float(strValor) * (1 - (float(strDesconto)/100)))
    