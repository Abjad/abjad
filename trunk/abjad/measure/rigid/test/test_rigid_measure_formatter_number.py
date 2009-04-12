from abjad import *


def test_rigid_measure_block_01( ):
   '''_MeasureFormatterNumberInterface can contribute 
      LilyPond comments to one measure at a time.'''

   t = Staff(measures_make([(2, 16), (3, 16), (3, 16)]))
   measures_populate(t, Rational(1, 16))
   t[0].formatter.number.self = 'comment'

   r'''
   \new Staff {
           % start measure 0
                   \time 2/16
                   c'16
                   c'16
           % stop measure 0
                   \time 3/16
                   c'16
                   c'16
                   c'16
                   \time 3/16
                   c'16
                   c'16
                   c'16
   }
   '''
  
   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t% start measure 0\n\t\t\\time 2/16\n\t\tc'16\n\t\tc'16\n\t% stop measure 0\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n}"


def test_rigid_measure_block_02( ):
   '''_MeasureFormatterNumberInterface can contribute 
      LilyPond comments to many leaves at once.'''

   t = Staff(measures_make([(2, 16), (3, 16), (3, 16)]))
   measures_populate(t, Rational(1, 16))
   t[0].formatter.number.leaves = 'markup'

   r'''
   \new Staff {
                   \time 2/16
                   c'16 ^ \markup { 0 }
                   c'16 ^ \markup { 1 }
                   \time 3/16
                   c'16
                   c'16
                   c'16
                   \time 3/16
                   c'16
                   c'16
                   c'16
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\t\\time 2/16\n\t\tc'16 ^ \\markup { 0 }\n\t\tc'16 ^ \\markup { 1 }\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n}"


def test_rigid_measure_block_03( ):
   '''_MeasureFormatterNumberInterface can contribute 
      LilyPond comments to one measure and markup
      to many leaves, all at the same time.'''

   t = Staff(measures_make([(2, 16), (3, 16), (3, 16)]))
   measures_populate(t, Rational(1, 16))
   t[0].formatter.number.self = 'comment'
   t[0].formatter.number.leaves = 'markup'

   r'''
   \new Staff {
           % start measure 0
                   \time 2/16
                   c'16 ^ \markup { 0 }
                   c'16 ^ \markup { 1 }
           % stop measure 0
                   \time 3/16
                   c'16
                   c'16
                   c'16
                   \time 3/16
                   c'16
                   c'16
                   c'16
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t% start measure 0\n\t\t\\time 2/16\n\t\tc'16 ^ \\markup { 0 }\n\t\tc'16 ^ \\markup { 1 }\n\t% stop measure 0\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n}"
