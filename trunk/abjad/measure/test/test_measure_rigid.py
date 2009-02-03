from abjad import *
import py.test


def test_measure_rigid_01( ):
   '''Rigid measures require meter at initialization.'''

   t = RigidMeasure((4, 8), scale(4))
   
   r'''
        \time 4/8
        c'8
        d'8
        e'8
        f'8 
   '''

   assert t.format == "\t\\time 4/8\n\tc'8\n\td'8\n\te'8\n\tf'8"


def test_measure_rigid_02( ):
   '''
   Rigid measures raise MisfilledMeasureError at format
   when meter duration and contents duration do not match.
   '''

   t = RigidMeasure((4, 8), scale(3))

   assert py.test.raises(MisfilledMeasureError, 't.format') 
