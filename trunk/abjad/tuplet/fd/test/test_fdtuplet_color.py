from abjad import *


def test_tuplet_fd_color_01( ):
   '''Setting 'color' on the FixedDurationTuplet class
      both prints and colors trivial tuplets at format-time.'''

   FixedDurationTuplet.color = True
   t = FixedDurationTuplet((3, 8), scale(3))

   r'''
   \tweak #'color #blue
   \times 1/1 {
      c'8
      d'8
      e'8
   }
   '''

   assert check(t)
   assert t.format == "\\tweak #'color #blue\n\\times 1/1 {\n\tc'8\n\td'8\n\te'8\n}"


def test_tuplet_fd_color_02( ):
   r'''Trivial tuplet coloring uses LilyPond \tweak to
      handle nested tuplets correctly.'''

   FixedDurationTuplet.color = True
   t = FixedDurationTuplet((3, 8), FixedDurationTuplet((2, 8), scale(2)) * 2)
   diatonicize(t)

   r'''
   \fraction \times 3/4 {
      \tweak #'color #blue
      \times 1/1 {
         c'8
         d'8
      }
      \tweak #'color #blue
      \times 1/1 {
         e'8
         f'8
      }
   }
   '''

   assert check(t)
   assert t.format == "\\fraction \\times 3/4 {\n\t\\tweak #'color #blue\n\t\\times 1/1 {\n\t\tc'8\n\t\td'8\n\t}\n\t\\tweak #'color #blue\n\t\\times 1/1 {\n\t\te'8\n\t\tf'8\n\t}\n}"
