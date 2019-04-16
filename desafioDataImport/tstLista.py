#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 22:06:50 2019

@author: mcunha
"""

import csv
from pprint import pprint

linhas = []
with open('dataApr-1-2019.csv', mode='r') as csv_file:
    linCsv = csv.reader(csv_file, delimiter=';')
    
    linhas.append(linCsv)
    
    for linha in linhas:
        print(linha)
