import copy

# this part of the code holds all the single methods for different criterias
# they are collected in the class Criteria for convenient & readable method-calls


class Criteria:
    def Definiteness(self, ranker):
        definit = ["der", "mein", "dies"]  # all definit german lemmas

        for cand in ranker.pron.candidates:
            score = -1  # indefinit scores -1, this is the standard

            for el in cand.token.partsOfConst:
                tok = ranker.sents[cand.sentID][el]
                if tok.tag == "DET" and tok.lemma.lower() in definit:
                    score = 0  # if there is a definit determiner, score of 0 is given
                else:
                    continue
            cand.allScores["definiteness"] = score

    def Giveness(self, ranker):
        firstNPS = {}
        # this loop filters all fist nps from every sentence
        for i in range(len(ranker.sents)):
            sent = ranker.sents[i]
            for tok in sent:
                if tok.tag in ["NOUN", "PROPN"]:
                    firstNPS[i] = tok.index
                    break

        # this loop check for every candidate if it is the first NP of its sentence
        for cand in ranker.pron.candidates:
            score = 0
            if firstNPS[cand.sentID] == cand.token.index:
                score = 1
            cand.allScores["giveness"] = score

    def IndicatingVerbs(self, ranker):
        indicatedNPs = {}
        listOfVerbs = [
            "diskutieren",
            "präsentieren",
            "illustrieren",
            "identifizieren",
            "zusammenfassen",
            "ausführen",
            "beschreiben",
            "definieren",
            "zeigen",
            "prüfen",
            "entwickeln",
            "betrachten",
            "berichten",
            "darlegen",
            "abwägen",
            "untersuchen",
            "erforschen",
            "ermöglichen",
            "analysieren",
            "studieren",
            "ausführen",
            "umgehen",
            "abdecken",
        ]

        # this loop checks for all sents, if an indicating verb is given
        for i in range(len(ranker.sents)):
            indicatedNPs[i] = []
            sent = ranker.sents[i]
            searching = False
            for tok in sent:
                if tok.tag in ["VERB"] and tok.lemma in listOfVerbs:
                    searching = True
                elif searching and tok.tag in ["NOUN", "PROPN"]:
                    indicatedNPs[i].append(tok.index)
                    searching = False
                else:
                    continue

        # if a candidate is in the same sentence like the verb, the criteria is fullfilled
        for cand in ranker.pron.candidates:
            score = 0
            if cand.token.index in indicatedNPs[cand.sentID]:
                score = 1
            cand.allScores["indicatingVerbs"] = score

    def LexicalReiteration(self, ranker):
        # check in the last 3 sentences for identical lemmas
        for cand in ranker.pron.candidates:
            counter = 0
            for i in range(cand.sentID - 2, cand.sentID + 1):
                try:
                    sent = ranker.sents[i]
                except:
                    continue
                for tok in sent:
                    if tok.lemma == cand.token.lemma:
                        counter += 1

            score = 0
            if counter == 0:
                print("Something went wrong on LexReit.")
            elif counter == 2:
                score = 1
            elif counter > 2:
                score = 2

            cand.allScores["lexicalReiteration"] = score

    def SectionHeadingPreference(self, ranker):
        # in the corpus, the first sent is always the section heading
        for cand in ranker.pron.candidates:
            score = 0
            if cand.sentID == 0:
                score = 1
            else:
                score = 0

            cand.allScores["sectionHeadingPreference"] = score

    def NonPrepositionalNPs(self, ranker):
        for cand in ranker.pron.candidates:
            score = 0
            # get the preceeding element of the candidate
            preceedingElementID = min(cand.token.partsOfConst) - 1
            try:
                if ranker.sents[cand.sentID][preceedingElementID].tag == "ADP":
                    score = -1
            except:
                score = 0

            cand.allScores["nonprepositionalNPs"] = score

    def CollocationPatternRef(self, ranker):
        for cand in ranker.pron.candidates:
            verb = None
            # first, check if preceeding or following element...
            preceedingElementID = min(cand.token.partsOfConst) - 1
            followingElementID = max(cand.token.partsOfConst) + 1

            # is an verb
            try:
                if ranker.sents[cand.sentID][preceedingElementID].tag == "VERB":
                    verb = ranker.sents[cand.sentID][preceedingElementID]
                if ranker.sents[cand.sentID][followingElementID].tag == "VERB":
                    verb = ranker.sents[cand.sentID][followingElementID]
            except:
                verb = None

            if verb == None:
                cand.allScores["collocationPatternRef"] = 0
                return

            score = 0
            # then search for other appeareances of that pattern
            for i in range(cand.sentID - 2, cand.sentID + 2):
                try:
                    sent = ranker.sents[i]
                except:
                    continue

                for tok in sent:
                    if tok != verb and tok.lemma == verb.lemma:
                        tok_before = sent[tok.index - 1]
                        if (
                            tok_before.lemma == cand.token.lemma
                            or tok_before.tag == "PRON"
                        ):
                            score = 2

                        tok_after = sent[tok.index + 1]
                        if tok_after.tag == "PRON":
                            score = 2
                        if len(tok_after.partsOfConst) > 0:
                            for i in range(len(tok_after.partsOfConst)):
                                if sent[i].lemma == cand.token.lemma:
                                    score = 2

            cand.allScores["collocationPatternRef"] = score

    # changed this to check for relative-clauses
    def ImmediateReference(self, ranker):
        candidate = -1
        # this loop gets the last NP in front of the pronoun
        for tok in ranker.sents[ranker.pron.sentID]:
            if tok.index < ranker.pron.token.index:
                if len(tok.partsOfConst) != 0:
                    candidate = tok.index
            else:
                break

        # this loop checks, if a candidate matches this last NP
        for cand in ranker.pron.candidates:
            score = 0
            if cand.token.index == candidate:
                # check, if the pronoun is preceeded by a punctuation
                if (
                    ranker.sents[ranker.pron.sentID][ranker.pron.token.index - 1].tag
                    == "PUNCT"
                ):
                    score = 2

            cand.allScores["immediateReference"] = score

    def ReferentialDistance(self, ranker):
        # this method checks if a sentence is "complex"
        def isComplex(sent):
            if len(sent) > 12:
                return True
            compl = False
            for tok in sent:
                if tok.string == ",":
                    compl = True
            return compl

        # a loop through all candidates
        for cand in ranker.pron.candidates:
            score = 0
            erg = ranker.pron.sentID - cand.sentID
            if erg == 0:
                if isComplex(ranker.sents[ranker.pron.sentID]):
                    # for complex sentences, candidates in the same part of the sentence
                    # score 3, so here is a check for commas in between the elemts
                    score = 3
                    for i in range(cand.token.index, ranker.pron.token.index):
                        tok = ranker.sents[cand.sentID][i]
                        if tok.tag == ",":
                            score = 2
                else:
                    # if the sentence is not complex, the score is 0!
                    score = 0
            elif erg == 1:
                score = 0
            elif erg >= 2:
                score = -1
            cand.allScores["referentialDistance"] = score

    def TermPreference(self, ranker):
        # baseline: if the tag is PROPN, its probably a Term of the field
        # the themes of the corpus are to variable to give a list of words
        for cand in ranker.pron.candidates:
            score = 0
            if cand.token.tag == "PROPN":
                score = 1
            cand.allScores["termPreference"] = score

    def QuotationMarks(self, ranker):
        # this method just loops trough the whole text and counts the quot-marks
        # so for a given element the status can be returned
        def isQuoted(sentID, tokID):
            count = 0
            for i in range(0, sentID+1):
                sent = ranker.sents[i]
                for tok in sent:
                    if i == sentID and tok.index == tokID:
                        break
                    if tok.string == "\"":
                        count += 1
            if count % 2 == 0:
                return "noQuote"
            else:
                return "Quote"

        pronStatus = isQuoted(ranker.pron.sentID, ranker.pron.token.index)

        # just a check, if the status is identical
        for cand in ranker.pron.candidates:
            candStatus = isQuoted(cand.sentID, cand.token.index)
            score = -2

            if candStatus == pronStatus:
                score = 2
            cand.allScores["quotationMarks"] = score
