from traceback import print_tb
#from turtle import pos
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




# ideias: contar nº de jogadores do plantel                     (Feito)
#         contar quantos jogadores cada posição tem
#         contar quantas posições cada jogador pode fazer
#         contar para quantas posicoes o plantel tem jogadores  (Feito)


# G = {T,N,P,S}
# T = {'[', ']', ',', 'Nome:', 'Posicoes:', 'id', 'GK', 'LAT', 'CEN', 'MED', 'EXT', 'PL'}
# N = {Plantel, Jogadores, Jogador, Cont1, Nome, Posicoes, Posicao, Cont2}
# S = Plantel
# P = {p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16}


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
#         Z      p1       --         --      --      --     --     --      --      --      --      -- 
#   Plantel      p2       --         --      --      --     --     --      --      --      --      -- 
# Jogadores      --       p3         --      --      --     --     --      --      --      --      -- 
#     Cont1      --       --         p4      p5      --     --     --      --      --      --      -- 
#   Jogador      --       p6         --      --      --     --     --      --      --      --      -- 
#      Nome      --       --         --      --      p7     --     --      --      --      --      -- 
#  Posicoes      --       --         --      --      --     p8     p8      p8      p8      p8      p8 
#     Cont2      --       --         p9      p10     --     --     --      --      --      --      -- 
#   Posicao      --       --         --      --      --     p11    p12     p13     p14     p15     p16
# --------------------------------------------------------------------------------------------------------------------


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
    global nrJogadores
    rec_term('ID')
    nrJogadores += 1
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

posicoes = []
#todasPosicoes = []

def rec_Posicao():
    global prox_simb
    global posicoesPreenchidas
    if prox_simb.type == 'GK':
        rec_term('GK')
        if "GK" not in posicoes:
            posicoes.append("GK")
            posicoesPreenchidas += 1
        # print("Reconheci p11: Posicao -> GK")
    elif prox_simb.type == 'LAT':
        rec_term('LAT') 
        if "LAT" not in posicoes:
            posicoes.append("LAT")
            posicoesPreenchidas += 1
        # print("Reconheci p12: Posicao -> LAT")
    elif prox_simb.type == 'CEN':
        rec_term('CEN')
        if "CEN" not in posicoes:
            posicoes.append("CEN")
            posicoesPreenchidas += 1
        # print("Reconheci p13: Posicao -> CEN")
    elif prox_simb.type == 'MED':
        rec_term('MED')
        if "MED" not in posicoes:
            posicoes.append("MED")
            posicoesPreenchidas += 1
        # print("Reconheci p14: Posicao -> MED")
    elif prox_simb.type == 'EXT':
        rec_term('EXT')        
        if "EXT" not in posicoes:
            posicoes.append("EXT")
            posicoesPreenchidas += 1
        # print("Reconheci p15: Posicao -> EXT")
    elif prox_simb.type == 'PL':
        rec_term('PL')
        if "PL" not in posicoes:
            posicoes.append("PL")
            posicoesPreenchidas += 1
        # print("Reconheci p16: Posicao -> PL")
    else: parserError(prox_simb)

    #posicoesCadaJogador = len(posicoes)
    #print("O jogador pode atuar em",posicoesCadaJogador,"posicoes")


nrJogadores = 0
posicoesPreenchidas = 0
posicoesCadaJogador = 0
jogadoresPorPosicao = 0

linha = input("Introduza uma frase válida: ")
# Teste do tokenizer
# lexer.input(linha)
# for tok in lexer:
#     print(tok)
rec_Parser(linha)
print("Este plantel é constituído por", nrJogadores, "jogadores")
print("Este plantel tem jogadores que podem atuar em", posicoesPreenchidas, "posicoes diferentes")


#import sys
#programa = sys.stdin.read()
#rec_Parser(programa)

## usar comando: cat teste.txt | python3 tp2.py