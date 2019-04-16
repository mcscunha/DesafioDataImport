#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Arquivo contendo funcoes e metodos para manipulacao de arquivos CSV

@author:    MuriloCunha
@email:     mcscunha@yahoo.com.br
@criacao:   13/04/2019
"""


import csv


class ArquivoCsv():
    '''
        Classe para manipulacao de arquivos CSV
    '''
    def __init__(self, strArqCsv, strDelimitador):
        '''
            Construtor da classe
        '''
        self.strArqCsv = strArqCsv
        self.strDelimitador = strDelimitador
        
    
    def obterConteudoCsv(self):
        '''
            Acessar o arquivo CSV e disponibilizar o conteudo em uma LISTA
        '''
        with open(self.strArqCsv, mode='r') as csv_file:
            return list(csv.reader(csv_file, delimiter=self.strDelimitador))
