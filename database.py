import json
import os

ARQUIVO_BANCO = 'acervo.json'

def carregar_acervo():
    if not os.path.exists(ARQUIVO_BANCO):
        return {} 
    
    with open(ARQUIVO_BANCO, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

def salvar_acervo(dados):
    with open(ARQUIVO_BANCO, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
