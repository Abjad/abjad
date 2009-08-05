from abjad import *


def test_leaftools_excise_01( ):
   '''Excise leaf that conflicts with meter duration.'''

   t = RigidMeasure((4, 4), 
      FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)

   r'''\time 4/4
        \times 2/3 {
                c'4
                cs'4
                d'4
        }
        \times 2/3 {
                ef'4
                e'4
                f'4
        }'''

   leaftools.excise(t.leaves[0])

   r'''\time 5/6
        \compressMusic #'(2 . 3) {
                        cs'4
                        d'4
                        ef'4
                        e'4
                        f'4
        }'''

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
   check.wf(t)


def test_leaftools_excise_02( ):
   '''Excise leaf that conflicts with meter duration.'''

   t = RigidMeasure((4, 4), 
      FixedDurationTuplet((2, 4), Note(0, (1, 8)) * 5) * 2)

   r'''\time 4/4
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
        }'''

   leaftools.excise(t.leaves[0])

   r'''\time 9/10
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
     }'''

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
   check.wf(t)


def test_leaftools_excise_03( ):
   '''Excise leaf that conflicts with meter duration;
      change meter denominator and reset tuplet target durations.'''

   t = RigidMeasure((5, 6), [
      FixedDurationTuplet((3, 4), Note(0, (1, 4)) * 5),
      FixedDurationTuplet((4, 8), Note(0, (1, 8)) * 7),
      ])
   
   from abjad.leaf.leaf import _Leaf
   for i, leaf in enumerate(iterate.naive(t, _Leaf)):
      leaf.pitch = i

   r'''\time 5/6
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
        }'''

   leaftools.excise(t.leaves[0])

   r'''\time 11/15
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
        }'''

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
   assert check.wf(t)


def test_leaftools_excise_04( ):
   '''Excise leaf that conflicts with meter duration;
      change meter denominator and reset tuplet target durations.'''

   t = RigidMeasure((5, 6), [
      FixedDurationTuplet((3, 4), Note(0, (1, 4)) * 5),
      FixedDurationTuplet((4, 8), Note(0, (1, 8)) * 7),
      ])

   from abjad.leaf.leaf import _Leaf
   for i, leaf in enumerate(iterate.naive(t, _Leaf)):
      leaf.pitch = i

   r'''\time 5/6
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
        }'''

   leaftools.excise(t.leaves[-1])

   r'''\time 11/14
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
        }'''

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
   assert check.wf(t)


def test_leaftools_excise_05( ):
   '''Excise leaf that conflicts with meter duration;
      trigger tuplet insertion.'''

   t = RigidMeasure((5, 6), 
      [FixedDurationTuplet((4, 8), construct.run(7))] + 
         construct.run(3, (1, 4)))
   pitchtools.chromaticize(t)

   r'''\time 5/6
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
        }'''

   leaftools.excise(t.leaves[0])

   r'''\time 11/14
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
        }'''

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
   assert check.wf(t)


def test_leaftools_excise_06( ):
   '''Excise leaf that matches meter duration;
      does not trigger trivial 1:1 tuplet insertion.'''

   t = RigidMeasure((5, 6), 
      [FixedDurationTuplet((4, 8), construct.run(7))] + 
         construct.run(3, (1, 4)))
   pitchtools.chromaticize(t)

   r'''\time 5/6
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
        }'''

   leaftools.excise(t.leaves[-1])

   r'''\time 4/6
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
        }'''

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
   assert check.wf(t)


