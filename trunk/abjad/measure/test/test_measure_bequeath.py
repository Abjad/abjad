from abjad import *


def test_measure_bequeath_01( ):
   '''
   Scaling measures can bequeath to dynamic measures.
   '''

   t = Measure((4, 8), scale(4))

   r'''
        \time 4/8
        c'8
        d'8
        e'8
        f'8
   '''

   t.pop( )

   r'''
        \time 4/8
        \scaleDurations #'(4 . 3) {
                c'8
                d'8
                e'8
        }
   '''

   assert t.format == "\t\\time 4/8\n\t\\scaleDurations #'(4 . 3) {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}"

   u = DynamicMeasure( )
   t.bequeath(u)

   r'''
        \time 3/8
        c'8
        d'8
        e'8
   '''
  
   assert u.format == "\t\\time 3/8\n\tc'8\n\td'8\n\te'8"
   assert t.format == '\t\\time 4/8'


def test_measure_bequeath_02( ):
   '''
   Dynamic measures can bequeath to scaling measures.
   '''

   t = DynamicMeasure(scale(4))

   r'''
        \time 1/2
        c'8
        d'8
        e'8
        f'8
   '''

   u = Measure((4, 8), [ ])
   t.bequeath(u)

   r'''
        \time 4/8
        c'8
        d'8
        e'8
        f'8
   '''

   assert u.format == "\t\\time 4/8\n\tc'8\n\td'8\n\te'8\n\tf'8"
   assert t.format == '\t\\time 0/1'
