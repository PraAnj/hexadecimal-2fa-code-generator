# Hexa Decimal Code Generator for 2FA [![Build Status](https://app.travis-ci.com/PraAnj/hexadecimal-2fa-code-generator.svg?branch=main)](https://app.travis-ci.com/PraAnj/hexadecimal-2fa-code-generator) [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

This repo can be used to generate 8 digit hexadecimal numbers for 2fa. Following rules are applied,

1. Every time you run the program, it should emit one 8-digit hexadecimal code;
2. It should emit every possible code before repeating;
3. It should not print "odd-looking" codes such as 0xAAAAAAAA or 0x01234567 or any commonly used words, phrases, or hexspeak such as 0xDEADBEEF;

# TODO
1. Document the design, installation and how to use.
2. PEP8 style checker, github actions (Refer:- https://github.com/marketplace/actions/pycodestyle)
3. Update pytests to catch edge cases
4. Update requirements.txt for easy installations.
5. Calculate perf values for first folder creation, and random number generation
6. Write a crawler utility to retrieve remaining magic hexa numbers (Ex:-Beautifilsoup)
7. Implement a way to encrypt the folder hierarchy and files