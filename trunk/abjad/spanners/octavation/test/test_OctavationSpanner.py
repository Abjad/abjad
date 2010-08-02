from abjad import *
from abjad.checks import OctavationsOverlapping


def test_octavation_spanner_01( ):
   '''Octavation has default start and stop arguments set to 0.'''

   t = Staff(leaftools.make_repeated_notes(4))
   o = Octavation(t[ : ])

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

   assert o.start == o.stop == 0
   assert t.format == "\\new Staff {\n\t\\ottava #0\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\t\\ottava #0\n}"
   

def test_octavation_spanner_02( ):

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Octavation(t[ : 4], 1)

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

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\ottava #1\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\ottava #0\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"


def test_octavation_spanner_03( ):

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Octavation(t[ : 4], 1, 2)

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

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\ottava #1\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\ottava #2\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"



def test_octavation_spanner_04( ):
   '''One-note octavation changes are allowed.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Octavation(t[0], 1)

   assert componenttools.is_well_formed_component(t)
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


def test_octavation_spanner_05( ):
   '''Adjacent one-note octavation changes are allowed;
      TODO - check for back-to-back set-octavation at format-
             time and compress to a single set-octavation.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Octavation(t[0], 1)
   Octavation(t[1], 2)

   assert componenttools.is_well_formed_component(t)
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


def test_octavation_spanner_06( ):
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
