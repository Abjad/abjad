from abjad import *
from abjad.tools.pitcharraytools.PitchArray.PitchArrayCell.PitchArrayCell \
   import PitchArrayCell
import py.test


def test_PitchArrayCell___init____01( ):
   '''Init empty.'''

   cell = PitchArrayCell( )
   assert cell.pitches == [ ]
   assert cell.width == 1


def test_PitchArrayCell___init____02( ):
   '''Init with positive integer width.'''

   cell = PitchArrayCell(2)
   assert cell.pitches == [ ]
   assert cell.width == 2


def test_PitchArrayCell___init____03( ):
   '''Init with pitch instance.'''

   cell = PitchArrayCell(pitchtools.NamedPitch(0))
   assert cell.pitches == [pitchtools.NamedPitch(0)]
   assert cell.width == 1


def test_PitchArrayCell___init____04( ):
   '''Init with list of pitch tokens.'''

   cell = PitchArrayCell([0, 2, 4])
   assert cell.pitches == [pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)]
   assert cell.width == 1


def test_PitchArrayCell___init____05( ):
   '''Init with list of pitch instances.'''

   cell = PitchArrayCell([pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)])
   assert cell.pitches == [pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)]
   assert cell.width == 1


def test_PitchArrayCell___init____06( ):
   '''Init with list of pitch pairs.'''

   cell = PitchArrayCell([('c', 4), ('d', 4), ('e', 4)])
   assert cell.pitches == [pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)]
   assert cell.width == 1


def test_PitchArrayCell___init____07( ):
   '''Init with pitch token, width pair.'''

   cell = PitchArrayCell((0, 2))
   assert cell.pitches == [pitchtools.NamedPitch(0)]
   assert cell.width == 2


def test_PitchArrayCell___init____08( ):
   '''Init with pitch instance, width pair.'''

   cell = PitchArrayCell((pitchtools.NamedPitch(0), 2))
   assert cell.pitches == [pitchtools.NamedPitch(0)]
   assert cell.width == 2


def test_PitchArrayCell___init____09( ):
   '''Init with pitch token list, width pair.'''

   cell = PitchArrayCell(([0, 2, 4], 2))
   assert cell.pitches == [pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)]
   assert cell.width == 2


def test_PitchArrayCell___init____10( ):
   '''Init with pitch instance list, width pair.'''

   cell = PitchArrayCell(([pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)], 2))
   assert cell.pitches == [pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)]
   assert cell.width == 2
