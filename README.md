# Hexa Decimal Code Generator for 2FA [![Build Status](https://app.travis-ci.com/PraAnj/hexadecimal-2fa-code-generator.svg?branch=main)](https://app.travis-ci.com/PraAnj/hexadecimal-2fa-code-generator)
This repo can be used to generate 8 digit hexadecimal numbers for 2fa. Following rules are applied,

1. Every time you run the program, it should emit one 8-digit hexadecimal code;
2. It should emit every possible code before repeating;
3. It should not print "odd-looking" codes such as 0xAAAAAAAA or 0x01234567 or any commonly used words, phrases, or hexspeak such as 0xDEADBEEF;

# TODO
1. Document the design, installation and how to use.
2. PEP8 style checker, github actions
3. Unit tests with pytest, catching edge cases too
4. Update requirements.txt for installations.
5. Perf values for first folder creation, and random number generation
6. Write a crawler utility to retrieve remaining magic hexa numbers
7. Way to encrypt the folder hierarchy and files