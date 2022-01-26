#!/usr/bin/python3

import os
import mmap
import code_generator
from bitarray import bitarray
import shutil

NUMBERS_COUNT = 16**8
LEAF_FILE_NAME = 'used-randoms.bin'
ROOT_FOLDER_NAME = 'ROOT'
CHARACTERS = ['0', '1', '2', '3', '4', '5', '6',
              '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
ROOT_DIR = os.path.join(os.getcwd(), ROOT_FOLDER_NAME)

def test_magic_numbers():
  initial_data = bitarray(NUMBERS_COUNT)
  initial_data.setall(0)
  code_generator.mark_magic_numbers_as_used(initial_data)
  
  assert initial_data[int("0xAAAAAAAA", 0)] == True
  assert initial_data[int("0xAAAAAAA1", 0)] == False

def test_folder_deletion():
  code_generator.prepare_initial_setup()

  for folder in CHARACTERS[1:16]:
    path = os.path.join(os.getcwd(),'ROOT/'+folder)
    if os.path.exists(path):
      shutil.rmtree(path)
    path = os.path.join(os.getcwd(),'ROOT/0/'+folder)
    if os.path.exists(path):
      shutil.rmtree(path)
    path = os.path.join(os.getcwd(),'ROOT/0/0/'+folder)
    if os.path.exists(path):
      shutil.rmtree(path)
 
  for folder in CHARACTERS[2:16]:
    path = os.path.join(os.getcwd(),'ROOT/0/0/0/'+folder)
    if os.path.exists(path):
      shutil.rmtree(path)
  
  with open(os.path.join(os.getcwd(),'ROOT/0/0/0/0/', LEAF_FILE_NAME), 'r+b') as f:
      mapping = mmap.mmap(f.fileno(), 0)
      array = bitarray(buffer=mapping)
      array[:] = True
      array[0] = False
  
  with open(os.path.join(os.getcwd(),'ROOT/0/0/0/1/', LEAF_FILE_NAME), 'r+b') as f:
      mapping = mmap.mmap(f.fileno(), 0)
      array = bitarray(buffer=mapping)
      array[:] = True
      array[0] = False

  hex_code, delete_me = code_generator.pop_random_hexa(1, ROOT_DIR)
  assert delete_me == False
  
  hex_code, delete_me = code_generator.pop_random_hexa(1, ROOT_DIR)
  if delete_me:
        shutil.rmtree(ROOT_DIR)
  assert delete_me == True
