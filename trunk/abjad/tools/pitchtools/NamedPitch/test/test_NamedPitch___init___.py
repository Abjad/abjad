from abjad import *


def test_NamedPitch__init_by_name_and_octave_01( ):
   '''Init by name and octave.'''

   p = pitchtools.NamedPitch('df', 5)
   assert p.diatonic_pitch_number == 8
   assert p.format == "df''"
   assert p.letter == 'd'
   assert p.pitch_class_name == 'df'
   assert p.number == 13
   assert p.octave_number == 5
   assert p.pitch_class == pitchtools.NumericPitchClass(1)


def test_NamedPitch__init_by_named_pitch_class_and_octave_number_01( ):

   npc = pitchtools.NamedPitchClass('cs')
   octave_number = 5
   pitch = pitchtools.NamedPitch(npc, octave_number)

   assert pitch == pitchtools.NamedPitch('cs', 5)


def test_NamedPitch__init_by_number_01( ):
   '''Init by number.'''

   p = pitchtools.NamedPitch(13)

   assert p.diatonic_pitch_number == 7
   assert p.format == "cs''"
   assert p.letter == 'c'
   assert p.pitch_class_name == 'cs'
   assert p.number == 13
   assert p.octave_number == 5
   assert p.pitch_class == pitchtools.NumericPitchClass(1)



def test_NamedPitch__init_by_number_and_letter_01( ):
   '''Init by number and letter.'''

   p = pitchtools.NamedPitch(13, 'd')

   assert p.diatonic_pitch_number == 8
   assert p.format == "df''"
   assert p.letter == 'd'
   assert p.pitch_class_name == 'df'
   assert p.number == 13
   assert p.octave_number == 5
   assert p.pitch_class == pitchtools.NumericPitchClass(1)



def test_NamedPitch__init_by_pair_01( ):
   '''Init by pair.'''

   p = pitchtools.NamedPitch(('df', 5))

   assert p.diatonic_pitch_number == 8
   assert p.format == "df''"
   assert p.letter == 'd'
   assert p.pitch_class_name == 'df'
   assert p.number == 13
   assert p.octave_number == 5
   assert p.pitch_class == pitchtools.NumericPitchClass(1)



def test_NamedPitch__init_by_pitch_string_01( ):
  
   assert pitchtools.NamedPitch("cs'''") == pitchtools.NamedPitch('cs', 6)
   assert pitchtools.NamedPitch("cs''") == pitchtools.NamedPitch('cs', 5)
   assert pitchtools.NamedPitch("cs'") == pitchtools.NamedPitch('cs', 4)
   assert pitchtools.NamedPitch('cs') == pitchtools.NamedPitch('cs', 3)
   assert pitchtools.NamedPitch('cs,') == pitchtools.NamedPitch('cs', 2)
   assert pitchtools.NamedPitch('cs,,') == pitchtools.NamedPitch('cs', 1)
   assert pitchtools.NamedPitch('cs,,,') == pitchtools.NamedPitch('cs', 0)



def test_NamedPitch__init_by_reference_01( ):
   '''Init by reference.'''

   r = pitchtools.NamedPitch('df', 5)
   p = pitchtools.NamedPitch(r)

   assert p.diatonic_pitch_number == 8
   assert p.format == "df''"
   assert p.letter == 'd'
   assert p.pitch_class_name == 'df'
   assert p.number == 13
   assert p.octave_number == 5
   assert p.pitch_class == pitchtools.NumericPitchClass(1)


def test_NamedPitch__init_empty_01( ):
   '''Init empty.'''

   p = pitchtools.NamedPitch( )

   assert p.diatonic_pitch_number == None
   assert p.format == ''
   assert p.letter == None
   assert p.pitch_class_name == None
   assert p.number == None
   assert p.octave_number == None
   assert p.pitch_class == None
