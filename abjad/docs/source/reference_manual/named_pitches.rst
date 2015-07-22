Named pitches
=============

Named pitches are the everyday pitches of notes and chords:

<abjad>
note = Note("cs''8")
note.written_pitch
</abjad>

<abjad>
show(note)
</abjad>


Creating named pitches
----------------------

Create named pitches like this:

<abjad>
named_pitch = NamedPitch("cs''")
</abjad>


Understanding the interpreter representation of a named pitch
-------------------------------------------------------------

<abjad>
named_pitch
</abjad>

``NamedPitch`` tells you the pitch's class.

``cs''`` tells you the pitch is equal to ``C#5``.


Understanding the string representation of a named pitch
--------------------------------------------------------

<abjad>
str(named_pitch)
</abjad>

``cs''`` tells you the pitch is equal to ``C#5``.


Getting the accidental of a named pitch
---------------------------------------

Use ``accidental`` to get the accidental of a named pitch:

<abjad>
named_pitch.accidental
</abjad>


Getting the octave of a named pitch
-----------------------------------

Use ``octave`` to get the octave of a named pitch:

<abjad>
named_pitch.octave
</abjad>


Comparing named pitches
-----------------------

Named pitches compare equal with equal pitch-class and octave:

<abjad>
named_pitch_1 = pitchtools.NamedPitch("cs''")
named_pitch_2 = pitchtools.NamedPitch("df''")
</abjad>

<abjad>
named_pitch_1 == named_pitch_1
named_pitch_1 == named_pitch_2
</abjad>

<abjad>
named_pitch_2 == named_pitch_1
named_pitch_2 == named_pitch_2
</abjad>

You can also compare named pitches with greater-than and less-than:

<abjad>
named_pitch_1 < named_pitch_1
named_pitch_1 < named_pitch_2
named_pitch_2 < named_pitch_1
named_pitch_2 < named_pitch_2
</abjad>

<abjad>
named_pitch_1 <= named_pitch_1
named_pitch_1 <= named_pitch_2
named_pitch_2 <= named_pitch_1
named_pitch_2 <= named_pitch_2
</abjad>

<abjad>
named_pitch_1 > named_pitch_1
named_pitch_1 > named_pitch_2
named_pitch_2 > named_pitch_1
named_pitch_2 > named_pitch_2
</abjad>

<abjad>
named_pitch_1 >= named_pitch_1
named_pitch_1 >= named_pitch_2
named_pitch_2 >= named_pitch_1
named_pitch_2 >= named_pitch_2
</abjad>


Changing named pitches to named pitch-classes
---------------------------------------------

Use ``named_pitch_class`` to change a named pitch to a named pitch-class:

<abjad>
named_pitch.named_pitch_class
</abjad>

Or use ``pitchtools``:

<abjad>
pitchtools.NamedPitchClass(named_pitch)
</abjad>


Changing named pitches to numbered pitches
------------------------------------------

Use ``numbered_pitch`` to change a named pitch to a numbered pitch:

<abjad>
named_pitch.numbered_pitch
</abjad>

Or use ``pitchtools``:

<abjad>
pitchtools.NumberedPitch(named_pitch)
</abjad>


Changing named pitches to numbered pitch-classes
------------------------------------------------

Use ``numbered_pitch_class`` to change a named pitch to a numbered pitch-class:

<abjad>
named_pitch.numbered_pitch_class
</abjad>

Or use ``pitchtools``:

<abjad>
pitchtools.NumberedPitchClass(named_pitch)
</abjad>
