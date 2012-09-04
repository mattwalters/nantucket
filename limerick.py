
import time
import re
import random
from random import shuffle


rhymeGroups = dict()
stressGroups = dict() 

def randomValue(list):
    return list[random.randint(0, len(list)-1)]

def stressKey(stresses):
    key = ""
    for stress in stresses:
        key += str(stress)
    return key

def stressSubsetUnion(stresses):
    keysubsets = []
    length = len(stresses)
    for i in range(0, length):
        keysubsets.append(stressKey(stresses[i:length]))
    stressUnion = []
    for key in keysubsets:
        if key in stressGroups:
            stressUnion.extend(stressGroups[key])
    return stressUnion

class Word(object):

    def __init__(self, line):
        ## store word and
        ## list of tuples (phone, stress) ; -1 for no stress
        alphaNumPattern = re.compile('\\w+')
        tokens = alphaNumPattern.findall(line)
        self.word = tokens[0]
        self.data = []
        for i in range(1, len(tokens)):
           token = tokens[i]
           numPattern = re.compile('\\d')
           stressMatch = numPattern.search(token)
           stress = None  # default
           if stressMatch: 
               stress = stressMatch.group(0)
               token = token.replace(stress, "")
           self.data.append((token, stress))
        ## find rhyme key (last vowel plus following consonants)
        lastvowel = 0
        for i in range(len(self.data)):
            stress = self.data[i][1]
            if stress:
                lastvowel = i
        end = ""
        for phone in self.data[lastvowel:]: # slice
            end += phone[0]
        # add to rhymeGroups
        if end in rhymeGroups.keys():
            rhymeGroups[end].append(self)
        else:
            rhymeGroups[end] = [self]      
        # add word to stressGroups
        key = stressKey(self.stresses())
        if key in stressGroups:
            stressGroups[key].append(self)
        else:
            stressGroups[key] = [self]
    
    def stresses(self):
        stresses = []
        for tup in self.data:
            stress = tup[1]
            if stress:
                stresses.append(stress)
        return stresses

    def phones(self):
        phones = []
        for tup in self.data:
            phones.append(tup[0])

class Line(object):
    
    def __init__(self, feet):
        self.stresses = []
        self.words = []
        for i in range(feet):
            self.stresses.append(0)
            self.stresses.append(0)
            self.stresses.append(1) 
    
    def getline(self):
        s = ""
        for word in self.words:
            s += (word + " ")
        return s.lower()
            
    
    def possibleWords(self):
        possible = []
        keySubsets = self.keySubset()
        for key in keySubsets:
            if key in stressGroups:
                possible.append(stressGroups[key])
        return possible
    
    def full(self):
        return len(self.stresses) == 0

    def stuff(self, word):
        self.words.insert(0, word.word)
        for i in range(len(word.stresses())):
            self.stresses.pop(len(self.stresses)-1)

class Limmerick(object):
    
    def __init__(self):
       self.lineGroups = ( [Line(3), Line(3), Line(3)], 
                           [Line(2), Line(2)] )
       for lineGroup in self.lineGroups:
           self.rhymeLineGroup(lineGroup)
       for lineGroup in self.lineGroups:
           for line in lineGroup:
               self.stuffLine(line)
       
    def stuffLine(self, line):
        while not line.full():
            stressWords = stressSubsetUnion(line.stresses)
            word = randomValue(stressWords)
            line.stuff(word)

    def rhymeLineGroup(self, lineGroup):
        rhymes = []
        stressWords = stressSubsetUnion(lineGroup[0].stresses)
        while len(rhymes) < len(lineGroup):
            rhymeGroup = randomValue(rhymeGroups.values())
            rhymes = list(set(stressWords) & set(rhymeGroup))
        shuffle(rhymes)
        for line in lineGroup:
            line.stuff(rhymes.pop())

    def printOut(self):
        print(self.lineGroups[0][0].getline())
        print(self.lineGroups[0][1].getline())
        print(self.lineGroups[1][0].getline())
        print(self.lineGroups[1][1].getline())
        print(self.lineGroups[0][2].getline())

        


