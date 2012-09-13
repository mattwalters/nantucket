
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
from nltk.corpus import brown
import limerick
import re
from collections import defaultdict
from random import *

_text = brown.words()

# create the pronunciation dictionary
_prondict = nltk.corpus.cmudict.dict()
for prons in _prondict.values(): # can be many prons
    for pron in prons:
        for i, phone in enumerate(pron):
            # strip out stress indictaor
            # create tuple: (phone, stress)
            match = re.compile('\\d').search(phone)
            stress = None
            value = phone
            if match is not None: 
                stress = match.group(0)
                value = phone.replace(stress, '')
                stress = int(stress)
                if stress == 2: stress = 0
            # replace original value with tuple
            pron[i] = (value, stress) 



# create the universe set. This is the set of all possible words
_universe = set(_prondict.keys())


# create a frequency distribution of all the words in the universe
_freqdist = nltk.FreqDist()
for word in _text:
    if word in _universe:
        _freqdist.inc(word)


# create a function that generates a sample based on the given freq dist
def sample(freqdist):
    return nltk.probability.MLEProbDist(freqdist).generate()
    



# create the bigram graph where bigram[1] --> bigram[0]
bigrams = nltk.bigrams(_text)
# create a defaultdict(defaultdict(int))
# there will be an implicit weight of 0 for all new edges
_bigramgraph = defaultdict(lambda: defaultdict(int))
for head, tail in bigrams:
    if head in _universe and tail in _universe:    
        _bigramgraph[tail][head] += 1 # increment edge weight


# create a function that takes a list of 


# create a function for finding a words rhyming key
# rhymekey is the last vowel phone concatenated with all following phones
def rhymekeys(word):
    if word in _universe:
        keys = []
        for pron in _prondict[word]:
            # find occurance of last vowel
            lastvowel = 0
            for i, phone in enumerate(pron):
                if phone[1] is not None: lastvowel = i
            key = ''
            for phone in pron[lastvowel:]:
                key += phone[0]
            keys.append(key)
        return keys
    else: return None


# create rhyme dictionary    
_rhymedict = defaultdict(list)
for word in _universe:
    for rhymekey in rhymekeys(word):
        _rhymedict[rhymekey].append(word)


# define a function for getting a tuple of the stresses (excluding all None values)
def stresskeys(word):
    keys = []
    for pron in _prondict[word]:
        key = [stress for word, stress in pron if stress is not None]
        keys.append(tuple(key))
    return keys

# create a dictionary of stresses where {stresskey : [wordone, wordtwo]}
_stressdict = defaultdict(list)
for word in _universe:
    for stresskey in stresskeys(word):
        _stressdict[stresskey].append(word)


# create a function that returns the union of all _stressdict lookups
# for stresskey[i:] for 0 <= i < len(stresskey)

def stresskeyunion(stresskey):
    words = []
    keylen = len(stresskey)
    for i in range(keylen):
        for word in _stressdict[tuple(stresskey[i:])]:
            words.append(word)
    return words

# create a function that produces a line group with rhymes at the end
# specify how many lines and how many feet per line
def linegroup(count, feet):
    linegroup = []
    rhymegroup = []
    for i in range(count):
        linegroup.append(limerick.Line(feet))
    rhymeset = []
    while len(rhymeset) < count:
        rando = choice(_rhymedict.values())
        rhymeset = set(rando).intersection(set(stresskeyunion(linegroup[0].stresses)))
    rhymelist = list(rhymeset)
    shuffle(rhymelist)
    for i in range(count):
        linegroup[i].add(rhymelist[i])
    return linegroup



## public access to lexicon resources ##

def universe():
    return _universe

def prondict():
    return _prondict

def bigramgraph():
    return _bigramgraph

def rhymedict():
    return _rhymedict

def stressdict():
    return _stressdict

def freqdist():
    return _freqdist
