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