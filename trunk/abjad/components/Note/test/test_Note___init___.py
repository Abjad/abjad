from abjad import *
from py.test import raises


def test_Note___init____01( ):
   '''Init note with pitch in octave zero.
   '''

   t = Note(-37, (1, 4))
   assert t.format == 'b,,,4'


def test_Note___init____02( ):
   '''Init note with non-assignable duration.
   '''

   raises(AssignabilityError, 'Note(0, (5, 8))')


def test_Note___init____03( ):
   '''Init note with LilyPond-style pitch string.
   '''

   t = Note('c,,', (1, 4))
   assert t.format == 'c,,4'


def test_Note___init____04( ):
   '''Init note with complete LilyPond-style note string.
   '''

   t = Note('cs8.')
   assert t.format == 'cs8.'


def test_Note___init____05( ):
   '''Init note with pitch, written duration and LilyPond multiplier.
   '''

   note = Note(12, (1, 4), (1, 2))
   assert isinstance(note, Note)
