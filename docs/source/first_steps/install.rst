Check Python
------------

Abjad requires Python 3.12 (or later):

..  code-block::

    ~$ python --version
    Python 3.13.3

Check LilyPond
--------------

Abjad requires LilyPond 2.25.26 (or later).

Make sure LilyPond is installed: http://lilypond.org/development.html

Make sure LilyPond is callable from the commandline:

..  code-block::

    ~$ lilypond --version
    GNU LilyPond 2.25.26

    Copyright (c) 1996--2023 by
    Han-Wen Nienhuys <hanwen@xs4all.nl>
    Jan Nieuwenhuizen <janneke@gnu.org>
    and others.

    This program is free software.  It is covered by the GNU General Public
    License and you are welcome to change it and/or distribute copies of it
    under certain conditions.  Invoke as `lilypond --warranty' for more
    information.

Install Abjad in a Python 3 virtual environment
-----------------------------------------------

Create a Python 3 virtual environment for Abjad:
https://docs.python.org/3/tutorial/venv.html

Activate the virtual environment and then use pip to install Abjad:

..  code-block::

    ~$ python -m pip install abjad
