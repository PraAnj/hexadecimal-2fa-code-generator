#!/usr/bin/python3

import os
import mmap
import random
from pathlib import Path
from bitarray import bitarray
import shutil
import multiprocessing

NUMBERS_COUNT = 16**8
ROOT_FOLDER_NAME = 'ROOT'
LEAF_FILE_NAME = 'used-randoms.bin'
MAX_LEVELS = 4
CHARACTERS = ['0', '1', '2', '3', '4', '5', '6',
              '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
MAGIC_NUMBERS_FILE = '../data/magic-hexa-numbers.txt'
ROOT_DIR = os.path.join(os.getcwd(), ROOT_FOLDER_NAME)


def mark_magic_numbers_as_used(array):
    with open(MAGIC_NUMBERS_FILE) as f:
        for line in f:
            # int identifies hexa automatically and converts to decimal
            decimal = int(line.strip(), 0)
            array[decimal] = True


def get_random_sub_folder(current_dir):
    p = Path(current_dir)
    sub_folder_names = [f.name for f in p.iterdir() if f.is_dir()]
    random_decimal = random.randint(0, len(sub_folder_names)-1)
    sub_folder = sub_folder_names[random_decimal]
    is_last_folder = (len(sub_folder_names) == 1)
    return sub_folder, os.path.join(current_dir, sub_folder), is_last_folder


def create_sub_dirs(level, prefix_dir, array):
    os.makedirs(prefix_dir)
    if (level > MAX_LEVELS):
        with open(os.path.join(prefix_dir, LEAF_FILE_NAME), 'wb') as fh:
            array.tofile(fh)
        return
    slice_size = int(len(array)/16)
    slices = [(level+1, os.path.join(prefix_dir, char), array[index*slice_size:(index+1)*slice_size]) for index, char in enumerate(CHARACTERS)]

    if level == 1:  # Parallel jobs only at the first level
        with multiprocessing.Pool(processes=8) as pool:
            pool.starmap(create_sub_dirs, slices)
            pool.close()
            pool.join()
    else:
        [create_sub_dirs(*slice) for slice in slices]


def prepare_initial_setup():
    if not os.path.exists(ROOT_FOLDER_NAME):
        initial_data = bitarray(NUMBERS_COUNT)
        initial_data.setall(0)  # False
        mark_magic_numbers_as_used(initial_data)
        create_sub_dirs(1, ROOT_DIR, initial_data)


def pop_random_hexa(level, prefix_dir):
    if (level > MAX_LEVELS):
        with open(os.path.join(prefix_dir, LEAF_FILE_NAME), 'r+b') as f:
            mapping = mmap.mmap(f.fileno(), 0)
            # endian='big' by default, can change to little
            array = bitarray(buffer=mapping)
            indices = [i for i, bit in enumerate(array) if bit == False]
            if (len(indices) > 0):
                index = random.randint(0, len(indices)-1)
                random_decimal = indices[index]
                array[random_decimal] = True       # persist used number
                delete_me = (len(indices) == 1)  # if last index is choosen
                return format(random_decimal, 'X'), delete_me

    sub_folder, sub_dir, is_last_folder = get_random_sub_folder(prefix_dir)
    hexa_rand, delete_me = pop_random_hexa(level+1, sub_dir)
    if delete_me:
        shutil.rmtree(sub_dir)
        delete_me = is_last_folder
    return sub_folder + hexa_rand, delete_me


def main():
    prepare_initial_setup()
    hex_code, delete_me = pop_random_hexa(1, ROOT_DIR)
    print("0x" + hex_code)
    if delete_me:
        shutil.rmtree(ROOT_DIR)  # deleting root finally


if __name__ == "__main__":
    main()
