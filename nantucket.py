
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
print('\n')
print("Welcome to Nantucket!")

from limerick import *
from line import *

__lines__ = [AnapesticLine, AmphibrachicLine]

__limericks__ = [RandomLimerick,
                LexigraphicLimerick,
                BigramGraphDFSLimerick,
                TrigramGraphDFSLimerick]

while True:
    print('\n')
    print('enter q to quit')
    print('\n')
    for i, lim in enumerate(__limericks__):
        print('enter ' + str(i) + ' for a ' + str(lim))
    limindex = raw_input('\nnantucket>>>')
    if limindex == 'q':
        break
    lim = None
    try:
        limindex = int(limindex)
        if limindex >= 0 and limindex < len(__limericks__):
            lim = __limericks__[limindex]
        else:
            raise ValueError
    except ValueError:
        print('bad input, try again...')
        continue
    print('\n')
    for i, l in enumerate(__lines__):
        print('enter ' + str(i) + ' for an ' + str(l))
    lineindex = raw_input('\nnantucket>>>')
    if lineindex == 'q':
        break
    ln = None
    try:
        lineindex = int(lineindex)
        if lineindex >= 0 and lineindex < len(__lines__):
            ln = __lines__[lineindex]
        else:
            raise ValueError
    except:
        print('bad input, try again...')
        continue
    print('generating limerick, please stand by...')
    print('\n\n')
    print(lim(ln))
    print('\n\n')
    raw_input('press enter to continue')
'''



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
'''
