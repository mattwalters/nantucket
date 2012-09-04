
import os
import limerick

cmudict_path = "cmudict.0.7a.txt"
if os.path.isfile(cmudict_path):
    cmudict = open(cmudict_path, "r")
    for line in cmudict:
        if not line.startswith(";;;"):
            limerick.Word(line)


limmerick = limerick.Limmerick()
limmerick.printOut()
