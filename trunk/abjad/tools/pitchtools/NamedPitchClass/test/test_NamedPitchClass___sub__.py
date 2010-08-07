from abjad import *


def test_NamedPitchClass___sub___01( ):

   mdi = pitchtools.NamedPitchClass('c') - pitchtools.NamedPitchClass('d')
   assert mdi == pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2)

   mdi = pitchtools.NamedPitchClass('d') - pitchtools.NamedPitchClass('c')
   assert mdi == pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2)


def test_NamedPitchClass___sub___02( ):

   mdi = pitchtools.NamedPitchClass('c') - pitchtools.NamedPitchClass('cf')
   assert mdi == pitchtools.InversionEquivalentDiatonicIntervalClass('augmented', 1)

   mdi = pitchtools.NamedPitchClass('cf') - pitchtools.NamedPitchClass('c')
   assert mdi == pitchtools.InversionEquivalentDiatonicIntervalClass('augmented', 1)
