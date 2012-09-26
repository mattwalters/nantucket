
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



 ###temporary hold for limericks 
class Limerick(object):

    def __init__(self):
        print('generating ' + self.__class__.name() + '...')
        self.lines = [
            Line(3), Line(3), 
            Line(2), Line(2), 
            Line(3)]
        self.construct()
        
    @abc.abstractmethod
    def construct(self):
        """
           This method should be overridden in
           subclasses of Limerick.
        """
        return

    def full(self):
        for line in self.lines:
            if not line.full(): return False
        return True


    def __str__(self):
        return reduce(lambda x,y: str(x) + '\n' + str(y), self.lines)

    def initrhymes(self):
        linegroupA = linegroup(3, 3)
        self.lines[0] = linegroupA[0]
        self.lines[1] = linegroupA[1]
        self.lines[4] = linegroupA[2]
        linegroupB = linegroup(2, 2)
        self.lines[2] = linegroupB[0]
        self.lines[3] = linegroupB[1]

    @staticmethod
    def name():
        return 'a limerick'
        
        


class RandomLimerick(Limerick):

    def construct(self):
        self.initrhymes()
        for line in self.lines:
            while not line.full():
                words = stresskeyunion(line.stresses)
                if len(words) > 0:
                    word = choice(words)
                    if line.fits(word): line.add(word)

    @staticmethod
    def name():
        return 'a random limerick'


class NonRhymingLimerick(Limerick):

    def construct(self):
        for line in self.lines:
            while not line.full():
                words = stresskeyunion(line.stresses)
                if len(words) > 0:
                    word = choice(words)
                    if line.fits(word): line.add(word)

    @staticmethod
    def name():
        return 'a non-rhyming limerick'



class DistributedLimerick(Limerick):
    
    def construct(self):
        self.initrhymes()
        for line in self.lines:
            while not line.full():
                words = stresskeyunion(line.stresses)
                if len(words) > 0:
                    word = sample(nltk.FreqDist(words))
                    if line.fits(word): line.add(word)
    @staticmethod
    def name():
        return 'a distributed limerick'



class BigramGraphDFSLimerick(Limerick):
    
    def construct(self):
        self.initrhymes()
        self.solution = (0, None)
        solutioncount = 0
        fringe = []
        bgg = lex.reversebigramgraph()
        fringe.append((copy.deepcopy(self.lines), self.lines[4].words[0]))
        while fringe:
            # unpack current context
            context = self.pop(fringe)
            currentlines = context[0]
            currentword = context[1]
            currentline = self.findcurrentline(currentlines)
            if currentline is None:  
                # we have found a complete solution, register it
                solutioncount += 1
                if not self.registersolution(currentlines, solutioncount):
                    self.lines = self.solution[1]
                    return
            else:                    
                # find all edges in the bgg
                # that also fit the stress structure
                # add them to the stack and continue graph search
                stresswords = stresskeyunion(currentline.stresses)
                bigrams = bgg[currentword]
                bigramwords = [key for key in bigrams]
                words = list(set(stresswords) & set(bigramwords))
                self.pushchildren(fringe, currentlines, words)
                
        # if the graph search finished then registersolution() didn't hault on a solution
        # most likely this indicated that the inital context supplied bu initrhymes() did
        # not lead to any complete solutions.
        # We should call self.construct() again. This will give us a new initial context
        # so graph search can be attemtped again.
        self.construct()
            
    def pop(self, fringe):
        """ this method abstracts popping an element off of the fringe.
            This way we can support DFS or BFS just by providing a seperate implementation.
            DFS by default.
        """
        return fringe.pop()

    def pushchildren(self, fringe, currentlines, words):
        """ This method abstract how a nodes children should be pushed to the fringe
            Default is random order
        """
        random.shuffle(words)
        for word in words:
            lines = copy.deepcopy(currentlines)
            self.findcurrentline(lines).add(word)
            fringe.append((lines, word))
        
    @staticmethod
    def name():
        return 'a bigram graph depth first search limerick'


    def registersolution(self, lines, solutioncount):
        """ This function is called when a solution if found.
            It also determines whether or not to continue the search.
            If we return True, the search continues, if we return False
            the search will hault and the currently registered solution
            will be the final solution.
            
            This implementation of solution haults the search after the first solution
            is found. Subclasses of BigramGraphSearchLimerick may wish to implement a
            different strategy. For example, applying an evaluation function to the first
            100 solutions found and haulting on the solution with the highest evalution.
        """
        self.solution = (0, lines)
        return False
 


    def findcurrentline(self, lines):
        """ This function steps through a list of lines in reverse order.
            It returns the first incomplete line it finds
            or None if all lines are complete
        """
        for i in range(len(lines)-1, -1, -1):
            if not lines[i].full():
                return lines[i]
            
            
        

class BigramGraphDFSHeuristicLimerick(BigramGraphDFSLimerick):

    def registersolution(self, lines, solutioncount):
        self.solution = max(self.solution, (evallines(lines), lines))
        return solutioncount < 10000

    @staticmethod
    def name():
        return 'a bigram graph depth first search limerick with heuristic'


class BigramGraphBFSHeuristicLimerick(BigramGraphDFSHeuristicLimerick):

    def pop(self, fringe):
        return fringe.pop(0)

    @staticmethod
    def name():
        return 'a bigram graph breadth first search limerick with heuristic'
    

  
  
