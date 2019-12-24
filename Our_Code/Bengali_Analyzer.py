# -*- coding: utf-8 -*-
import io
from bengali_stemmer.rafikamal2014.parser import RafiStemmer
from nltk.corpus.reader import PlaintextCorpusReader
from nltk import RegexpTokenizer
import re
import csv

with open('f:/dataset_fake.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} dsfjksd {row[1]}')
            line_count += 1
        print(f'total {line_count}.')

my_stemmer = RafiStemmer()

directory = 'F:/Minhaz/GitHubRepo/Fake_N_D/Our_Code/'
corpus_dir = directory + 'corpus/'
w_t = RegexpTokenizer("[\u0980-\u09FF']+")
corpus = PlaintextCorpusReader(corpus_dir, r'.*\.txt', word_tokenizer=w_t)

corpus_text = []

for file in corpus.fileids():
    corpus_text.append([corpus.words(file)])
corpus_text = [[re.sub(r'\d+', '', word) for word in document]for document in corpus_text]

#vectorizer = TfidfVectorizer()
#response = vectorizer.fit_transform(corpus_text)
f_out = io.open('f:/out.txt', 'w', encoding='utf-8')
#my_stemmer.stem_word('করছে')
'''
for words in c_words:
    f_out.write(my_stemmer.stem_word(words) + '\t')
f_out.close()
'''