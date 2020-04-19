import copy

# this part of the code holds the tester class to test if
# the results of the system where right


class Tester:
    def __init__(self, DM):
        self.data = DM.readXML()
        # these are just counters
        self.right = 0
        self.candidateWasThereCount = 0
        self.randomBase = 0
        self.nearestBase = 0
        self.allProns = 0
        self.allRightProns = self.calculateAllRightProns()

    # this method does all the testing
    def doTests(self, pron, best):
        # check if the given resolution is correct
        erg = self.resolutionIsRight(pron, best)

        if erg == "True":
            self.right += 1
        elif erg == "no res found":
            # if no resolution is found, it get ignored
            return
        elif erg == "no cand given":
            # if no candidate was found, there can be no right solution
            # therefore, no other tests are needed
            self.allProns += 1
            return

        # check random-baseline
        if self.resolutionIsRight(pron, pron.chooseRandomCand()) == "True":
            self.randomBase += 1

        # check nearest-baseline
        if self.resolutionIsRight(pron, pron.chooseNearestCand()) == "True":
            self.nearestBase += 1

        # check if the pronoun holds at least the right candidate
        if self.candidateWasThere(pron):
            self.candidateWasThereCount += 1

        self.allProns += 1

    # this method loops through the xml-file and searches for
    # resolutions for the given pronoun
    def resolutionIsRight(self, pron, best):
        for node in self.data.getroot().findall("markable"):
            test = "word_" + str(pron.token.mainIndex)
            if test == node.attrib["span"] or test + ".." + test == node.attrib["span"] and node.attrib["type"] == "anaphoric":
                res = (
                    self.getResolution(node)
                    .replace("word_", "")
                    .replace("..", ",")
                    .split(",")
                )
                # if best is of the type list, no candidate was found
                if type(best) == list:
                    return "no cand given"
                # resolution can be a single word...
                if len(res) == 1:
                    if res[0] == best.token.mainIndex:
                        return "True"
                    else:
                        return "False"
                # .. or more the one. in this case, the resolution counts right,
                # if it is in the right range
                elif len(res) == 2:
                    if int(res[0]) <= int(best.token.mainIndex) <= int(res[1]):
                        return "True"
                    else:
                        return "False"
                else:
                    print("Something went wrong in tester.")
        return "no res found"

    # this method finds the nearest span that corefers to the given node
    def getResolution(self, nd):
        nearestSpan = ""
        for node in self.data.getroot().findall("markable"):
            if (node.attrib["coref_class"] == nd.attrib["coref_class"] and node.attrib["mention"] == "np"):
                nearestSpan = copy.copy(node.attrib["span"])
            if node.attrib["id"] == nd.attrib["id"]:
                break

        return nearestSpan

    # this method loops trough all candidates and checks if the right one
    # was included
    def candidateWasThere(self, pron):
        # first, find the solution...
        for node in self.data.getroot().findall("markable"):
            test = "word_" + str(pron.token.mainIndex)
            if test == node.attrib["span"] or test + ".." + test == node.attrib["span"]:
                res = (self.getResolution(node)
                       .replace("word_", "")
                       .replace("..", ",")
                       .split(","))
                found = False
                # ... then check if it was included
                for cand in pron.candidates:
                    if len(res) == 1:
                        if res[0] == cand.token.mainIndex:
                            found = True
                    elif len(res) == 2:
                        if int(res[0]) <= int(cand.token.mainIndex) <= int(res[1]):
                            found = True
                return found

    def calculateAllRightProns(self):
        all = 0
        for node in self.data.getroot():
            if node.attrib["mention"] == "pronoun" and node.attrib["type"] == "anaphoric":
                all += 1
        return all

    def printResults(self):
        if self.allProns > 0:
            return (
                (f"{format((self.right/self.allProns)/(self.candidateWasThereCount/self.allProns)*100, '.2f')} % right/candidate-Ratio")+"\n" +
                (f"{format((self.nearestBase/self.allProns)/(self.candidateWasThereCount/self.allProns)*100, '.2f')} % near/candidate-Ratio")+"\n" +
                (f"{format((self.randomBase/self.allProns)/(self.candidateWasThereCount/self.allProns)*100, '.2f')} % rand/candidate-Ratio")
            )
        else:
            return "Nothing"
