


print("Welcome to Nantucket!")
print("Loading...")

import os
from limerick import *

_limericks = [RandomLimerick, 
              DistributedLimerick, 
              BigramGraphDFSLimerick,
              BigramGraphDFSHeuristicLimerick,
              BigramGraphBFSHeuristicLimerick]

while True:
    print('\n')
    for i, lim in enumerate(_limericks):
        print('enter ' + str(i) + ' for ' + lim.name())
    print('enter q to quit')
    reply = raw_input("\n")
    try:
        index = int(reply)
        if index >= 0 and index < len(_limericks):
            l = _limericks[index]
            l = l()
            print('\n')
            print(l)
            print('\n\npress enter')
            raw_input('')
    except ValueError:
        pass
    if reply == 'q': 
        break
