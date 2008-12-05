from abjad import *
from py.test import raises


def test_staff_invocation_01( ):
   t = Staff([ ])
   t.invocation.type = 'RhythmicStaff'
   assert repr(t.invocation) == '_Invocation(RhythmicStaff)'
   assert t.format == '\\new RhythmicStaff {\n}'
