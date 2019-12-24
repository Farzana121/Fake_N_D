from bengali_stemmer.rafikamal2014.parser import RafiStemmer  # noqa: F401
import os

my_stemmer = RafiStemmer()
my_stemmer.stem_word('করছে')
