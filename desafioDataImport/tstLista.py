#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 22:06:50 2019

@author: mcunha
"""


import sys
import csv
from pprint import pprint
import xml.etree.ElementTree as ET


tree = ET.parse('dataApr-1-2019 2.xml')
root = tree.getroot()

LinhasXml = []
cabecalho = root.find('record')
lstCabecalho = [cab.tag for cab in root.find('record')]
print(lstCabecalho)

lstDados = [dado.find(tagname).text for dado in root.findall('record') for tagname in lstCabecalho]
print(lstDados)

sys.exit(0)

'''
lstLinha.append(xmlNoRaiz.find(strNoContendoDados)
for dado in xmlNoRaiz.findall(strNoContendoDados):
    lstValor.append(dado.find('user_id').text)
    lstValor.append(dado.find('name').text)
    lstValor.append(dado.find('email_user').text)
    lstValor.append(dado.find('phone').text)
    lstValor.append(dado.find('buy_value').text)
    lstLinha.append(lstValor[:])
    lstValor.clear()
return list(lstLinha)
'''


linhasCsv = []
with open('dataApr-1-2019.csv', mode='r') as csv_file:
    linCsv = csv.reader(csv_file, delimiter=';')
    
    linhasCsv.append(linCsv)
    
    for linha in linhasCsv:
        print(linha)
