from abjad import *
import py.test


def test_NamedPitch___init____01( ):
   '''Init by name and octave.'''

   p = pitchtools.NamedPitch('df', 5)
   #assert p.diatonic_pitch_number == 8
   assert p.format == "df''"
   assert p.diatonic_pitch_class_name == 'd'
   assert p.named_pitch_class == pitchtools.NamedPitchClass('df')
   assert p.pitch_number == 13
   assert p.octave_number == 5
   assert p.numeric_pitch_class == pitchtools.NumberedChromaticPitchClass(1)


def test_NamedPitch___init____02( ):

   npc = pitchtools.NamedPitchClass('cs')
   octave_number = 5
   pitch = pitchtools.NamedPitch(npc, octave_number)

   assert pitch == pitchtools.NamedPitch('cs', 5)


def test_NamedPitch___init____03( ):
   '''Init by number.'''

   p = pitchtools.NamedPitch(13)

   #assert p.diatonic_pitch_number == 7
   assert p.format == "cs''"
   assert p.diatonic_pitch_class_name == 'c'
   assert p.named_pitch_class == pitchtools.NamedPitchClass('cs')
   assert p.pitch_number == 13
   assert p.octave_number == 5
   assert p.numeric_pitch_class == pitchtools.NumberedChromaticPitchClass(1)



def test_NamedPitch___init____04( ):
   '''Init by number and diatonic_pitch_class_name.'''

   p = pitchtools.NamedPitch(13, 'd')

   #assert p.diatonic_pitch_number == 8
   assert p.format == "df''"
   assert p.diatonic_pitch_class_name == 'd'
   assert p.named_pitch_class == pitchtools.NamedPitchClass('df')
   assert p.pitch_number == 13
   assert p.octave_number == 5
   assert p.numeric_pitch_class == pitchtools.NumberedChromaticPitchClass(1)



def test_NamedPitch___init____05( ):
   '''Init by pair.'''

   p = pitchtools.NamedPitch(('df', 5))

   #assert p.diatonic_pitch_number == 8
   assert p.format == "df''"
   assert p.diatonic_pitch_class_name == 'd'
   assert p.named_pitch_class == pitchtools.NamedPitchClass('df')
   assert p.pitch_number == 13
   assert p.octave_number == 5
   assert p.numeric_pitch_class == pitchtools.NumberedChromaticPitchClass(1)



def test_NamedPitch___init____06( ):
  
   assert pitchtools.NamedPitch("cs'''") == pitchtools.NamedPitch('cs', 6)
   assert pitchtools.NamedPitch("cs''") == pitchtools.NamedPitch('cs', 5)
   assert pitchtools.NamedPitch("cs'") == pitchtools.NamedPitch('cs', 4)
   assert pitchtools.NamedPitch('cs') == pitchtools.NamedPitch('cs', 3)
   assert pitchtools.NamedPitch('cs,') == pitchtools.NamedPitch('cs', 2)
   assert pitchtools.NamedPitch('cs,,') == pitchtools.NamedPitch('cs', 1)
   assert pitchtools.NamedPitch('cs,,,') == pitchtools.NamedPitch('cs', 0)



def test_NamedPitch___init____07( ):
   '''Init by reference.'''

   r = pitchtools.NamedPitch('df', 5)
   p = pitchtools.NamedPitch(r)

   #assert p.diatonic_pitch_number == 8
   assert p.format == "df''"
   assert p.diatonic_pitch_class_name == 'd'
   assert p.named_pitch_class == pitchtools.NamedPitchClass('df')
   assert p.pitch_number == 13
   assert p.octave_number == 5
   assert p.numeric_pitch_class == pitchtools.NumberedChromaticPitchClass(1)


def test_NamedPitch___init____08( ):
   '''Empty pitches now allowed.
   '''

   assert py.test.raises(Exception, 'pitchtools.NamedPitch( )')
