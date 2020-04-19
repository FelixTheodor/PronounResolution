import xml.etree.ElementTree as ET

# just sort the elements by id

name = "19"


def sortchildrenby(parent, attr):
    parent[:] = sorted(
        parent, key=lambda child: int(child.get(attr).replace("markable_", ""))
    )


tree = ET.parse("corpus/xml/" + name + "_coref_level.xml")
root = tree.getroot()

sortchildrenby(root, "id")
for child in root:
    sortchildrenby(child, "id")

tree.write("corpus/xml/" + name + ".xml")
