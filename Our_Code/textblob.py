# -*- coding: utf-8 -*-
import io
from bengali_stemmer.rafikamal2014.parser import RafiStemmer

my_stemmer = RafiStemmer()

f = io.open('F:/Minhaz/GitHubRepo/Fake_N_D/Minhaz/corpus/1.txt', 'r', encoding='utf-8')
text = f.read()
blob_obj = TextBlob(text)

f_out = io.open('f:/out.txt', 'w', encoding='utf-8')

#my_stemmer.stem_word('করছে')
for words in :
    f_out.write(my_stemmer.stem_words(words) + '\t')
f_out.close()