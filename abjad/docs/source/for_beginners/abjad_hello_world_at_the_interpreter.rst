Abjad "hello, world" (at the interpreter)
=========================================


Starting the interpreter
------------------------

Open the terminal and start the Python interpreter:

::

    abjad$ python

::

    Python 2.7.3 (v2.7.3:70274d53c1dd, Apr  9 2012, 20:52:43)
    [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

Then import Abjad:

::

    >>> from abjad import *

If Abjad is installed on your system then Python will silently load Abjad.
If Abjad isn't installed on your system then Python will raise
an import error.

Go to ``www.projectabjad.org`` and follow the instructions there
to install Abjad if necessary.


Entering commands
-----------------

After you've imported Abjad you can create a note like this:

..  abjad::

    note = Note("c'4")

And you can show the note like this:

..  abjad::

    show(note)


Stopping the interpreter
------------------------

Type ``quit()`` or ``ctrl+D`` when you're done.

Working with the interpreter is a good way to test out small bits of code in
Abjad. As your scores become more complex you will want to organize the code
your write with Abjad in files. This is the topic of the next tutorial.
