import re
import sys

### Recebe a primeira linha de um ficheiro csv
### Reconhece o nome das colunas
### Reconhece as colunas que 'são' listas e o seu tamanho ou intrevalo de tamanho -> notas{3,5} | notas{5}
### Reconhece o nome das funções de agregação associadas às listas
### Retorna uma lista de (nome,min,max,size,funcao)
def cabecalho(cabecalho):

    colunas = [] # lista de (nome,min,max,size,funcao) -> (notas,3,5,'',avg) | (notas,'','',5,sum) | (curso,'','','','')

    captures = re.findall(r'([^,{]+)(?:\{(\d+),(\d+)\}|\{(\d+)\})?(?:::(\w+))?', cabecalho)

    for capture in captures:
        colunas.append(capture)
    
    return colunas


### Recebe uma lista de valores e uma função de agregação
### Devolve o resultado de aplicar a função à lista
def funcao(valores, funcao):
    if funcao == 'avg':
        return round(sum(valores) / len(valores), 2)    # arredonda a 2 casas decimais
    elif funcao == "sum":
        return sum(valores)
    elif funcao == 'min':
        return min(valores)
    elif funcao == 'max':
        return max(valores)
    else:
        raise Exception("Função de agregação - " + funcao + " - desconhecida...")


### Verifica se uma determinada coluna é uma lista de valores
### coluna = (nome,min,max,size,funcao)
###    caso 1: (notas,3,5,'', sum) -> é uma lista
###    caso 2: (notas,'','',5,avg) -> é uma lista
### restantes: (curso,'','','','') -> nao é uma lista
def isList(coluna):
    return coluna[1] != '' and coluna[2] != '' or coluna[3] != ''


### Verifica se uma determinada coluna tem funcao de agregacacao, admitindo que ja se confirmou que é uma lista de valores
### coluna = (nome,min,max,size,funcao)
###    caso 1: (notas,3,5,'', sum) -> tem funcao de agregacao
### restantes: (curso,'','','','') -> nao tem funcao de agregacao
def hasFunction(coluna):
    return coluna[4] != ''


### Devolve a string em formato json associado a uma campo de uma coluna que representa uma lista de valores ao qual é
### necessário aplicar uma função de agregação. Recebe uma coluna do tipo (nome,min,max,size,funcao), uma lista de
### valores e um boleano que indica se a coluna em questão é a última ou não
def listWithOp(coluna,valores,fim):
    if fim:
        return f'\t\t"{coluna[0]}": {funcao(valores,coluna[4])}'
    else:
        return f'\t\t"{coluna[0]}": {funcao(valores,coluna[4])}' + ","


### Devolve a string em formato json associado a uma campo de uma coluna que representa uma lista de valores
### Recebe uma coluna do tipo (nome,min,max,size,funcao), uma lista de valores e um boleano que indica se
### a coluna em questão é a última ou não
def listWithoutOp(coluna,valores,fim):
    if fim:
        return f'\t\t"{coluna[0]}": {valores}'
    else:
        return f'\t\t"{coluna[0]}": {valores}' + ","


### Recebe os títulos de todas as colunas e todas as linhas do ficheiro sem os \n
### Percorre todas as linhas e constrói uma string de acordo com um ficheiro json
### Retorna a string construída
def csv2json(colunas,lines):
    json_txt = []
    json_txt.append("[")

    # percorremos todas as linhas do ficheiro
    for i, line in enumerate(lines):
        json_txt.append("\t{")

        # colunas
        campos = line.split(',')    # estou a assumir que o separador de campos é a vírgula

        c = 0 # indice da lista colunas
        j = 0 # indice dos campos da linha
        # percorremos todas as colunas de cada linha
        while(j < len(campos)):
            if campos[j]:   # ignora campos vazios
                if isList(colunas[c]): # verificar se a coluna c é uma lista de valores ou não
                    # guardar os valores da lista em questao
                    valores = []
                    size = 0
                    max = 0

                    if (colunas[c][1] != ''): # valor minimo do intervalo de valores
                        size = int(colunas[c][1])
                        
                    if (colunas[c][3] != ''): # valor fixo
                        size = int(colunas[c][3])

                    for z in range(size): # quer seja um intervalo ou um fixo, tem que se 'capturar' size valores
                        valores.append(int(campos[j+z]))

                    if (colunas[c][2] != ''): # caso seja um intervalo, temos de 'capturar' até max valores
                        max = int(colunas[c][2]) # valor maximo do intervalo de valores
                    
                        for z in range(size+j,max+j):
                            if (z < len(campos) and re.match(r'\d+', campos[z])):
                                valores.append(int(campos[z]))
                                size = size + 1
                            else:
                                break
                    
                    j = j + size-1 # incremeta se o j, uma vez que os valores dos campos à frente ja foram lidos

                    fim = len(list(filter(None,campos[j:]))) <= 1 # booleano que indica se é o fim de uma linha
                    
                    if hasFunction(colunas[c]): # verificar se a coluna j tem função de agregação ou não
                        json_txt.append(listWithOp(colunas[c], valores, fim))
                    else:
                        json_txt.append(listWithoutOp(colunas[c], valores, fim))
                
                else:
                    json_txt.append(f'\t\t"{colunas[c][0]}": "{campos[j]}"' + ("," if (len(list(filter(None,campos[j:]))) > 1) else ""))   # condição que verifica se é o campo da última coluna, se for não leva vírgula
            c = c + 1
            j = j + 1

        # condição que verifiva se é a última linha, se for não leva vírgula
        if (i != len(lines)-1):
            json_txt.append("\t},")
        else:
            json_txt.append("\t}")
    
    json_txt.append("]")
    
    return '\n'.join(json_txt)     # junta todas as strings da lista, metendo um \n entre elas



# Leitura dos argumentos
if len(sys.argv) == 3:
	csv = f"./database/{sys.argv[1]}"      # input
	json = f"./database/{sys.argv[2]}"     # output
else:
	raise Exception("Número de argumentos inválido...\n")

# Ler CSV
file = open(csv, encoding="utf8")
linhas = file.read().splitlines()  # remove os \n
file.close()

# Trabalhar CSV e preparar JSON
colunas = cabecalho(linhas[0])
json_txt = csv2json(colunas,linhas[1:])

# Criar JSON
json_file = open(json, "w")
json_file.write(json_txt)
json_file.close()