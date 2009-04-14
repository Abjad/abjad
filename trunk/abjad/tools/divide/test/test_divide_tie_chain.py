from abjad import *
import py.test


def test_divide_tie_chain_01( ):
   '''Divide tie chain and bequeath spanners and parentage.'''
   
   t = Staff(construct.notes(0, [(5, 32), (5, 32)]))
   Beam(t[:2])
   Beam(t[2:])
   Crescendo(t[:])

   r'''\new Staff {
      c'8 [ \< ~
      c'32 ]
      c'8 [ ~
      c'32 ] \!
   }'''

   divide.tie_chain(t[0].tie.chain, divisions = 6)

   r'''\new Staff {
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
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\fraction \\times 5/6 {\n\t\tc'32 [ \\<\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32 ]\n\t}\n\tc'8 [ ~\n\tc'32 ] \\!\n}"


def test_divide_tie_chain_02( ):
   '''You can NOT divide an orphan tie chain, 
      ie, not within a staff or voice.'''

   notes = construct.notes(0, [(5, 32)])
   Beam(notes)
   assert py.test.raises(Exception, 
      'divide.tie_chain(notes, divisions = 3)')


def test_divide_tie_chain_03( ):
   '''Divide a trivial (ie, length-one) tie chain.'''

   t = Staff(construct.run(4))
   divide.tie_chain(t[1].tie.chain, 3)

   r'''\new Staff {
      c'8
      \times 2/3 {
         c'16
         c'16
         c'16
      }
      c'8
      c'8
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8\n\t\\times 2/3 {\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t}\n\tc'8\n\tc'8\n}"
