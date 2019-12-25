# -*- coding: utf-8 -*-
import io
from bengali_stemmer.rafikamal2014.parser import RafiStemmer
from nltk.corpus.reader import PlaintextCorpusReader
from nltk import RegexpTokenizer
import re

#Reading Datasets with word tokenization

dir_fake = 'f:/DataSetFake/'
dir_real = 'f:/DataSetReal/'

w_t = RegexpTokenizer("[\u0980-\u09FF']+")
corpus_fake = PlaintextCorpusReader(dir_fake, r'.*\.txt', word_tokenizer=w_t)
corpus_real = PlaintextCorpusReader(dir_real, r'.*\.txt', word_tokenizer=w_t)

corpus_fake_text = []
corpus_real_text = []

#Removing Numbers

for file in corpus_fake.fileids():
    corpus_fake_text.append(corpus_fake.words(file))
corpus_fake_text = [[re.sub(r'\d+', ' ', word) for word in document]for document in corpus_fake_text]

for file in corpus_real.fileids():
    corpus_real_text.append(corpus_real.words(file))
corpus_real_text = [[re.sub(r'\d+', ' ', word) for word in document]for document in corpus_real_text]

#Stemming for dimensionality reduction and removing hanging single/double letters
vocab = []
my_stemmer = RafiStemmer()
for doc in corpus_fake_text:
    for index, word in enumerate(doc):
        stemmed_word = my_stemmer.stem_word(word)
        if len(stemmed_word) < 3:
            del(doc[index])
        else:
            doc[index] = stemmed_word
            vocab.append(stemmed_word)

for doc in corpus_real_text:
    for index, word in enumerate(doc):
        stemmed_word = my_stemmer.stem_word(word)
        if len(stemmed_word) < 3:
            del(doc[index])
        else:
            doc[index] = stemmed_word
            vocab.append(stemmed_word)
#Total data size 14,675 words after stemming and dropping small words
#Should use Word-Embedding here
vocab.sort()
vocab_set = set(vocab)
#Total unique words 4,580


f_out = io.open('f:/out.txt', 'w', encoding='utf-8')
#my_stemmer.stem_word('করছে')
'''
for words in c_words:
    f_out.write(my_stemmer.stem_word(words) + '\t')
f_out.close()
'''