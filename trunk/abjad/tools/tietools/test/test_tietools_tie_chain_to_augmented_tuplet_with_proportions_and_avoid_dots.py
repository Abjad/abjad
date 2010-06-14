from abjad import *


def test_tietools_tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots_01( ):

   t = Staff([Note(0, (1, 8)), Note(0, (1, 16)), Note(0, (1, 16))])
   Tie(t[:2])
   Beam(t[:])

   r'''
   \new Staff {
           c'8 [ ~
           c'16
           c'16 ]
   }
   '''

   tietools.tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots(t[0].tie.chain, [1])

   r'''
      \new Staff {
              \fraction \times 3/2 {
                      c'8 [
              }
              c'16 ]
      }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\fraction \\times 3/2 {\n\t\tc'8 [\n\t}\n\tc'16 ]\n}"


def test_tietools_tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots_02( ):

   t = Staff([Note(0, (1, 8)), Note(0, (1, 16)), Note(0, (1, 16))])
   Tie(t[:2])
   Beam(t[:])
   tietools.tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots(t[0].tie.chain, [1, 2])

   r'''
   \new Staff {
           {
                   c'16
                   c'8
           }
           c'16 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\tc'16 [\n\t\tc'8\n\t}\n\tc'16 ]\n}"


def test_tietools_tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots_03( ):

   t = Staff([Note(0, (1, 8)), Note(0, (1, 16)), Note(0, (1, 16))])
   Tie(t[:2])
   Beam(t[:])
   tietools.tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots(
      t[0].tie.chain, [1, 2, 2])

   r'''
   \new Staff {
           \fraction \times 6/5 {
                   c'32 [
                   c'16
                   c'16
           }
           c'16 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\fraction \\times 6/5 {\n\t\tc'32 [\n\t\tc'16\n\t\tc'16\n\t}\n\tc'16 ]\n}"
