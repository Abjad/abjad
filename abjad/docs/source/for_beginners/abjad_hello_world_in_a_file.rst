Abjad "hello, world!" (in a file)
=================================


Writing the file
----------------

Open the terminal and change to whatever directory you'd like.

Use your text editor to create a new file called ``hello_world.py``.
If you have ``hello_world.py`` left over from earlier you should delete it
and create a new file.

Type the following lines of code into ``hello_world.py``::

    from abjad import *


    note = Note("c'4")
    show(note)

Save ``hello_world.py`` and quit your text editor.


Interpreting the file
---------------------

Call Python on ``hello_world.py``::

    $ python hello_world.py

..  abjad::
    :hide:

    note = Note("c'4")
    show(note)

Python reads ``hello_world.py`` and shows the score you've created.


Repeating the process
---------------------

Working with files in Abjad means that you do these things::

    1. edit a file
    2. interpret the file

These steps make up a type of edit-interpret loop.

This way of working with Abjad remains the same
no matter how complex the scores you build.
