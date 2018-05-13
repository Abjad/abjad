Named pitches
=============

..  abjad::

    import abjad

Named pitches are the everyday pitches of notes and chords:

..  abjad::

    note = abjad.Note("cs''8")
    note.written_pitch

..  abjad::

    show(note)


Creating named pitches
----------------------

Create named pitches like this:

..  abjad::

    named_pitch = abjad.NamedPitch("cs''")


Understanding the interpreter representation of a named pitch
-------------------------------------------------------------

..  abjad::

    named_pitch

``NamedPitch`` tells you the pitch's class.

``cs''`` tells you the pitch is equal to ``C#5``.


Understanding the string representation of a named pitch
--------------------------------------------------------

..  abjad::

    str(named_pitch)

``cs''`` tells you the pitch is equal to ``C#5``.


Getting the accidental of a named pitch
---------------------------------------

Use ``accidental`` to get the accidental of a named pitch:

..  abjad::

    named_pitch.accidental


Getting the octave of a named pitch
-----------------------------------

Use ``octave`` to get the octave of a named pitch:

..  abjad::

    named_pitch.octave


Comparing named pitches
-----------------------

Named pitches compare equal with equal pitch-class and octave:

..  abjad::

    named_pitch_1 = abjad.NamedPitch("cs''")
    named_pitch_2 = abjad.NamedPitch("df''")

..  abjad::

    named_pitch_1 == named_pitch_1
    named_pitch_1 == named_pitch_2

..  abjad::

    named_pitch_2 == named_pitch_1
    named_pitch_2 == named_pitch_2

You can also compare named pitches with greater-than and less-than:

..  abjad::

    named_pitch_1 < named_pitch_1
    named_pitch_1 < named_pitch_2
    named_pitch_2 < named_pitch_1
    named_pitch_2 < named_pitch_2

..  abjad::

    named_pitch_1 <= named_pitch_1
    named_pitch_1 <= named_pitch_2
    named_pitch_2 <= named_pitch_1
    named_pitch_2 <= named_pitch_2

..  abjad::

    named_pitch_1 > named_pitch_1
    named_pitch_1 > named_pitch_2
    named_pitch_2 > named_pitch_1
    named_pitch_2 > named_pitch_2

..  abjad::

    named_pitch_1 >= named_pitch_1
    named_pitch_1 >= named_pitch_2
    named_pitch_2 >= named_pitch_1
    named_pitch_2 >= named_pitch_2


Changing named pitches to named pitch-classes
---------------------------------------------

Use ``pitch_class`` to change a named pitch to a named pitch-class:

..  abjad::

    named_pitch.pitch_class

Or use ``NamedPitchClass``:

..  abjad::

    abjad.NamedPitchClass(named_pitch)


Changing named pitches to numbered pitches
------------------------------------------

Use ``NumberedPitch`` to change a named pitch to a numbered pitch:

..  abjad::

    abjad.NumberedPitch(named_pitch)


Changing named pitches to numbered pitch-classes
------------------------------------------------

Change named pitches to numbered pitch-classes like this:

Or use ``pitchtools``:

..  abjad::

    abjad.NumberedPitchClass(named_pitch)
