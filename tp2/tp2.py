import ply.lex as lex

tokens = ['PA','PF','VIRG','ID','GK','LAT','CEN','MED','EXT','PL','NOME','POSICOES']

t_PA   = r'\['
t_PF   = r'\]'
t_VIRG = r','
t_ID   = r'[A-Za-z]+'
#t_GK   = r'GK'
#t_LAT  = r'LAT'
#t_CEN  = r'CEN'
#t_MED  = r'MED'
#t_EXT  = r'EXT'
#t_PL   = r'PL'
#t_NOME = r'Nome\:'
#t_POSICOES = r'Posicoes\:'

def t_NOME(t):
    r'Nome\:'
    return t

def t_POSICOES(t):
    r'Posicoes\:'
    return t

def t_GK(t):
    r'GK'
    return t

def t_LAT(t):
    r'LAT'
    return t

def t_CEN(t):
    r'CEN'
    return t

def t_MED(t):
    r'MED'
    return t

def t_EXT(t):
    r'EXT'
    return t
    
def t_PL(t):
    r'PL'
    return t   

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t\r'

# Error handling rule
def t_error(t):
    print("Erro léxico no token '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()




#####################################################################################################################




# ideias: contar nº de jogadores do plantel
#         contar quantos jogadores cada posição tem
#         contar quantas posições cada jogador pode fazer
            
# G = {T,N,P,S}
# T = {'[', ']', ',', 'Nome:', 'Posicoes:', 'id', 'GK', 'LAT', 'CEN', 'MED', 'EXT', 'PL'}
# N = {Plantel, Jogadores, Jogador, Cont1, Nome, Posicoes, Posicao, Cont2}
# S = Plantel
# P = {p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16}

# def p_grammar(p):                                                 LOOKAHEADS
#  p1    Z         : Plantel '$'                                        {'['}
#  p2    Plantel   : '[' Jogadores ']'                                  {'['}
#  p3    Jogadores : Jogador Cont1                                      {"Nome: "}
#  p4    Cont1     : ',' Jogador Cont1                                  {','}
#  p5              | ϵ                                                  {']'}
#  p6    Jogador   : "Nome: " Nome "Posicoes: " '[' Posicoes ']'        {"Nome: "}
#  p7    Nome      : id                                                 {id}
#  p8    Posicoes  : Posicao Cont2                                      {GK,LAT,CEN,MED,EXT,PL}
#  p9    Cont2     : ',' Posicao Cont2                                  {','}
# p10              | ϵ                                                  {']'}
# p11    Posicao   : GK                                                 {GK}
# p12              | LAT                                                {LAT}
# p13              | CEN                                                {CEN}
# p14              | MED                                                {MED}
# p15              | EXT                                                {EXT}
# p16              | PL                                                 {PL}

#    estado     '['     "Nome: "     ','     ']'     id     GK     LAT     CEN     MED     EXT     PL
# -------------------------------------------------------------------------------------------------------
#         Z      p1                                                                                      
#   Plantel      p2                                                                                      
# Jogadores               p3                                                                             
#     Cont1                          p4      p5                                                          
#   Jogador               p6                                                                             
#      Nome                                          p7                                                  
#  Posicoes                                                 p9     p9      p9      p9      p9      p9   
#     Cont2                          p9      p10                                                         
#   Posicao                                                 p11    p12     p13     p14     p15     p16   
# -------------------------------------------------------------------------------------------------------

prox_simb = ('Erro', '', 0, 0)

def parserError(simb):
    print("Erro Sintático: ", simb)

def rec_term(simb):
    global prox_simb
    print("term:",prox_simb.value)
    if prox_simb.type == simb:
        v_term = prox_simb.value
        prox_simb = lexer.token()
    else:
        parserError(prox_simb)
        v_term = 'Erro Léxico'
    return v_term

def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    rec_Plantel()
    print("That's the end...")

def rec_Plantel():
    rec_term('PA') 
    rec_Jogadores()
    rec_term('PF')
    # print("Reconheci p2: Plantel -> '[' Jogadores ']'")
    
def rec_Jogadores():
    rec_Jogador()
    rec_Cont1()
    # print("Reconheci p3: Jogadores -> Jogador Cont1")

def rec_Cont1():
    global prox_simb
    if prox_simb.type == 'VIRG':
            rec_term('VIRG')
            rec_Jogador()
            rec_Cont1()
            # print("Reconheci p4: Cont1 -> ',' Jogador Cont1")
    elif prox_simb.type == 'PF':
        # print("Reconheci p5: Cont1 -> ")
        pass
    else:
        parserError(prox_simb)

def rec_Jogador():
    rec_term('NOME')
    rec_Nome()
    rec_term('POSICOES')
    rec_term('PA')
    rec_Posicoes()
    rec_term('PF')
    # print("Reconheci p6: Jogador -> 'Nome: ' Nome 'Posicoes: ' '[' Posicoes ']'")

def rec_Nome():
    rec_term('ID')
    # print("Reconheci p7: Nome -> id")

def rec_Posicoes():
    rec_Posicao()
    rec_Cont2()
    # print("Reconheci p8: Posicoes -> Posicao Cont2")

def rec_Cont2():
    global prox_simb
    if prox_simb.type == 'VIRG':
        rec_term('VIRG')
        rec_Posicao()
        rec_Cont2()
        # print("Reconheci p9: Cont2 -> ',' Posicao Cont2")
    elif prox_simb.type == 'PF':
        # print("Reconheci p10: Cont2 -> ")
        pass
    else: parserError(prox_simb)

def rec_Posicao():
    global prox_simb
    if prox_simb.type == 'GK':
        rec_term('GK')
        # print("Reconheci p11: Posicao -> GK")
    elif prox_simb.type == 'LAT':
        rec_term('LAT')
        # print("Reconheci p12: Posicao -> LAT")
    elif prox_simb.type == 'CEN':
        rec_term('CEN')
        # print("Reconheci p13: Posicao -> CEN")
    elif prox_simb.type == 'MED':
        rec_term('MED')
        # print("Reconheci p14: Posicao -> MED")
    elif prox_simb.type == 'EXT':
        rec_term('EXT')
        # print("Reconheci p15: Posicao -> EXT")
    elif prox_simb.type == 'PL':
        rec_term('PL')
        # print("Reconheci p16: Posicao -> PL")
    else: parserError(prox_simb)

#linha = input("Introduza uma frase válida: ")
# Teste do tokenizer
# lexer.input(linha)
# for tok in lexer:
#     print(tok)
#rec_Parser(linha)

import sys
programa = sys.stdin.read()
rec_Parser(programa)

## usar comando: cat teste.txt | python3 tp2.py