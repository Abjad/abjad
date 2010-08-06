Abjad?
======

Abjad is an interactive software system designed to help composers
build up complex pieces of music notation in an iterative and
incremental way. You can use Abjad to create a symbolic representation
of all the notes, rests, staves, nested rhythms, beams, slurs and
other notational elements in any score. Because Abjad wraps the
powerful LilyPond music notation package, you can use Abjad to control
extremely fine-grained typographic details of all elements of any
score, like the color and thickness of noteheads, dots, slurs and
brackets. And because Abjad extends the Python programming language,
you can use Abjad to make powerful and systematic changes to any part
of any score. The scores that you make in Abjad can range in size from
small examples of only one or two notes to full pieces of orchestral
score worked out against many dozes of staves.


Abjad extends python
--------------------

`Python <http://www.python.org>`__ is an object-oriented, dynamic programming
language developed by Guido van Rossum in the 1990s. Python is now
widely used for everything from straightforward scripting applications
to the development and deployment of complex distributed systems. The
language and interpreter features of Python are similar to Ruby,
though the syntax of Python more closely resembles C, C++ and Java
than most other languages. Much has been written about the benefits of
Python and we are happy to add our voice to the chorus. We find Python
to be an excellent all-purpose language that scales well, tests well,
develops quickly, and keeps total lines of code to a minimum. For more
on the benefits (and some limitations) of Python, see our page on 
:doc:`/chapters/background/python/index`.



Abjad extends lilypond
----------------------

`LilyPond <http://www.lilypond.org>`__ is an open source music notation
package invented by Han-Wen Nienhuys and Jan Niewenhuizen in the 1990s
and still under development today. LilyPond is a command-line driven
music typography system that allows for the generation of music
notation of extremely high quality. LilyPond differs from other music
engraving programs in a number of important ways, some of which were
critical in our choice of LilyPond as the notational powerhouse
underneath Abjad. LilyPond separates musical content and page layout.
LiyPond affords typographic control over almost everything. And,
perhaps most importantly, LilyPond implements the rhythmic model of
western music correctly: broken tuplets, nonbinary meters, and
durations that cross measure and line boundaries all work correctly
out of the box. For these and other details relating to our selection
of LilyPond as the notational engine for Abjad, see our page on 
:doc:`/chapters/background/lilypond/index`.
