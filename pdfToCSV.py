# Usaremos a biblioteca camelot para extrair as tables especificas do pdf
# Devem ser instaladas as dependências Ghostscript e Tkinter
# O tutorial completo se encontra aqui:
# https://camelot-py.readthedocs.io/en/master/user/install-deps.html

# Após instalar elas, instale o camelot usando:
# pip install "camelot-py[cv]"

# OPCIONAL - Para uso com notebook / Linux
#!pip install "camelot-py"[cv]
#!apt install ghostscript python3-tk

import camelot

# Usaremos zipFile para compactar os arquivos
from zipfile import ZipFile
import os

# Para facilitar a obtenção do arquivo, usaremos requests para baixar o próprio.
import requests

# Verifica se o arquivo já existe. Caso ele exista, o download do mesmo será ignorado
if os.path.isfile('./tiss.pdf'):
    print("The file already exists. Skipping download... \n")
else:
    url = "http://www.ans.gov.br/images/stories/Plano_de_saude_e_Operadoras/tiss/Padrao_tiss/tiss3/Padr%C3%A3o_TISS_Componente_Organizacional_202103.pdf"
    r = requests.get(url)
    with open('./tiss.pdf', 'wb') as f:
        f.write(r.content)


# Por padrão, o pdf deve ser inserido na pasta raiz. O camelot irá percorrer as páginas especificas, que é onde se encontram os quadros 30,31,31.
print("Reading PDF and loading tables into the stream. It may take a while... \n")
tables = camelot.read_pdf('./tiss.pdf', pages='79,80,81,82,83,84,85')
print("Table loaded into stream.\n")

# A função export permite que transformar todas as tabelas encontradas para um formato especifico. Nesse caso, transformaremos em csv.
tables.export('table.csv', f='csv')
print("Table successfully exported as .csv. \n")

# Passamos o diretório atual ao python e guardamos todos os nomes dos arquivos em uma variável
directory = "./"
dir_files = os.listdir(directory)

# Depois, filtramos para acessar apenas os arquivos que terminam em .csv
csv_files = [file for file in dir_files if file.endswith(".csv")]

# Verifica se o arquivo zip já existe por algum motivo.
zipName = 'Teste_Intuitive_Care_FelipeFreire.zip'
if os.path.isfile(zipName):
    print("The compressed files already exists. Skipping compression... \n")
else:
    # Criamos um arquivo do tipo zip, passando o parametro 'w', dizendo ao zipfile que queremos apenas escrever arquivos nele
    zipObj = ZipFile('Teste_Intuitive_Care_FelipeFreire.zip', 'w')

    # E aqui adicionaremos os arquivos csv ao zip...
    for file in csv_files:
        csv_table = os.path.join(directory, file)
        zipObj.write(csv_table)

    # E tiramos o arquivo da stream, removendo ele.
    zipObj.close()
    print(".csv files compressed into .zip. \n")

# Essa parte final tem como objetivo deletar todos os arquivos csv. É opcional, a resposta deve ser dada pelo console
print("Delete all .csv files? Y / N \n")
ans = input()

if ans == 'Y':
    for file in csv_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)
    print(".csv files deleted.\n")

print("Done!")
