#nantucket

A limerick generator written in python.

A [limerick](http://en.wikipedia.org/wiki/Limerick_(poetry) is a poetic form consisting of 5 lines of antidactyl meter with a
with a strict rhyme scheme of AABBA.

###Limerick Form:  
A ^^- ^^- ^^-  
A ^^- ^^- ^^-  
B ^^- ^^-    
B ^^- ^^-  
A ^^- ^^- ^^-  

##Usage


You must have limerick.py, nantucket.py, and the cmu dictionary text file in the same directory. 
Do not rename the dictionary. Simply run "python nantucket.py". Once the program parses the dictionary,
you will be able to generate limericks on demand by pressing enter. To quit, press q.


##Roadmap#

This code is just a prototype. It generates limericks that satisfy the requirements of the limerick form,
but does not yet attempt to generate aesthetic poetry.
I have very little experience with natural language processing, so any contributions are very welcome.
I have a few ideas about how to generate limericks that satisfy the structural requirements of a limerick and
create reasonably coherent and interesting poems. The next proposols are ordered by how complex I think they would be to implement.

1. My first observation from using the prototype is that an extremely esoteric word is as likely to be included as very common words.
It is said that 80% of language is spoken using only 20% of the lexicon. As it stands now, the probability distribution
over the words in the cmu dictionary is uniform and does not reflect the actual distribution of word frequency. We can 
use a large data set (maybe from the nltk corpus) to find ground truth of word frequency.

2. We can also look at the probability of a word following another word. Again using a large data set we can construct a
graph where nodes are words and weighted edges indicate the probability of the two words occuring next to each other.
In the worst case this method could be prohibitively space ineffecient at O(words^2) but I think its ok to assume a sparse
graph.

3. Use the nltk library for tagging parts of speech to provide structured data for human authored limericks. Use a machine learning
library to create strings of words that match that structure. Possibly provide some manually structured data.

I would also like to develop a module that allows the output of the generator to be piped to a speech generator. 
If a machine is going to write my poetry, I want it to read it to me as well.