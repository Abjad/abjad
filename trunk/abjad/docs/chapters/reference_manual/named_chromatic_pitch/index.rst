Pitches
=======

Named chromatic pitches are the everyday pitches attached to notes and chords:

::

	abjad> note = Note("cs''8")


::

	abjad> note.written_pitch
	NamedChromaticPitch("cs''")



Creating pitches
----------------

Use pitch tools to create named chromatic pitches:

::

	abjad> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")


::

	abjad> named_chromatic_pitch
	NamedChromaticPitch("cs''")



Inspecting the name of a pitch
------------------------------

Use ``str()`` to get the name of named chromatic pitches:

::

	abjad> str(named_chromatic_pitch)
	cs''



Inspecting the octave of a pitch
--------------------------------

Get the octave number of named chromatic pitches with ``octave_number``:

::

	abjad> named_chromatic_pitch.octave_number
	5



Working with pitch deviation
----------------------------

Use deviation to model the fact that two pitches differ by a fraction of a semitone:

::

	abjad> note_1 = Note(24, (1, 2))
	abjad> note_2 = Note(24, (1, 2))
	abjad> staff = Staff([note_1, note_2])


::

	abjad> show(staff)

.. image:: images/pitch-deviation-1.png

::

	abjad> note_2.written_pitch = pitchtools.NamedChromaticPitch(24, deviation = -31)


The pitch of the the first note is greater than the pitch of the second:

::

	abjad> note_1.written_pitch > note_2.written_pitch
	True


Use markup to include indications of pitch deviation in your score:

::

	abjad> markuptools.Markup(note_2.written_pitch.deviation_in_cents, 'up')(note_2)

.. image:: images/pitch-deviation-2.png


Sorting pitches
---------------

Named chromatic pitches sort by octave, diatonic pitch-class and accidental,
in that order:

::

	abjad> pitchtools.NamedChromaticPitch('es') < pitchtools.NamedChromaticPitch('ff')
	True



Comparing pitches
-----------------

Compare named chromatic pitches to each other:

::

	abjad> named_chromatic_pitch_1 = pitchtools.NamedChromaticPitch("c''")
	abjad> named_chromatic_pitch_2 = pitchtools.NamedChromaticPitch("d''")


::

	abjad> named_chromatic_pitch_1 == named_chromatic_pitch_2
	False


::

	abjad> named_chromatic_pitch_1 != named_chromatic_pitch_2
	True


::

	abjad> named_chromatic_pitch_1 > named_chromatic_pitch_2
	False


::

	abjad> named_chromatic_pitch_1 < named_chromatic_pitch_2
	True


::

	abjad> named_chromatic_pitch_1 >= named_chromatic_pitch_2
	False


::

	abjad> named_chromatic_pitch_1 <= named_chromatic_pitch_2
	True



Converting one type of pitch to another
---------------------------------------

Convert any named chromatic pitch to a named diatonic pitch:

::

	abjad> named_chromatic_pitch.named_diatonic_pitch
	NamedDiatonicPitch("c''")


To a numbered chromatic pitch:

::

	abjad> named_chromatic_pitch.numbered_chromatic_pitch
	NumberedChromaticPitch(13)


Or to a numbered diatonic pitch:

::

	abjad> named_chromatic_pitch.numbered_diatonic_pitch
	NumberedDiatonicPitch(7)



Converting pitches to pitch-classes
-----------------------------------

Convert any named chromatic pitch to a named chromatic pitch-class:

::

	abjad> named_chromatic_pitch.named_chromatic_pitch_class
	NamedChromaticPitchClass('cs')


To a named diatonic pitch-class:

::

	abjad> named_chromatic_pitch.named_diatonic_pitch_class
	NamedDiatonicPitchClass('c')


To a numbered chromatic pitch-class:

::

	abjad> named_chromatic_pitch.numbered_chromatic_pitch_class
	NumberedChromaticPitchClass(1)


Or to a numbered diatonic pitch-class:

::

	abjad> named_chromatic_pitch.numbered_diatonic_pitch_class
	NumberedDiatonicPitchClass(0)



Copying pitches
---------------

Use ``copy.copy()`` to copy named chromatic pitches:

::

	abjad> import copy


::

	abjad> copy.copy(named_chromatic_pitch)
	NamedChromaticPitch("cs''")


Or use ``copy.deepcopy()`` to do the same thing.
