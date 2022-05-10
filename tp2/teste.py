import re 

# recursividade à esquerda
# verifica se o que vem a seguir aos ':' é o mesmo que estava antes
# se for o mesmo tem recursividade à esquerda
# se não for o mesmo, dá None, não tem recursividade à esquerda

#Use the Python regex lookahead X(?=Y) that matches X only if it is followed by Y
#Use the negative regex lookahead X(?!Y) that matches X only if it is not followed by Y

p1 = re.search(r'Z: (?=Z)',  
                    "Z: Plantel '$'")

p2 = re.search(r'Plantel: (?=Plantel)',  
                    "Plantel: '[' Jogadores ']'")

p3 = re.search(r'Jogadores: (?=Jogadores)',  
                    "Jogadores: Jogador Cont1") 

p4 = re.search(r'Cont1: (?=Cont1)',  
                    "Cont1: ',' Jogador Cont1") 

p5 = re.search(r'Cont1: (?=Cont1)',  
                    "Cont1: ") 

p6 = re.search(r'Jogador: (?=Jogador)',  
                    "Jogador: 'Nome: ' Nome 'Posicoes: ' '[' Posicoes ']'") 

p7 = re.search(r'Nome: (?=Nome)',  
                    "Nome: id") 

p8 = re.search(r'Posicoes: (?=Posicoes)',  
                    "Posicoes: Posicao Cont2") 

p9 = re.search(r'Cont2: (?=Cont2)',  
                    "Cont2: ',' Posicao Cont2") 

p10 = re.search(r'Cont2: (?=Cont2)',  
                    "Cont2: ") 

p11 = re.search(r'Posicao: (?=Posicao)',  
                    "Posicao: GK") 

p12 = re.search(r'Posicao: (?=Posicao)',  
                    "Posicao: LAT") 

p13 = re.search(r'Posicao: (?=Posicao)',  
                    "Posicao: CEN") 

p14 = re.search(r'Posicao: (?=Posicao)',  
                    "Posicao: MED") 

p15 = re.search(r'Posicao: (?=Posicao)',  
                    "Posicao: EXT") 

p16 = re.search(r'Posicao: (?=Posicao)',  
                    "Posicao: Posicao PL") 

#recursividade = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16]

#for p in recursividade:
#    if p != "None":
#        print("Existe recursividade à esquerda na produção", p)
#    else:
#        print("Não existe recursividade à esquerda na produção", p)


