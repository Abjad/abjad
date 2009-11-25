from abjad import *


def test_pitch_init_01( ):
   '''Empty pitch initialization.'''

   p = Pitch( )

   assert repr(p) == 'Pitch( )'
   assert p.altitude == None
   assert p.degree == None
   assert p.format == ''
   assert p.letter == None
   assert p.name == None
   assert p.number == None
   assert p.octave == None
   assert p.pair == None
   assert p.pc == None
   assert p.ticks == None


def test_pitch_init_02( ):
   '''Integer pitch initialization.'''

   p = Pitch(13)

   assert repr(p) == "Pitch(cs, 5)"
   assert p.altitude == 7
   assert p.degree == 1
   assert p.format == "cs''"
   assert p.letter == 'c'
   assert p.name == 'cs'
   assert p.number == 13
   assert p.octave == 5
   assert p.pair == ('cs', 5)
   assert p.pc == pitchtools.PitchClass(1)
   assert p.ticks == "''"


def test_pitch_init_03( ):
   '''Name-and-octave initialization.'''

   p = Pitch('df', 5)
   assert repr(p) == "Pitch(df, 5)"
   assert p.altitude == 8
   assert p.degree == 2
   assert p.format == "df''"
   assert p.letter == 'd'
   assert p.name == 'df'
   assert p.number == 13
   assert p.octave == 5
   assert p.pair == ('df', 5)
   assert p.pc == pitchtools.PitchClass(1)
   assert p.ticks == "''"


def test_pitch_init_04( ):
   '''Pitch pair initialization.'''

   p = Pitch(('df', 5))

   assert repr(p) == "Pitch(df, 5)"
   assert p.altitude == 8
   assert p.degree == 2
   assert p.format == "df''"
   assert p.letter == 'd'
   assert p.name == 'df'
   assert p.number == 13
   assert p.octave == 5
   assert p.pair == ('df', 5)
   assert p.pc == pitchtools.PitchClass(1)
   assert p.ticks == "''"


def test_pitch_init_05( ):
   '''Pitch reference initialization.'''

   r = Pitch('df', 5)
   p = Pitch(r)

   assert repr(p) == "Pitch(df, 5)"
   assert p.altitude == 8
   assert p.degree == 2
   assert p.format == "df''"
   assert p.letter == 'd'
   assert p.name == 'df'
   assert p.number == 13
   assert p.octave == 5
   assert p.pair == ('df', 5)
   assert p.pc == pitchtools.PitchClass(1)
   assert p.ticks == "''"


def test_pitch_init_06( ):
   '''Pitch number-and-letter initialization.'''

   p = Pitch(13, 'd')

   assert repr(p) == "Pitch(df, 5)"
   assert p.altitude == 8
   assert p.degree == 2
   assert p.format == "df''"
   assert p.letter == 'd'
   assert p.name == 'df'
   assert p.number == 13
   assert p.octave == 5
   assert p.pair == ('df', 5)
   assert p.pc == pitchtools.PitchClass(1)
   assert p.ticks == "''"
