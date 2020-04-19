# this part of the code holds the objects to work with:
# tokens, pronouns and candidates
import random
import copy

# just an information-holder
class Token:
    def __init__(self, index, string, lemma, tag, gender, number, poc, mainIndex):
        # a sentence-intern-index, often used in the prgram
        self.index = index
        self.string = string
        self.lemma = lemma
        self.tag = tag
        self.gender = gender
        self.number = number
        self.partsOfConst = poc
        # this index is unqiue in the whole text
        # its needed for the comparison with the xml-files
        self.mainIndex = mainIndex

# holds its token with all information and some additional informations
# and methods
class Pronoun:
    def __init__(self, sent, token):
        self.token = token
        self.sentID = sent
        self.candidates = []

    #returns a list of all candidate-scores
    def getAllScores(self):
        allScores = []
        for cand in self.candidates:
            allScores.append(cand.computeScore())
        return allScores

    # method for the random-baseline
    def chooseRandomCand(self):
        i = random.randint(0, len(self.candidates)-1)
        return self.candidates[i]

    # method fpr the nearest-baseline
    def chooseNearestCand(self):
        indexOfNearest = 0
        for i in range(0, len(self.candidates)):
            cand = self.candidates[i]
            if int(cand.token.mainIndex) > int(self.candidates[indexOfNearest].token.mainIndex):
                indexOfNearest = copy.copy(i)
        return self.candidates[indexOfNearest]


# holds its own token and all scores
class Candidate:
    def __init__(self, sent, token, index):
        self.token = token
        self.sentID = sent
        self.index = index
        self.Score = 0
        self.allScores = {}

    def __repr__(self):
        return (
            self.token.string
            + "("
            + str(self.sentID)
            + ","
            + str(self.index)
            + ") :"
            + str(self.Score)
        )

    # this method adds all scores up and returns the result
    def computeScore(self):
        for val in self.allScores.values():
            self.Score += val

        return self.Score
