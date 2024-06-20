```
elifoot98's equipa format

1. introduction

this document aims to give a full technical description of the equipa's file format of elifoot98,
focusing on how the team data is arranged into the file and how it is interpred by the game.

2. the equipa format

the equipa is a binary file and contains all the team data (whose will be discussed in the
following sub topics), stored as sequential chunks of information across the file. it has the
following format:

 0                   1                 2                   3                   4
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                                               |
|                                                                               |
|                                                                               |
|                                                                               |
|                                                                               |
|                                 efa header                                    |
|                                                                               |
|                                                                               |
|                                                                               |
|                                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| ext name size |                extended name (variable size)                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|short name size|                 short name (variable size)                    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    bg colour                  |     unused    |   fg colour   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                               |     unused    |            country            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                               |     level     |  players qty  |               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


2.1 the efa header

2.2 the short name/extendend name

2.3 the colours

2.4 the level

2.5 the player list

2.6 the coach

3. the encryptiong algorithm

TODO

4. glossary

TODO
```
