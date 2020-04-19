from src.token import Token
from src.criteria import Criteria

import operator

import copy

# this section of code creates a Ranker, that can apply criterias to a given pronoun & its candidates


class Ranker:
    def __init__(self, sents, pronoun, crit):
        self.pron = pronoun
        self.sents = sents
        self.criteria = crit

    # Main-Method of the Ranker
    def getBestCandidate(self):
        self.computeCandidateScores()
        return self.chooseBest()

    def computeCandidateScores(self):
        # compute the points for each single criteria
        if self.criteria["definiteness"]:
            Criteria.Definiteness(self, self)
        if self.criteria["giveness"]:
            Criteria.Giveness(self, self)
        if self.criteria["indicatingVerbs"]:
            Criteria.IndicatingVerbs(self, self)
        if self.criteria["lexicalReiteration"]:
            Criteria.LexicalReiteration(self, self)
        if self.criteria["sectionHeadingPreference"]:
            Criteria.SectionHeadingPreference(self, self)
        if self.criteria["nonPrepositionalNPs"]:
            Criteria.NonPrepositionalNPs(self, self)
        if self.criteria["collocationPatternRef"]:
            Criteria.CollocationPatternRef(self, self)
        if self.criteria["immediateReference"]:
            Criteria.ImmediateReference(self, self)
        if self.criteria["referentialDistance"]:
            Criteria.ReferentialDistance(self, self)
        if self.criteria["termPreference"]:
            Criteria.TermPreference(self, self)
        if self.criteria["quotationMarks"]:
            Criteria.QuotationMarks(self, self)

    def chooseBest(self):
        allScores = self.pron.getAllScores()
        try:
            # try to get the highest score
            maximumValue = max(allScores)
        except:
            # return a list, if this is not possible
            return [-1]

        bestCands = []

        # add all candidates, that have the best score
        for cand in self.pron.candidates:
            if cand.Score == maximumValue:
                bestCands.append(cand)

        # if there is more than one, further steps need to be done
        if len(bestCands) > 1:
            return self.getBestOfBests(bestCands)
        else:
            return bestCands[0]

    def getBestOfBests(self, bestCands):
        newBestCands = []
        # first, check for the immediate-reference-criteria
        if self.criteria["immediateReference"]:
            for cand in bestCands:
                if len(newBestCands) == 0:
                    newBestCands.append(copy.deepcopy(cand))
                else:
                    if (cand.allScores["immediateReference"] == newBestCands[0].allScores["immediateReference"]):
                        newBestCands.append(copy.deepcopy(cand))
                    elif (cand.allScores["immediateReference"] > newBestCands[0].allScores["immediateReference"]):
                        newBestCands = [copy.deepcopy(cand)]
                    else:
                        continue
            if len(newBestCands) == 1:
                return newBestCands[0]
            else:
                bestCands = copy.deepcopy(newBestCands)
                newBestCands = []
        # if still no decision, try the same with quotation-marks-criteria
        if self.criteria["quotationMarks"]:
            for cand in bestCands:
                if len(newBestCands) == 0:
                    newBestCands.append(copy.deepcopy(cand))
                else:
                    if (cand.allScores["quotationMarks"] == newBestCands[0].allScores["quotationMarks"]):
                        newBestCands.append(copy.deepcopy(cand))
                    elif (cand.allScores["quotationMarks"] > newBestCands[0].allScores["quotationMarks"]):
                        newBestCands = [copy.deepcopy(cand)]
                    else:
                        continue
            if len(newBestCands) == 1:
                return newBestCands[0]
            else:
                bestCands = copy.deepcopy(newBestCands)
                newBestCands = []

        # if nothing else helps, just chosse the nearest candidate
        for cand in bestCands:
            if len(newBestCands) == 0:
                newBestCands.append(copy.deepcopy(cand))
            else:
                if int(cand.token.mainIndex) > int(newBestCands[0].token.mainIndex):
                    newBestCands = [copy.deepcopy(cand)]

        return newBestCands[0]
