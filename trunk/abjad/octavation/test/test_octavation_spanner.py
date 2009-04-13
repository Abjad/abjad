from abjad import *
from abjad.checks import OctavationsOverlapping


def test_octavation_01( ):
   '''Octavation has default start and stop arguments set to 0.'''
   t = Staff(construct.run(4))
   o = Octavation(t[ : ])
   assert o.start == o.stop == 0
   assert t.format == "\\new Staff {\n\t\\ottava #0\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\t\\ottava #0\n}"
   r'''
   \new Staff {
           \ottava #0 
           c'8
           c'8
           c'8
           c'8
           \ottava #0 
   }
   '''
   

def test_octavation_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Octavation(t[ : 4], 1)
   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\ottava #1\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\ottava #0\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   r'''
   \new Staff {
           \ottava #1
           c'8
           cs'8
           d'8
           ef'8
           \ottava #0
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_octavation_03( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Octavation(t[ : 4], 1, 2)
   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\ottava #1\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\ottava #2\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   r'''
   \new Staff {
           \ottava #1
           c'8
           cs'8
           d'8
           ef'8
           \ottava #2
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_octavation_04( ):
   '''One-note octavation changes are allowed.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Octavation(t[0], 1)
   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\ottava #1\n\tc'8\n\t\\ottava #0\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   r'''
   \new Staff {
           \ottava #1
           c'8
           \ottava #0
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_octavation_05( ):
   '''Adjacent one-note octavation changes are allowed;
      TODO - check for back-to-back set-octavation at format-
             time and compress to a single set-octavation.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Octavation(t[0], 1)
   Octavation(t[1], 2)
   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\ottava #1\n\tc'8\n\t\\ottava #0\n\t\\ottava #2\n\tcs'8\n\t\\ottava #0\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   r'''
   \new Staff {
           \ottava #1
           c'8
           \ottava #0
           \ottava #2
           cs'8
           \ottava #0
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_octavation_06( ):
   '''Overlapping octavation spanners are allowed but not well-formed.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Octavation(t[ : 4], 1)
   Octavation(t[2 : 6], 2)
   checker = OctavationsOverlapping( )
   assert not checker.check(t)
   assert t.format == "\\new Staff {\n\t\\ottava #1\n\tc'8\n\tcs'8\n\t\\ottava #2\n\td'8\n\tef'8\n\t\\ottava #0\n\te'8\n\tf'8\n\t\\ottava #0\n\tfs'8\n\tg'8\n}"
   r'''
   \new Staff {
           \ottava #1
           c'8
           cs'8
           \ottava #2
           d'8
           ef'8
           \ottava #0
           e'8
           f'8
           \ottava #0
           fs'8
           g'8
   }
   '''

#def test_octavation_01( ):
#   t = Staff([Note(n, (1, 8)) for n in range(8)])
#   Octavation(t[ : 4], 1)
#   assert check.wf(t)
#   assert t.format == "\\new Staff {\n\t#(set-octavation 1)\n\t\\set Staff.middleCPosition = #-13\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t#(set-octavation 0)\n\t\\set Staff.middleCPosition = #-6\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
#   '''
#   \new Staff {
#           #(set-octavation 1)
#           \set Staff.middleCPosition = #-13
#           c'8
#           cs'8
#           d'8
#           ef'8
#           #(set-octavation 0)
#           \set Staff.middleCPosition = #-6
#           e'8
#           f'8
#           fs'8
#           g'8
#   }
#   '''
#
#
#def test_octavation_02( ):
#   t = Staff([Note(n, (1, 8)) for n in range(8)])
#   Octavation(t[ : 4], 1, 2)
#   assert check.wf(t)
#   assert t.format == "\\new Staff {\n\t#(set-octavation 1)\n\t\\set Staff.middleCPosition = #-13\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t#(set-octavation 2)\n\t\\set Staff.middleCPosition = #-20\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
#   '''
#   \new Staff {
#           #(set-octavation 1)
#           \set Staff.middleCPosition = #-13
#           c'8
#           cs'8
#           d'8
#           ef'8
#           #(set-octavation 2)
#           \set Staff.middleCPosition = #-20
#           e'8
#           f'8
#           fs'8
#           g'8
#   }
#   '''
#
#
#def test_octavation_03( ):
#   '''One-note octavation changes are allowed.'''
#   t = Staff([Note(n, (1, 8)) for n in range(8)])
#   Octavation(t[0], 1)
#   assert t.format == "\\new Staff {\n\t#(set-octavation 1)\n\t\\set Staff.middleCPosition = #-13\n\tc'8\n\t#(set-octavation 0)\n\t\\set Staff.middleCPosition = #-6\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
#   assert check.wf(t)
#   '''
#   \new Staff {
#           #(set-octavation 1)
#           \set Staff.middleCPosition = #-13
#           c'8
#           #(set-octavation 0)
#           \set Staff.middleCPosition = #-6
#           cs'8
#           d'8
#           ef'8
#           e'8
#           f'8
#           fs'8
#           g'8
#   }
#   '''
#
#
#def test_octavation_04( ):
#   '''Adjacent one-note octavation changes are allowed;
#      TODO - check for back-to-back set-octavation at format-
#             time and compress to a single set-octavation.'''
#   t = Staff([Note(n, (1, 8)) for n in range(8)])
#   Octavation(t[0], 1)
#   Octavation(t[1], 2)
#   assert t.format == "\\new Staff {\n\t#(set-octavation 1)\n\t\\set Staff.middleCPosition = #-13\n\tc'8\n\t#(set-octavation 0)\n\t\\set Staff.middleCPosition = #-6\n\t#(set-octavation 2)\n\t\\set Staff.middleCPosition = #-20\n\tcs'8\n\t#(set-octavation 0)\n\t\\set Staff.middleCPosition = #-6\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
#   assert check.wf(t)
#   '''
#   \new Staff {
#           #(set-octavation 1)
#           \set Staff.middleCPosition = #-13
#           c'8
#           #(set-octavation 0)
#           \set Staff.middleCPosition = #-6
#           #(set-octavation 2)
#           \set Staff.middleCPosition = #-20
#           cs'8
#           #(set-octavation 0)
#           \set Staff.middleCPosition = #-6
#           d'8
#           ef'8
#           e'8
#           f'8
#           fs'8
#           g'8
#   }
#   '''
#
#
#def test_octavation_05( ):
#   '''Overlapping octavation spanners are allowed but not well-formed.'''
#   t = Staff([Note(n, (1, 8)) for n in range(8)])
#   Octavation(t[ : 4], 1)
#   Octavation(t[2 : 6], 2)
#   assert t.format == "\\new Staff {\n\t#(set-octavation 1)\n\t\\set Staff.middleCPosition = #-13\n\tc'8\n\tcs'8\n\t#(set-octavation 2)\n\t\\set Staff.middleCPosition = #-20\n\td'8\n\tef'8\n\t#(set-octavation 0)\n\t\\set Staff.middleCPosition = #-6\n\te'8\n\tf'8\n\t#(set-octavation 0)\n\t\\set Staff.middleCPosition = #-6\n\tfs'8\n\tg'8\n}"
#   checker = OctavationsOverlapping( )
#   assert not checker.check(t)
#   '''
#   \new Staff {
#           #(set-octavation 1)
#           \set Staff.middleCPosition = #-13
#           c'8
#           cs'8
#           #(set-octavation 2)
#           \set Staff.middleCPosition = #-20
#           d'8
#           ef'8
#           #(set-octavation 0)
#           \set Staff.middleCPosition = #-6
#           e'8
#           f'8
#           #(set-octavation 0)
#           \set Staff.middleCPosition = #-6
#           fs'8
#           g'8
#   }
#   '''
