import textract
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import nltk
import unidecode


pt_stopwords = stopwords.words("portuguese") + [
    'sobre',
    'p',
    'v',
    'a',
    'e',
    "1",
    '0',
    '8',
    'c',
    'p.',
    'm.',
    'f.',
    "''",
    '``',
    "...",
] + [c for c in '.,-–()":*a“”;[]%#&;;;\'!<>']

stemmer = SnowballStemmer("portuguese")


T = pd.read_csv("trabalhos.csv")
W = []


def process_words_1gram(words):
    words = (
        w for w in words
        if w not in pt_stopwords
    )
    # words = [stemmer.stem(w) for w in words]
    return words


def process_words_2gram(words):
    bigrams = nltk.bigrams(words)
    bigrams = (
        '%s %s' % (w1, w2) for w1, w2 in bigrams
        if w1 not in pt_stopwords and w2 not in pt_stopwords
    )
    return [b for b in bigrams if b not in [
            "de uma",
            "0 0",
            "= >",
            ") –"
        ]]


for i, row in T.iterrows():
    pdf = row['Pdf']
    words = textract.process(pdf).decode()
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
            # 'Freq': len([t == termo for t in unigrams]) / len(unigrams)
        })

    for termo in bigrams:
        W.append({
            **base_row,
            'Tipo': 'Bigram',
            'Termo': termo,
            'Freq': len([t == termo for t in bigrams]) / len(bigrams)
        })
(
    pd.DataFrame
    .from_records(W)
    .to_csv('frequencias.csv', index=False)
)