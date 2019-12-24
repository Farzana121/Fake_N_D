# -*- coding: utf-8 -*-
import io
from bengali_stemmer.rafikamal2014.parser import RafiStemmer
from nltk.corpus.reader import PlaintextCorpusReader
from nltk import RegexpTokenizer
import re

my_stemmer = RafiStemmer()

directory = 'F:/Minhaz/GitHubRepo/Fake_N_D/Minhaz/'
corpus_dir = directory + 'corpus/'
w_t = RegexpTokenizer("[\u0980-\u09FF']+")
corpus = PlaintextCorpusReader(corpus_dir, r'.*\.txt', word_tokenizer=w_t)
c_words = corpus.words()


f_out = io.open('f:/out.txt', 'w', encoding='utf-8')
#my_stemmer.stem_word('করছে')
for words in c_words:
    f_out.write(my_stemmer.stem_word(words) + '\t')
f_out.close()