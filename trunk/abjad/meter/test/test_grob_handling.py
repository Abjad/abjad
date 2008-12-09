from abjad import *


def test_grob_handling_01( ):
   '''Leaf grob override without context promotion.'''
   t = Measure((4, 4), Note(0, (1, 4)) * 4)
   t.meter.transparent = True
   assert t.format == "\t\\once \\override TimeSignature #'transparent = ##t\n\t\\time 4/4\n\tc'4\n\tc'4\n\tc'4\n\tc'4"
   '''
   \once \override TimeSignature #'transparent = ##t
   \time 4/4
   c'4
   c'4
   c'4
   c'4
   '''


def test_grob_handling_02( ):
   '''Leaf grob override with context promotion.'''
   t = Measure((4, 4), Note(0, (1, 4)) * 4)
   t.meter.color = 'red'
   t.meter.promote('color', 'Staff')
   assert t.format == "\t\\once \\override Staff.TimeSignature #'color = #red\n\t\\time 4/4\n\tc'4\n\tc'4\n\tc'4\n\tc'4"
   '''
   \once \override Staff.TimeSignature #'color = #red
   \time 4/4
   c'4
   c'4
   c'4
   c'4
   '''


def test_grob_handling_03( ):
   '''Context grob override formats context automatically;
      context grob override omits \once frequency indicator.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.meter.color =  'red'
   assert t.format == "\\new Staff {\n\t\\override Staff.TimeSignature #'color = #red\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"
   r'''
   \new Staff {
      \override Staff.TimeSignature #'color = #red
      c'4
      c'4
      c'4
      c'4
      c'4
      c'4
      c'4
      c'4
   }
   '''


def test_grob_handling_04( ):
   '''All overrides remove with clear( ).'''
   t = Note(0, (1, 4))
   t.meter.color = 'red'
   t.meter.transparent = True
   t.meter.clear( )
   assert t.format == "c'4"
