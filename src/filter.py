import copy

from src.token import Pronoun, Candidate

# in this section of code, pronouns and their candidates are filtered


def doAllFilter(sents):
    prons = filterProNouns(sents)  # first, get all pronouns
    for pron in prons:
        # append candidates for each pronoun
        filterCandidatesForProNoun(pron, sents)

    return prons


def filterProNouns(sents):
    pronouns = []  # list for all pronouns, will be filled in the loop
    for i in range(len(sents)):
        for tok in sents[i]:  # iterate through tokens in sentences
            if tok.tag == "PRON":
                pronouns.append(Pronoun(i, tok))  # append recognized pronouns
            else:
                continue
    return pronouns


def filterCandidatesForProNoun(pronoun, sents):
    indexer = 0  # create Indices for Candidates
    for i in range(pronoun.sentID - 2, pronoun.sentID + 1):
        if i > -1:  # there is no sentence with -2 and -1
            for tok in sents[i]:
                if tok.tag in ["NOUN", "PROPN"]:  # possible heads of phrases
                    # check for gender & number agreement
                    if checkAgreement(pronoun.token, tok):
                        # check if np is mentioned before pronoun
                        if not (i == pronoun.sentID and tok.index > pronoun.token.index):
                            pronoun.candidates.append(
                                Candidate(i, tok, indexer))  # append cnadidate
                            indexer += 1


def checkAgreement(pron, tok):
    gender = False
    number = False

    if (pron.gender == []
        or tok.gender == []
        or "noGender" in pron.gender
        or "noGender" in tok.gender
        ):
        gender = True  # if the value is not distinct, everything fits

    if pron.number == [] or tok.number == []:
        number = True  # see above

    for el in pron.gender:
        if el in tok.gender:
            gender = True  # if one value is the same, possible agreement is given
        else:
            continue

    for el in pron.number:
        if el in tok.number:
            number = True  # see above
        else:
            continue

    return gender and number  # only true if both agrees
