from abjad import *


def test_pitchtools_PitchRange___init___01( ):
   '''Init infinite pitch range.'''

   pr = pitchtools.PitchRange( )
   assert pr.start is None
   assert pr.stop is None


def test_pitchtools_PitchRange___init___02( ):
   '''Init stop-specified pitch range.'''

   pr = pitchtools.PitchRange((-39, 'inclusive'), None)
   assert pr.start == (pitchtools.NamedChromaticPitch(-39), 'inclusive')
   assert pr.stop is None

   pr = pitchtools.PitchRange((-39, 'exclusive'), None)
   assert pr.start == (pitchtools.NamedChromaticPitch(-39), 'exclusive')
   assert pr.stop is None
   

def test_pitchtools_PitchRange___init___03( ):
   '''Init start-specified pitch range.'''

   pr = pitchtools.PitchRange(None, (48, 'inclusive'))
   assert pr.start is None
   assert pr.stop == (pitchtools.NamedChromaticPitch(48), 'inclusive')

   pr = pitchtools.PitchRange(None, (48, 'exclusive'))
   assert pr.start is None
   assert pr.stop == (pitchtools.NamedChromaticPitch(48), 'exclusive')


def test_pitchtools_PitchRange___init___04( ):
   '''Init start- and stop-specified pitch range.'''

   pr = pitchtools.PitchRange((-39, 'inclusive'), (48, 'inclusive'))
   assert pr.start == (pitchtools.NamedChromaticPitch(-39), 'inclusive')
   assert pr.stop == (pitchtools.NamedChromaticPitch(48), 'inclusive')


def test_pitchtools_PitchRange___init___05( ):
   '''Short-form init with only integers.'''

   pr = pitchtools.PitchRange(-39, 48)
   assert pr.start == (pitchtools.NamedChromaticPitch(-39), 'inclusive')
   assert pr.stop == (pitchtools.NamedChromaticPitch(48), 'inclusive')
