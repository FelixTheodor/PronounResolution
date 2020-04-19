import xml.etree.ElementTree as ET

# the corpus is already preprocessed, so this scripts do not need to run
# in order to start the system

name = "25"
tree = ET.parse("corpus/raw/" + name + ".de.xml")
root = tree.getroot()

out = open("corpus/raw/" + name + ".txt", "w")

for child in root:
    sents = child.findall("seg")
    for sent in sents:
        # print only the text without the tags
        out.write(sent.text + "\n")
