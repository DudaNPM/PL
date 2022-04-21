import ply.lex as lex

tokens = ['PA','PF','VIRG','ID','GK','LAT','CEN','MED','EXT','PL']

t_ID   = r'[A-Za-z]'
t_PA   = r'\['
t_PF   = r'\]'
t_VIRG = r','
t_GK   = r'GK'
t_CEN  = r'CEN'
t_MED  = r'MED'
t_EXT  = r'EXT'
t_PL   = r'PL'
 
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print('Caráter ilegal: ', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
