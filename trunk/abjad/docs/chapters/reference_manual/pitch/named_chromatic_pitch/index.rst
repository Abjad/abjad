Pitches
=======

Named chromatic pitches are the everyday pitches attached to notes and chords:

::

	abjad> note = Note("cs''8")


::

	abjad> note.written_pitch
	NamedChromaticPitch("cs''")


Creation
--------

Use pitch tools to create named chromatic pitches:

::

	abjad> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")


::

	abjad> named_chromatic_pitch
	NamedChromaticPitch("cs''")


Name inspection
---------------

Use ``str( )`` to get the name of named chromatic pitches:

::

	abjad> str(named_chromatic_pitch)
	cs''


Octave inspection
-----------------

Get the octave number of named chromatic pitches with ``octave_number``:

::

	abjad> named_chromatic_pitch.octave_number
	5


Sorting
-------

Named chromatic pitches sort by octave, diatonic pitch-class and accidental,
in that order:

::

	abjad> pitchtools.NamedChromaticPitch('es') < pitchtools.NamedChromaticPitch('ff')
	True


Pitch comparison
----------------

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


Pitch conversion
----------------

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


Pitch-class conversion
----------------------

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


Copying
-------

Use ``copy.copy( )`` to copy named chromatic pitches:

::

	abjad> import copy


::

	abjad> copy.copy(named_chromatic_pitch)
	NamedChromaticPitch("cs''")


Or use ``copy.deepcopy( )`` to do the same thing:

::

	abjad> copy.deepcopy(named_chromatic_pitch)
	NamedChromaticPitch("cs''")

