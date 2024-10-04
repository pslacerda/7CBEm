import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt
from collections import Counter


NORDESTE = ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"]
SUDESTE = ["ES", "MG", "RJ", "SP"]
NORTE = ["AM", "AP", "PA", "RO", "RR", "TO"]
CENTROOESTE = ["DF", "GO", "MS", "MT"]
SUL = ["PR", "RS", "SC"]


I = pd.read_csv("instituicoes.csv")
I = I.rename(columns={
    'INSTITUIÇÃO':  'Instituição',
    'UF': 'Estado',
    'ARTIGO': 'Pdf',
})
I = I[~pd.isna(I.Instituição)]
I.Pdf = I.Pdf.replace('.*/', '', regex=True)

edges = []
def add_edges(df):
    s = df.Instituição.drop_duplicates().sort_values()
    w = []
    for i1, n1 in enumerate(s):
        for i2, n2 in enumerate(s):
            if i1 < i2:
                n1, n2 = tuple(sorted([n1, n2]))
                edges.append((n1, n2))
I.groupby('Pdf').apply(add_edges)


G1 = nx.MultiGraph()
G1.add_edges_from(edges)

G2 = nx.Graph()

e_count = Counter()
for e in G1.edges:
    n1, n2 = tuple(sorted(e[:2]))
    e_count[(n1, n2)] += 1
    G2.add_edge(n1, n2)

for e in G1.edges:
    n1, n2 = tuple(sorted(e[:2]))
    G2.edges[(n1, n2)]['weight'] = e_count[(n1, n2)]


for n in G2:
    estado = I[I.Instituição == n].drop_duplicates().Estado.iloc[0]
    if estado in NORDESTE:
        c = 'NORDESTE'
    elif estado in SUDESTE:
        c = 'SUDESTE'
    elif estado in NORTE:
        c = 'NORTE'
    elif estado in CENTROOESTE:
        c = 'CENTROOESTE'
    elif estado in SUL:
        c = 'SUL'
    else:
        c = 'white'
    G2.nodes[n]['color'] = c

nx.write_graphml(G2, 'instituicoes.xml')
