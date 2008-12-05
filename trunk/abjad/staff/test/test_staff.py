from abjad import *
from py.test import raises


### TEST SET STAFF INVOCATION ###

def test_set_staff_invocation_01( ):
   t = Staff([ ])
   t.invocation.type = 'RhythmicStaff'
   assert repr(t.invocation) == '_Invocation(RhythmicStaff)'
   assert t.format == '\\new RhythmicStaff {\n}'
