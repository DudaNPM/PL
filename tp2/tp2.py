import ply.yacc as yacc
from grammarTP2 import tokens
import ply.lex as lex

# ideias: contar nº de jogadores do plantel
#         contar quantos jogadores cada posição tem
#         contar quantas posições cada jogador pode fazer

# def p_grammar(p):
#     Z         : Plantel '$'
#     Plantel   : '[' Jogadores ']'
#     Jogadores : Jogadores ',' Jogador
#               | Jogador
#     Jogador   : "Nome: " Nome "Posições: " '[' Posições ']'
#     Nome      : id
#     Posições  : Posições ',' Posição
#               | Posição
#     Posição   : GK | LAT | CEN | MED | EXT | PL
#              

# [Nome: Ricardo Posições: [MED,EXT], Nome: Miguel Posições: [EXT,PL], Nome: Filipe Posições: [PL]]

prox_simb = ('Erro', '', 0, 0)

def parserErro(simb):
    print("Erro: ", simb)

def rec_term(simb):
    global prox_simb
    if prox_simb.type == simb:
        prox_simb = lex.token()
    else: parserErro(prox_simb)

parser = yacc.yacc()
