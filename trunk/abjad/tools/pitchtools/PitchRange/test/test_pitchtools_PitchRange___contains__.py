from abjad import *


def test_pitchtools_PitchRange___contains___01( ):
   '''Closed / closed range.'''

   pr = pitchtools.PitchRange((-39, 'inclusive'), (48, 'inclusive'))
   assert -99 not in pr
   assert -39     in pr
   assert   0     in pr
   assert  48     in pr
   assert  99 not in pr
   

def test_pitchtools_PitchRange___contains___02( ):
   '''Closed / open range.'''

   pr = pitchtools.PitchRange((-39, 'inclusive'), (48, 'exclusive'))
   assert -99 not in pr
   assert -39     in pr
   assert   0     in pr
   assert  48 not in pr
   assert  99 not in pr


def test_pitchtools_PitchRange___contains___03( ):
   '''Closed / infinite range.'''

   pr = pitchtools.PitchRange((-39, 'inclusive'), None)
   assert -99 not in pr
   assert -39     in pr
   assert   0     in pr
   assert  48     in pr
   assert  99     in pr
   

def test_pitchtools_PitchRange___contains___04( ):
   '''Open / closed range.'''

   pr = pitchtools.PitchRange((-39, 'exclusive'), (48, 'inclusive'))
   assert -99 not in pr
   assert -39 not in pr
   assert   0     in pr
   assert  48     in pr
   assert  99 not in pr
   

def test_pitchtools_PitchRange___contains___05( ):
   '''Open / open range.'''

   pr = pitchtools.PitchRange((-39, 'exclusive'), (48, 'exclusive'))
   assert -99 not in pr
   assert -39 not in pr
   assert   0     in pr
   assert  48 not in pr
   assert  99 not in pr
   

def test_pitchtools_PitchRange___contains___06( ):
   '''Open / infinite range.'''

   pr = pitchtools.PitchRange((-39, 'exclusive'), None)
   assert -99 not in pr
   assert -39 not in pr
   assert   0     in pr
   assert  48     in pr
   assert  99     in pr


def test_pitchtools_PitchRange___contains___07( ):
   '''Infinite / closed range.'''

   pr = pitchtools.PitchRange(None, (48, 'inclusive'))
   assert -99     in pr
   assert -39     in pr
   assert   0     in pr
   assert  48     in pr
   assert  99 not in pr
   

def test_pitchtools_PitchRange___contains___08( ):
   '''Infinite / open range.'''

   pr = pitchtools.PitchRange(None, (48, 'exclusive'))
   assert -99     in pr
   assert -39     in pr
   assert   0     in pr
   assert  48 not in pr
   assert  99 not in pr
   

def test_pitchtools_PitchRange___contains___09( ):
   '''Infinite / infinite range.'''

   pr = pitchtools.PitchRange(None, None)
   assert -99     in pr
   assert -39     in pr
   assert   0     in pr
   assert  48     in pr
   assert  99     in pr


def test_pitchtools_PitchRange___contains___10( ):
   '''Chord containement.'''

   pr = pitchtools.PitchRange((-39, 'inclusive'), (48, 'inclusive'))
   assert Chord([-99, -98, -97], (1, 4)) not in pr
   assert Chord([-39, -38, -37], (1, 4)) in pr
   assert Chord([0, 2, 3], (1, 4)) in pr
   assert Chord([46, 47, 48], (1, 4)) in pr
   assert Chord([48, 49, 50], (1, 4)) not in pr


def test_pitchtools_PitchRange___contains___11( ):
   '''Note containement.'''

   pr = pitchtools.PitchRange((-39, 'inclusive'), (48, 'inclusive'))
   assert Note(-99, (1, 4)) not in pr
   assert Note(-39, (1, 4))     in pr
   assert Note(  0, (1, 4))     in pr
   assert Note( 48, (1, 4))     in pr
   assert Note( 99, (1, 4)) not in pr


def test_pitchtools_PitchRange___contains___12( ):
   '''Rest and skip containement.'''

   pr = pitchtools.PitchRange((-39, 'inclusive'), (48, 'inclusive'))
   assert Rest((1, 4)) not in pr
   assert Skip((1, 4)) not in pr
