Notes
=====

Making notes from a string
--------------------------

You can make notes from string:

::

	abjad> note = Note("c'4")


::

	abjad> show(note)

.. image:: images/example-1.png

Making notes from chromatic pitch number and duration
-----------------------------------------------------

You can also make notes from chromatic pitch number and duration:

::

	abjad> note = Note(0, Duration(1, 4))


::

	abjad> show(note)

.. image:: images/example-2.png

(You even use ``Note(0, (1, 4))`` to create notes with numbers alone.)

Getting the written pitch of notes
----------------------------------

You can get the written pitch of notes:

::

	abjad> note.pitch
	NamedChromaticPitch("c'")


Changing the written pitch of notes
-----------------------------------

And you can change the written pitch of notes:

::

	abjad> note.pitch = "cs'"

.. image:: images/example-3.png

(You can use ``note.pitch = 1`` to change pitch with numbers, too.)

Getting the duration attributes of notes
----------------------------------------

Get the written duration of notes like this:

::

	abjad> note.duration.written
	Duration(1, 4)


Which is usually the same as preprolated duration:

::

	abjad> note.duration.preprolated
	Duration(1, 4)


And prolated duration:

::

	abjad> note.duration.prolated
	Duration(1, 4)


Except for notes inside a tuplet:

::

	abjad> tuplet = Tuplet((2, 3), [Note("c'4"), Note("d'4"), Note("e'4")])


::

	abjad> show(tuplet)

.. image:: images/example-4.png

::

	abjad> note = tuplet[0]


Tupletted notes carry written duration:

::

	abjad> note.duration.written
	Duration(1, 4)


Prolation:

::

	abjad> note.duration.prolation
	Fraction(2, 3)


And prolated duration that is the product of the two:

::

	abjad> note.duration.prolated
	Duration(1, 6)


Changing the written duration of notes
--------------------------------------

You can change the written duration of notes:

::

	abjad> tuplet[0].duration.written = Duration(1, 8)
	abjad> tuplet[1].duration.written = Duration(1, 8)
	abjad> tuplet[2].duration.written = Duration(1, 8)


::

	abjad> show(tuplet)

.. image:: images/example-5.png

Other duration attributes are read-only.

Overriding notes
----------------

The notes below are black with fixed thickness and predetermined spacing:

::

	abjad> staff = Staff("c'4 d'4 e'4 f'4 g'4 a'4 g'2")
	abjad> slur_1 = spannertools.SlurSpanner(staff[:2])
	abjad> slur_2 = spannertools.SlurSpanner(staff[2:4])
	abjad> slur_3 = spannertools.SlurSpanner(staff[4:6])


::

	abjad> f(staff)
	\new Staff {
		c'4 (
		d'4 )
		e'4 (
		f'4 )
		g'4 (
		a'4 )
		g'2
	}


::

	abjad> show(staff)

.. image:: images/example-6.png

But you can override LilyPond grobs to change the look of notes, rests and chords:

::

	abjad> staff[-1].override.note_head.color = 'red'
	abjad> staff[-1].override.stem.color = 'red'


::

	abjad> f(staff)
	\new Staff {
		c'4 (
		d'4 )
		e'4 (
		f'4 )
		g'4 (
		a'4 )
		\once \override NoteHead #'color = #red
		\once \override Stem #'color = #red
		g'2
	}


::

	abjad> show(staff)

.. image:: images/example-7.png

Removing note overrides
-----------------------

Delete grob overrides you no longer want:

::

	abjad> del(staff[-1].override.stem)


::

	abjad> f(staff)
	\new Staff {
		c'4 (
		d'4 )
		e'4 (
		f'4 )
		g'4 (
		a'4 )
		\once \override NoteHead #'color = #red
		g'2
	}


::

	abjad> show(staff)

.. image:: images/example-8.png
