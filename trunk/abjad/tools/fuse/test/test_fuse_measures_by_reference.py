from abjad import *
import py.test


def test_fuse_measures_by_reference_01( ):
   '''Fuse unicorporated binary measures.'''

   t1 = RigidMeasure((1, 8), construct.scale(2, Rational(1, 16)))
   Beam(t1[:])
   t2 = RigidMeasure((2, 16), construct.scale(2, Rational(1, 16)))
   Slur(t2[:])

   r'''
   {
           \time 1/8
           c'16 [
           d'16 ]
   }
   '''

   r'''
   {
           \time 2/16
           c'16 (
           d'16 )
   }
   '''

   new = fuse.measures_by_reference([t1, t2])

   r'''
   {
           \time 2/8
           c'16 [
           d'16 ]
           c'16 (
           d'16 )
   }
   '''

   assert new is not t1 and new is not t2
   assert len(t1) == 0
   assert len(t2) == 0
   assert check.wf(new)
   assert new.format == "{\n\t\\time 2/8\n\tc'16 [\n\td'16 ]\n\tc'16 (\n\td'16 )\n}"
   

def test_fuse_measures_by_reference_02( ):
   '''Fuse binary measures with different denominators.
      Helpers selects minimum of two denominators.
      Beams are OK because they attach to leaves rather than containers.'''

   t = Voice(measuretools.make([(1, 8), (2, 16)]))
   measuretools.populate(t, Rational(1, 16))
   pitchtools.diatonicize(t)
   Beam(t.leaves)

   r'''
   \new Voice {
           {
                   \time 1/8
                   c'16 [
                   d'16
           }
           {
                   \time 2/16
                   e'16
                   f'16 ]
           }
   }
   '''

   fuse.measures_by_reference(t[:])

   r'''
   \new Voice {
           {
                   \time 2/8
                   c'16 [
                   d'16
                   e'16
                   f'16 ]
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\t\\time 2/8\n\t\tc'16 [\n\t\td'16\n\t\te'16\n\t\tf'16 ]\n\t}\n}"


def test_fuse_measures_by_reference_03( ):
   '''Fuse binary measures with different denominators.
      Helpers selects minimum of two denominators.
      Beam attaches to container rather than leaves.'''

   t = Voice(measuretools.make([(1, 8), (2, 16)]))
   measuretools.populate(t, Rational(1, 16))
   pitchtools.diatonicize(t)
   Beam(t[0])

   r'''
   \new Voice {
           {
                   \time 1/8
                   c'16 [
                   d'16 ]
           }
           {
                   \time 2/16
                   e'16
                   f'16
           }
   }
   '''

   fuse.measures_by_reference(t[:])

   r'''
   \new Voice {
           {
                   \time 2/8
                   c'16
                   d'16
                   e'16
                   f'16
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\t\\time 2/8\n\t\tc'16\n\t\td'16\n\t\te'16\n\t\tf'16\n\t}\n}"


def test_fuse_measures_by_reference_04( ):
   '''Fuse binary and nonbinary measures.
      Helpers selects least common multiple of denominators.
      Beams are OK because they attach to leaves rather than containers.'''

   m1 = RigidMeasure((1, 8), construct.run(1))
   m2 = RigidMeasure((1, 12), construct.run(1))
   t = Voice([m1, m2])
   pitchtools.diatonicize(t)
   Beam(t.leaves)

   r'''
   \new Voice {
           {
                   \time 1/8
                   c'8 [
           }
           {
                   \time 1/12
                   \scaleDurations #'(2 . 3) {
                           d'8 ]
                   }
           }
   }
   '''

   fuse.measures_by_reference(t[:])

   r'''
   \new Voice {
           {
                   \time 5/24
                   \scaleDurations #'(2 . 3) {
                           c'8. [
                           d'8 ]
                   }
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\t\\time 5/24\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\tc'8. [\n\t\t\td'8 ]\n\t\t}\n\t}\n}"


def test_fuse_measures_by_reference_05( ):
   '''Fusing empty list raises no excpetion but returns None.'''

   result = fuse.measures_by_reference([ ])
   assert result is None


def test_fuse_measures_by_reference_06( ):
   '''Fusing list of only one measure returns measure unaltered.'''

   t = RigidMeasure((3, 8), construct.scale(3))
   new = fuse.measures_by_reference([t])

   assert new is t


def test_fuse_measures_by_reference_07( ):
   '''Fuse three measures.'''

   t = Voice(measuretools.make([(1, 8), (1, 8), (1, 8)]))
   measuretools.populate(t, Rational(1, 16))
   pitchtools.diatonicize(t)
   Beam(t.leaves)

   r'''
   \new Voice {
           {
                   \time 1/8
                   c'16 [
                   d'16
           }
           {
                   \time 1/8
                   e'16
                   f'16
           }
           {
                   \time 1/8
                   g'16
                   a'16 ]
           }
   }
   '''

   fuse.measures_by_reference(t[:])

   r'''
   \new Voice {
           {
                   \time 3/8
                   c'16 [
                   d'16
                   e'16
                   f'16
                   g'16
                   a'16 ]
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\t\\time 3/8\n\t\tc'16 [\n\t\td'16\n\t\te'16\n\t\tf'16\n\t\tg'16\n\t\ta'16 ]\n\t}\n}"


def test_fuse_measures_by_reference_08( ):
   '''Measure fusion across intervening container boundaries is undefined.'''

   t = Voice(Container(RigidMeasure((2, 8), construct.run(2)) * 2) * 2)
   pitchtools.diatonicize(t)

   r'''
   \new Voice {
           {
                   {
                           \time 2/8
                           c'8
                           d'8
                   }
                   {
                           \time 2/8
                           e'8
                           f'8
                   }
           }
           {
                   {
                           \time 2/8
                           g'8
                           a'8
                   }
                   {
                           \time 2/8
                           b'8
                           c''8
                   }
           }
   }
   '''

   assert py.test.raises(ContiguityError, 
      'fuse.measures_by_reference([t[0][1], t[1][0]])')


def test_fuse_measures_by_reference_09( ):
   '''Fusing binary and nonbinary measures.
      With change in number of note_heads because of nonbinary multiplier.'''

   t = Staff([
      RigidMeasure((9, 80), [ ]),
      RigidMeasure((2, 16), [ ])])
   measuretools.populate(t, 'meter series')

   r'''
   \new Staff {
           {
                   \time 9/80
                   \scaleDurations #'(4 . 5) {
                           c'64
                           c'64
                           c'64
                           c'64
                           c'64
                           c'64
                           c'64
                           c'64
                           c'64
                   }
           }
           {
                   \time 2/16
                   c'16
                   c'16
           }
   }
   '''

   new = fuse.measures_by_reference(t[:]) 

   r'''
   {
           \time 19/80
           \scaleDurations #'(4 . 5) {
                   c'64
                   c'64
                   c'64
                   c'64
                   c'64
                   c'64
                   c'64
                   c'64
                   c'64
                   c'16 ~
                   c'64
                   c'16 ~
                   c'64
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 19/80\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\tc'64\n\t\t\tc'64\n\t\t\tc'64\n\t\t\tc'64\n\t\t\tc'64\n\t\t\tc'64\n\t\t\tc'64\n\t\t\tc'64\n\t\t\tc'64\n\t\t\tc'16 ~\n\t\t\tc'64\n\t\t\tc'16 ~\n\t\t\tc'64\n\t\t}\n\t}\n}"
