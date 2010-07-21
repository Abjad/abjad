from abjad import *


def test_SchemeMoment___init____01( ):

   t = schemetools.SchemeMoment(Rational(1, 68))
   assert t.format == '#(ly:make-moment 1 68)'
