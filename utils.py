import random

class NGramOutOfBoundsException(Exception):
    pass
class Utils:
    # choices should be an array of tuples, of the form (choice, weight)
    # where choice is the choice to be made, and weight is some percentage
    # chance that it should be picked.
    @staticmethod
    def randomWeightedChoice(choices):
        rand = random.random()
        sumSoFar = 0
        for choice, weight in choices:
            assert weight <= 1
            if (sumSoFar) <= rand < (sumSoFar + weight):
                return choice
            sumSoFar += weight
        assert False, "Shouldn't get here"

    @staticmethod
    def getNGramFromWordList(wordList, position, ngramSize):
        ngram = ""
        if position + ngramSize > len(wordList):
            raise NGramOutOfBoundsException("Index out of range")
        wordList = wordList[position:position + ngramSize]
        for word in wordList:
            ngram += word + " "
        ngram = ngram.rstrip()
        return ngram
