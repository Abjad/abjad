Windows
=======

Check Python
------------

Abjad requires Python 3.10 or later:

..  code-block::

    > py --version
    Python 3.10.2

Check LilyPond
--------------

Abjad requires LilyPond 2.23.6 or later.

Make sure LilyPond is installed: http://lilypond.org/development.html

When installing LilyPond, first unzip the archive downloaded from the site above.

You should get a directory like ``lilypond-2.23.8``.

Move the resulting folder to ``C:\Program Files (x86)``.

Add ``C:\Program Files (x86)\Lilypond/bin`` to the Windows path.

Make sure LilyPond is callable from the commandline:

..  code-block::

    > lilypond --version
    GNU LilyPond 2.23.8

    Copyright (c) 1996--2022 by
    Han-Wen Nienhuys <hanwen@xs4all.nl>
    Jan Nieuwenhuizen <janneke@gnu.org>
    and others.

    This program is free software.  It is covered by the GNU General Public
    License and you are welcome to change it and/or distribute copies of it
    under certain conditions.  Invoke as `lilypond --warranty' for more
    information.

Install Abjad in a Python 3 virtual environment
-----------------------------------------------

Create a Python 3 virtual environment for Abjad: https://docs.python.org/3/tutorial/venv.html

..  code-block::

    > py -m venv FirstAbjad

Activate the virtual environment:

..  code-block::

    > FirstAbjad\Scripts\activate

Update pip:

..  code-block::

    > py -m pip install --upgrade pip

Install Abjad:

..  code-block::

    > py -m pip install abjad

Test installation:

..  code-block::

    > py
    > import abjad
    > note = abjad.Note("c'4")
    > abjad.show(note)

:author:`[Hollerweger (3.20).]`
