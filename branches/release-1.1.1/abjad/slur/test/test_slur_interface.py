from abjad import *
from abjad.slur.interface import SlurInterface

def test_slur_interface_01( ):
   '''The slur interface exists.'''
   t = Voice(construct.scale(4))
   assert isinstance(t.slur, SlurInterface)


def test_slur_interface_02( ):
   '''Slur interface GrobHandles 'Slur'.'''
   t = Voice(construct.scale(4))
   t.slur.color = 'red'
   assert t.format == "\\new Voice \\with {\n\t\\override Slur #'color = #red\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
   r'''
   \new Voice \with {
           \override Slur #'color = #red
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''
