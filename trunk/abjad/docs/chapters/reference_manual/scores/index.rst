Scores
======

Creating scores
---------------

Create a score like this:

::

	abjad> treble_staff_1 = Staff("e'4 d'4 e'4 f'4 g'1")
	abjad> treble_staff_2 = Staff("c'2. b8 a8 b1")


::

	abjad> score = Score([treble_staff_1, treble_staff_2])


::

	abjad> show(score)

.. image:: images/scores-1.png

Inspecting score music
----------------------

Return score components with ``music``:

::

	abjad> score.music
	(Staff{5}, Staff{4})


Inspecting score length
-----------------------

Get score length with ``len()``:

::

	abjad> len(score)
	2


Inspecting score duration
-------------------------

Score contents duration is equal to the duration of the longest component in score:

::

	abjad> score.contents_duration
	Duration(2, 1)


Adding one component to the bottom of a score
---------------------------------------------

Add one component to the bottom of a score with ``append``:

::

	abjad> bass_staff = Staff("g4 f4 e4 d4 d1")
	abjad> contexttools.ClefMark('bass')(bass_staff)


::

	abjad> score.append(bass_staff)


::

	abjad> show(score)

.. image:: images/scores-2.png

Finding the index of a score component
--------------------------------------

Find the index of a score component with ``index``:

::

	abjad> score.index(treble_staff_1)
	0


Removing a score component by index
-----------------------------------

Use ``pop`` to remove a score component by index:

::

	abjad> score.pop(1)


::

	abjad> show(score)

.. image:: images/scores-3.png

Removing a score component by reference
---------------------------------------

Remove a score component by reference with ``remove``:

::

	abjad> score.remove(treble_staff_1)


::

	abjad> show(score)

.. image:: images/scores-4.png

Testing score containment
-------------------------

Use ``in`` to find out whether a score contains a given component:

::

	abjad> treble_staff_1 in score
	False


::

	abjad> treble_staff_2 in score
	False


::

	abjad> bass_staff in score
	True


Naming scores
-------------

You can name Abjad scores:

::

	abjad> score.name = 'Example Score'


Score names appear in LilyPond input:

::

	abjad> f(score)
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

	abjad> show(score)

.. image:: images/scores-5.png
