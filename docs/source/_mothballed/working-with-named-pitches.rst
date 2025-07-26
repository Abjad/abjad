:orphan:

..  todo:: Include in complete overview of Abjad's pitch system.

Working with named pitches
==========================

Abjad's named pitches model the everyday pitches of notes and chords:

::

    >>> note = abjad.Note("cs''8")
    >>> abjad.show(note)

    >>> pitch = note.get_written_pitch()
    >>> pitch

----

**Properties.** Get the accidental of a named pitch like this:

::

    >>> pitch.get_accidental()

Get the octave of a named pitch like this:

::

    >>> pitch.get_octave()

----

**Equality testing.** Named pitches compare equal with equal pitch-class and octave:

::

    >>> pitch_1 = abjad.NamedPitch("cs''")
    >>> pitch_2 = abjad.NamedPitch("df''")

::

    >>> pitch_1 == pitch_1
    >>> pitch_1 == pitch_2

::

    >>> pitch_2 == pitch_1
    >>> pitch_2 == pitch_2

You can also compare named pitches with greater-than and less-than:

::

    >>> pitch_1 < pitch_1
    >>> pitch_1 < pitch_2
    >>> pitch_2 < pitch_1
    >>> pitch_2 < pitch_2

::

    >>> pitch_1 <= pitch_1
    >>> pitch_1 <= pitch_2
    >>> pitch_2 <= pitch_1
    >>> pitch_2 <= pitch_2

::

    >>> pitch_1 > pitch_1
    >>> pitch_1 > pitch_2
    >>> pitch_2 > pitch_1
    >>> pitch_2 > pitch_2

::

    >>> pitch_1 >= pitch_1
    >>> pitch_1 >= pitch_2
    >>> pitch_2 >= pitch_1
    >>> pitch_2 >= pitch_2

----

**Conversion.** Change a named pitch to a named pitch-class like this:

::

    >>> pitch.get_pitch_class()

    >>> abjad.NamedPitchClass(pitch)

Change a named pitch to a numbered pitch like this:

::

    >>> abjad.NumberedPitch(pitch)

Change a named pitch to a numbered pitch-class like this:

::

    >>> abjad.NumberedPitchClass(pitch)