def test_leaftools_excise_07( ):
   '''Nested fixed-duration tuplet.'''

   t = RigidMeasure((4, 4), [
      FixedDurationTuplet((2, 2), [Note(0, (1, 2)), Note(1, (1, 2)), 
      FixedDurationTuplet((2, 4), [Note(i, (1, 4)) for i in range(2, 5)])])])

   r'''\time 4/4
      \times 2/3 {
             c'2
             cs'2
             \times 2/3 {
                     d'4
                     ef'4
                     e'4
             }
      }'''

   leaftools.excise(t.leaves[-1])
   measure = t
   assert isinstance(measure, RigidMeasure)
   assert measure.meter.forced == (8, 9)
   assert len(measure) == 1
   tuplet = t[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 3
   assert tuplet.duration.target == Rational(1)
   assert tuplet.duration.prolated == Rational(8, 9)
   assert tuplet.duration.multiplier == Rational(3, 4)
   note = t[0][0]
   assert isinstance(note, Note)
   assert note.duration.written == Rational(1, 2)
   assert note.duration.prolated == Rational(1, 3)
   tuplet = t[0][-1]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 2
   assert tuplet.duration.target == Rational(1, 3)
   assert tuplet.duration.prolated == Rational(2, 9)
   assert tuplet.duration.multiplier == Rational(2, 3)
   note = t[0][-1][0]
   assert isinstance(note, Note)
   assert note.duration.written == Rational(1, 4)
   assert note.duration.prolated == Rational(1, 9)

   r'''\time 8/9
      \compressMusic #'(8 . 9) {
             \fraction \times 3/4 {
                     c'2
                     cs'2
                     \times 2/3 {
                             d'4
                             ef'4
                     }
             }
      } '''


def test_excise_container_01( ):
   '''Plain vanilla container.'''
   t = Container(Note(0, (1, 4)) * 6)
   leaftools.excise(t.leaves[0])
   assert isinstance(t, Container)
   assert len(t) == 5
   assert t.duration.preprolated == Rational(5, 4)
   assert t.duration.prolated == Rational(5, 4)
   assert isinstance(t[0], Note)
   assert t[0].duration.written == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 4)
   assert check.wf(t)


def test_excise_container_02( ):
   '''Container container.'''
   t = Container(Note(0, (1, 4)) * 6)
   leaftools.excise(t.leaves[0])
   assert isinstance(t, Container)
   assert len(t) == 5
   assert t.duration.preprolated == Rational(5, 4)
   assert t.duration.prolated == Rational(5, 4)
   assert isinstance(t[0], Note)
   assert t[0].duration.written == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 4)
   assert check.wf(t)


def test_excise_container_03( ):
   '''Voice.'''
   t = Voice(Note(0, (1, 4)) * 6)
   leaftools.excise(t.leaves[0])
   assert isinstance(t, Voice)
   assert len(t) == 5
   assert t.duration.preprolated == Rational(5, 4)
   assert t.duration.prolated == Rational(5, 4)
   assert isinstance(t[0], Note)
   assert t[0].duration.written == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 4)
   assert check.wf(t)


def test_excise_container_04( ):
   '''Staff.'''
   t = Staff(Note(0, (1, 4)) * 6)
   leaftools.excise(t.leaves[0])
   assert isinstance(t, Staff)
   assert len(t) == 5
   assert t.duration.preprolated == Rational(5, 4)
   assert t.duration.prolated == Rational(5, 4)
   assert isinstance(t[0], Note)
   assert t[0].duration.written == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 4)
   assert check.wf(t)


