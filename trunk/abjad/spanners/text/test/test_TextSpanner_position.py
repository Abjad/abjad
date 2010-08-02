from abjad import *
from py.test import raises


def test_TextSpanner_position_01( ):

   t = Staff(leaftools.make_repeated_notes(4))
   p = TextSpanner(t[:])

   r'''
   \new Staff {
           c'8 \startTextSpan
           c'8
           c'8
           c'8 \stopTextSpan
   }
   '''

   assert p.position is None
   assert t.format == "\\new Staff {\n\tc'8 \\startTextSpan\n\tc'8\n\tc'8\n\tc'8 \\stopTextSpan\n}"


def test_TextSpanner_position_02( ):

   t = Staff(leaftools.make_repeated_notes(4))
   p = TextSpanner(t[:])
   p.position = 'neutral'

   r'''
   \new Staff {
           \textSpannerNeutral
           c'8 \startTextSpan
           c'8
           c'8
           c'8 \stopTextSpan
   }
   '''

   assert t.format == "\\new Staff {\n\t\\textSpannerNeutral\n\tc'8 \\startTextSpan\n\tc'8\n\tc'8\n\tc'8 \\stopTextSpan\n}"


def test_TextSpanner_position_03( ):

   t = Staff(leaftools.make_repeated_notes(4))
   p = TextSpanner(t[:])
   p.position = 'up'

   r'''
   \new Staff {
           \textSpannerUp
           c'8 \startTextSpan
           c'8
           c'8
           c'8 \stopTextSpan
   }
   '''

   assert t.format == "\\new Staff {\n\t\\textSpannerUp\n\tc'8 \\startTextSpan\n\tc'8\n\tc'8\n\tc'8 \\stopTextSpan\n}"


def test_TextSpanner_position_04( ):

   t = Staff(leaftools.make_repeated_notes(4))
   p = TextSpanner(t[:])
   p.position = 'down'

   r'''
   \new Staff {
           \textSpannerDown
           c'8 \startTextSpan
           c'8
           c'8
           c'8 \stopTextSpan
   }
   '''

   assert t.format == "\\new Staff {\n\t\\textSpannerDown\n\tc'8 \\startTextSpan\n\tc'8\n\tc'8\n\tc'8 \\stopTextSpan\n}"


def test_TextSpanner_position_05( ):
   '''Setting unknown position raises ValueError.'''

   t = Staff(leaftools.make_repeated_notes(4))
   p = TextSpanner(t[:])

   assert raises(ValueError, 'p.position = "xxx"')


def test_TextSpanner_position_06( ):
   '''TextSpanner attaching to container formats correctly.'''

   t = Staff(leaftools.make_repeated_notes(4))
   p = TextSpanner(t)

   r'''
   \new Staff {
           c'8 \startTextSpan
           c'8
           c'8
           c'8 \stopTextSpan
   }
   '''

   assert p.position is None
   assert t.format == "\\new Staff {\n\tc'8 \\startTextSpan\n\tc'8\n\tc'8\n\tc'8 \\stopTextSpan\n}"
