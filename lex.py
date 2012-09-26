
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


import nltk, re, random
from nltk.corpus import brown
from collections import defaultdict


""" This module provides lexigraphical resources used
    for constructing Limericks. Construction of resources is
    lazy and memoized.

    1. terms        A set of terminal punctuation characters.
                    
    2. puncts       A set of punctuation; a superset of terms

    3. sents        A list of sentences used to construct other
                    lexigraphic resrouces
    
    3. lexicon      A set of all words and punctuation used in
                    this module. The lexicon does not contain all
                    dictionary words. Instead it contains only words
                    for which there is sufficient information
                    (pronunciation, syllables, etc).

    5. prondict     A pronunciation dictionary provided by the Carnegie
                    Mellon pronunciation dictionary. The structure of
                    resource is different than that provided by
                    nltk.corpus.cmudict.dict(). Specifically a value is
                    a list of pronunciations where earch pronunciation is
                    a list of tuples of the form (phoneme, stress). If the
                    phoneme is not a vowel, then stress is None. Generally
                    there is a single stress per syllable. Stresses are
                    simplified to 0 for unstressed and 1 for stressed.
                    No secondary stress is considered.

    6. freqdist     A frequency distribution of the tokens in sents. Tokens
                    not present in lexicon are disregarded.

    7. ngrams       a dictionary of ngrams over sents. Only tokens present in
                    lexicon are considered. Convenience methods for bigrams
                    and trigrams simply wrap ngrams(n)

    8 ngramgraph    A dictionary of ngram graphs. An ngram graph is
                    constructed by taking the ngram and partitioning it
    

"""
    

def sents():
    if sents.memo is None:
        sents.memo = [[word.lower() for word in sent] for sent in brown.sents()]
    return sents.memo
sents.memo = None

def linkedsents():
    if linkedsents.memo is None:
        ls = [sent for sent in sents()]
        curr = None
        prev = None
        for sent in ls:
            prev = curr
            curr = sent
            if prev is not None:
                curr.insert(0, prev[-1])
        linkedsents.memo = ls
    return linkedsents.memo
linkedsents.memo = None

def lexicon():
    if lexicon.memo is None:
        l = set(prondict().keys())
        for punct in puncts():
            l.add(punct)
        lexicon.memo = l
    return lexicon.memo
lexicon.memo = None


# pronunciation dictionary #####################################################
################################################################################


def prondict():
    if prondict.memo is None:
        pd = nltk.corpus.cmudict.dict()
        for prons in pd.values(): # can be many prons
            for pron in prons:
                for i, phone in enumerate(pron):
                    # strip out stress indictaor
                    # create tuple: (phone, stress)
                    match = re.compile('\\d').search(phone)
                    stress = None
                    if match is not None: 
                        stress = match.group(0)
                        # remove stress idicator from phone
                        phone = phone.replace(stress, '') 
                        stress = int(stress)
                        # convert secondary stress indicator
                        # to no stress indicator
                        if stress == 2: stress = 0
                    # replace original value with tuple
                    pron[i] = (phone, stress)
        prondict.memo = pd
    return prondict.memo
prondict.memo = None


# punctuation  #################################################################
################################################################################

def terms():
    if terms.memo is None:
        terms.memo = ['.', '!', '?']
    return terms.memo
terms.memo = None

def randomterm():
    return random.choice(terms())

def puncts():
    if puncts.memo is None:
        puncts.memo = [',', ':', ';'] + terms()
    return puncts.memo
puncts.memo = None

def randompunct():
    return random.choice(puncts())

       
# frequency distribution #######################################################
################################################################################
 

def freqdist():
    if freqdist.memo is None:
        fd = nltk.FreqDist()
        for sent in sents():
            for word in sent:
                if word in lexicon():
                    fd.inc(word)
        freqdist.memo = fd
    return freqdist.memo
freqdist.memo = None



# ngram ########################################################################
################################################################################



def __ngrammaker__(n, s):
    ng = [ngram for sent in s
          for ngram in nltk.ngrams(sent, n)
          if all(token in lexicon() for token in ngram)]
    return ng

def ngrams(n):
    if n not in ngrams.memo:
        ngrams.memo[n] = __ngrammaker__(n, sents())
    return ngrams.memo[n]
