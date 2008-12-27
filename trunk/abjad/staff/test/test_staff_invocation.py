from abjad import *


def test_staff_invocation_01( ):
   t = Staff([ ])
   t.invocation.type = 'RhythmicStaff'
   assert t.format == '\\new RhythmicStaff {\n}'
