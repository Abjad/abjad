Scores
======


Making a score from a LilyPond input string
-------------------------------------------

You can make an Abjad score from a LilyPond input string:

..  abjad::

    input = r'''
    \new Staff { e''4 d''8 ( c''8 ) d''4 g'4 }
    \new Staff { \clef bass c4 a,4 b,4 e4 }
    '''

..  abjad::

    score = Score(input)

..  abjad::

    show(score)


Making a score from a list of Abjad components
----------------------------------------------

You can also make a score from a list of other Abjad components:

..  abjad::

    treble_staff_1 = Staff("e'4 d'4 e'4 f'4 g'1")
    treble_staff_2 = Staff("c'2. b8 a8 b1")

..  abjad::

    score = Score([treble_staff_1, treble_staff_2])

..  abjad::

    show(score)


Understanding the interpreter representation of a score
-------------------------------------------------------

The interpreter representation of an Abjad score contains three parts:

..  abjad::

    score

``Score`` tells you the score's class.

``2`` tells you the score's length (which is the number of top-level components
the score contains).

Curly braces ``{`` and ``}`` tell you that the music inside the score is
interpreted sequentially rather than simultaneously.


Understanding the LilyPond format of a score
--------------------------------------------

Use ``format()`` to get the LilyPond format of a score:

..  abjad::

    print(format(score, 'lilypond'))


Selecting the music in a score
------------------------------

Slice a score to select its components:

..  abjad::

    score[:]


Selecting a score's leaves
--------------------------

Use ``list(iterate(score).by_leaf())`` to select the leaves in a score:

..  abjad::

    list(iterate(score).by_leaf())


Getting the length of a score
-----------------------------

Use ``len()`` to get the length of a score.

The length of a score is defined equal to the number of top-level components
the score contains:

..  abjad::

    len(score)


Inspecting duration
-------------------

Use the inspector to get the duration of a score:

..  abjad::

    inspect_(score).get_duration()


Appending one component to the bottom of a score
------------------------------------------------

Use ``append()`` to append one component to the bottom of a score:

..  abjad::

    staff = Staff("g4 f4 e4 d4 d1")
    clef = Clef('bass')
    attach(clef, staff)

..  abjad::

    score.append(staff)

..  abjad::

    show(score)


Finding the index of a score component
--------------------------------------

Use ``index()`` to find the index of a score component:

..  abjad::

    score.index(treble_staff_1)


Removing a score component by index
-----------------------------------

Use ``pop()`` to remove a score component by index:

..  abjad::

    score.pop(1)

..  abjad::

    show(score)


Removing a score component by reference
---------------------------------------

Use ``remove()`` to remove a score component by reference:

..  abjad::

    score.remove(treble_staff_1)

..  abjad::

    show(score)


Inspecting whether or not a score contains a component
------------------------------------------------------

Use ``in`` to find out whether a score contains a given component:

..  abjad::

    treble_staff_1 in score

..  abjad::

    treble_staff_2 in score

..  abjad::

    staff in score


Naming scores
-------------

You can name Abjad scores:

..  abjad::

    score.name = 'Example Score'

Score names appear in LilyPond input but not in notational output:

..  abjad::

    print(format(score))

..  abjad::

    show(score)
