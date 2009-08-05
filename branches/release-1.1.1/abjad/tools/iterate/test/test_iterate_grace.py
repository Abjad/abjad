from abjad import *


def test_iterate_grace_01( ):
   '''Yield before-gracenotes and after-gracenotes.'''

   t = Voice(construct.scale(4))
   Beam(t[:])
   notes = construct.scale(4, Rational(1, 16))
   t[1].grace.before.extend(notes[:2])
   t[1].grace.after.extend(notes[2:])

   r'''\new Voice {
      c'8 [
      \grace {
         c'16
         d'16
      }
      \afterGrace
      d'8
      {
         e'16
         f'16
      }
      e'8
      f'8 ]
   }'''

   notes = list(iterate.grace(t, Note))

   "[Note(c', 8), Note(c', 16), Note(d', 16), Note(d', 8), Note(e', 16), Note(f', 16), Note(e', 8), Note(f', 8)]"

   assert notes[0] is t[0]
   assert notes[1] is t[1].grace.before[0]
   assert notes[2] is t[1].grace.before[1]
   assert notes[3] is t[1]
   assert notes[4] is t[1].grace.after[0]
   assert notes[5] is t[1].grace.after[1]
   assert notes[6] is t[2]
   assert notes[7] is t[3]
