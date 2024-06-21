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

1. introduction

this document aims to give a full technical description of the equipa's file format of elifoot98,
focusing on how the team data is arranged into the file and how it is interpred by the game.

2. the equipa format

the equipa is a binary file and contains all the team data (whose will be discussed in the
following sub topics), stored as sequential chunks of information across the file. it has the
following format:

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
|                           team country                        |
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
|                        player 2 country                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   field size  | player 2 name (variable size) |    position   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        player n country                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   field size  | player n name (variable size) |    position   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                  coach name (variable size)                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

2.1 the efa header

2.2 the short name/extendend name

2.3 the colours

2.5 the country

2.6 the level

2.7 the player list

2.6 the coach

3. the encryptiong algorithm

TODO

4. glossary

TODO
```
