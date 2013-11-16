Scores
======


Making a score from a LilyPond input string
-------------------------------------------

You can make an Abjad score from a LilyPond input string:

::

   >>> input = r'''
   ... \new Staff { e''4 d''8 ( c''8 ) d''4 g'4 }
   ... \new Staff { \clef bass c4 a,4 b,4 e4 }
   ... '''


::

   >>> score = Score(input)


::

   >>> show(score)

.. image:: images/index-1.png



Making a score from a list of Abjad components
----------------------------------------------

You can also make a score from a list of other Abjad components:

::

   >>> treble_staff_1 = Staff("e'4 d'4 e'4 f'4 g'1")
   >>> treble_staff_2 = Staff("c'2. b8 a8 b1")


::

   >>> score = Score([treble_staff_1, treble_staff_2])


::

   >>> show(score)

.. image:: images/index-2.png



Understanding the interpreter representation of a score
-------------------------------------------------------

The interpreter representation of an Abjad score contains three parts:

::

   >>> score
   Score<<2>>


``Score`` tells you the score's class.

``3`` tells you the score's length (which is the number of top-level components
the score contains).

Curly braces ``{`` and ``}`` tell you that the music inside the score is
interpreted sequentially rather than simultaneously.


Inspecting the LilyPond format of a score
-----------------------------------------

Get the LilyPond input format of any Abjad object with ``lilypond_format``:

::

   >>> score.lilypond_format
   "\\new Score <<\n\t\\new Staff {\n\t\te'4\n\t\td'4\n\t\te'4\n\t\tf'4\n\t\tg'1\n\t}\n\t\\new Staff {\n\t\tc'2.\n\t\tb8\n\t\ta8\n\t\tb1\n\t}\n>>"


Use ``f()`` as a short-cut to print the LilyPond format of any Abjad object:

::

   >>> f(score)
   \new Score <<
       \new Staff {
           e'4
           d'4
           e'4
           f'4
           g'1
       }
       \new Staff {
           c'2.
           b8
           a8
           b1
       }
   >>



Selecting the music in a score
------------------------------

Slice a score to select its components:

::

   >>> score[:]
   SimultaneousSelection(Staff{5}, Staff{4})


Abjad returns a selection.


Inspecting a score's leaves
---------------------------

Get the leaves in a score with ``select_leaves()``:

::

   >>> score.select_leaves(allow_discontiguous_leaves=True)
   Selection(Note("e'4"), Note("d'4"), Note("e'4"), Note("f'4"), Note("g'1"), Note("c'2."), Note('b8'), Note('a8'), Note('b1'))


Abjad returns a selection.


Getting the length of a score
-----------------------------

Get the length of a score with ``len()``:

::

   >>> len(score)
   2


The length of a score is defined equal to the number of top-level components
the score contains.


Inspecting duration
-------------------

Use the inspector to get the duration of a score:

::

   >>> inspect(score).get_duration()
   Duration(2, 1)



Adding one component to the bottom of a score
---------------------------------------------

Add one component to the bottom of a score with ``append()``:

::

   >>> bass_staff = Staff("g4 f4 e4 d4 d1")
   >>> bass_clef = indicatortools.Clef('bass')
   >>> bass_clef.attach(bass_staff)
   Clef('bass')(Staff{5})


::

   >>> score.append(bass_staff)


::

   >>> show(score)

.. image:: images/index-3.png



Finding the index of a score component
--------------------------------------

Find the index of a score component with ``index()``:

::

   >>> score.index(treble_staff_1)
   0



Removing a score component by index
-----------------------------------

Use ``pop()`` to remove a score component by index:

::

   >>> score.pop(1)
   Staff{4}


::

   >>> show(score)

.. image:: images/index-4.png



Removing a score component by reference
---------------------------------------

Remove a score component by reference with ``remove()``:

::

   >>> score.remove(treble_staff_1)


::

   >>> show(score)

.. image:: images/index-5.png



Inspecting whether or not a score contains a component
------------------------------------------------------

Use ``in`` to find out whether a score contains a given component:

::

   >>> treble_staff_1 in score
   False


::

   >>> treble_staff_2 in score
   False


::

   >>> bass_staff in score
   True



Naming scores
-------------

You can name Abjad scores:

::

   >>> score.name = 'Example Score'


Score names appear in LilyPond input:

::

   >>> f(score)
   \context Score = "Example Score" <<
       \new Staff {
           \clef "bass"
           g4
           f4
           e4
           d4
           d1
       }
   >>


But do not appear in notational output:

::

   >>> show(score)

.. image:: images/index-6.png

