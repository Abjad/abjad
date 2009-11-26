from abjad import *
from abjad.tools.pitchtools.PitchArray.PitchArrayCell.PitchArrayCell \
   import PitchArrayCell
import py.test


def test_PitchArrayCell___init___01( ):
   '''Init empty.'''

   cell = PitchArrayCell( )
   assert cell.pitches == [ ]
   assert cell.width == 1


def test_PitchArrayCell___init___02( ):
   '''Init with positive integer width.'''

   cell = PitchArrayCell(2)
   assert cell.pitches == [ ]
   assert cell.width == 2


def test_PitchArrayCell___init___03( ):
   '''Init with pitch instance.'''

   cell = PitchArrayCell(Pitch(0))
   assert cell.pitches == [Pitch(0)]
   assert cell.width == 1


def test_PitchArrayCell___init___04( ):
   '''Init with list of pitch tokens.'''

   cell = PitchArrayCell([0, 2, 4])
   assert cell.pitches == [Pitch(0), Pitch(2), Pitch(4)]
   assert cell.width == 1


def test_PitchArrayCell___init___05( ):
   '''Init with list of pitch instances.'''

   cell = PitchArrayCell([Pitch(0), Pitch(2), Pitch(4)])
   assert cell.pitches == [Pitch(0), Pitch(2), Pitch(4)]
   assert cell.width == 1


def test_PitchArrayCell___init___06( ):
   '''Init with pitch token, width pair.'''

   cell = PitchArrayCell((0, 2))
   assert cell.pitches == [Pitch(0)]
   assert cell.width == 2


def test_PitchArrayCell___init___07( ):
   '''Init with pitch instance, width pair.'''

   cell = PitchArrayCell((Pitch(0), 2))
   assert cell.pitches == [Pitch(0)]
   assert cell.width == 2


def test_PitchArrayCell___init___08( ):
   '''Init with pitch token list, width pair.'''

   cell = PitchArrayCell(([0, 2, 4], 2))
   assert cell.pitches == [Pitch(0), Pitch(2), Pitch(4)]
   assert cell.width == 2


def test_PitchArrayCell___init___09( ):
   '''Init with pitch instance list, width pair.'''

   cell = PitchArrayCell(([Pitch(0), Pitch(2), Pitch(4)], 2))
   assert cell.pitches == [Pitch(0), Pitch(2), Pitch(4)]
   assert cell.width == 2
