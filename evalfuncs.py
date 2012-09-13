
#      Copyright 2012 Matthew Walters
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

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
  
  
