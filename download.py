import requests
from pprint import pprint
from os.path import basename
import pandas as pd


url = "https://www.even3.com.br/anais/retornarlistaprocessosanais/"
filtro = """{"url":"7-congresso-brasileiro-de-etnomatematica-cbem-324105","ie":324105,"filtroCampoTexto":"","localEvento":"","modalidade":"","areaTematica":""}"""


trabalhos = []

for pagina in range(11):
    ret = requests.post(url, json=dict(
        filtro=filtro,
        paginacao=pagina
    ))

    data = ret.json()
    assert data['IsValid']

    for obj in data['Object']['lista']:
        titulo = obj['tituloProjeto']
        area_tematica = obj['areaTematica']
        modalidade = obj['modalidade']
        autores = obj['autores']
        pdf_url = obj['urlDocumento']
        pdf_file = basename(pdf_url)
        trabalhos.append(dict(
            Titulo=titulo,
            Autores=autores,
            Eixo=area_tematica,
            Modalidade=modalidade,
            Pdf=pdf_file
        ))

        # ret = requests.get(pdf_url)
        # with open(pdf_file, 'wb') as pdf_file:
        #     pdf_file.write(ret.content)

(
    pd.DataFrame
    .from_records(trabalhos)
    .to_csv("trabalhos.csv", index=False)
)