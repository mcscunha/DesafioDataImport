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
import pprint

class ArquivoXml():
    '''
        Classe para manipulacao de arquivos XML
    '''
    def __init__(self, strArqXml):
        self.strArqXml = strArqXml
        

    def carregarXml(self):
        tree = ET.parse(self.strArqXml)
        return tree.getroot()


    def obterConteudoXml(self, xmlNoContendoDados, ):
        lstLinha = []
        lstValor = []
        for dado in xmlNoContendoDados.findall('record'):
            lstValor.append(dado.find('user_id').text)
            lstValor.append(dado.find('name').text)
            lstValor.append(dado.find('email_user').text)
            lstValor.append(dado.find('phone').text)
            lstValor.append(dado.find('buy_value').text)
            lstLinha.append(lstValor[:])
            lstValor.clear()
        
        
        
'''
        
# Testando arquivo XML
ARQXML = 'dataApr-1-2019 2.xml'
arqXml = ArquivoXml(ARQXML)
root = arqXml.carregarXml()

i = 0
print('Tag Root:', root.tag)
print('Atributo Root:', root.attrib)
print('Texto Root:', root.text)
print('Nos:',  )
root.
lstLinha = []
lstValor = []
vez = 0
for dado in root.findall('record'):
    lstValor.append(dado.find('user_id').text)
    lstValor.append(dado.find('name').text)
    lstValor.append(dado.find('email_user').text)
    lstValor.append(dado.find('phone').text)
    lstValor.append(dado.find('buy_value').text)
    lstLinha.append(lstValor[:])
    lstValor.clear()
pprint.pprint(lstLinha)        
'''

'''
lstLinha = []
lstValor = []
lstValores = [(x.tag, x.text) for x in root.iter() 
                        if (x.text != '\n\t\t') and (x.text != '\n\t')
                        ]
#print(lstValores)

for dado in lstValores:
    if (dado[0] == 'user_id') and (idx != 0):
        lstLinha.append(lstValor) 
        lstValor = []
    else:
        lstValor.append(dado)        

#for linha in lstLinha:
pprint.pprint(lstLinha)
'''

'''
for ch in root.iter():
    print('Tag Pai:', ch.tag)
    #print('Atributo Pai:', ch.attrib)
    print('Texto Pai:', ch.text)

    for gr in ch:
        print('Tag Filho:', gr.tag)
        print('Atributo Filho:', gr.attrib)
        print('Texto Filho:', gr.text)

    i += 1
    #print('Iteração: ', i)
    if i > 10:
        break
'''
