import ply.yacc as yacc
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
 
t_ignore = ' \t'

def t_NOME(t):
    r'Nome\: '
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
            
# G = {T,N,P,S}
# T = {'[', ']', ',', 'Nome:', 'Posicoes:', 'id', 'GK', 'LAT', 'CEN', 'MED', 'EXT', 'PL'}
# N = {Plantel, Jogadores, Jogador, Cont1, Nome, Posicoes, Posicao, Cont2}
# S = Plantel
# P = {p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16}

# def p_grammar(p):
#  p1    Z         : Plantel '$'
#  p2    Plantel   : '[' Jogadores ']'
#  p3    Jogadores : Jogador Cont1
#  p4    Cont1     : ',' Jogador Cont1
#  p5              |
#  p6    Jogador   : "Nome: " Nome "Posicoes: " '[' Posicoes ']'
#  p7    Nome      : id
#  p8    Posicoes  : Posicao Cont2
#  p9    Cont2     : ',' Posicao Cont2
# p10              |   
# p11    Posição   : GK
# p12              | LAT
# p13              | CEN
# p14              | MED
# p15              | EXT
# p16              | PL

# LA(p1) = {'['}
# LA(p2) = {'['}
# LA(p3) = {"Nome: "}
# LA(p4) = {','}
# LA(p5) = {']'}
# LA(p6) = {"Nome: "}
# LA(p7) = {id}
# LA(p8) = {GK | LAT | CEN | MED | EXT | PL}
# LA(p9) = {','}
# LA(p10) = {']'}
# LA(p11) = {GK}
# LA(p12) = {LAT}
# LA(p13) = {CEN}
# LA(p14) = {MED}
# LA(p15) = {EXT}
# LA(p16) = {PL}

#    estado     '['     "Nome: "     ','     ']'     id     GK     LAT     CEN     MED     EXT     PL
# -------------------------------------------------------------------------------------------------------
#         Z      p1                                                                                      
#   Plantel      p2                                                                                      
# Jogadores               p3                                                                             
#     Cont1                          p4      p5                                                          
#   Jogador               p6                                                                             
#      Nome                                          p7                                                  
#  Posicoes                                                 p11    p12     p13     p14     p15     p16   
#     Cont2                          p9      p10                                                         
#   Posicao                                                 p11    p12     p13     p14     p15     p16   
# -------------------------------------------------------------------------------------------------------

# [Nome: Ricardo Posicoes: [MED,EXT], Nome: Miguel Posicoes: [EXT,PL], Nome: Filipe Posicoes: [PL]]

prox_simb = ('Erro', '', 0, 0)

def parserErro(simb):
    print("Erro: ", simb)

def rec_term(simb):
    global prox_simb
    print("term:",prox_simb.value)
    if prox_simb.type == simb:
        prox_simb = lexer.token()
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
    print("Reconheci p2: Plantel -> '[' Jogadores ']'")
    
def rec_Jogadores():
    rec_Jogador()
    rec_Cont1()
    print("Reconheci p3: Jogadores -> Jogador Cont1")

def rec_Cont1():
    global prox_simb
    if prox_simb.type == 'VIRG':
            rec_term('VIRG')
            rec_Jogador()
            rec_Cont1()
            print("Reconheci p4: Cont1 -> ',' Jogador Cont1")
    elif prox_simb.type == 'PF':
        print("Reconheci p5: Cont1 -> ")
        pass
    else:
        parserErro(prox_simb)

def rec_Jogador():
    rec_term('NOME')
    rec_Nome()
    rec_term('POSICOES')
    rec_term('PA')
    rec_Posicoes()
    rec_term('PF')
    print("Reconheci p6: Jogador -> 'Nome: ' Nome 'Posicoes: ' '[' Posicoes ']'")

def rec_Nome():
    rec_term('ID')
    print("Reconheci p7: Nome -> id")

def rec_Posicoes():
    rec_Posicao()
    rec_Cont2()
    print("Reconheci p8: Posicoes -> Posicao Cont2")

def rec_Cont2():
    global prox_simb
    if prox_simb.type == 'VIRG':
        rec_term('VIRG')
        rec_Posicao()
        rec_Cont2()
        print("Reconheci p9: Cont2 -> ',' Posicao Cont2")
    elif prox_simb.type == 'PF':
        print("Reconheci p10: Cont2 -> ")
        pass
    else: parserErro(prox_simb)

def rec_Posicao():
    global prox_simb
    if prox_simb.type == 'GK':
        rec_term('GK')
        print("Reconheci p11: Posicao -> GK")
    elif prox_simb.type == 'LAT':
        rec_term('LAT')
        print("Reconheci p12: Posicao -> LAT")
    elif prox_simb.type == 'CEN':
        rec_term('CEN')
        print("Reconheci p13: Posicao -> CEN")
    elif prox_simb.type == 'MED':
        rec_term('MED')
        print("Reconheci p14: Posicao -> MED")
    elif prox_simb.type == 'EXT':
        rec_term('EXT')
        print("Reconheci p15: Posicao -> EXT")
    elif prox_simb.type == 'PL':
        rec_term('PL')
        print("Reconheci p16: Posicao -> PL")
    else: parserErro(prox_simb)

linha = input("Introduza uma frase válida: ")

rec_Parser(linha)