from src.token import Token
import copy
import xml.etree.ElementTree as ET

# this section of code holds the class DataManager, which is used for all reading & writing to files
# therefore, the DataManager holds all strings for splitter etc, so no errors can arise from typos
# the class is instantiated once in the Config, so all part of the code use the same Manager


class DataManager:
    def __init__(self, inPath, prePath, resPath, xmlPath):
        self.elSplit = "__"
        self.sentSplit = "############################"
        self.inPath = inPath
        self.prePath = prePath
        self.resPath = resPath
        self.xmlPath = xmlPath

    def readText(self):
        text = open(self.inPath, "r")

        return text.readlines()

    def resetResOutput(self):
        self.resetOutput(self.resPath)

    def writeResOutput(self, message):
        self.writeOutput(message, self.resPath)

    def resetPreOutput(self):
        self.resetOutput(self.prePath)

    def writePreOutput(self, message):
        self.writeOutput(message, self.prePath)

    # this method deletes the contents of an file
    def resetOutput(self, path):
        out = open(path, "w").close()

    # this method only appends to an file
    def writeOutput(self, message, path):
        out = open(path, "a")
        out.write(message)
        out.write("\n")
        out.close()

    # this is the method to create Token-Objects from written Token-Objects
    def createTokenFromString(self, inp):
        li = inp.split(self.elSplit)
        index = int(li[0])
        string = li[1]
        lemma = li[2]
        tag = li[3]
        gender = []

        if li[4] != "set()" and li[4] != "empty":
            gen = (li[4]
                   .replace("{", "")
                   .replace("}", "")
                   .replace("'", "")
                   .replace(" ", "")
                   )
            gender = gen.split(",")

        number = []

        if li[5] != "set()" and li[5] != "empty":
            num = (li[5]
                   .replace("{", "")
                   .replace("}", "")
                   .replace("'", "")
                   .replace(" ", "")
                   )
            number = num.split(",")

        poc = []

        if li[6] != "[]":
            pocs = (li[6]
                    .replace("[", "")
                    .replace("]", "")
                    .replace("\n", "")
                    .replace(" ", "")
                    )
            pocs = pocs.split(",")
            for pc in pocs:
                poc.append(int(pc))

        mainIndex = li[7].replace("\n", "")

        return Token(index, string, lemma, tag, gender, number, poc, mainIndex)

    def createSentsFromText(self):
        txt = open(self.prePath, "r")
        lines = txt.readlines()

        sents = []
        sent = []
        for line in lines:
            if line == self.sentSplit + "\n":
                sents.append(copy.deepcopy(sent))
                sent.clear()
            else:
                tok = self.createTokenFromString(line)
                sent.append(copy.deepcopy(tok))

        return sents

    sentCount = -1

    def printResult(self, sents, pron, best):
        if pron.sentID != self.sentCount:
            sent = ""
            for s in sents[pron.sentID]:
                sent += " " + s.string
            self.sentCount = pron.sentID
            self.writeResOutput("\n\n\n")
            self.writeResOutput(sent)
            self.writeResOutput("\n")

        str_out = self.createOutput(pron, best)
        self.writeResOutput(str_out)

    def createOutput(self, pron, best):
        return "%-10s%-10i%-48s" % (pron.token.string, pron.token.index, best,)

    # this method parses xml-data
    def readXML(self):
        root = ET.parse(self.xmlPath)
        return root
