from abjad import *


def test_DiatonicIntervalClass__init_by_quality_string_and_number_01( ):
   '''Init unison.'''

   assert str(pitchtools.DiatonicIntervalClass('perfect', 1)) == 'P1'
   assert str(pitchtools.DiatonicIntervalClass('perfect', -1)) == 'P1'
   assert str(pitchtools.DiatonicIntervalClass('augmented', 1)) == 'aug1'
   assert str(pitchtools.DiatonicIntervalClass('augmented', -1)) == 'aug1'
   assert str(pitchtools.DiatonicIntervalClass('diminished', 1)) == 'dim1'
   assert str(pitchtools.DiatonicIntervalClass('diminished', -1)) == 'dim1'


def test_DiatonicIntervalClass__init_by_quality_string_and_number_02( ):
   '''Init usual cases.'''

   assert str(pitchtools.DiatonicIntervalClass('minor', 2)) == 'm2'
   assert str(pitchtools.DiatonicIntervalClass('major', 2)) == 'M2'
   assert str(pitchtools.DiatonicIntervalClass('minor', 3)) == 'm3'
   assert str(pitchtools.DiatonicIntervalClass('major', 3)) == 'M3'
   assert str(pitchtools.DiatonicIntervalClass('perfect', 4)) == 'P4'
   assert str(pitchtools.DiatonicIntervalClass('augmented', 4)) == 'aug4'


def test_DiatonicIntervalClass__init_by_quality_string_and_number_03( ):
   '''Init inverted cases less than one octave.'''

   assert str(pitchtools.DiatonicIntervalClass('major', 7)) == 'm2'
   assert str(pitchtools.DiatonicIntervalClass('minor', 7)) == 'M2'
   assert str(pitchtools.DiatonicIntervalClass('major', 6)) == 'm3'
   assert str(pitchtools.DiatonicIntervalClass('minor', 6)) == 'M3'
   assert str(pitchtools.DiatonicIntervalClass('perfect', 5)) == 'P4'
   assert str(pitchtools.DiatonicIntervalClass('diminished', 5)) == 'aug4'


def test_DiatonicIntervalClass__init_by_quality_string_and_number_04( ):
   '''Init noninverted cases greater than one octave.'''

   assert str(pitchtools.DiatonicIntervalClass('minor', 9)) == 'm2'
   assert str(pitchtools.DiatonicIntervalClass('major', 9)) == 'M2'
   assert str(pitchtools.DiatonicIntervalClass('minor', 10)) == 'm3'
   assert str(pitchtools.DiatonicIntervalClass('major', 10)) == 'M3'
   assert str(pitchtools.DiatonicIntervalClass('perfect', 11)) == 'P4'
   assert str(pitchtools.DiatonicIntervalClass('augmented', 11)) == 'aug4'


def test_DiatonicIntervalClass__init_by_quality_string_and_number_05( ):
   '''Init inverted cases greater than one octave.'''

   assert str(pitchtools.DiatonicIntervalClass('major', 14)) == 'm2'
   assert str(pitchtools.DiatonicIntervalClass('minor', 14)) == 'M2'
   assert str(pitchtools.DiatonicIntervalClass('major', 13)) == 'm3'
   assert str(pitchtools.DiatonicIntervalClass('minor', 13)) == 'M3'
   assert str(pitchtools.DiatonicIntervalClass('perfect', 12)) == 'P4'
   assert str(pitchtools.DiatonicIntervalClass('diminished', 12)) == 'aug4'
