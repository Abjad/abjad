Python, LilyPond and Abjad for beginners
========================================

..  toctree::
    :numbered:
    :maxdepth: 1

    getting_started
    lilypond_hello_world
    python_hello_world_at_the_interpreter
    python_hello_world_in_a_file
    more_about_python
    abjad_hello_world_at_the_interpreter
    abjad_hello_world_in_a_file
    more_about_abjad

Abjad extends LilyPond
----------------------

`LilyPond`_ is an open-source music notation package
invented by Han-Wen Nienhuys and Jan Niewenhuizen and extended by an
international team of developers and musicians.  LilyPond differs from other
music engraving programs in a number of ways.  LilyPond separates musical
content from page layout.  LilyPond affords typographic control over almost
everything.  And LilyPond implements a powerfully correct model of the musical
score.

You can start working with Abjad right away because Abjad creates LilyPond
files for you automatically.  But you will work with Abjad faster and more
effectively if you understand the structure of the LilyPond files Abjad
creates.  For this reason we recommend new users spend a couple of days
learning LilyPond first.

Start by reading about `text input <http://lilypond.org/text-input.html>`_ in
LilyPond.  Then work the `LilyPond tutorial
<http://www.lilypond.org/doc/v2.19/Documentation/learning/tutorial>`_.  You can
test your understanding of LilyPond by using the program to engrave the first
few phrases of a Bach chorale. Once you can engrave a chorale in LilyPond
you'll understand the way Abjad works with LilyPond behind the scenes.

Abjad extends Python
--------------------

`Python`_ is an open-source programming language invented by Guido van Rossum
and further developed by a team of programmers working in many countries around
the world.  Python is used to provision servers, process text, develop
distributed systems and do much more besides. The dynamic language and
interpreter features of Python are similar to Ruby while the syntax of Python
resembles C, C++ and Java.

To get the most out of Abjad you need to know (or learn) the basics of
programming in Python.  Abjad extends Python because it makes no sense to
reinvent the wheel modern programming langauges have developed to find, sort,
store, model and encapsulate information.  Abjad simply piggy-backs on the ways
of doing these things that Python provides.  So to use Abjad effectively you
need to know the way these things are done in Python.

Start with the `Python tutorial <http://docs.python.org/tutorial/>`_.  The
tutorial is structured in 15 chapters and you should work through the first 12.
This will take a day or two and you'll be able to use all the information you
read in the Python tutorial in Abjad.  If you're an experienced programmer you
should skip chapters 1 - 3 but read 4 - 12.  When you're done you can give
yourself the equivalent of the chorale test suggested above.  First open a file
and define a couple of classes and functions in it.  Then open a second file
and write some code to first import and then do stuff with the classes and
functions you defined in the first file.  Once you can easily do this without
looking at the Python docs you'll be in a much better position to work with
Abjad.

..  _LilyPond: http://lilypond.org/
..  _Python: https://www.python.org/