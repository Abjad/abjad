from abjad import *


def test_fdtuplet_in_place_apply_01( ):
   t = Container([Note(n, (1, 8)) for n in range(8)])
   leaves_before = t.leaves
   FixedDurationTuplet((2, 8), t[0 : 3])
   leaves_after = t.leaves
   assert leaves_before == leaves_after
   assert len(t) == 6
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, FixedDurationTuplet)
      else:
         assert isinstance(x, Note)
   assert check.wf(t)


def test_fdtuplet_in_place_apply_02( ):
   t = FixedDurationTuplet((7, 8), [Note(n, (1, 8)) for n in range(8)])
   leaves_before = t.leaves
   FixedDurationTuplet((2, 8), t[0 : 3])
   leaves_after = t.leaves
   assert leaves_before == leaves_after
   assert len(t) == 6
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, FixedDurationTuplet)
      else:
         assert isinstance(x, Note)
   assert check.wf(t)


def test_fdtuplet_in_place_apply_03( ):
   t = FixedMultiplierTuplet((7, 8), [Note(n, (1, 8)) for n in range(8)])
   leaves_before = t.leaves
   FixedDurationTuplet((2, 8), t[0 : 3])
   leaves_after = t.leaves
   assert leaves_before == leaves_after
   assert len(t) == 6
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, FixedDurationTuplet)
      else:
         assert isinstance(x, Note)
   assert check.wf(t)


def test_fdtuplet_in_place_apply_04( ):
   t = RigidMeasure((8, 8), [Note(n, (1, 8)) for n in range(8)])
   leaves_before = t.leaves
   FixedDurationTuplet((2, 8), t[0 : 3])
   t.meter.forced = Meter(7, 8)
   leaves_after = t.leaves
   assert leaves_before == leaves_after
   assert len(t) == 6
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, FixedDurationTuplet)
      else:
         assert isinstance(x, Note)
   assert check.wf(t)


def test_fdtuplet_in_place_apply_05( ):
   t = Voice([Note(n, (1, 8)) for n in range(8)])
   leaves_before = t.leaves
   FixedDurationTuplet((2, 8), t[0 : 3])
   leaves_after = t.leaves
   assert leaves_before == leaves_after
   assert len(t) == 6
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, FixedDurationTuplet)
      else:
         assert isinstance(x, Note)
   assert check.wf(t)


def test_fdtuplet_in_place_apply_06( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   leaves_before = t.leaves
   FixedDurationTuplet((2, 8), t[0 : 3])
   leaves_after = t.leaves
   assert leaves_before == leaves_after
   assert len(t) == 6
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, FixedDurationTuplet)
      else:
         assert isinstance(x, Note)
   assert check.wf(t)
