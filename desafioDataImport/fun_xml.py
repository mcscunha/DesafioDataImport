#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Arquivo contendo funcoes e metodos para manipulacao de arquivos XML

    # ------------------------------------------------------------------------
    # CURIOSIDADE:
    # A forma abaixo COPIA os valores, ou seja, se alterar a variavel lstValor
    # essa alteracao não é percebida por lstLinha
    lstLinha.append(lstValor[:]) # Copiando os valores
    
    # Nessa outra forma, é passado um PONTEIRO de lstValor para lstLinha
    # apontando o conteudo de lstValor. Se houver alteracoes em lstValor,
    # essas mudancas serao passadas para lstLinha, ja que foi inserido em
    # lstLinha um apontamento para o conteudo de lstValor e nao o valor como
    # no caso acima.
    lstLinha.append(lstValor)     # Copiando a referencia de memoria da lista
    
    # ------------------------------------------------------------------------
    # CUIDADO: 
    # A ordem das linhas abaixo influencia no resultado
    # Nesta ordem, o Python cria uma OUTRA lista independente na memoria
    # e limpa o seu conteudo, com isso, os dados acima nao sao afetados,
    # ja que ele esta limpando o conteudo da variavel NOVA (recem criada)
    lstValor = []    # Cria uma lista nova na memoria
    lstValor.clear() # Apaga o conteudo da lista, utilizando a MESMA lista

    # Invertendo a situacao, a lista lstLinha é afetada, pois o conteudo da
    # lista foi apagado e em seguida criado uma nova lista independente
    lstValor.clear() # Apaga o conteudo da lista, utilizando a MESMA lista
    lstValor = []    # Cria uma lista nova na memoria
    # ------------------------------------------------------------------------

@author:    MuriloCunha
@email:     mcscunha@yahoo.com.br
@criacao:   13/04/2019
"""


import xml.etree.ElementTree as ET


class ArquivoXml():
    '''
        Classe para manipulacao de arquivos XML
    '''
    def __init__(self, strArqXml):
        self.strArqXml = strArqXml
        

    def carregarXml(self):
        tree = ET.parse(self.strArqXml)
        return tree.getroot()


    def obterConteudoXml(self, xmlNoRaiz, strNoContendoDados):
        # Pegar o cabecalho dos campos
        lstLinha = [ [cab.tag for cab in xmlNoRaiz.find(strNoContendoDados)] ]
        # =====================================================================
        #         '''
        #             Poderia usar a forma abaixo para pegar todos os valores 
        #         do XML e guardar em uma lista, mas nessa forma nao separa em
        #         "linhas" para melhor controle dos dados no futuro
        #         '''
        #         lstTodosDados = [dado.find(tagname).text 
        #                          for dado in root.findall('record') 
        #                          for tagname in ( [cab.tag 
        #                               for cab in xmlNoRaiz.find(
        #                                    strNoContendoDados) ]
        #                              )
        #                          ]
        #         lstValor = []
        # =====================================================================
        lstValor = []
        for dado in xmlNoRaiz.findall(strNoContendoDados):
            lstValor.append(dado.find('user_id').text)
            lstValor.append(dado.find('name').text)
            lstValor.append(dado.find('email_user').text)
            lstValor.append(dado.find('phone').text)
            lstValor.append(dado.find('buy_value').text)
            lstLinha.append(lstValor[:])
            lstValor.clear()
        return list(lstLinha)
        