ngrams.memo = {}
    

def bigrams():
    return ngrams(2)

def trigrams():
    return ngrams(3)



def linkedngrams(n):
    if n not in linkedngrams.memo:
        linkedngrams.memo[n] = __ngrammaker__(n, linkedsents())
    return linkedngrams.memo[n]
linkedngrams.memo = {}




# ngram graphs #################################################################
################################################################################

__front__ = lambda i, ngram: ngram[:i]
__back__ = lambda i, ngram: ngram[i:]

def __graphmaker__(n, ngfunc, keyfunc, valuefunc):
    ngg = defaultdict(lambda: defaultdict(int))
    for ngram in ngfunc(n):
        if all(token in lexicon() for token in ngram):
            for i in range(1, n):
                key = keyfunc(i, ngram)
                value = valuefunc(i, ngram)
                ngg[tuple(key)][tuple(value)] += 1
    return ngg
    

def ngramgraph(n):
    if n not in ngramgraph.memo:
        ngramgraph.memo[n] = __graphmaker__(n, ngrams, __front__, __back__)
    return ngramgraph.memo[n]
ngramgraph.memo = {}

def r_ngramgraph(n):
    if n not in r_ngramgraph.memo:
        r_ngramgraph.memo[n] = __graphmaker__(n, ngrams, __back__, __front__)
    return r_ngramgraph.memo[n]
r_ngramgraph.memo = {}
                    
def bigramgraph():
    return ngramgraph(2)

def r_bigramgraph():
    return r_ngramgraph(2)

def trigramgraph():
    return ngramgraph(3)

def r_trigramgraph():
    return r_ngramgraph(3)


def linkedngramgraph(n):
    if n not in linkedngramgraph.memo:
        linkedngramgraph.memo[n] = __graphmaker__(n, linkedngrams, __front__, __back__)
    return linkedngramgraph.memo[n]
linkedngramgraph.memo = {}


def r_linkedngramgraph(n):
    if n not in r_linkedngramgraph.memo:
        r_linkedngramgraph.memo[n] = __graphmaker__(n, linkedngrams, __back__, __front__)
    return r_linkedngramgraph.memo[n]
r_linkedngramgraph.memo = {}



# rhyme ########################################################################
################################################################################

def rhymedict():
    if rhymedict.memo is None:
        rd = defaultdict(list)
        for word in lexicon():
            if word not in puncts():
                for rhymekey in rhymekeys(word):
                    rd[rhymekey].append(word)
        rhymedict.memo = rd
    return rhymedict.memo
rhymedict.memo = None

def rhymekeys(word):
    keys = []
    for pron in prondict()[word]:
        # find occurance of last vowel
        lastvowel = 0
        for i, phone in enumerate(pron):
            if phone[1] is not None: lastvowel = i
        key = ''
        for phone in pron[lastvowel:]:
            key += phone[0]
        keys.append(key)
    return keys


def randomrhymepool():
    rd = rhymedict()
    return rd[random.choice(rd.keys())]




# stress #######################################################################
################################################################################

def stresscounts(word):
    return [len(stresskey) for stresskey in stresskeys(word)]

def stresskeys(word):
    return [[stress for phone, stress in pron
             if stress is not None]
            for pron in prondict()[word]]

def stressdict():
    if stressdict.memo is None:
        sd = defaultdict(list)
        for word in lexicon():
            if word not in puncts():
                stresskeys = [[stress for phone, stress in pron
                               if stress is not None]
                              for pron in prondict()[word]]
                for stresskey in stresskeys:
                    sd[tuple(stresskey)].append(word)
        stressdict.memo = sd
    return stressdict.memo
stressdict.memo = None

def legalstresswords(line):
    words = []
    keylen = len(line.stresses)
    for i in range(keylen):
        for word in stressdict()[tuple(line.stresses[i:])]:
            if not line.fits(word):
                raise Exception('word is not legal: ' + word)
            words.append(word)
    if line.words and line.words[0] not in puncts():
        words += puncts()
    return words

################################################################################




def lexigraphicsample(words):
    wordsdist = {}
    for word in words:
        wordsdist[word] = freqdist()[word]
    pd = nltk.probability.DictionaryProbDist(wordsdist, normalize=True)
    return pd.generate()

        


