from src.datamanager import DataManager

# this section of code holds a class for convinient configs


class Config:
    def __init__(self, number):
        # convert int to fitting string
        str_number = str(number)
        if number < 10:
            str_number = "0" + str_number

        # configure the path to the texts
        self.DM = DataManager("corpus/raw/" + str_number + ".txt",
                              "corpus/processed/" + str_number + ".txt",
                              "corpus/resoluted/" + str_number + ".txt",
                              "corpus/xml/" + str_number + ".xml",
                              )

    doPreprocessing = False

    # configure, which criterias to apply
    Rules = {
        "definiteness": False, #worse
        "giveness": True,
        "indicatingVerbs": True,  
        "lexicalReiteration": True,
        "sectionHeadingPreference": True,
        "nonPrepositionalNPs": True,
        "collocationPatternRef": True,
        "immediateReference": True,
        "referentialDistance": True,
        "termPreference": True,
        "quotationMarks": True,
    }
