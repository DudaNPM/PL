import ply.yacc as yacc
import ply.lex as lex

tokens = ['PA','PF','VIRG','ID','GK','LAT','CEN','MED','EXT','PL','NOME','POSICOES']

t_ID   = r'[A-Za-z]+'
t_PA   = r'\['
t_PF   = r'\]'
t_VIRG = r','
t_GK   = r'GK'
t_CEN  = r'CEN'
t_MED  = r'MED'
t_EXT  = r'EXT'
t_PL   = r'PL'
t_NOME = r'Nome\:'
t_POSICOES = r'Posicoes\:'
 
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print('Caráter ilegal: ', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

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

# [Nome: Ricardo Posicoes: [MED,EXT], Nome: Miguel Posicoes: [EXT,PL], Nome: Filipe Posicoes: [PL]]

prox_simb = ('Erro', '', 0, 0)

def parserErro(simb):
    print("Erro: ", simb)

def rec_term(simb):
    global prox_simb
    print("term:",prox_simb.value)
    if prox_simb.type == simb:
        prox_simb = lex.token()
    else: parserErro(prox_simb)

def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    rec_Plantel()
    print("Acabei")

def rec_Plantel():
    rec_term('PA') 
    rec_Jogadores()
    rec_term('PF')
    
def rec_Jogadores():
    rec_Jogador()
    rec_Cont1()

def rec_Cont1():
    global prox_simb
    if prox_simb:
        if prox_simb.type == 'VIRG':
            rec_term('VIRG')
            rec_Jogador()
            rec_Cont1()
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
    if prox_simb:
        if prox_simb.type == 'VIRG':
            rec_Posicao()
            rec_Cont2()
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

linha = input("Introduza uma frase válida: ")

rec_Parser(linha)