def test_excise_container_05( ):
   '''Container.'''
   t = Container(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   leaftools.excise(t[0])
   assert isinstance(t, Container)
   assert len(t) == 1
   assert t.duration.preprolated == Rational(2, 4)
   assert t.duration.prolated == Rational(2, 4)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration.target == Rational(2, 4)
   assert t[0].duration.prolated == Rational(2, 4)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration.written == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check.wf(t)


def test_excise_container_06( ):
   '''Container.'''
   t = Container(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   leaftools.excise(t[0])
   assert isinstance(t, Container)
   assert len(t) == 1
   assert t.duration.preprolated == Rational(2, 4)
   assert t.duration.prolated == Rational(2, 4)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration.target == Rational(2, 4)
   assert t[0].duration.prolated == Rational(2, 4)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration.written == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check.wf(t)


def test_excise_container_07( ):
   '''Voice.'''
   t = Voice(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   leaftools.excise(t[0])
   assert isinstance(t, Voice)
   assert len(t) == 1
   assert t.duration.preprolated == Rational(2, 4)
   assert t.duration.prolated == Rational(2, 4)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration.target == Rational(2, 4)
   assert t[0].duration.prolated == Rational(2, 4)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration.written == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check.wf(t)


def test_excise_container_08( ):
   '''Staff.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   leaftools.excise(t[0])
   assert isinstance(t, Staff)
   assert len(t) == 1
   assert t.duration.preprolated == Rational(2, 4)
   assert t.duration.prolated == Rational(2, 4)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration.target == Rational(2, 4)
   assert t[0].duration.prolated == Rational(2, 4)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration.written == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check.wf(t)


def test_excise_container_09( ):
   '''Container.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   leaftools.excise(t.leaves[0])
   assert isinstance(t, Staff)
   assert len(t) == 2
   assert t.duration.preprolated == Rational(5, 6)
   assert t.duration.prolated == Rational(5, 6)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration.target == Rational(2, 6)
   assert t[0].duration.prolated == Rational(2, 6)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration.written == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check.wf(t)


def test_excise_container_10( ):
   '''Container.'''
   t = Container(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   leaftools.excise(t.leaves[0])
   assert isinstance(t, Container)
   assert len(t) == 2
   assert t.duration.preprolated == Rational(5, 6)
   assert t.duration.prolated == Rational(5, 6)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration.target == Rational(2, 6)
   assert t[0].duration.prolated == Rational(2, 6)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration.written == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check.wf(t)


def test_excise_container_11( ):
   '''Voice.'''
   t = Voice(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   leaftools.excise(t.leaves[0])
   assert isinstance(t, Voice)
   assert len(t) == 2
   assert t.duration.preprolated == Rational(5, 6)
   assert t.duration.prolated == Rational(5, 6)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration.target == Rational(2, 6)
   assert t[0].duration.prolated == Rational(2, 6)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration.written == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check.wf(t)


def test_excise_container_12( ):
   '''Staff.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   leaftools.excise(t.leaves[0])
   assert isinstance(t, Staff)
   assert len(t) == 2
   assert t.duration.preprolated == Rational(5, 6)
   assert t.duration.prolated == Rational(5, 6)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration.target == Rational(2, 6)
   assert t[0].duration.prolated == Rational(2, 6)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration.written == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check.wf(t)


def test_excise_singletons_01( ):
   '''Singly-nested singleton.'''
   t = FixedDurationTuplet((2, 4), [
      Note(0, (1, 4)),
      Note(0, (1, 4)),
      FixedDurationTuplet((1, 4), [Note(0, (1, 4))])])
   leaftools.excise(t.leaves[-1])
   assert isinstance(t, FixedDurationTuplet)
   assert len(t) == 2
   assert t.duration.target == Rational(2, 6)
   assert t.duration.multiplier == Rational(2, 3)
   assert t.duration.prolated == Rational(2, 6)
   assert isinstance(t[0], Note)
   assert t[0].duration.written == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 6)


def test_excise_singletons_02( ):
   '''Doubly-nested singleton.'''
   t = FixedDurationTuplet((2, 4), [
      Note(0, (1, 4)),
      Note(0, (1, 4)),
      FixedDurationTuplet((1, 4), [
         FixedDurationTuplet((1, 4), [Note(0, (1, 4))])])])
   leaftools.excise(t.leaves[-1])
   assert isinstance(t, FixedDurationTuplet)
   assert len(t) == 2
   assert t.duration.target == Rational(2, 6)
   assert t.duration.multiplier == Rational(2, 3)
   assert t.duration.prolated == Rational(2, 6)
   assert isinstance(t[0], Note)
   assert t[0].duration.written == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 6)


def test_excise_singletons_03( ):
   '''Doubly-nested singleton.'''
   t = FixedDurationTuplet((2, 4), [
      Note(0, (1, 4)),
      Note(0, (1, 4)),
      FixedDurationTuplet((1, 4), [
         FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 2)])])
   r'''
   \times 2/3 {
        c'4
        cs'4
                        d'8
                        ef'8
   }
   '''
   leaftools.excise(t.leaves[-1])
   assert isinstance(t, FixedDurationTuplet)
   assert len(t) == 3
   assert t.duration.target == Rational(5, 12)
   assert t.duration.prolated == Rational(5, 12)
   assert t.duration.multiplier == Rational(2, 3)
   assert isinstance(t[0], Note)
   assert t[0].duration.written == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 6)
   tuplet = t[-1]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 1
   assert tuplet.duration.preprolated == Rational(1, 8)
   assert tuplet.duration.prolated == Rational(1, 12)
   assert tuplet.duration.multiplier == Rational(1, 1)
   tuplet = t[-1][0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 1
   assert tuplet.duration.preprolated == Rational(1, 8)
   assert tuplet.duration.prolated == Rational(1, 12)
   assert tuplet.duration.multiplier == Rational(1, 1)
   note = t.leaves[-1]
   assert isinstance(note, Note)
   assert note.duration.written == Rational(1, 8)
   assert note.duration.prolated == Rational(1, 12)
   r'''
   \times 2/3 {
           c'4
           cs'4
                           d'8
   }
   '''


def test_excise_tuplet_01(  ):
   '''Nonnested fixed-duration tuplet.'''
   t = FixedDurationTuplet((4, 4), Note(0, (1, 4)) * 5)
   leaftools.excise(t.leaves[0])
   assert isinstance(t, FixedDurationTuplet)
   assert len(t) == 4
   assert t.duration.target == Rational(4, 5)
   assert t.duration.prolated == Rational(4, 5)
   assert isinstance(t[0], Note)
   assert t[0].duration.written == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 5)


def test_excise_tuplet_02(  ):
   '''Nonnested fixed-multiplier tuplet.'''
   t = FixedMultiplierTuplet((4, 5), Note(0, (1, 4)) * 5)
   leaftools.excise(t.leaves[0])
   assert isinstance(t, FixedMultiplierTuplet)
   assert len(t) == 4
   assert t.duration.preprolated == Rational(4, 5)
   assert t.duration.prolated == Rational(4, 5)
   assert isinstance(t[0], Note)
   assert t[0].duration.written == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 5)


def test_excise_tuplet_03( ):
   '''Nested fixed-duration tuplet.'''
   t = FixedDurationTuplet((2,2), [Note(0, (1,2)), Note(1, (1,2)), \
      FixedDurationTuplet((2,4), [Note(i, (1,4)) for i in range(2, 5)])])
   leaftools.excise(t.leaves[-1])
   assert isinstance(t, FixedDurationTuplet)
   assert len(t) == 3
   assert t.duration.target == Rational(8,9)
   assert t.duration.prolated == Rational(8,9)
   assert isinstance(t[2], FixedDurationTuplet)
   assert t[2].duration.target == Rational(2,6)
   assert t[2].duration.prolated == Rational(2, 9)


def test_excise_tuplet_04( ):
   '''Nested fixed-multiplier tuplet.'''
   t = FixedMultiplierTuplet((2,3), [Note(0, (1,2)), Note(1, (1,2)), \
      FixedMultiplierTuplet((2,3), [Note(i, (1,4)) for i in range(2, 5)])])
   leaftools.excise(t.leaves[-1])
   assert isinstance(t, FixedMultiplierTuplet)
   assert len(t) == 3
   assert t.duration.preprolated == Rational(8,9)
   assert t.duration.prolated == Rational(8,9)
   assert isinstance(t[2], FixedMultiplierTuplet)
   assert t[2].duration.preprolated == Rational(2,6)
   assert t[2].duration.prolated == Rational(2, 9)
