#!/usr/bin/python3

import mmap
import random
import os.path
from pathlib import Path
from bitarray import bitarray

numbersCount = 16**8
rootFileName = 'ROOT'
leafFileName = 'Used_Randoms.npy'
MAX_LEVELS = 4
characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
current_dir = os.getcwd()
root_dir = os.path.join(current_dir, rootFileName)

def markMagicNumbersAsUsed(array):
    # Load a file of magic numbers to ignore, mark them in the array
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

def popRandomHex(level, prefix_dir):
    if (level > MAX_LEVELS):
        with open(os.path.join(prefix_dir, leafFileName), 'r+b') as f:
            mapping = mmap.mmap(f.fileno(), 0)
            array = bitarray(buffer=mapping) #endian='big' by default, can change to little
            indexes = [i for i,bit in enumerate(array) if bit == False]
            if (len(indexes) > 0):
                index = random.randint(0, len(indexes)-1)
                decimalRand = indexes[index]
                array[decimalRand] = True
                return format(decimalRand, 'X')      
    
    p = Path(prefix_dir)
    folder_names = [f.name for f in p.iterdir() if f.is_dir()]
    decimalRand = random.randint(0, len(folder_names)-1)
    sub_dir = os.path.join(prefix_dir, folder_names[decimalRand])
    
    return folder_names[decimalRand] + popRandomHex(level+1, sub_dir)

prepareInitialSetup()
hex_code = popRandomHex(1, root_dir)
print ("0x" + hex_code)
