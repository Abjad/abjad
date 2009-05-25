from abjad import *


def test_scm_moment_format_01( ):
   '''*LilyPond* moment formats in a special way.'''

   t = Moment(Rational(1, 68))
   assert t.format == '(ly:make-moment 1 . 68)'
