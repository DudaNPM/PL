import re
import sys
from unittest import result


### Exemplo de ficheiros csv e o seu resultado em json

#   CABEÇALHO :: Número,Nome,Curso
#   CONTEUDO  :: 3162,Cândido Faísca,Teatro
#             :: 7777,Cristiano Ronaldo,Desporto
#             :: 264,Marcelo Sousa,Ciência Política

#   RESULTADO ::
#   [
#       {
#           "Número": "3612",
#           "Nome": "Cândido Faísca",
#           "Curso": "Teatro"
#       },
#       {
#           "Número": "7777",
#           "Nome": "Cristiano Ronaldo",
#           "Curso": "Desporto"
#       },
#       {
#           "Número": "264",
#           "Nome": "Marcelo Sousa",
#           "Curso": "Ciência Política"
#       }
#   ]


#   CABEÇALHO :: Número,Nome,Curso,Notas{5},,,,,
#   CONTEUDO  :: 3162,Cândido Faísca,Teatro,12,13,14,,
#             :: 7777,Cristiano Ronaldo,Desporto,17,12,20,11,12
#             :: 264,Marcelo Sousa,Ciência Política,18,19,19,20,

#   RESULTADO ::
#   [
#       {
#           ...
#       },
#       {
#           "Número": "7777",
#           "Nome": "Cristiano Ronaldo",
#           "Curso": "Desporto"
#           "Notas": [17,12,20,11,12]
#       },
#       {
#           ...
#       }
#   ]


#   CABEÇALHO :: Número,Nome,Curso,Notas{3,5}::sum,,,,,
#   CONTEUDO  :: 3162,Cândido Faísca,Teatro,12,13,14,,
#             :: 7777,Cristiano Ronaldo,Desporto,17,12,20,11,12
#             :: 264,Marcelo Sousa,Ciência Política,18,19,19,20,

#   RESULTADO ::
#   [
#       {
#           ...
#       },
#       {
#           "Número": "7777",
#           "Nome": "Cristiano Ronaldo",
#           "Curso": "Desporto",
#           "Notas_sum": 72
#       },
#       {
#           ...
#       }
#   ]

### Recebe a primeira linha de um ficheiro csv
### Reconhece o nome das colunas
### Reconhece as colunas que 'são' listas e o seu tamanho ou intrevalo de tamanho -> notas{3,5} | notas{5}
### Reconhece o nome das funções de agregação associadas às listas
### Retorna uma lista com os títulos das colunas
def cabecalho(cabecalho):

    colunas = [] # nome das colunas

    captures = re.findall(r'([^,{}]+)(\{\d+,\d+\}|\{\d+\})?(?:::(\w+))?', cabecalho)

    for capture in captures:
        colunas.append(capture[0])

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
        print(campos)

        # percorremos todas as colunas de cada linha
        for j, campo in enumerate(campos):
            print(colunas[j])
            if campo:   # ignora campos vazios
                ### neste ponto, verificar se a coluna j é uma lista de valores e se tem função de agregação ou não
                ### para isso ao ler o cabeçalho vai ter que se guardar num tuplo (?) qql coisa como (titulo,min,max,funcao) -> (nome,0,0,"") | (notas,3,5,"sum") | (notas,5,5,avg)
                # if coluna[j] not lista:
                json_txt.append(f'\t\t"{colunas[j]}": "{campo}"' + ("," if (len(list(filter(None,campos[j:]))) > 1) else ""))   # condição que verifica se é o campo da última coluna, se for não leva vírgula
                # else:
                #   valores = re.findall(r'...', ','.join(campos[j:]))
                #   
                #   if coluna[j] not função_agregação:
                #       append colunas[j] + os valores numa lista
                #   else:
                #       resultado = funcao(valores,funcao)
                #       append colunas[j] + resultado
                #   
                #   incrementar o j de acordo com o numero de valores encontrados

        # condição que verifiva se é a última linha, se for não leva vírgula
        if (i != len(lines)-1):
            json_txt.append("\t},")
        else:
            json_txt.append("\t}")
    
    json_txt.append("]")
    return '\n'.join(json_txt)  # junta todas as strings da lista, metendo um \n entre elas



# Leitura dos argumentos
if len(sys.argv) == 3:
	csv = f"{sys.argv[1]}"      # input
	json = f"{sys.argv[2]}"     # output
else:
	raise Exception("Número de argumentos inválido...\n")

# Ler CSV
file = open(csv)
lines = file.read().splitlines()  # remove os \n
file.close()

if len(lines) < 2:
	raise Exception("Ficheiro mal configurado...\n")

# Trabalhar CSV e preparar JSON
colunas = cabecalho(lines[0])
json_txt = csv2json(colunas,lines[1:])

# Criar JSON
json_file = open(json, "w")
json_file.write(json_txt)
json_file.close()