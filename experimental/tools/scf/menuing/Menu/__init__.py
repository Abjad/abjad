'''Menu implements an intelligent ordered list of MenuSections.
MenuSection implements an ordered list of menu entries.
This means that every SCF Menu is essentially a list of lists.

(Menu entries are modelled with built-in dicts; no custom class exists.)

CONSTRUCTION TIME SETTINGS:
Menu is dumb and implements no construction-time settings.
MenuSection is smart and implements important construction-time settings.

RUN TIME BEHAVIOR:
Call Menu.run() to run any SCF menu.
The method queries for user input until a match is found.

MATCH TIME BEHAVIOR:
The menu match algorithm is basically an O(n) traversal of menu entries.

RETURN VALUE:
Menu.run() returns exactly one value.
Return value may be none, a string or an object of another type.
'''

from Menu import Menu
