
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


import lex, line, copy, random, abc


class Limerick(object):

    def __init__(self, l):
        self.structure = [(3, 'A'), (3, 'A'), (2, 'B'), (2, 'B'), (3, 'A')]
        self.linetype = l
        self.construct()


    def construct(self):
        self.linegroup = line.LineGroup()
        for count, rhymegroup in self.structure:
            self.linegroup.addline(self.linetype(count, rhymegroup))

    def __str__(self):
        return '\n'.join([str(l) for l in self.linegroup.lines])



## Independent-Line Limericks ########################################################

  
class IndependentLineLimerick(Limerick):

    def __init__(self, l):
        Limerick.__init__(self, l)
        for line in self.linegroup.lines:
            while not line.full():
                if line.empty():
                    # we must rhyme
                    self.addrhyme(line)
                else:
                    # select a random legal word
                    self.addword(line)

    def addrhyme(self, l):
        legalstresswords = lex.legalstresswords(l)
        legalwords = [word for word in self.linegroup.rhymepool(l.rhymegroup)
                      if word in legalstresswords]
        l.add(random.choice(legalwords))

    @abc.abstractmethod
    def addword(self, l):
        pass


class RandomLimerick(IndependentLineLimerick):

    def __init__(self, l):
        IndependentLineLimerick.__init__(self, l)

    def addword(self, l):
        l.add(random.choice(lex.legalstresswords(l)))

class LexigraphicLimerick(IndependentLineLimerick):

    def __init__(self, l):
        IndependentLineLimerick.__init__(self, l)
        
    def addword(self, l):
        l.add(lex.lexigraphicsample(lex.legalstresswords(l)))
                

########################################################################################


class NgramGraphSearchLimerick(Limerick):

    def __init__(self, n, l):
        Limerick.__init__(self, l)
        self.n = n
        self.ngramgraph = lex.r_linkedngramgraph(self.n)
        self.fringe = None
        self.search()

    def search(self):
        self.primefringe()
        while self.fringe:
            currentlinegroup = self.popfringe()
            # check if we are done
            if currentlinegroup.full():
                if self.registersolution(currentlinegroup): return
            # we are not done, add children to fringe
            currentline = currentlinegroup.currentline()
            lastwords = currentlinegroup.senttrunc(self.n-1)
            nextwords = [words[-1] for words in self.ngramgraph[lastwords]]
            nextwords = [word for word in nextwords if currentline.fits(word)]
            # if we need to rhyme, whittle down next words...
            if currentline.needsrhyme():
                rp = currentlinegroup.rhymepool(currentline.rhymegroup)
                nextwords = [word for word in nextwords if word in rp]
            # order nextwordds. default is random, but you can override method
            # to order children going into the fringe, for A* for example
            nextwords = self.ordernextwords(nextwords)
            for nextword in nextwords:
                lg = copy.deepcopy(currentlinegroup)
                lg.currentline().add(nextword)
                self.fringe.append(lg)
        self.search()
                    
    def ordernextwords(self, nextwords):
        random.shuffle(nextwords)
        return nextwords
            
    def popfringe(self):
        return self.fringe.pop()
    

    def registersolution(self, linegroup):
        self.linegroup = linegroup
        return True

    def primefringe(self):
        self.construct()
        lg = self.linegroup
        l = lg.currentline()
        l.add(lex.randomterm())
        self.fringe = []
        self.fringe.append(copy.deepcopy(lg))



class BigramGraphDFSLimerick(NgramGraphSearchLimerick):

    def __init__(self, l):
        NgramGraphSearchLimerick.__init__(self, 2, l) 
            

class TrigramGraphDFSLimerick(NgramGraphSearchLimerick):

    def __init__(self, l):
        NgramGraphSearchLimerick.__init__(self, 3, l)


class BigramGraphBFSLimerick(NgramGraphSearchLimerick):

    def __init__(self, l):
        print('warning, this limerick requires a prohibitive amount of space...')
        print('be prepared to kill process...')
        NgramGraphSearchLimerick.__init__(self, 2, l)

    def popfringe(self):
        return self.fringe.pop(0)
        






        




        

    

