from abjad import *
from py.test import raises

def test_text_spanner_01( ):
   t = Staff(run(4))
   p = Text(t[:])
   assert p.position is None
   assert t.format == "\\new Staff {\n\tc'8 \\startTextSpan\n\tc'8\n\tc'8\n\tc'8 \\stopTextSpan\n}"
   r'''
   \new Staff {
           c'8 \startTextSpan
           c'8
           c'8
           c'8 \stopTextSpan
   }
   '''

def test_text_spanner_02( ):
   t = Staff(run(4))
   p = Text(t[:])
   p.position = 'neutral'
   assert t.format == "\\new Staff {\n\t\\textSpannerNeutral\n\tc'8 \\startTextSpan\n\tc'8\n\tc'8\n\tc'8 \\stopTextSpan\n}"
   r'''
   \new Staff {
           \textSpannerNeutral
           c'8 \startTextSpan
           c'8
           c'8
           c'8 \stopTextSpan
   }
   '''

def test_text_spanner_03( ):
   t = Staff(run(4))
   p = Text(t[:])
   p.position = 'up'
   assert t.format == "\\new Staff {\n\t\\textSpannerUp\n\tc'8 \\startTextSpan\n\tc'8\n\tc'8\n\tc'8 \\stopTextSpan\n}"
   r'''
   \new Staff {
           \textSpannerUp
           c'8 \startTextSpan
           c'8
           c'8
           c'8 \stopTextSpan
   }
   '''

def test_text_spanner_04( ):
   t = Staff(run(4))
   p = Text(t[:])
   p.position = 'down'
   assert t.format == "\\new Staff {\n\t\\textSpannerDown\n\tc'8 \\startTextSpan\n\tc'8\n\tc'8\n\tc'8 \\stopTextSpan\n}"
   r'''
   \new Staff {
           \textSpannerDown
           c'8 \startTextSpan
           c'8
           c'8
           c'8 \stopTextSpan
   }
   '''

def test_text_spanner_05( ):
   '''Setting unknown position raises ValueError.'''
   t = Staff(run(4))
   p = Text(t[:])
   assert raises(ValueError, 'p.position = "xxx"')


def test_text_spanner_06( ):
   '''TextSpanner attaching to container formats correctly.'''
   t = Staff(run(4))
   p = Text(t)
   assert p.position is None
   assert t.format == "\\new Staff {\n\tc'8 \\startTextSpan\n\tc'8\n\tc'8\n\tc'8 \\stopTextSpan\n}"
   r'''
   \new Staff {
           c'8 \startTextSpan
           c'8
           c'8
           c'8 \stopTextSpan
   }
   '''
