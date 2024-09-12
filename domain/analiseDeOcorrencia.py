import csv
from collections import Counter

def ler_csv(nome_arquivo):
    numeros = []
    with open(nome_arquivo, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dezenas = row['Dezenas'].split(", ")
            numeros.extend(dezenas)
    return numeros

def contar_ocorrencias(numeros):
    contador = Counter(numeros)
    return contador.most_common()  

def salvar_analise_csv(contador, nome_arquivo):
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Número", "Ocorrências"])
        for numero, ocorrencias in contador:
            writer.writerow([numero, ocorrencias])


nome_arquivo_csv = 'resultados_megasena.csv'
nome_arquivo_analise = 'analise_ocorrencias.csv'
numeros = ler_csv(nome_arquivo_csv)
contador = contar_ocorrencias(numeros)

print("Números mais frequentes:")
for numero, ocorrencias in contador:
    print(f"Número {numero}: {ocorrencias} vezes")

salvar_analise_csv(contador, nome_arquivo_analise)
print(f"Análise salva em '{nome_arquivo_analise}'.")