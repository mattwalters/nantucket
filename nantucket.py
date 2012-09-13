
#      Copyright 2012 Matthew Walters
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

print("Welcome to Nantucket!")
print("Loading...")

import os
from limerick import *

_limericks = [NonRhymingLimerick,
              RandomLimerick, 
              DistributedLimerick, 
              BigramGraphDFSLimerick,
              BigramGraphDFSHeuristicLimerick,
              BigramGraphBFSHeuristicLimerick]

while True:
    print('\n')
    for i, lim in enumerate(_limericks):
        print('enter ' + str(i) + ' for ' + lim.name())
    print('enter q to quit')
    reply = raw_input("\nnantucket>>>")
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
