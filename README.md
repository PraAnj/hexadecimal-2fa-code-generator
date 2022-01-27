# Hexa Decimal Code Generator for 2FA [![Build Status](https://app.travis-ci.com/PraAnj/hexadecimal-2fa-code-generator.svg?branch=main)](https://app.travis-ci.com/PraAnj/hexadecimal-2fa-code-generator) [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

This repo can be used to generate 8 digit hexadecimal numbers for 2fa. Following rules are applied,

1. Every time you run the program, it should emit one 8-digit hexadecimal code;
2. It should emit every possible code before repeating;
3. It should not print "odd-looking" codes such as 0xAAAAAAAA or 0x01234567 or any commonly used words, phrases, or hexspeak such as 0xDEADBEEF;

# Design
In order to avoid using duplicate codes, already used codes should be persisted on the disk. Since hexa corpus would be more than 4B numbers, storing 4B hexa numbers would take more than 64GB disk space. Hence only a boolean flag whether the positional code is used or not is persisted to disk which only takes less than half a GigaByte. These numbers are stored in a hierarchycal folder system for faster retrieval by reducing the search scope by a factor of 16 at each iteration as shown in figure below. Once all the codes in a particular path are used, those paths are deleted recursively from the tree to avoid traversing non existance paths. The folder hierarchy will be re-created once all the codes are used, which eventually after deletion of ROOT folder.

<img src="https://github.com/PraAnj/hexadecimal-2fa-code-generator/blob/main/data/folder_hierarchy.drawio.png" data-canonical-src="https://github.com/PraAnj/hexadecimal-2fa-code-generator/blob/main/data/folder_hierarchy.drawio.png" width="630" height="350" />

# How to use
1. Clone the repository
2. Install the dependencies via requirements.txt

        pip install -r requirements.txt
4. Run the code generator

        cd src
        ./code_generator.py
        pytest pytester.py # for testing

# TODO
1. PEP8 style checker, github actions (Refer:- https://github.com/marketplace/actions/pycodestyle)
2. Update pytests to catch edge cases
3. Update requirements.txt for easy installations.
4. Calculate perf values for first folder creation, and random number generation
5. Write a crawler utility to retrieve remaining magic hexa numbers (Ex:-Beautifilsoup)
6. Implement a way to encrypt the folder hierarchy and files
