# -*- coding: utf-8 -*-
from bengali_stemmer.rafikamal2014.parser import RafiStemmer
from nltk.corpus.reader import PlaintextCorpusReader
from nltk import RegexpTokenizer
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
#from sklearn.model_selection import KFold
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle

def generator(input_document, cl_output, batch_size):
    #generator not implemented yet, loading full training set
    x = np.zeros((batch_size, len(vocab_set)), dtype=np.bool)
    y = np.zeros(batch_size, dtype=np.bool)
    for i in range(batch_size):
        for w in input_document[i]:
            x[i, word_indices[w]] = 1
        y[i] = bool(cl_output[i])
    return (x, y)

def vectorizer(input_document):
    #generator not implemented yet
    x = np.zeros((len(input_document), len(vocab_set)), dtype=np.bool)
    for i in range(len(input_document)):
        for w in input_document[i]:
            x[i, word_indices[w]] = 1
    return x

def shuffle_training_set(doc_orig, class_orig):
    tmp_sentences = []
    tmp_class = []
    for i in np.random.permutation(len(doc_orig)):
        tmp_sentences.append(doc_orig[i])
        tmp_class.append(class_orig[i])
    
    return (tmp_sentences, tmp_class)

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

document_fake = []
for doc in corpus_fake_text:
    doc_fake = []
    for word in doc:
        stemmed_word = my_stemmer.stem_word(word)
        if len(stemmed_word) < 2:
            continue
        doc_fake.append(stemmed_word)
        vocab.append(stemmed_word)
    document_fake.append(doc_fake)

document_real = []
for doc in corpus_real_text:
    doc_real = []
    for word in doc:
        stemmed_word = my_stemmer.stem_word(word)
        if len(stemmed_word) < 2:
            continue
        doc_real.append(stemmed_word)
        vocab.append(stemmed_word)
    document_real.append(doc_real)

# Number of input document 1384
# Number of words in document 1,54,407 after stemming and dropping small words
vocab_set = sorted(set(vocab))
#Total unique words 14,392
#Building Dictionary
word_indices = dict((c, i) for i, c in enumerate(vocab_set))
vocab_file =  open('f:/Minhaz/GitHubRepo/Fake_N_D/Our_Code/vocabulary.txt', 'w', encoding='utf-8')
for words in vocab_set:
    vocab_file.write(words + '\n')
vocab_file.close()

document = document_fake + document_real
classification = []
for doc in document_fake:
    classification.append(0)
for doc in document_real:
    classification.append(1)

document, classification = shuffle_training_set(document, classification)
(X, Y) = generator(document, classification, len(document))

'''
# K-Fold Cross Validation
kf = KFold(n_splits=4)
modelMLP = MLPClassifier(hidden_layer_sizes = (64,32,16,8), max_iter=500)
for trn_i, tst_i in kf.split(X):
    modelMLP.fit(X[trn_i], Y[trn_i])
    print(modelMLP.score(X[tst_i], Y[tst_i]))
'''

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size =  0.2)
chosen_models = {}

chosen_models['f:/Fake_N_D/LogiRegr.sav'] = LogisticRegression(max_iter=200)
chosen_models['f:/Fake_N_D/GausNB.sav'] = GaussianNB()
chosen_models['f:/Fake_N_D/RanFor.sav'] = RandomForestClassifier(max_depth=2, random_state=0)
chosen_models['f:/Fake_N_D/KNeiCls.sav'] = KNeighborsClassifier(n_neighbors=2)
chosen_models['f:/Fake_N_D/DTree.sav'] = DecisionTreeClassifier()

for fname, model in chosen_models.items():
    print("working on " + fname)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print(classification_report(predictions, y_test))
    print("*************")
    pickle.dump(model, open(fname, 'wb'))
    
