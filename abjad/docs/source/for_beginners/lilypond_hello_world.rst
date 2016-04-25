LilyPond "hello, world!"
========================

Working with Abjad means working with LilyPond.

To start we'll need to make sure LilyPond is installed.

Open the terminal and type ``lilypond --version``::

    $ lilypond --version
    GNU LilyPond 2.17.3

    Copyright (c) 1996--2012 by
      Han-Wen Nienhuys <hanwen@xs4all.nl>
      Jan Nieuwenhuizen <janneke@gnu.org>
      and others.

    This program is free software.  It is covered by the GNU General Public
    License and you are welcome to change it and/or distribute copies of it
    under certain conditions.  Invoke as `lilypond --warranty' for more
    information.

LilyPond responds with version and copyright information.
If the terminal tells you that LilyPond is not found then
either LilyPond isn't installed on your computer or else
your computer doesn't know where LilyPond is installed.

If you haven't installed LilyPond go to ``www.lilypond.org``
and download the current version of LilyPond for your operating system.

If your computer doesn't know where LilyPond is installed
then you'll have to tell your computer where LilyPond is.
Doing this depends on your operating system.
If you're running MacOS X or Linux then you need to make sure that the
location of the LilyPond binary is present in your ``PATH``
environment variable.
If you don't know how to add things to your path you should Google or ask a friend.


Writing the file
----------------

Change to whatever directory you'd like and then use your text editor
to create a new file called ``hello_world.ly``.

Type the following lines of LilyPond input into ``hello_world.ly``::

    \version "2.17.3"
    \language "english"

    \score {
        c'4
    }

Save ``hello_world.ly`` and quit your text editor when you're done.

Note the following::

    1. You can use either spaces or tabs while you type.
    2. The version string you type must match the LilyPond version you found above.
    3. The English language command tells LilyPond to use English note names.
    4. The score block tells LilyPond that you're entering actual music.
    5. The expression c'4 tells LilyPond to create a quarter note middle C.
    6. LilyPond files end in .ly by convention.


Interpreting the file
---------------------

Call LilyPond on ``hello_world.ly``::

    $ lilypond hello_world.ly
    GNU LilyPond 2.17.3
    Processing `hello_world.ly'
    Parsing...
    Interpreting music...
    Preprocessing graphical objects...
    Finding the ideal number of pages...
    Fitting music on 1 page...
    Drawing systems...
    Layout output to `hello_world.ps'...
    Converting to `./hello_world.pdf'...
    Success: compilation successfully completed

LilyPond reads ``hello_world.ly`` as input and creates ``hello_world.pdf`` as output.

Open the ``hello_world.pdf`` file LilyPond creates.

You can do this by clicking on the file.
Or you can open the file from the command line.

If you're using MacOS X you can open ``hello_world.pdf`` like this::

    $ open hello_world.pdf

..  abjad::
    :hide:

    note = Note("c'4")
    show(note)

Your operating system shows the score you created.


Repeating the process
---------------------

Working with LilyPond means doing these things::

    1. edit a LilyPond input file
    2. interpet the input file
    3. open the PDF and inspect your work

You'll repeat this process many times to make your scores look the way you want.
But no matter how complex your music this edit-interpret-view loop
will be the basic way you work.
