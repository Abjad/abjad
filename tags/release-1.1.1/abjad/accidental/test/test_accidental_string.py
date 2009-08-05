from abjad import *


def test_accidental_string_01( ):
   t = Accidental('s')
   assert t.string == 's'


def test_accidental_string_02( ):
   t = Accidental('')
   assert t.string == ''


def test_accidental_string_03( ):
   t = Accidental( )
   assert t.string == ''


def test_accidental_string_04( ):
   t = Accidental('!')
   assert t.string == '!'
