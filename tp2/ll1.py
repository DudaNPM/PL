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



# Verifica se um simbolo nao terminal é nullable
def isNullable(nt):
    return [] in producoes[nt]



# Cálculo do First de uma produção
def first(prod):

    # simbolos terminais e nulos
    if len(prod) != 0:
        if prod[0] in T:
            return [prod[0]]
    else:
        return []
 
    # simbolos não terminais
    if prod[0] in NT:
        res = []
        # ocurrencias de prod[0] do lado esquerdo
        occur = producoes[prod[0]]
        # calc first por cada ocurrencia e unimos
        for o in occur:
            for i in first(o):
                res.append(i)

        # se nao for anulavel acaba
        if [] not in res:
            return res
        # se for anulavel
        else:
            # a nossa gramática não cobre este caso
            # no entanto se cobrisse teriamos que ir
            # calcular os firsts dos simbs à frente
            pass

# Cálculo de todos os firsts
firsts = {}
def calc_firsts():
    for key, value in producoes.items():
        for p in value:
            if key in firsts:
                firsts.get(key).append(first(p))
            else:
                firsts[key] = [first(p)]

# Print firsts
def print_firsts():
    print()
    print("Calculated Firsts:")
    print("--------------------------------------------------------------------------")
    for key,value in firsts.items():
        print(key,value)
    print("--------------------------------------------------------------------------")
    print()



# Cálculo do Follow de um simb não terminal
def follow(nt):
 
    # follows calculados ate ao momento
    current = set()
    if nt == 'Plantel':
        current.add('$')
 
    # lado esquerdo das producoes
    for le in producoes:
        # todos os lados direitos do respetivo lado esquerdo, lista de listas
        lds = producoes[le]
        # todos os lados direitos do respetivo lado esquerdo, por lista
        for ld in lds:
            if nt in ld:
                while nt in ld:
                    index_nt = ld.index(nt) # indice do simb na producao
                    ld = ld[index_nt + 1:] # o que está para a frente do simb

                    # verificar se estamos no fim da producao ou nao
                    if len(ld) != 0:
                        # verificamos o que é que está à frente e calculamos o first
                        res = []
                        if ld[0] in NT:
                            prod = producoes[ld[0]]
                            for p in prod:
                                if len(first(p)) != 0:
                                    res.append(first(p))
                                else:
                                    res.append(['#'])   # para representar null
                        else:
                            res.append(first(ld))
                        
                        aux = []
                        for i in res:
                            aux = aux + i
                        res = aux

                        # se a producao for anulavel vamos ter que unir com o follow do lado esquerdo
                        if '#' in res:
                            newList = []
                            res.remove('#')
                            ansNew = follow(le)

                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = res + ansNew
                                else:
                                    newList = res + [ansNew]
                            else:
                                newList = res
                            res = newList
                    else:
                        # se tivermos no fim da producao
                        # calculamos o follow do lado esquerdo
                        # garantindo que não são iguais
                        if nt != le:
                            res = follow(le)

                    # atualizamos os follows ja calculados
                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                current.add(g)
                        else:
                            current.add(res)
    return list(current)

# Cálculo de todos os follows
follows = {}
def calc_follows():
    for nt in NT:
        follows[nt] = follow(nt)

# Print follows
def print_follows():
    print()
    print("Calculated Follows:")
    print("--------------------------------------------------------------------------")
    for key,value in follows.items():
        print(key,value)
    print("--------------------------------------------------------------------------")
    print()



# Cálculo de LookAheads
def lookAhead(le,ld):
    fi = []
    for p in ld:
        fi.append(first(p))
    fo = follow(le)

    if isNullable(le):
        fi.remove([])
        return fi + [fo]
    else:
        return fi

# Cálculo de todos os lookaheads
lookAheads = {}
def calc_lookaheads():
    for key, value in producoes.items():
        lookAheads[key] = lookAhead(key,value)

# Print lookaheads
def print_lookaheads():
    print()
    print("Calculated Lookaheads:")
    print("--------------------------------------------------------------------------")
    for key,value in lookAheads.items():
        print(key,value)
    print("--------------------------------------------------------------------------")
    print()



# Verifica se a gramatica obedece ás regras dos lookaheads numa gramatica ll(1)
def verify_lookAheads():
    res = True
    for value in lookAheads.values():
        if len(value) > 1:
            aux = []
            for i in value:
                aux = aux + i
            if len(aux) != len(set(aux)):
                res = False
    return res



calc_firsts()
calc_follows()
calc_lookaheads()

print_firsts()
print_follows()
print_lookaheads()
print("Obedece ás regras de lookaheads: ", verify_lookAheads())