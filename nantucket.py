
import os
import limerick

print("Welcome to Nantucket!")
print("loading cmu dictionary...")
cmudict_path = "cmudict.0.7a.txt"
if os.path.isfile(cmudict_path):
    cmudict = open(cmudict_path, "r")
    for line in cmudict:
        if not line.startswith(";;;"):
            limerick.Word(line)


while True:
    reply = raw_input("press enter for a limerick. press q to quit.\n")
    if reply == "q": break
    limmerick = limerick.Limmerick()
    limmerick.printOut()
    print("\n")
