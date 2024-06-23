```
                                          _ _  __             _      ___   ___
                                      ___| (_)/ _| ___   ___ | |_   / _ \ ( _ )
                                     / _ \ | | |_ / _ \ / _ \| __| | (_) |/ _ \
                                    |  __/ | |  _| (_) | (_) | |_   \__, | (_) |
                                     \___|_|_|_|  \___/ \___/ \__|    /_/ \___/
                                          _                __                            _
                          ___  __ _ _   _(_)_ __   __ _   / _| ___  _ __ _ __ ___   __ _| |_
                         / _ \/ _` | | | | | '_ \ / _` | | |_ / _ \| '__| '_ ` _ \ / _` | __|
                        |  __/ (_| | |_| | | |_) | (_| | |  _| (_) | |  | | | | | | (_| | |_
                         \___|\__, |\__,_|_| .__/ \__,_| |_|  \___/|_|  |_| |_| |_|\__,_|\__|
                                 |_|       |_|

1. Introduction

This document aims to provide a technical description of the equipa's file format of elifoot98,
focusing on how the team data is arranged into the file and how it's interpred by the game.

2. The equipa format

The equipa is a binary file and as you can guess, it contains all the team data (which will be
discussed in the following sub topics), that are stored as sequential chunks of information
across the file. It has the following format:

 0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                                                               |
|                                                               |
|                                                               |
|                                                               |
|                                                               |
|                            efa header                         |
|                                                               |
|                                                               |
|                                                               |
|                                                               |
|                                                               |
|                                 |XXXXXXXXXXXXXXXXXXXXXXXXXXXXX|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   field size  |    team extended name (variable size)         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   field size  |      team short name (variable size)          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|            team background colour             |     unused    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|            team foreground colour             |     unused    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   field size  |                 team country                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   team level  |   team size   |XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        player 0 country                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   field size  | player 0 name (variable size) |    position   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        player 1 country                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   field size  | player 1 name (variable size) |    position   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        player n country                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   field size  | player n name (variable size) |    position   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                  coach name (variable size)                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

2.1 The efa header

The efa header doesn't contain any special information, it just acts as an identifier for the equipa
file and without it, the file is not recognized as a valid equipa by the game. The header occupies
the offset range 0x00-0x31, having 50 bytes of size. Its content is composed by the 'EFa' ascii
string followed by 47 zero bytes.

2.2 The short name/extendend name

The short and extended name fields shares the same structure: both starts with 1 byte containing the
field size, followed by the field value itself. The field value is encrypted and how the encryption
algorithm works will be discussed in section 3.

2.3 The colours

2.5 The country

The country field represents the country of the equipa and has 4 bytes, the first one containing
the country size (which usually is 3) and the last 3 bytes containing the encrypted initials of the
country (which must match the entries of FLAGS directory).

2.6 The level

2.7 The player list

2.6 The coach

3. The encryptiong algorithm

TODO
```
