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
|              team background color            |     unused    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|              team foreground color            |     unused    |
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
|   field size  |           coach name (variable size)          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

2.1 The efa header

The efa header doesn't contain any special information, it just acts as an identifier for the equipa
file and without it, the file is not recognized as a valid equipa by the game. The header occupies
the offset range 0x00-0x31, having 50 bytes of size. Its content is composed by the 'EFa' ascii
string followed by 47 zero bytes.

2.2 The short name/extendend name

The 'short' and 'extended name' fields shares the same structure: both starts with 1 byte containing the
field size, followed by the field value itself. The field value is encrypted and how the encryption
algorithm works will be discussed in section 3.

2.3 The colors

The 'colors' field has 8 bytes of size, 4 bytes for each color. Both background and text colors has
the same structure: 3 bytes for the color itself (in RGB format) followed by 1 unused byte.

2.5 The country

The 'country' field contains the initial letters (in portuguese) of the equipa's country and has 4
bytes of size. The first byte contains the field size (which usually is 3) and the last 3 bytes
contains the encrypted initial letters. This information is used by elifoot to group the equipas
according to its country and show the equipa's country flag correctly. Thus, the value of this
field must to correspond to a bitmap entry on "FLAGS" directory, placed at the root directory of
the game.

2.6 The level

The 'level' field contains 1 byte of size and defines the level of equipa in hex format.

2.7 The number of players

This field contains 1 byte of size and defines the number of players who composes the equipa, in
hex format.

2.8 The player list

The 'player list' field defines the list of players who composes the equipa and has 'n' entries,
where 'n' is defined according to the prior field. The first 4 bytes of each entry of the list
defines the player's nationality, according to the format described on section 2.5. The next 1
byte contains the player's name size followed by the encrypted player's name itself. The last
byte defines the player's position code: 0 to goalkeeper, 1 to defender, 2 to midfielder and 3
to forward.

2.9 The coach

The 'coach' field defines the equipa's coach and has the same structure of the other fields with
variable size, starting with 1 size byte followed by the encrypted coach's name itself.

3. The encryption algorithm

TODO
```
