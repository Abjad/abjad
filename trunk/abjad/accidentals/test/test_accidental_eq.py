from abjad import *


def test_accidental_eq_01( ):
   '''
   Accidentals compare equal when they carry the same string.
   '''

   assert Accidental('ff') == Accidental('ff')
   assert Accidental('tqf') == Accidental('tqf')
   assert Accidental('f') == Accidental('f')
   assert Accidental('qf') == Accidental('qf')
   assert Accidental('!') == Accidental('!')
   assert Accidental('qs') == Accidental('qs')
   assert Accidental('s') == Accidental('s')
   assert Accidental('tqs') == Accidental('tqs')
   assert Accidental('ss') == Accidental('ss')


def test_accidental_eq_02( ):
   '''
   Accidentals compare equal when they carry no string.
   '''

   assert Accidental( ) == Accidental( )
   assert Accidental('') == Accidental('')
   assert Accidental( ) == Accidental('')


def test_accidental_eq_03( ):
   '''
   Accidentals compare not equal when they carry only the same adjustment.
   '''

   assert Accidental('') != Accidental('!')
