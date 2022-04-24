import ply.yacc as yacc
from grammarTP2 import tokens
import ply.lex as lex

# ideias: contar nº de jogadores do plantel
#         contar quantos jogadores cada posição tem
#         contar quantas posições cada jogador pode fazer
            
# def p_grammar(p):
#     Z         : Plantel '$'
#     Plantel   : '[' Jogadores ']'
#     Jogadores : Jogador Cont1
#     Cont1     : ',' Jogador Con1
#               |
#     Jogador   : "Nome: " Nome "Posições: " '[' Posições ']'
#     Nome      : id
#     Posições  : Posição Cont2
#     Cont2     : ',' Posição Cont2
#               |   
#     Posição   : GK | LAT | CEN | MED | EXT | PL

# LA(p1) = {'['}
# LA(p2) = {"Nome: "}
# LA(p3) = {','}
# LA(p4) = {']'}
# LA(p5) = {"Nome: "}
# LA(p6) = {id}
# LA(p7) = {GK | LAT | CEN | MED | EXT | PL}
# LA(p8) = {','}
# LA(p9) = {']'}
# LA(p10) = {GK | LAT | CEN | MED | EXT | PL}

# [Nome: Ricardo Posições: [MED,EXT], Nome: Miguel Posições: [EXT,PL], Nome: Filipe Posições: [PL]]

prox_simb = ('Erro', '', 0, 0)

lexer = lex.lex()

def parserErro(simb):
    print("Erro: ", simb)

def rec_term(simb):
    global prox_simb
    if prox_simb.type == simb:
        prox_simb = lex.token()
    else: parserErro(prox_simb)

def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    rec_Plantel()

def rec_Plantel():
    rec_term('PA') 
    rec_Jogadores()
    rec_term('PF')
    
def rec_Jogadores():
    rec_Jogador()
    rec_Cont1()

def rec_Cont1():
    global prox_simb
    if prox_simb.type == 'VIRG':
        rec_term('VIRG')
        rec_Jogador()
        rec_Cont1()
    elif prox_simb.type == 'PF':
        pass
    else: parserErro(prox_simb)

def rec_Jogador():
    rec_term('NOME')
    rec_Nome()
    rec_term('POSICOES')
    rec_term('PA')
    rec_Posicoes()
    rec_term('PF')

def rec_Nome():
    rec_term('ID')

def rec_Posicoes():
    rec_Posicao()
    rec_Cont2()

def rec_Cont2():
    global prox_simb
    if prox_simb.type == 'VIRG':
        rec_Posicao()
        rec_Cont2()
    elif prox_simb.type == 'PF':
        pass
    else: parserErro(prox_simb)

def rec_Posicao():
    global prox_simb
    if prox_simb.type == 'GK':
        rec_term('GK')
    elif prox_simb.type == 'LAT':
        rec_term('LAT')
    elif prox_simb.type == 'CEN':
        rec_term('CEN')
    elif prox_simb.type == 'MED':
        rec_term('MED')
    elif prox_simb.type == 'EXT':
        rec_term('EXT')
    elif prox_simb.type == 'PL':
        rec_term('PL')
    else: parserErro(prox_simb)

parser = yacc.yacc()
