###
# LL(1) GRAMMAR
# 
# The constraints are:
# 
#     -If you have several rules X→Y,X→Z, then First(Y) ∩ First(Z) = ∅
#     -If you have several rules X→Y,X→Z, and First(Z) contains ϵ, then First(Y) ∩ Follow(Z) = ∅
#     -No left recursions: X→X…
#     -If you have several rules X→Y,X→Z, then Z must not be non-false (i.e. must be able to return false)
###

producoes = {
    #Plantel   : '[' Jogadores ']'
    "Plantel": [['PA', 'Jogadores', 'PF']],
    #Jogadores : Jogador Cont1
    "Jogadores": [['Jogador', 'Cont1']],
    #Cont1     : ',' Jogador Cont1 | ϵ
    "Cont1": [['VIRG', 'Jogador', 'Cont1'], []],
    #Jogador   : "Nome: " Nome "Posicoes: " '[' Posicoes ']'
    "Jogador": [['Nome:', 'Nome', 'Posicoes:', 'PA', 'Posicoes', 'PF']],
    #Nome      : id
    "Nome": [['id']],
    #Posicoes  : Posicao Cont2
    "Posicoes": [['Posicao', 'Cont2']],
    #Cont2     : ',' Posicao Cont2 | ϵ
    "Cont2": [['VIRG', 'Posicao', 'Cont2'], []],
    #Posicao   : GK | LAT | CEN | MED | EXT | EXT | PL
    "Posicao": [['GK'],['LAT'],['CEN'],['MED'],['EXT'],['PL']]
}

# Símbolos não terminais
NT = ['Plantel', 'Jogadores', 'Cont1', 'Jogador', 'Nome', 'Posicoes', 'Cont2', 'Posicao']

# Símbolos terminais
T = ['PA', 'PF', 'VIRG', 'Nome:', 'Posicoes:', 'id', 'GK', 'LAT', 'CEN', 'MED', 'EXT', 'PL']

# Acho que está bem, falta verificar quando o proximo simbolo não é NT voltar a fazer o ciclo mas agora com p[1]
# E falta fazer para as produções que são vazias

# Cálculo de LookAheads
lookAheads = {}
for n in NT:
    lookAheads[n] = []
    for p in producoes[n]:
        encontrado = False
        i = 0
        while not encontrado and i < len(p):
            if p[i] in T:
                if p[i] not in NT:
                    lookAheads[n].append(p[i])
                    encontrado = True
            else:
                print(p[i])
            i = i + 1

print(lookAheads)

