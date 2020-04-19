import de_core_news_sm
import copy
import re

from src.token import Token
from demorphy import Analyzer

# this section of code takes an normal text and preprocess them for the Pronoun-Resolution
# warning: due to the import of demorphy, this part of code cant be debugged (on my machine)
# therefore, the results are printed in a text-file, so the other parts of code can be debugged if you exclude this


def doPreprocessing(DM):
    # read the text
    text = DM.readText()
    # load spacy
    spacy = de_core_news_sm.load()
    sentences = []
    # mainIndex is needed for the comparison with xml-data
    mainIndex = 1
    # read the text sentence by sentence
    for sent in text:
        sentence = []
        # get the tags from spacy
        doc = spacy(sent)
        for tok in doc:
            # ignore spaces
            if tok.pos_ != "SPACE":
                # prune the token: not all spacy-infos are needed
                sentence.append(pruneToken(tok, mainIndex))
                mainIndex += 1
        # expand the token with morphological information
        expandToken(sentence)
        sentences.append(sentence)
    printAllToFile(sentences, DM)


# prunes all unneded infos from spacy
def pruneToken(nlptok, mainIndex):

    return Token(
        0,
        "".join(nlptok.string.split()),
        nlptok.lemma_,
        nlptok.pos_,
        "empty",
        "empty",
        [],
        mainIndex,
    )

# this method add gender, number and parts-of-constitute-infos


def expandToken(sent):
    # this is the morphy-analyzer
    analyzer = Analyzer(char_subs_allowed=True)
    # this is the sentence-intern-index
    index = 0
    for tok in sent:
        tok.index = index
        if tok.tag in ["NOUN", "DET", "ADJ", "PROPN", "PRON"]:
            appendGenderAndNumber(tok, sent, analyzer)
        index += 1
    appendPOCs(sent)
    clearPOCInfos(sent)


def printAllToFile(sents, DM):
    DM.resetPreOutput()
    for sent in sents:
        for tok in sent:
            DM.writePreOutput(
                str(tok.index)
                + DM.elSplit
                + tok.string
                + DM.elSplit
                + tok.lemma
                + DM.elSplit
                + tok.tag
                + DM.elSplit
                + str(tok.gender)
                + DM.elSplit
                + str(tok.number)
                + DM.elSplit
                + str(tok.partsOfConst)
                + DM.elSplit
                + str(tok.mainIndex)
            )
        DM.writePreOutput(DM.sentSplit)

# this method tries to get all possible gender and numbers


def appendGenderAndNumber(tok, sent, analyzer):
    s = analyzer.analyze(tok.string)
    gen = set()
    num = set()
    for anlyss in s:
        gen.add(anlyss.gender)
        num.add(anlyss.numerus)

    if tok.tag == "PRON":
        gen.update(proGender(tok.string))
        num.update(proNumber(tok.string))

    tok.gender = copy.deepcopy(gen)
    tok.gender.discard("")
    tok.gender.discard("noGender")
    tok.number = copy.deepcopy(num)
    tok.number.discard("")


def proGender(tok):
    # some pronouns are not fully implemented in demorphy
    # therefore, this hack-list is needed
    pronouns = {
        "ich": ["noGender"],
        "du": ["noGender"],
        "er": ["masc"],
        "sie": ["fem", "masc", "neut"],
        "es": ["neut"],
        "dieser": ["masc"],
        "dieses": ["neut"],
        "diese": ["fem", "masc", "neut"],
    }
    gen = set()
    try:
        li = pronouns[tok.lower()]
        for el in li:
            gen.add(el)
    except:
        return gen

    try:
        gen.remove("")
        return copy.deepcopy(gen)
    except:
        return copy.deepcopy(gen)


def proNumber(tok):
    # see above comment
    pronouns = {
        "ich": ["sing"],
        "du": ["sing"],
        "er": ["sing"],
        "sie": ["sing", "plu"],
        "es": ["sing"],
        "dieser": ["sing"],
        "dieses": ["sing"],
        "diese": ["sing", "plu"],
    }
    num = set()
    try:
        li = pronouns[tok.lower()]
        for el in li:
            num.add(el)
    except:
        return num
    try:
        num.remove("")
        return copy.deepcopy(num)
    except:
        return copy.deepcopy(num)

# this method tries to find simple patterns on the sentence-level
# so NPs can be found


def appendPOCs(sent):
    indices = []
    # regular expression for:
    # DET-ADJ*-NOUN/PROPN
    # DET-NOUN/PROPN
    # ADJ*-NOUN/PROPN
    rule = "(?:DET[0-9]{1,2} )?(?:ADJ[0-9]{1,2} )*(?:NOUN[0-9]{1,2}|PROPN[0-9]{1,2})"
    searchstr = ""
    teststr = ""

    # create a searchstring to find the pattern in the sentence
    for tok in sent:
        searchstr += tok.tag + str(tok.index) + " "
        teststr += " " + tok.string

    # try to find matches and append the poc-infos
    for match in re.findall(rule, searchstr):
        match = match.split(" ")
        inds = []
        for el in match:
            try:
                inds.append(int(el[-2:]))
            except:
                inds.append(int(el[-1]))

        for tok in sent:
            if tok.index in inds:
                tok.partsOfConst = copy.deepcopy(inds)


# this method tries to clear the gender and number information of an poc
# all parts of an NP should have the same set
# honestly, the method is a little messy
def clearPOCInfos(sent):
    doneIndex = []
    for tok in sent:
        if tok.index in doneIndex:
            continue
        if len(tok.partsOfConst) == 0:
            continue
        else:
            # check via sets, if the parts of the NP aggree in number & gender
            gen = set()
            num = set()
            ind = tok.partsOfConst
            for i in range(len(tok.partsOfConst)):
                doneIndex.append(ind[i])
                if i == 0:
                    gen = copy.deepcopy(sent[ind[i]].gender)
                    num = copy.deepcopy(sent[ind[i]].number)
                else:
                    if gen.isdisjoint(sent[ind[i]].gender):
                        gen = set()
                    else:
                        gen = gen.intersection(sent[ind[i]].gender)
                        gen.discard("")
                    if num.isdisjoint(sent[ind[i]].number):
                        num = set()
                    else:
                        num = num.intersection(sent[ind[i]].number)
                        num.discard("")

            if len(gen) == 0:
                for i in tok.partsOfConst:
                    if sent[i].tag in ["NOUN", "PROPN"]:
                        gen = copy.deepcopy(sent[i].gender)
            if len(num) == 0:
                for i in tok.partsOfConst:
                    if sent[i].tag in ["NOUN", "PROPN"]:
                        num = copy.deepcopy(sent[i].number)

            for i in tok.partsOfConst:
                sent[i].gender = copy.deepcopy(gen)
                sent[i].number = copy.deepcopy(num)
