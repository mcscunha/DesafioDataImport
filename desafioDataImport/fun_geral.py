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
        telefone = '+55{}{}'.format(strTelefone[:2],
                      strTelefone[2:]) if len(strTelefone) > 0 else ''
    else:
        telefone = '+{}'.format(strTelefone[:])
    
    return telefone
    

def corrigirValor(strValor):
    '''
    Correcao da coluna VALOR - Formatado como dinheiro
    Formato Final: 250.00
    '''
    for carac in ('R$',):
        strValor = strValor.replace(carac, '')
    valor = strValor.replace(',', '.')
    return '{:.2f}'.format(float(valor))


def calcularValorTotalComDesconto(strValor, strDesconto):
    '''
    Adicao da coluna Valor Total Com Desconto
    Formato Final: Valor_Total * (1 - (Desconto/100))
    '''
    strDesconto = strDesconto.replace('-', '0')
    strDesconto = strDesconto.replace('', '0')
    valorTotalDesc = float(strValor) * (1 - (float(strDesconto)/100))
    return '{:.2f}'.format(valorTotalDesc)
    