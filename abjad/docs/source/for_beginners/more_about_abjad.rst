More about Abjad
================


How it works
------------

How does Python suddenly know what musical notes are?
And how to make musical score?

Use Python's ``dir()`` built-in to get a sense of the answer:

..  abjad::
    :text-width: 80

    dir()

Calling ``from abjad import *`` causes Python to load hundreds or thousands of
lines of Abjad's code into the global namespace for you to use.  Abjad's code
is organized into a collection of several dozen different score-related
packages.  These packages comprise hundreds of classes that model things like
notes and rests and more than a thousand functions that let you do things like
transpose music or change the way beams look in your score.

Inspecting output
-----------------

Use ``dir()`` to take a look at the contents of the ``systemtools`` package:

..  abjad::
    :text-width: 80

    dir(systemtools)

The ``systemtools`` package implements I/O functions that help you work with the
files you create in Abjad.

Use ``systemtools.open_last_ly()`` to see the last LilyPond input file created
in Abjad::

    % Abjad revision 12452
    % 2013-10-22 13:32

    \version "2.17.3"
    \language "english"

    \header {
        tagline = \markup {  }
    }

    \score {
        c'4
    }

Notice:

1.  Abjad inserts two lines of %-prefixed comments at the top of the LilyPond
    files it creates.

2.  Abjad includes version and language commands automatically.

3.  Abjad includes a special abjad.scm file resident somewhere on your
    computer.

4.  Abjad includes dummy LilyPond header.

5.  Abjad includes a one-note score expression similar to the one you created
    in the last tutorial.

When you called ``show(note)`` Abjad created the LilyPond input file shown
above.  Abjad then called LilyPond on that ``.ly`` file to create a PDF.

(Quit your text editor in the usual way to return to the Python interpreter.)

Now use ``systemtools.open_last_log()`` to see the output LilyPond created as
it ran::

    GNU LilyPond 2.17.3
    Processing `7721.ly'
    Parsing...
    Interpreting music...
    Preprocessing graphical objects...
    Finding the ideal number of pages...
    Fitting music on 1 page...
    Drawing systems...
    Layout output to `7721.ps'...
    Converting to `./7721.pdf'...
    Success: compilation successfully completed

This will look familiar from the previous tutorial where we created a LilyPond
file by hand.

(Quit your text editor in the usual way to return to the Python interpreter.)
