# C.O.M.P.A.S.S.

## OVERVIEW

This code aids in Russian -> English translation of S.T.A.L.K.E.R. gamefiles.

It is particularly useful for machine translation web applications.

It supports the following file formats:
  * XML
  * (LTX support to be added)

## DETAILS

COMPASS consists of two scripts - an unpacker and a repacker.

The unpacker crawls a user supplied root folder (i.e. gamedata) for candidate files
  that may contain cyrillic text used in the game. It then generates two files:
   1. Text Corpus: A single file containing all the text to be translated across all files
   2. Mapping: A single file containing the associated **line numbers** and **line type*** of
     the text corpus.

The repacker takes two files as input:
   1. **Translated** Text Corpus: A single file containing the translated text from the unpacker Text Corpus file.
   2. Mapping: Same as above

The repacker then "glues together" the information from both files to generate a new root folder with the translated files.


Comparing the original files with the COMPASS result files, the files should luck structurally identical.
The only differences should be all Russian text has been translated to English.
