import textract
import pandas as pd
from nltk.corpus import stopwords
import nltk
import unidecode


pt_stopwords = stopwords.words("portuguese") + [
    'sobre',
    'p',
    'v',
    'a',
    'e',
    "01",
    "1",
    '0',
    "6",
    '8',
    "13",
    'c',
    "c."
    "a."
    'p.',
    'm.',
    'f.',
    "r",
    "''",
    '``',
    "...",
    "'s",
    "k.",
    "l.",
    "cm",
    "nao",
    "sao",
    "2022.",
    "2023",
    "figura",
    "et",
    "ai"
] + [c for c in '.,-––()":*a“”;[]%#&;;;\'!@<>=?1234567890$db/']


T = pd.read_csv("trabalhos.csv")
W = []


def process_words_1gram(words):
    words = (
        w for w in words
        if w not in pt_stopwords
    )
    return words


def process_words_2gram(words):
    return [
        '%s %s' % (w1, w2) for w1, w2 in nltk.bigrams(words)
        if w1 not in pt_stopwords and w2 not in pt_stopwords and 
            '%s %s' % (w1, w2) not in [
                "alem disso",
                "dessa forma",
                "desta forma",
                "desse modo",
                "nesse sentido",
                "muitas vezes",
                "nesse contexto",
                "et al",
                "0 0",
                "campus sao",
                "etapas construtivas",
                "fazem parte",
                "culturalmente relevante",
                "arquivo pessoal",
                "knijnik et",
                "a. lorenzoni",
                "primeira autora",
                "acervo proprio",
                "referido autor",
                "consideracoes finais",
                "vai dar",
                "duas variaveis",
                "colega sentado",
                "sao raimundo",
                "sao luis",
                "sao domingos",
                "raimundo nonato",
                "candomble pode",
                "campo maior",
                "educacao culturalmente",
                "/ /",
                "/ voce",
            ]
    ]

for i, row in T.iterrows():
    pdf = row['Pdf']
    words = textract.process(pdf).decode()
    words = words[words.index('\n\n\x0c'):]
    for chave in ['REFERÊNCIAS', 'REFERENCIAS', 'REFERENCIAL BIBLIOGRÁFICO', 'COM QUEM VOAMOS', 'REFERÊNCIA', 'Referências', 'Referência']:
        try:
            words = words[:words.index(chave)]
            break
        except ValueError:
            continue
    else:
        raise

    words = unidecode.unidecode(words).lower()
    tokens = nltk.tokenize.word_tokenize(words, language='portuguese')    

    unigrams = process_words_1gram(tokens)
    bigrams = process_words_2gram(tokens)

    base_row = {
        'Pdf': pdf,
        'Eixo': row['Eixo'],
        'Modalidade': row['Modalidade'],
    }

    for termo in unigrams:
        W.append({
            **base_row,
            'Tipo': 'Unigram',
            'Termo': termo,
        })

    for termo in bigrams:
        W.append({
            **base_row,
            'Tipo': 'Bigram',
            'Termo': termo,
        })
(
    pd.DataFrame
    .from_records(W)
    .to_csv('frequencias.csv', index=False)
)