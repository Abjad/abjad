from abjad import *


def test_excise_01( ):
   '''Excise leaf that conflicts with meter duration.'''

   t = RigidMeasure((4, 4), 
      FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)

   r'''
        \time 4/4
        \times 2/3 {
                c'4
                cs'4
                d'4
        }
        \times 2/3 {
                ef'4
                e'4
                f'4
        }
   '''

   excise(t.leaves[0])

   r'''
        \time 5/6
        \compressMusic #'(2 . 3) {
                        cs'4
                        d'4
                        ef'4
                        e'4
                        f'4
        }
   '''

   assert isinstance(t, RigidMeasure)
   assert len(t) == 2
   assert t.meter.forced == (5, 6)
   tuplet = t[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 2
   assert tuplet.duration.preprolated == Rational(2, 4)
   assert tuplet.duration.prolated == Rational(2, 6)
   tuplet = t[1]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 3
   assert tuplet.duration.preprolated == Rational(3, 4)
   assert tuplet.duration.prolated == Rational(3, 6)
   check(t)


def test_excise_02( ):
   '''Excise leaf that conflicts with meter duration.'''

   t = RigidMeasure((4, 4), 
      FixedDurationTuplet((2, 4), Note(0, (1, 8)) * 5) * 2)

   r'''
        \time 4/4
        \times 4/5 {
                c'8
                cs'8
                d'8
                ef'8
                e'8
        }
        \times 4/5 {
                f'8
                fs'8
                g'8
                af'8
                a'8
        }
   '''

   excise(t.leaves[0])

   r'''
     \time 9/10
     \compressMusic #'(4 . 5) {
                     cs'8
                     d'8
                     ef'8
                     e'8
                     f'8
                     fs'8
                     g'8
                     af'8
                     a'8
     }
   '''

   assert isinstance(t, RigidMeasure)
   assert len(t) == 2
   assert t.meter.forced == (9, 10)
   tuplet = t[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 4
   assert tuplet.duration.preprolated == Rational(4, 8)
   assert tuplet.duration.prolated == Rational(4, 10)
   tuplet = t[1]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 5
   assert tuplet.duration.preprolated == Rational(5, 8)
   assert tuplet.duration.prolated == Rational(5, 10)
   check(t)


def test_excise_03( ):
   '''Excise leaf that conflicts with meter duration;
      change meter denominator and reset tuplet target durations.'''

   t = RigidMeasure((5, 6), [
      FixedDurationTuplet((3, 4), Note(0, (1, 4)) * 5),
      FixedDurationTuplet((4, 8), Note(0, (1, 8)) * 7),
      ])
   
   from abjad.leaf.leaf import _Leaf
   for i, leaf in enumerate(iterate.naive(t, _Leaf)):
      leaf.pitch = i

   r'''
        \time 5/6
        \compressMusic #'(2 . 3) {
                \fraction \times 3/5 {
                        c'4
                        cs'4
                        d'4
                        ef'4
                        e'4
                }
                \times 4/7 {
                        f'8
                        fs'8
                        g'8
                        af'8
                        a'8
                        bf'8
                        b'8
                }
        }
   '''

   excise(t.leaves[0])

   r'''
        \time 11/15
        \compressMusic #'(8 . 15) {
                \fraction \times 3/4 {
                        cs'4
                        d'4
                        ef'4
                        e'4
                }
                \fraction \times 5/7 {
                        f'8
                        fs'8
                        g'8
                        af'8
                        a'8
                        bf'8
                        b'8
                }
        }
   '''

   assert isinstance(t, RigidMeasure)
   assert t.meter.forced == (11, 15)
   assert len(t) == 2
   tuplet = t[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 4
   assert tuplet.duration.target == Rational(3, 4)
   assert tuplet.duration.prolated == Rational(2, 5)
   note = t[0][0]
   assert note.duration.written == Rational(1, 4)
   assert note.duration.prolated == Rational(1, 10)
   tuplet = t[1]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 7
   assert tuplet.duration.target == Rational(5, 8)
   assert tuplet.duration.prolated == Rational(2, 6)
   note = t[1][0]
   assert note.duration.written == Rational(1, 8)
   assert note.duration.prolated == Rational(1, 21)
   assert check(t)


def test_excise_04( ):
   '''Excise leaf that conflicts with meter duration;
      change meter denominator and reset tuplet target durations.'''

   t = RigidMeasure((5, 6), [
      FixedDurationTuplet((3, 4), Note(0, (1, 4)) * 5),
      FixedDurationTuplet((4, 8), Note(0, (1, 8)) * 7),
      ])

   from abjad.leaf.leaf import _Leaf
   for i, leaf in enumerate(iterate.naive(t, _Leaf)):
      leaf.pitch = i

   r'''
        \time 5/6
        \compressMusic #'(2 . 3) {
                \fraction \times 3/5 {
                        c'4
                        cs'4
                        d'4
                        ef'4
                        e'4
                }
                \times 4/7 {
                        f'8
                        fs'8
                        g'8
                        af'8
                        a'8
                        bf'8
                        b'8
                }
        }
   '''

   excise(t.leaves[-1])

   r'''
        \time 11/14
        \compressMusic #'(4 . 7) {
                \fraction \times 7/10 {
                        c'4
                        cs'4
                        d'4
                        ef'4
                        e'4
                }
                \times 2/3 {
                        f'8
                        fs'8
                        g'8
                        af'8
                        a'8
                        bf'8
                }
        }
   '''

   assert isinstance(t, RigidMeasure)
   assert t.meter.forced == (11, 14)
   assert len(t) == 2
   tuplet = t[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 5
   assert tuplet.duration.target == Rational(7, 8)
   assert tuplet.duration.prolated == Rational(2, 4)
   note = t[0][0]
   assert note.duration.written == Rational(1, 4)
   assert note.duration.prolated == Rational(1, 10)
   tuplet = t[1]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 6
   assert tuplet.duration.target == Rational(4, 8)
   assert tuplet.duration.prolated == Rational(2, 7)
   note = t[1][0]
   assert note.duration.written == Rational(1, 8)
   assert note.duration.prolated == Rational(1, 21)
   assert check(t)


def test_excise_05( ):
   '''Excise leaf that conflicts with meter duration;
      trigger tuplet insertion.'''

   t = RigidMeasure((5, 6), 
      [FixedDurationTuplet((4, 8), run(7))] + run(3, (1, 4)))
   pitchtools.chromaticize(t)

   r'''
        \time 5/6
        \compressMusic #'(2 . 3) {
                \times 4/7 {
                        c'8
                        cs'8
                        d'8
                        ef'8
                        e'8
                        f'8
                        fs'8
                }
                g'4
                af'4
                a'4
        }
   '''

   excise(t.leaves[0])

   r'''
        \time 11/14
        \compressMusic #'(4 . 7) {
                \times 2/3 {
                        cs'8
                        d'8
                        ef'8
                        e'8
                        f'8
                        fs'8
                }
                \fraction \times 7/6 {
                        g'4
                }
                \fraction \times 7/6 {
                        af'4
                }
                \fraction \times 7/6 {
                        a'4
                }
        }
   '''

   assert isinstance(t, RigidMeasure)
   assert t.meter.forced == (11, 14)
   assert len(t) == 4
   tuplet = t[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 6
   assert tuplet.duration.target == Rational(2, 4)
   assert tuplet.duration.prolated == Rational(2, 7)
   note = t[0][0]
   assert note.duration.written == Rational(1, 8)
   assert note.duration.prolated == Rational(1, 21)
   tuplet = t[1]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 1
   assert tuplet.duration.target == Rational(7, 24)
   assert tuplet.duration.prolated == Rational(1, 6)
   note = t[1][0]
   assert note.duration.written == Rational(1, 4)
   assert note.duration.prolated == Rational(1, 6)
   assert check(t)


def test_excise_06( ):
   '''Excise leaf that matches meter duration;
      does not trigger trivial 1:1 tuplet insertion.'''

   t = RigidMeasure((5, 6), 
      [FixedDurationTuplet((4, 8), run(7))] + run(3, (1, 4)))
   pitchtools.chromaticize(t)

   r'''
        \time 5/6
        \compressMusic #'(2 . 3) {
                \times 4/7 {
                        c'8
                        cs'8
                        d'8
                        ef'8
                        e'8
                        f'8
                        fs'8
                }
                g'4
                af'4
                a'4
        }
   '''

   excise(t.leaves[-1])

   r'''
        \time 4/6
        \scaleDurations #'(2 . 3) {
                \times 4/7 {
                        c'8
                        cs'8
                        d'8
                        ef'8
                        e'8
                        f'8
                        fs'8
                }
                g'4
                af'4
        }
   '''

   assert isinstance(t, RigidMeasure)
   assert t.meter.forced == (4, 6)
   assert len(t) == 3
   tuplet = t[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 7
   assert tuplet.duration.target == Rational(2, 4)
   assert tuplet.duration.prolated == Rational(2, 6)
   note = t[0][0]
   assert note.duration.written == Rational(1, 8)
   assert note.duration.prolated == Rational(1, 21)
   note = t[1]
   assert note.duration.written == Rational(1, 4)
   assert note.duration.prolated == Rational(1, 6)
   assert check(t)
