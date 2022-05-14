import ply.lex as lex

tokens = ['PA','PF','VIRG','ID','GK','LAT','CEN','MED','EXT','PL','NOME','POSICOES']

t_PA   = r'\['
t_PF   = r'\]'
t_VIRG = r','
t_ID   = r'[A-Za-z]+'

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


# G = {T,N,P,S}
# T = {'[', ']', ',', 'Nome:', 'Posicoes:', 'id', 'GK', 'LAT', 'CEN', 'MED', 'EXT', 'PL'}
# N = {Plantel, Jogadores, Jogador, Cont1, Nome, Posicoes, Posicao, Cont2}
# S = Plantel
# P = {p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16}


# COM RECURSIVIDADE À ESQUERDA
# def p_grammar(p):
#   Z         : Plantel '$'
#   Plantel   : '[' Jogadores ']'
#   Jogadores : Jogadores ',' Jogador
#             | Jogador
#   Jogador   : "Nome: " Nome "Posicoes: " '[' Posicoes ']'
#   Nome      : id
#   Posicoes  : Posicoes ',' Posicao
#             | Posicao
#   Posicao   : GK
#             | LAT
#             | CEN
#             | MED
#             | EXT
#             | PL


# SEM RECURSIVIDADE À ESQUERDA
# def p_grammar(p):                                                 FIRST                           FOLLOW          LOOKAHEADS
#  p1    Z         : Plantel '$'                                    {'['}                           {}              {'['}
#  p2    Plantel   : '[' Jogadores ']'                              {'['}                           {$}             {'['}
#  p3    Jogadores : Jogador Cont1                                  {"Nome: "}                      {']'}           {"Nome: "}
#  p4    Cont1     : ',' Jogador Cont1                              {','}                           {']'}           {','}
#  p5              | ϵ                                              {}                              {}              {']'}
#  p6    Jogador   : "Nome: " Nome "Posicoes: " '[' Posicoes ']'    {"Nome: "}                      {']',','}       {"Nome: "}
#  p7    Nome      : id                                             {id}                            {"Posicoes:"}   {id}
#  p8    Posicoes  : Posicao Cont2                                  {GK,LAT,CEN,MED,EXT,PL}         {']'}           {GK,LAT,CEN,MED,EXT,PL}
#  p9    Cont2     : ',' Posicao Cont2                              {','}                           {']'}           {','}
# p10              | ϵ                                              {}                              {}              {']'}
# p11    Posicao   : GK                                             {GK}                            {']',','}       {GK}
# p12              | LAT                                            {LAT}                           {}              {LAT}
# p13              | CEN                                            {CEN}                           {}              {CEN}
# p14              | MED                                            {MED}                           {}              {MED}
# p15              | EXT                                            {EXT}                           {}              {EXT}
# p16              | PL                                             {PL}                            {}              {PL}


# Transition Table

#    estado     '['     "Nome: "     ','     ']'     id     GK     LAT     CEN     MED     EXT     PL    "Posicoes:"
# --------------------------------------------------------------------------------------------------------------------
#         Z      p1       --         --      --      --     --     --      --      --      --      --         --
#   Plantel      p2       --         --      --      --     --     --      --      --      --      --         --
# Jogadores      --       p3         --      --      --     --     --      --      --      --      --         --
#     Cont1      --       --         p4      p5      --     --     --      --      --      --      --         --
#   Jogador      --       p6         --      --      --     --     --      --      --      --      --         --
#      Nome      --       --         --      --      p7     --     --      --      --      --      --         --
#  Posicoes      --       --         --      --      --     p8     p8      p8      p8      p8      p8         --
#     Cont2      --       --         p9      p10     --     --     --      --      --      --      --         --
#   Posicao      --       --         --      --      --     p11    p12     p13     p14     p15     p16        --
# --------------------------------------------------------------------------------------------------------------------


prox_simb = ('Erro', '', 0, 0)

def parserError(simb):
    print("Erro Sintático: ", simb)
    print()
    raise Exception("Erro no reconhecimento da gramática...\n")

def rec_term(simb):
    global prox_simb
    print("term:",prox_simb.value)
    if prox_simb.type == simb:
        prox_simb = lexer.token()
    else:
        parserError(prox_simb)

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
        elif prox_simb.type == 'PF':
            pass
    else:
        parserError(prox_simb)

def rec_Jogador():
    global posicoesCadaJogador
    rec_term('NOME')
    rec_Nome()
    rec_term('POSICOES')
    rec_term('PA')
    rec_Posicoes()
    rec_term('PF')
    print("Este jogador é capaz de jogar em",posicoesCadaJogador,"posicoes diferentes")
    posicoesCadaJogador = 0

def rec_Nome():
    global nrJogadores
    rec_term('ID')
    nrJogadores += 1

def rec_Posicoes():
    rec_Posicao()
    rec_Cont2()

def rec_Cont2():
    global prox_simb
    if prox_simb.type == 'VIRG':
        rec_term('VIRG')
        rec_Posicao()
        rec_Cont2()
    elif prox_simb.type == 'PF':
        pass
    else: parserError(prox_simb)

posicoes = []

def rec_Posicao():
    global prox_simb
    global posicoesCadaJogador
    global gks
    global lats
    global cens
    global meds
    global exts
    global pls
    global posicoesPreenchidas
    if prox_simb.type == 'GK':
        rec_term('GK')
        if "GK" not in posicoes:
            posicoes.append("GK")
            posicoesPreenchidas += 1
        gks += 1
        posicoesCadaJogador += 1
    elif prox_simb.type == 'LAT':
        rec_term('LAT') 
        if "LAT" not in posicoes:
            posicoes.append("LAT")
            posicoesPreenchidas += 1
        lats += 1
        posicoesCadaJogador += 1
    elif prox_simb.type == 'CEN':
        rec_term('CEN')
        if "CEN" not in posicoes:
            posicoes.append("CEN")
            posicoesPreenchidas += 1
        cens += 1
        posicoesCadaJogador += 1
    elif prox_simb.type == 'MED':
        rec_term('MED')
        if "MED" not in posicoes:
            posicoes.append("MED")
            posicoesPreenchidas += 1
        meds += 1
        posicoesCadaJogador += 1
    elif prox_simb.type == 'EXT':
        rec_term('EXT')        
        if "EXT" not in posicoes:
            posicoes.append("EXT")
            posicoesPreenchidas += 1
        exts += 1
        posicoesCadaJogador += 1
    elif prox_simb.type == 'PL':
        rec_term('PL')
        if "PL" not in posicoes:
            posicoes.append("PL")
            posicoesPreenchidas += 1
        pls += 1
        posicoesCadaJogador += 1
    else:
        parserError(prox_simb)


nrJogadores = 0
posicoesPreenchidas = 0
posicoesCadaJogador = 0
gks = 0
cens = 0
lats = 0
meds = 0
exts = 0
pls = 0


import sys
programa = sys.stdin.read()
rec_Parser(programa)

## usar comando: cat teste.txt | python3 tp2.py

print("\n\n|---------------------------------------------PLANTEL INFO---------------------------------------------|\n")
print("Este plantel é constituído por", nrJogadores, "jogadores")
print("Este plantel tem jogadores que podem atuar em", posicoesPreenchidas, "posicoes diferentes")
print("Existem",gks,"guarda-redes neste plantel")
print("Existem",lats,"laterais neste plantel")
print("Existem",cens,"centrais neste plantel")
print("Existem",meds,"medios neste plantel")
print("Existem",exts,"extremos neste plantel")
print("Existem",pls,"pontas-de-lança neste plantel\n")