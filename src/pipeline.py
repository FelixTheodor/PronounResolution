from src.config import Config
from src.filter import doAllFilter
from src.ranker import Ranker
from src.tester import Tester

# this part of the code controls the order of the methods called


def resoluteProNouns(num):
    # create all shared objects
    config = Config(num)
    DM = config.DM
    tester = Tester(DM)

    if config.doPreprocessing:  # defaults to false for debugging
        from src.preprocess import (
            doPreprocessing,
        )  # as soon as this line is included, debugger hangs due to demorphy

        doPreprocessing(DM)

    sents = DM.createSentsFromText()  # read preprocessed sentences
    prons = doAllFilter(sents)  # filter pronouns & their candidates

    DM.resetResOutput()

    for pron in prons:  # for each pronoun...
        if pron.token.lemma in ["mein", "ich","dies", "der", "was", "seinen"]:
            ranker = Ranker(sents, pron, config.Rules)  # ...create a Ranker...
            best = ranker.getBestCandidate()  # and get the best cands
            tester.doTests(pron, best)  # test if the choosen candidate is right
            DM.printResult(sents, pron, best)  # print the result to file

    DM.writeResOutput("\n\n\n#########################\n" +
                      tester.printResults())

    return tester
