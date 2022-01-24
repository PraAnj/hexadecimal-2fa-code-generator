#!/usr/bin/python3

import numpy as np
import random
import os.path
import mmap
from bitarray import bitarray

numbersCount = 16**8
rootFileName = 'ROOT'
leafFileName = 'Used_Randoms.npy'
MAX_LEVELS = 4
characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

current_dir = os.getcwd()
root_dir = os.path.join(current_dir, rootFileName)

def markMagicNumbersAsUsed(array):
    array[500] = True

def createSubDirs(level, prefix_dir, array):
    if (level > MAX_LEVELS):
        with open(os.path.join(prefix_dir, leafFileName), 'wb') as fh:
            array.tofile(fh)
        return
    slice_size = int(len(array)/16)
    for index, char in enumerate(characters):
        sub_dir = os.path.join(prefix_dir, char)
        os.makedirs(sub_dir)
        createSubDirs(level+1, sub_dir, array[index*slice_size:(index+1)*slice_size])

def prepareInitialSetup():
    if os.path.exists(rootFileName) == False:
        initialData = bitarray(numbersCount)
        initialData.setall(0)
        markMagicNumbersAsUsed(initialData)
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)
        createSubDirs(1, root_dir, initialData)
    else:
        print ('Check availability of remianing codes, if not cle an hierarchy')

def findRandomHex(level, prefix_dir):
    if (level > MAX_LEVELS):
        with open(os.path.join(prefix_dir, leafFileName), 'r+b') as f:
            mapping = mmap.mmap(f.fileno(), 0)
            array = bitarray(buffer=mapping) #endian='little'
            while True:
                decimalRand = random.randint(0, len(array)-1)
                if (array[decimalRand] == False):
                    array[decimalRand] = True
                    return format(decimalRand, 'X')      
    decimalRand = random.randint(0, 15)
    sub_dir = os.path.join(prefix_dir, characters[decimalRand])
    return characters[decimalRand] + findRandomHex(level+1, sub_dir)

prepareInitialSetup()
hex_code = findRandomHex(1, root_dir)
print ("0x" + hex_code)
