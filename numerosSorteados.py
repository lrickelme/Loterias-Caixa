import requests
import csv
from datetime import datetime

def obter_ultimo_concurso(loteria):
    url = f"https://loteriascaixa-api.herokuapp.com/api/{loteria}/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter o último concurso")
        return None

def obter_ultimos_sorteios(loteria, concurso_inicial):
    url_base = f"https://loteriascaixa-api.herokuapp.com/api/{loteria}"
    resultados = []
    concurso_atual = concurso_inicial
    total_solicitados = 0

    while len(resultados) < 100:
        url = f"{url_base}/{concurso_atual}"
        response = requests.get(url)

        if response.status_code == 200:
            resultado = response.json()
            total_solicitados += 1
            if verificar_dia_semana(resultado['data']):
                resultados.append(resultado)
            if total_solicitados % 10 == 0:
                print(f"Concursos verificados: {total_solicitados}, Encontrados: {len(resultados)}")
        else:
            print(f"Erro ao obter o concurso {concurso_atual}")
            break
        
        concurso_atual -= 1

    print(f"Total de concursos verificados: {total_solicitados}")
    return resultados

def verificar_dia_semana(data_str):
    data = datetime.strptime(data_str, "%d/%m/%Y")
    return data.weekday() in [2, 5] 

def salvar_resultados_csv(resultados, nome_arquivo):
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Concurso", "Data", "Dezenas"])

        for resultado in resultados:
            writer.writerow([
                resultado['concurso'],
                resultado['data'],
                ", ".join(resultado['dezenas'])
            ])

loteria = "megasena"

ultimo_concurso = obter_ultimo_concurso(loteria)
if ultimo_concurso:
    concurso_inicial = ultimo_concurso['concurso']
    resultados = obter_ultimos_sorteios(loteria, concurso_inicial)
    salvar_resultados_csv(resultados, 'resultados_megasena.csv')
    print(f"Resultados filtrados e salvos em 'resultados_megasena.csv'.")
else:
    print("Não foi possível obter o último concurso.")
