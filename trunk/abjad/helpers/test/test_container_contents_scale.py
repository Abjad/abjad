from abjad import *


## TODO: Add tests for (fd / fm) tuplets sitting inside voice. ##

def test_container_contents_scale_01( ):
   '''Scale leaves in voice by 3/2; ie, dot leaves.'''

   t = Voice(scale(4))
   container_contents_scale(t, Rational(3, 2))

   r'''
   \new Voice {
           c'8.
           d'8.
           e'8.
           f'8.
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8.\n\td'8.\n\te'8.\n\tf'8.\n}"


def test_container_contents_scale_02( ):
   '''Scale leaves in voice by 5/4; ie, quarter-tie leaves.'''

   t = Voice(scale(4))
   container_contents_scale(t, Rational(5, 4))

   r'''
   \new Voice {
           c'8 ~
           c'32
           d'8 ~
           d'32
           e'8 ~
           e'32
           f'8 ~
           f'32
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 ~\n\tc'32\n\td'8 ~\n\td'32\n\te'8 ~\n\te'32\n\tf'8 ~\n\tf'32\n}"


def test_container_contents_scale_03( ):
   '''Scale leaves in voice by untied nonbinary 4/3;
       ie, tupletize notes.'''

   t = Voice(scale(4))
   container_contents_scale(t, Rational(4, 3))

   r'''
   \new Voice {
           \times 2/3 {
                   c'4
           }
           \times 2/3 {
                   d'4
           }
           \times 2/3 {
                   e'4
           }
           \times 2/3 {
                   f'4
           }
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'4\n\t}\n\t\\times 2/3 {\n\t\td'4\n\t}\n\t\\times 2/3 {\n\t\te'4\n\t}\n\t\\times 2/3 {\n\t\tf'4\n\t}\n}"


def test_container_contents_scale_04( ):
   '''Scale leaves in voice by tied nonbinary 5/4;
       ie, tupletize notes.'''

   t = Voice(scale(4))
   container_contents_scale(t, Rational(5, 6))

   r'''
   \new Voice {
           \times 2/3 {
                   c'8 ~
                   c'32
           }
           \times 2/3 {
                   d'8 ~
                   d'32
           }
           \times 2/3 {
                   e'8 ~
                   e'32
           }
           \times 2/3 {
                   f'8 ~
                   f'32
           }
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 ~\n\t\tc'32\n\t}\n\t\\times 2/3 {\n\t\td'8 ~\n\t\td'32\n\t}\n\t\\times 2/3 {\n\t\te'8 ~\n\t\te'32\n\t}\n\t\\times 2/3 {\n\t\tf'8 ~\n\t\tf'32\n\t}\n}"
