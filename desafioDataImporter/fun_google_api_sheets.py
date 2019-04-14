#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
        Arquivo contendo funcoes e metodos para manipulacao de SHEETS
    remotamente através da biblioteca do Google

@author:    MuriloCunha
@email:     mcscunha@yahoo.com.br
@criacao:   13/04/2019
"""
import pickle
from os import path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


class SpreadSheetsGoogle():
    
    def __init__(self,
                 strScopo,
                 strArqToken,
                 strArqCredentials
                 ):
        '''
            Construtor da classe
        '''
        self.strScopo = strScopo
        self.strArqToken = strArqToken
        self.strArqCredentials = strArqCredentials
        
        
    def logarContaGoogleDocs(self):
        """
            Logar na conta Google Docs.
            Se for a primeira vez que este sistema está executando 
        (sem o arquivo token.pickle), o navegador abrirá a pagina para escolha do
        usuário do Google para validar as credenciais.
            Nas proximas vezes E com o arquivo token.pickle presente na aplicacao,
        nao será mais perguntado sobre permissoes, usando as permissoes 
        anteriormente concedidas
        """
        creds = None
        
        # Procurar arquivo "pickle" para validacao de credenciais (arquivo json)
        if path.exists(self.strArqToken):
            with open(self.strArqToken, 'rb') as token:
                creds = pickle.load(token)
        
        # Se não encontrar o arquivo, valide as credenciais 
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                        self.strArqCredentials, self.strScopo)
                creds = flow.run_local_server()
            
            # Gravar a credencial para a proxima execucao
            with open(self.strArqToken, 'wb') as token:
                pickle.dump(creds, token)
    
        return creds
    
    
    def obterPlanilhaGoogleDocs(self,
                                objCredentials,
                                strSpreadSheetID,
                                strRange
                                ):
        '''
            Tendo uma credencial valida, retorna um objeto sheet com um range de
        celulas (passados nos parametros).
            Cada objeto retornado contem um range definido ou uma planilha inteira,
        mas somente uma planilha, nao a pasta de trabalho inteira
        '''
        service = build('sheets', 'v4', credentials=objCredentials)
        
        # Chama a API do Google para acessar uma pasta de trabalho do tipo sheets
        sheet = service.spreadsheets()
        
        # Retorna o objeto sheet com o range especificado
        try:
            return sheet.values().get(spreadsheetId=strSpreadSheetID,
                                      range=strRange).execute()
        except:
            print('Erro ao acessar documento, talvez o ID seja incorreto')
            return None
    
    
    def obterCelulasDaPlanilha(self, planPlanilhaGoogleDocs):
        '''
            Retorna o conteudo das celulas do objeto planilha como uma
            LISTA DE LISTA (de strings)
        '''
        return planPlanilhaGoogleDocs.get('values', [])