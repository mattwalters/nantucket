from lex import *
import abc
import copy
from evalfuncs import *
import random

class Line(object):
    

    def __init__(self, feet):
        self.words = []
        self.stresses = []
        for i in range(feet): self.stresses += [0, 0, 1]
        

    def fits(self, word):
        if word is not None:
            for stresskey in stresskeys(word):
                match = True
                keylen = len(stresskey)
                if keylen > len(self.stresses): continue
                stresstail = self.stresses[-keylen:]
                for i in range(keylen):
                    if stresstail[i] is not stresskey[i]: match = False
                if match: return True
        return False


    def add(self, word):
        if self.fits(word):
            stresskey = min(stresskeys(word), key=len)
            keylen = len(stresskey)
            self.stresses = self.stresses[:-keylen]
            self.words.insert(0, word)


    def full(self):
        return len(self.stresses) == 0

    def __str__(self):
        out = self.words
        if not self.full(): out = [str(stress) for stress in self.stresses] + out 
        return ' '.join(out)


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
        return 'a Limerick'
        
        


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
        return 'a RandomLimerick'



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
        return 'a DistributedLimerick'



class BigramGraphDFSLimerick(Limerick):
    
    def construct(self):
        self.initrhymes()
        self.solution = (0, None)
        solutioncount = 0
        fringe = []
        bgg = bigramgraph()
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
        return 'a BigramGraphDFSLimerick'


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
        return solutioncount < 1

    @staticmethod
    def name():
        return 'a BigramGraphDFSHeuristicLimerick'


class BigramGraphBFSHeuristicLimerick(BigramGraphDFSHeuristicLimerick):

    def pop(self, fringe):
        return fringe.pop(0)

    @staticmethod
    def name():
        return 'a BigramGraphBFSHeuristicLimerick'
    
