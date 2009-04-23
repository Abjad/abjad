from abjad import *


def test_measuretools_binary_to_nonbinary_01( ):
   '''Make binary measure into equivalent nonbinary measure.
      Assignable 3/2 multiplier conserves noteheads.'''

   t = RigidMeasure((2, 8), construct.scale(2))
   Beam(t[:])

   r'''\time 2/8
   c'8 [
   d'8 ]'''

   measuretools.binary_to_nonbinary(t, 3)

   r'''\time 3/12
   \scaleDurations #'(2 . 3) {
      c'8. [
      d'8. ]
   }'''

   assert check.wf(t)
   assert t.format == "\t\\time 3/12\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'8. [\n\t\td'8. ]\n\t}"

   
def test_measuretools_binary_to_nonbinary_02( ):
   '''Make binary measure into equivalent nonbinary measure.
      Nonassignable 5/4 multiplier induces ties.'''

   t = RigidMeasure((2, 8), construct.scale(2))
   Beam(t[:])

   r'''\time 2/8
   c'8 [
   d'8 ]'''

   measuretools.binary_to_nonbinary(t, 5)

   r'''\time 5/20
   \scaleDurations #'(4 . 5) {
      c'8 [ ~
      c'32
      d'8 ~
      d'32 ]
   }'''

   assert check.wf(t)
   assert t.format == "\t\\time 5/20\n\t\\scaleDurations #'(4 . 5) {\n\t\tc'8 [ ~\n\t\tc'32\n\t\td'8 ~\n\t\td'32 ]\n\t}"


def test_measuretools_binary_to_nonbinary_03( ):
   '''Make binary measure into equivalent nonbinary measure.
      Assignable 7/4 multiplier conserves noteheads.'''

   t = RigidMeasure((2, 8), construct.scale(2))
   Beam(t[:])

   r'''\time 2/8
   c'8 [
   d'8 ]'''

   measuretools.binary_to_nonbinary(t, 7)

   r'''\time 7/28
   \scaleDurations #'(4 . 7) {
      c'8.. [
      d'8.. ]
   }'''

   assert check.wf(t)
   assert t.format == "\t\\time 7/28\n\t\\scaleDurations #'(4 . 7) {\n\t\tc'8.. [\n\t\td'8.. ]\n\t}"


def test_measuretools_binary_to_nonbinary_04( ):
   '''Make binary measure into equivalent nonbinary measure.
      Nonassignable 9/8 multiplier induces ties.'''

   t = RigidMeasure((2, 8), construct.scale(2))
   Beam(t[:])

   r'''\time 2/8
   c'8 [
   d'8 ]'''

   r'''measuretools.binary_to_nonbinary(t, 9)
   \time 9/36
   \scaleDurations #'(8 . 9) {
      c'8 [ ~
      c'64
      d'8 ~
      d'64 ]
   }'''

   assert check.wf(t)
   assert t.format == "\t\\time 9/36\n\t\\scaleDurations #'(8 . 9) {\n\t\tc'8 [ ~\n\t\tc'64\n\t\td'8 ~\n\t\td'64 ]\n\t}"
