# -*- coding: utf-8 -*-
import io
from bengali_stemmer.rafikamal2014.parser import RafiStemmer
from nltk.corpus.reader import PlaintextCorpusReader
from nltk import RegexpTokenizer
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report

#Reading Datasets with word tokenization
def generator(input_document, cl_output, batch_size = 16):
    #while True:
    x = np.zeros((batch_size, len(vocab_set)), dtype=np.bool)
    y = np.zeros(batch_size, dtype=np.bool)
    for i in range(batch_size):
        for w in input_document[i]:
            x[i, word_indices[w]] = 1
        y[i] = bool(cl_output[i])
        #yield x, y
    return (x, y)

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

document_fake_text = []
for doc in corpus_fake_text:
    doc_fake = []
    for word in doc:
        stemmed_word = my_stemmer.stem_word(word)
        if len(stemmed_word) < 2:
            continue
        doc_fake.append(stemmed_word)
        vocab.append(stemmed_word)
    document_fake_text.append(doc_fake)

document_real_text = []
for doc in corpus_real_text:
    doc_real = []
    for word in doc:
        stemmed_word = my_stemmer.stem_word(word)
        if len(stemmed_word) < 2:
            continue
        doc_real.append(stemmed_word)
        vocab.append(stemmed_word)
    document_real_text.append(doc_real)

# Number of input document 662
# Number of words in document 1,34,606 after stemming and dropping small words
vocab_set = sorted(set(vocab))
#Total unique words 14,210
#Building Dictionary
word_indices = dict((c, i) for i, c in enumerate(vocab_set))
indices_word = dict((i, c) for i, c in enumerate(vocab_set))

document = document_fake_text + document_real_text
classification = []
for doc in document_fake_text:
    classification.append(0)

for doc in document_real_text:
    classification.append(1)

(X, Y) = generator(document, classification, len(document))

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size =  0.1)
model = MLPClassifier(hidden_layer_sizes = (64,32,16,8), max_iter=500)
model.fit(X_train, y_train)

predictions = model.predict(X_train)
print("Report")
print(classification_report(predictions, y_train))

predictions = model.predict(X_test)
print("Report")
print(classification_report(predictions, y_test))




