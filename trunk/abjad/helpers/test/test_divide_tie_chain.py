from abjad import *
from abjad.tools import construct


def test_divide_tie_chain_01( ):
   '''Divide tie chain and bequeath spanners and parentage.'''
   
   t = Staff(construct.notes(0, [(5, 32), (5, 32)]))
   Beam(t[:2])
   Beam(t[2:])
   Crescendo(t[:])

   r'''
   \new Staff {
      c'8 [ \< ~
      c'32 ]
      c'8 [ ~
      c'32 ] \!
   }
   '''

   divide_tie_chain(t[0].tie.chain, divisions = 6)

   r'''
   \new Staff {
      \fraction \times 5/6 {
         c'32 [ \<
         c'32
         c'32
         c'32
         c'32
         c'32 ]
      }
      c'8 [ ~
      c'32 ] \!
   }
   '''

   assert check(t)
   assert t.format == "\\new Staff {\n\t\\fraction \\times 5/6 {\n\t\tc'32 [ \\<\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32 ]\n\t}\n\tc'8 [ ~\n\tc'32 ] \\!\n}"


def test_divide_tie_chain_02( ):
   '''You can divide an orphan tie chain, 
      ie, not within a staff or voice.'''

   notes = construct.notes(0, [(5, 32)])
   Beam(notes)

   r'''
   c'8 [ ~
   c'32 ]
   '''

   t = divide_tie_chain(notes, divisions = 3)

   r'''
   \fraction \times 5/6 {
      c'16 [
      c'16
      c'16 ]
   }
   '''

   assert check(t)
   assert t.format == "\\fraction \\times 5/6 {\n\tc'16 [\n\tc'16\n\tc'16 ]\n}"
