Working with LilyPond multipliers
=================================

The LilyPond ``*`` operator allows the creation of duration multipliers
against notes, rests, chords and skips.

You can assign LilyPond multipliers in Abjad:

::

	abjad> note = Note("c'4")
	abjad> note.duration_multiplier = Fraction(1, 6)


LilyPond multipliers change the multiplied duration of notes, rests, chords and skips:

::

	abjad> note.multiplied_duration
	Duration(1, 24)


LilyPond multipliers leave written duration unchanged:

::

	abjad> note.written_duration
	Duration(1, 4)

