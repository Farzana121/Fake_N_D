# -*- coding: utf-8 -*-
from bengali_stemmer.rafikamal2014.parser import RafiStemmer
from nltk.corpus.reader import PlaintextCorpusReader
from nltk import RegexpTokenizer
import re
import numpy as np

#Reading Datasets with word tokenization
dir_fake = 'f:/TitleFake/'
dir_real = 'f:/TitleReal/'

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
vocab_fake = []
vocab_real = []
my_stemmer = RafiStemmer()

document_fake_text = []
for doc in corpus_fake_text:
    doc_fake = []
    for word in doc:
        stemmed_word = my_stemmer.stem_word(word)
        if len(stemmed_word) < 2:
            continue
        doc_fake.append(stemmed_word)
        vocab_fake.append(stemmed_word)
    document_fake_text.append(doc_fake)

document_real_text = []
for doc in corpus_real_text:
    doc_real = []
    for word in doc:
        stemmed_word = my_stemmer.stem_word(word)
        if len(stemmed_word) < 2:
            continue
        doc_real.append(stemmed_word)
        vocab_real.append(stemmed_word)
    document_real_text.append(doc_real)

vocab_fake = sorted(set(vocab_fake))
fake_dict = {}
for word in vocab_fake:
    fake_dict[word] = 0
for doc in document_fake_text:
    for word in doc:
        fake_dict[word] += 1
fake_top = sorted(fake_dict, key = fake_dict.get, reverse=True)[:10]

vocab_real = sorted(set(vocab_real))
real_dict = {}
for word in vocab_real:
    real_dict[word] = 0
for doc in document_real_text:
    for word in doc:
        real_dict[word] += 1
real_top = sorted(real_dict, key = real_dict.get, reverse=True)[:10]

tf_title = []
for word in fake_top:
    freq = 0
    if word in real_dict:
        freq = real_dict[word]
    tf_title.append([word, fake_dict[word], freq])

for word in real_top:
    freq = 0
    if word in fake_dict:
        freq = fake_dict[word]
    tf_title.append([word, freq, real_dict[word]])

# Number of input document 662
# Number of words in document 1,34,606 after stemming and dropping small words
vocab_set = sorted(set(vocab))
#Total unique words 14,210
#Building Dictionary
word_indices = dict((c, i) for i, c in enumerate(vocab_set))
indices_word = dict((i, c) for i, c in enumerate(vocab_set))

