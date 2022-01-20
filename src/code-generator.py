#!/usr/bin/python3

import numpy as np
import random
import os.path

numbersCount = 16**8
filename = 'Used_Randoms.npy'

def markMagicNumbersAsUsed(array):
    array[500] = True;

if os.path.exists(filename) == False:
    initialData = np.full((numbersCount), False, dtype=bool) # All array set to False
    markMagicNumbersAsUsed(initialData)
    np.save(filename, initialData) # saves 1 byte per each --> fix (bitarray)

usedNumbers = np.load(filename, mmap_mode='r+', allow_pickle=True)
# print ("array length = " + str(len(usedNumbers)))

while True:
    decimalRand = random.randint(0, numbersCount-1)
    if usedNumbers[decimalRand] == False:
        print (hex(decimalRand))
        usedNumbers[decimalRand] = True     # Update the number in file as used 
        break
