from abjad import *


def test_pitchtools_PitchRange___init____01( ):
   '''Init infinite pitch range.'''

   pr = pitchtools.PitchRange( )
   assert pr.start is None
   assert pr.stop is None


def test_pitchtools_PitchRange___init____02( ):
   '''Init stop-specified pitch range.'''

   pr = pitchtools.PitchRange((-39, 'inclusive'), None)
   assert pr.start == (NamedPitch(-39), 'inclusive')
   assert pr.stop is None

   pr = pitchtools.PitchRange((-39, 'exclusive'), None)
   assert pr.start == (NamedPitch(-39), 'exclusive')
   assert pr.stop is None
   

def test_pitchtools_PitchRange___init____03( ):
   '''Init start-specified pitch range.'''

   pr = pitchtools.PitchRange(None, (48, 'inclusive'))
   assert pr.start is None
   assert pr.stop == (NamedPitch(48), 'inclusive')

   pr = pitchtools.PitchRange(None, (48, 'exclusive'))
   assert pr.start is None
   assert pr.stop == (NamedPitch(48), 'exclusive')


def test_pitchtools_PitchRange___init____04( ):
   '''Init start- and stop-specified pitch range.'''

   pr = pitchtools.PitchRange((-39, 'inclusive'), (48, 'inclusive'))
   assert pr.start == (NamedPitch(-39), 'inclusive')
   assert pr.stop == (NamedPitch(48), 'inclusive')


def test_pitchtools_PitchRange___init____05( ):
   '''Short-form init with only integers.'''

   pr = pitchtools.PitchRange(-39, 48)
   assert pr.start == (NamedPitch(-39), 'inclusive')
   assert pr.stop == (NamedPitch(48), 'inclusive')
