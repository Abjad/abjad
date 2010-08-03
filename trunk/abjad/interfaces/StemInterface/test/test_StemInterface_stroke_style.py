from abjad import *


def test_StemInterface_stroke_style_01( ):

   t = Note(0, (1, 16))
   t.stem.stroke_style = schemetools.SchemeString('grace')

   r'''
   \once \override Stem #'stroke-style = #"grace"
   c'16
   '''

   assert t.format == '\\once \\override Stem #\'stroke-style = #"grace"\nc\'16'
