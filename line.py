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

import lex, copy
from collections import defaultdict

class Foot(object):

    def __init__(self):
        self.pattern = []

    def __str__(self):
        return ''.join([str(stress) for stress in self.pattern])
        
class AnapesticFoot(Foot):

    def __init__(self):
        self.pattern = [0, 0, 1]

class AmphibrachicFoot(Foot):

    def __init__(self):
        self.pattern = [0, 1, 0]



class Line(object):
    
    def __init__(self, foot, count, rhymegroup):
        self.words = []
        self.stresses = []
        for i in range(count):
            self.stresses += foot().pattern
        self.rhymegroup = rhymegroup
        
        

    def fits(self, word):
        if self.full(): return False
        if word in lex.puncts():
            return not self.words or self.words[0] not in lex.puncts()
        else:
            stresskeys = lex.stresskeys(word)
            for stresskey in stresskeys:
                if len(stresskey) > self.stresses: continue
                stresszip = zip(reversed(stresskey), reversed(self.stresses))
                if all(x == y for x, y in stresszip): 
                    return True
            return False

    def needsrhyme(self):
        for word in self.words:
            if word not in lex.puncts(): return False
        return True


    def full(self):
        return not self.stresses
     
    def empty(self):
        return not self.words

    def add(self, word):
        if not self.fits(word):
            raise Exception('word does not fit: ' + word)

        if word in lex.puncts():
            self.words.insert(0, word)
        else:
            stresslen = len(min(lex.stresskeys(word), key=len))
            self.stresses = self.stresses[:-stresslen]
            self.words.insert(0, word)
            

    def __str__(self):
        out = []
        for i, word in enumerate(self.words):
            if word in lex.puncts() and i != 0:
                out[-1] += word
            else:
                out.append(word)
        if not self.full():
            out = [str(stress) for stress in self.stresses] + out
            out = [self.rhymegroup + ':'] + out
        return ' '.join(out)




class AnapesticLine(Line):

    def __init__(self, count, rhymegroup):
        Line.__init__(self, AnapesticFoot, count, rhymegroup)


class AmphibrachicLine(Line):

    def __init__(self, count, rhymegroup):
        Line.__init__(self, AmphibrachicFoor, count, rhymegroup)




class LineGroup(object):

    def __init__(self):
        self.lines = []
        self.rhymepools = {}
        self.rhymegroups = defaultdict(list)

    def addline(self, l):
        self.lines.append(l)
        self.rhymegroups[l.rhymegroup].append(l)
        

    def words(self):
        w = []
        for line in self.lines:
            for word in line.words:
                w.append(word)
        return w

    def lastnwords(self, n):
        w = self.words()
        if len(w) > n:
            w = w[:n]
        return tuple(w)

    def senttrunc(self, n):
        w = []
        for word in self.lastnwords(n):
            w.append(word)
            if word in lex.terms(): break
        return tuple(w)

    
    def currentline(self):
        for line in reversed(self.lines):
            if not line.full(): return line
        return None

    def full(self):
        for line in self.lines:
            if not line.full(): return False
        return True

    def rhymepool(self, rhymegroup):
        if rhymegroup not in self.rhymepools:
            rhymepool = None
            while not rhymepool:
                rhymepool = lex.randomrhymepool()
                for line in self.rhymegroups[rhymegroup]:
                    if not any(line.fits(word) for word in rhymepool):
                        rhymepool = []
            self.rhymepools[rhymegroup] = rhymepool
        return self.rhymepools[rhymegroup]
