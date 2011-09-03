Chords
======

Making chords from a LilyPond input string
------------------------------------------

You can make chords from a LilyPond input string:

::

	abjad> chord = Chord("<c' d' bf'>4")


::

	abjad> show(chord)

.. image:: images/chords-1.png

Making chords from chromatic pitch numbers and duration
-------------------------------------------------------

You can also make chords from chromatic pitch numbers and duration:

::

	abjad> chord = Chord([0, 2, 10], Duration(1, 4))


::

	abjad> show(chord)

.. image:: images/chords-2.png

Getting all the written pitches of a chord at once
--------------------------------------------------

You can get all the written pitches of a chord at one time:

::

	abjad> chord.written_pitches
	(NamedChromaticPitch("c'"), NamedChromaticPitch("d'"), NamedChromaticPitch("bf'"))


Abjad returns a read-only tuple of named chromatic pitches.

Getting the written pitches of a chord one at a time
----------------------------------------------------

You can get the written pitches of a chord one at a time:

::

	abjad> chord.written_pitches[0]
	NamedChromaticPitch("c'")


Chords index the pitch they contain starting from ``0`` (just like tuples and lists).

Adding one pitch to a chord at a time
-------------------------------------

Use ``append()`` to add one note to a chord.

You can add a pitch to a chord with a chromatic pitch number:

::

	abjad> chord.append(9)


::

	abjad> show(chord)

.. image:: images/chords-3.png

Or you can add a pitch to a chord with a chromatic pitch name:

::

	abjad> chord.append("df''")


::

	abjad> show(chord)

.. image:: images/chords-4.png

Chords sort their pitches every time you add a new one.

This means you can add pitches to your chord in any order.

Adding many pitches to a chord at once
--------------------------------------

Use ``extend()`` to add many pitches to a chord.

You can use chromatic pitch numbers:

::

	abjad> chord.extend([3, 4, 14])


::

	abjad> show(chord)

.. image:: images/chords-5.png

Or you can chromatic pitch names:

::

	abjad> chord.extend(["g''", "af''"])


::

	abjad> show(chord)

.. image:: images/chords-6.png

Deleting pitches from a chord
-----------------------------

Delete pitches from a chord with ``del()``:

::

	abjad> del(chord[0])


::

	abjad> show(chord)

.. image:: images/chords-7.png

::

	abjad> del(chord[0])


::

	abjad> show(chord)

.. image:: images/chords-8.png

Negative indices work too:

::

	abjad> del(chord[-1])


::

	abjad> show(chord)

.. image:: images/chords-8.png

Formatting chords
-----------------

Get the LilyPond input format of any Abjad object with ``format``:

::

	abjad> chord.format
	<ef' e' a' bf' df'' d'' g''>4


Use ``f()`` as a short-cut to print the LilyPond input format of any Abjad object:

::

	abjad> f(chord)
	<ef' e' a' bf' df'' d'' g''>4


Working with note heads
-----------------------

Most of the time you will work with the pitches of a chord.
But you can get the note heads of a chord, too:

::

	abjad> chord.note_heads
	(NoteHead("ef'"), NoteHead("e'"), NoteHead("a'"), NoteHead("bf'"), NoteHead("df''"), NoteHead("d''"), NoteHead("g''"))


This is useful when you want to apply LilyPond overrides to note heads in a chord one at a time:

::

	abjad> chord[2].tweak.color = 'red'
	abjad> chord[3].tweak.color = 'blue'
	abjad> chord[4].tweak.color = 'green'


::

	abjad> f(chord)
	<
		ef'
		e'
		\tweak #'color #red
		a'
		\tweak #'color #blue
		bf'
		\tweak #'color #green
		df''
		d''
		g''
	>4


::

	abjad> show(chord)

.. image:: images/chords-9.png


Working with empty chords
-------------------------

Abjad allows empty chords:

::

	abjad> chord = Chord([], Duration(1, 4))
	Chord('<>4')


Abjad formats empty chords, too:

::

	abjad> f(chord)
	<>4


But if you pass empty chords to ``show()`` LilyPond will complain
because empty chords don't constitute valid LilyPond input.

When you are done working with an empty chord you can add pitches back
into it chord in any of the ways described above:

::

	abjad> chord.extend(["gf'", "df''", "g''"])


::

	abjad> show(chord)

.. image:: images/chords-10.png
