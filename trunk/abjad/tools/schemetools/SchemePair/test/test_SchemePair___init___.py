from abjad import *


def test_SchemePair___init____01( ):

   pair = schemetools.SchemePair(1, 2)
   assert str(pair) == '(1 . 2)'


def test_SchemePair___init____02( ):

   pair = schemetools.SchemePair(True, False)
   assert str(pair) == '(#t . #f)'


def test_SchemePair___init____02( ):

   pair = schemetools.SchemePair('spacing', 4)
   assert str(pair) == '(spacing . 4)'
