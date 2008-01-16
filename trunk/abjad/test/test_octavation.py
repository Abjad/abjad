from abjad import *


def test_octavation_01( ):
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   Octavation(staff[ : 4], 1)
   assert staff.tester.testAll(ret = True)
   assert staff.format == "\\new Staff {\n\t#(set-octavation 1)\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t#(set-octavation 0)\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
   \new Staff {
           #(set-octavation 1)
           c'8
           cs'8
           d'8
           ef'8
           #(set-octavation 0)
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_octavation_02( ):
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   Octavation(staff[ : 4], 1, 2)
   assert staff.tester.testAll(ret = True)
   assert staff.format == "\\new Staff {\n\t#(set-octavation 1)\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t#(set-octavation 2)\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
   \new Staff {
           #(set-octavation 1)
           c'8
           cs'8
           d'8
           ef'8
           #(set-octavation 2)
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_octavation_03( ):
   '''One-note octavation changes are allowed.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   Octavation(staff[0], 1)
   assert staff.format == "\\new Staff {\n\t#(set-octavation 1)\n\tc'8\n\t#(set-octavation 0)\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert staff.tester.testAll(ret = True)
   '''
   \new Staff {
           #(set-octavation 1)
           c'8
           #(set-octavation 0)
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_octavation_04( ):
   '''Adjacent one-note octavation changes are allowed;
      TODO - check for back-to-back set-octavation at format-
             time and compress to a single set-octavation.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   Octavation(staff[0], 1)
   Octavation(staff[1], 2)
   assert staff.format == "\\new Staff {\n\t#(set-octavation 1)\n\tc'8\n\t#(set-octavation 0)\n\t#(set-octavation 2)\n\tcs'8\n\t#(set-octavation 0)\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert staff.tester.testAll(ret = True)
   '''
   \new Staff {
           #(set-octavation 1)
           c'8
           #(set-octavation 0)
           #(set-octavation 2)
           cs'8
           #(set-octavation 0)
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_octavation_05( ):
   '''Overlapping octavation spanners are allowed;
      but tester will grumble.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   Octavation(staff[ : 4], 1)
   Octavation(staff[2 : 6], 2)
   assert staff.format == "\\new Staff {\n\t#(set-octavation 1)\n\tc'8\n\tcs'8\n\t#(set-octavation 2)\n\td'8\n\tef'8\n\t#(set-octavation 0)\n\te'8\n\tf'8\n\t#(set-octavation 0)\n\tfs'8\n\tg'8\n}"
   assert not staff.tester.testOverlappingOctavation(ret = True)
   '''
   \new Staff {
           #(set-octavation 1)
           c'8
           cs'8
           #(set-octavation 2)
           d'8
           ef'8
           #(set-octavation 0)
           e'8
           f'8
           #(set-octavation 0)
           fs'8
           g'8
   }
   '''
