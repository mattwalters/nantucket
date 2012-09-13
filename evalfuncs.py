
import nltk


def randomeval(lines):
    return random()


def rawstring(lines):
    return ' '.join([line.__str__() for line in lines])

_lexical_diversity_coeff = 1

def lexicaldiversity(text):
    tokens = nltk.word_tokenize(text)
    return _lexical_diversity_coeff * (float(len(set(tokens))) / float(len(tokens)))


_funcs = [lexicaldiversity]

def evallines(lines):
    text = rawstring(lines)
    values = [func(text) for func in _funcs]
    return reduce(lambda x, y: x + y, values) 
  
  
