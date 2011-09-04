Abjad?
======

Abjad is an interactive software system designed to help composers
build up complex pieces of music notation in an iterative and incremental way. 
Use Abjad to create a symbolic representation
of all the notes, rests, staves, tuplets, beams and slurs in any score.
Because Abjad extends the Python programming language,
you can use Abjad to make systematic changes to your music as you work.
And because Abjad wraps the powerful LilyPond music notation package, 
you can use Abjad to control the typographic details of the symbols on the page.


Abjad extends LilyPond
----------------------

`LilyPond <http://www.lilypond.org>`__ is an open-source music notation
package invented by Han-Wen Nienhuys and Jan Niewenhuizen and extended
by an international team of developers and musicians.
LilyPond differs from other music engraving programs in a number of ways.
LilyPond separates musical content from page layout.
LiyPond affords typographic control over almost everything. 
And LilyPond implements a powerfully correct model of the musical score.

You can start working with Abjad right away because
Abjad creates LilyPond files for you automatically.
But you will work with Abjad faster and more effectively if you understand the
structure of the LilyPond files Abjad creates.
For this reason we recommend new users spend a couple of days learning LilyPond first.

Start by reading about `text input <http://lilypond.org/text-input.html>`__ in LilyPond.
Then work the 
`LilyPond tutorial <http://www.lilypond.org/doc/v2.15/Documentation/learning/tutorial>`__.
You can test your understanding of LilyPond by using the program to engrave
of a Bach chorale.
Use a grand staff and and include slurs, fermatas and so on.
Once you can engrave a chorale in LilyPond you'll understand the way 
Abjad works with LilyPond behind the scenes.


Abjad extends Python
--------------------

`Python <http://www.python.org>`__ is an open-source programming
language invented by Guido van Rossum and further developed by a team 
of programmers working in many countries around the world. 
Python is used to provision servers, process text, develop distributed systems
and do much more besides.
The dynamic language and interpreter features of Python are similar to Ruby
while the syntax of Python resembles C, C++ and Java.

To get the most out of Abjad you need to know (or learn) the basics of programming in Python.
Abjad extends Python because it makes no sense to reinvent the wheel modern programming 
langauges have developed to find, sort, store, model and encapsulate information.
Abjad simply piggy-backs on the ways of doing these things that Python provides.
So to use Abjad effectively you need to know the way these things are done in Python.

Start with the `Python tutorial <http://docs.python.org/tutorial/>`__.
The tutorial is structured in 15 chapters and you should work through the first 12.
This will take a day or two and 
you'll be able to use all the information you read in the Python tutorial in Abjad.
If you're an experienced programmer you should skip chapters 1 - 3 but read 4 - 12.
When you're done you can give yourself the equivlanent of the chorale test suggested above.
First open a file and define a couple of classes and functions in it.
Then open a second file and write some code to first import and then do stuff with 
the classes and functions you defined in the first file.
Once you can easily do this without looking at the Python docs you'll be in a much 
better position to work with Abjad.


What next?
----------

The most important parts of Abjad are the interlocking objects that structure the system. 
Read about the way Abjad models pitch, duration, leaves, containers, spanners and marks 
in the :doc:`Abjad reference manual </index>`.

But note that important parts of the system are missing from the manual.
The reason for this is that we completed the Abjad API months before we started the manual.
This means that classes and functions you look up in the API may not yet be documented 
in the manual.
The reference manual will eventually document all parts of the system.
But until then check the API if the manual doesn't yet have what you need.

Once you understand the basics about how to work with Abjad you should
spend some time with the :doc:`Abjad API </chapters/api/index>`.
The API documents all the functionality available in the system.
Abjad comprises about 153,000 lines of code.
About half of these implement the automated tests that check the correctness of Abjad.
The rest of the code implements 39 packages comprising 197 classes and 941 functions.
All of these are documented in the API.


Mailing lists
-------------

As you begin working with Abjad please be in touch.

Questions, comments and contributions are welcomed from composers everywhere.

**Questions or comments?**
Join the `abjad-user <http://groups.google.com/group/abjad-user>`__ list.

**Want to contribute?**
Join the `abjad-devel <http://groups.google.com/group/abjad-devel>`__ list.
