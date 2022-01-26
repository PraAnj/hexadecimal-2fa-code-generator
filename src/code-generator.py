#!/usr/bin/python3

import os
import mmap
import random
from pathlib import Path
from bitarray import bitarray

numbersCount = 16**8
rootFileName = 'ROOT'
leafFileName = 'Used_Randoms.npy'
MAX_LEVELS = 4
characters = ['0', '1', '2', '3', '4', '5', '6',
              '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
current_dir = os.getcwd()
root_dir = os.path.join(current_dir, rootFileName)


def markMagicNumbersAsUsed(array):
    # Load a file of magic numbers to ignore, mark them in the array
    array[500] = True


def getRandomSubFolder(current_dir):
    p = Path(current_dir)
    sub_folder_names = [f.name for f in p.iterdir() if f.is_dir()]
    decimalRand = random.randint(0, len(sub_folder_names)-1)
    sub_folder = sub_folder_names[decimalRand]
    is_last_folder = (len(sub_folder_names) == 1)
    return sub_folder, os.path.join(current_dir, sub_folder), is_last_folder


def createSubDirs(level, prefix_dir, array):
    if (level > MAX_LEVELS):
        with open(os.path.join(prefix_dir, leafFileName), 'wb') as fh:
            array.tofile(fh)
        return
    slice_size = int(len(array)/16)
    for index, char in enumerate(characters):
        sub_dir = os.path.join(prefix_dir, char)
        os.makedirs(sub_dir)
        createSubDirs(level+1, sub_dir,
                      array[index*slice_size:(index+1)*slice_size])


def prepareInitialSetup():
    if not os.path.exists(rootFileName):
        initialData = bitarray(numbersCount)
        initialData.setall(0)  # False
        markMagicNumbersAsUsed(initialData)
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)
        createSubDirs(1, root_dir, initialData)


def popRandomHex(level, prefix_dir):
    if (level > MAX_LEVELS):
        with open(os.path.join(prefix_dir, leafFileName), 'r+b') as f:
            mapping = mmap.mmap(f.fileno(), 0)
            # endian='big' by default, can change to little
            array = bitarray(buffer=mapping)
            indexes = [i for i, bit in enumerate(array) if bit == False]
            if (len(indexes) > 0):
                index = random.randint(0, len(indexes)-1)
                decimalRand = indexes[index]
                array[decimalRand] = True       # persist used number
                delete_me = (len(indexes) == 1)  # if last index is choosen
                return format(decimalRand, 'X'), delete_me

    sub_folder_name, sub_dir, is_last_folder = getRandomSubFolder(prefix_dir)
    hexa_rand, delete_me = popRandomHex(level+1, sub_dir)
    if delete_me:
        os.remove(sub_dir)
        delete_me = is_last_folder
    return sub_folder_name + hexa_rand, delete_me


prepareInitialSetup()
hex_code, delete_me = popRandomHex(1, root_dir)
print("0x" + hex_code)
if delete_me:
    os.remove(root_dir)  # deleting root finally
