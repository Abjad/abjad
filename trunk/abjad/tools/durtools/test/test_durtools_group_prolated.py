from abjad import *


def test_durtools_group_prolated_01( ):

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
   pitchtools.diatonicize(t)

   r'''\new Staff {
         \time 2/8
         c'8
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8
   }'''

   groups = durtools.group_prolated(t.leaves, [Rational(3, 8)], )

   "[[Note(c'', 8), Note(b', 8), Note(a', 8)]]"

   assert len(groups) == 1
   assert groups[0] == list(t.leaves[:3])


def test_durtools_group_prolated_02( ):

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
   pitchtools.diatonicize(t)

   r'''\new Staff {
         \time 2/8
         c'8
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8
   }'''

   groups = durtools.group_prolated(t.leaves, [Rational(3, 8)], cyclic = True)

   "[[Note(c'', 8), Note(b', 8), Note(a', 8)], [Note(g', 8), Note(f', 8), Note(e', 8)]]"

   assert len(groups) == 2
   assert groups[0] == list(t.leaves[:3])
   assert groups[1] == list(t.leaves[3:6])


def test_durtools_group_prolated_03( ):

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
   pitchtools.diatonicize(t)

   r'''\new Staff {
         \time 2/8
         c'8
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8
   }'''

   groups = durtools.group_prolated(
      t.leaves, [Rational(3, 8)], cyclic = True, overhang = True)

   "[[Note(c'', 8), Note(b', 8), Note(a', 8)], [Note(g', 8), Note(f', 8), Note(e', 8)], [Note(d', 8), Note(c', 8)]]"

   assert len(groups) == 3
   assert groups[0] == list(t.leaves[:3])
   assert groups[1] == list(t.leaves[3:6])
   assert groups[2] == list(t.leaves[6:8])


def test_durtools_group_prolated_04( ):

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
   pitchtools.diatonicize(t)

   r'''\new Staff {
         \time 2/8
         c'8
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8
   }'''

   groups = durtools.group_prolated(
      t.leaves, [Rational(3, 16)], fill = 'less')

   "[[Note(c', 8)]]"

   assert len(groups) == 1
   assert groups[0] == list(t.leaves[:1])


def test_durtools_group_prolated_05( ):

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
   pitchtools.diatonicize(t)

   r'''\new Staff {
         \time 2/8
         c'8
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8
   }'''

   groups = durtools.group_prolated(
      t.leaves, [Rational(3, 16)], cyclic = True, fill = 'less')

   "[[Note(c', 8)], [Note(d', 8)], [Note(e', 8)], [Note(f', 8)], [Note(g', 8)], [Note(a', 8)], [Note(b', 8)]]"

   assert len(groups) == 7
   assert groups[0] == list(t.leaves[:1])
   assert groups[1] == list(t.leaves[1:2])
   assert groups[2] == list(t.leaves[2:3])
   assert groups[3] == list(t.leaves[3:4])
   assert groups[4] == list(t.leaves[4:5])
   assert groups[5] == list(t.leaves[5:6])
   assert groups[6] == list(t.leaves[6:7])
