from utils import Utils, NGramOutOfBoundsException
import random
import sys
import time

# A Markov Node maps a string to a probability that the string occurs.
class MarkovNode:
    def __init__(self, associations = 0, edges = {}):
        self.associations = associations 
        self.edges = edges.copy()

    def __str__(self):
        string = ""
        for word, percentage in self.edges.items():
            string += "\t" + word.rstrip() + ": " + str(percentage) + "\n"
        return string

    def addWord(self, word):
        self.associations += 1
        percentSum = 0
        for w in self.getWords():
            if w != word:
                self._setProbability(w, (self.associations - 1) * self.edges[w] / self.associations)
                percentSum += self.getProbability(w)
        self._setProbability(word, 1.0 - percentSum)

    def getProbability(self, word):
        if self.hasWord(word):
            return self.edges[word]
        else:
            return 0

    def copy(self):
        return MarkovNode(associations = self.associations, edges = self.edges)

    def hasWord(self, word):
        return word in self.edges

    def getWords(self):
        return self.edges.keys()

    def items(self):
        return self.edges.items();

    # We should be weary of the floating point errors here.
    # The percentages are not guaranteed add up to 1.0 after
    # its use. Empirically we can except at most a 10% error which is
    # pretty bad. However, it shouldn't matter much for our purposes.

    # But if we continue to use this method more generally in the
    # future, we should strongly consider refactoring.
    @staticmethod
    def meanCombine(nodes, weight = 4):
        for i in range(weight):
            nodes.append(nodes[len(nodes) - 1])
        summedNode = nodes[0].copy()
        for node in nodes[1:len(nodes)]:
            summedNode = MarkovNode._sumNodes(summedNode, node)
        summedNode = MarkovNode._multiplyBy(summedNode, 1.0 / float(len(nodes)))
        return summedNode

    # private 
    # PRIVATE METHODS WILL NOT ENSURE THAT THE SUM OF ALL PROBABILITIES ARE CLOSE TO ONE. USE WITH CAUTION
    def _setProbability(self, word, probability):
        self.edges[word] = probability

    @staticmethod
    def _multiplyBy(markovNode, num):
        newNode = markovNode.copy()
        for word in markovNode.getWords():
            a = newNode.getProbability(word) * num
            newNode._setProbability(word, a)
        return newNode
        
    @staticmethod
    def _sumNodes(markovNode1, markovNode2):
        newNode = MarkovNode(associations = markovNode1.associations + markovNode2.associations, edges = markovNode1.edges.copy())
        for word in markovNode2.getWords():
            newNode._setProbability(word, newNode.getProbability(word) + markovNode2.getProbability(word))
        return newNode

class MarkovChain:
    nodes = {}
    def __init__(self):
        self.nodes = {}

    def __str__(self):
        string = ""
        for word, node in self.nodes.items():
            print word
            print node
        return string

    def generateText(markovChain, length):
        string = ""
        state = random.choice(markovChain.nodes.keys())
        for i in range(length):
            if state not in markovChain.nodes:
                break
            state = MarkovChain.getNextState(markovChain.nodes[state])
            string += state + " "
        return string

    def addAssociation(self, word1, word2):
        if word1 not in self.nodes:
            self.nodes[word1] = MarkovNode()
        self.nodes[word1].addWord(word2)

    @staticmethod
    def getNextState(markovNode):
        return Utils.randomWeightedChoice(markovNode.items())

    @staticmethod
    def generate(string, ngramSize = 1, verbose = False):
        wordList = string.split()
        chain = MarkovChain()
        for i in range(len(wordList)):
            if verbose and i % 10000 == 0:
                sys.stdout.write("%d%%   \r" % ((100 * i) / len(wordList)) )
                sys.stdout.flush()
            try:
                ngram1 = Utils.getNGramFromWordList(wordList, i, ngramSize)
                ngram2 = Utils.getNGramFromWordList(wordList, i + ngramSize, ngramSize)
            except NGramOutOfBoundsException:
                break

            chain.addAssociation(ngram1, ngram2)

        return chain
