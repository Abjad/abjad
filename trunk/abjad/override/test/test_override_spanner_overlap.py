from abjad import *


### TODO - make overlapping one-note overrides work ###

def test_override_overlap_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Override(t[ : ], 'NoteHead', 'color', 'red')

   assert check(t)
   assert t.format == "\\new Staff {\n\t\\override NoteHead #'color = #red\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\t\\revert NoteHead #'color\n}"

#   for note in t:
#      assert note.spanners.find('NoteHead', 'color') == 'red'

   r'''
   \new Staff {
           \override NoteHead #'color = #red
           c'8
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
           \revert NoteHead #'color
   }
   '''


def test_override_overlap_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Override(t[ : ], 'NoteHead', 'color', 'red')
   Override(t[2 : 6], 'NoteHead', 'color', 'blue')

   assert check(t)
   assert t.format == "\\new Staff {\n\t\\override NoteHead #'color = #red\n\tc'8\n\tcs'8\n\t\\override NoteHead #'color = #blue\n\td'8\n\tef'8\n\te'8\n\tf'8\n\t\\revert NoteHead #'color\n\tfs'8\n\tg'8\n\t\\revert NoteHead #'color\n}"

   #assert [leaf.spanners.find('NoteHead', 'color') for leaf in t] == \
   #   ['red', 'red', 'blue', 'blue', 'blue', 'blue', None, None]

   r'''
   \new Staff {
           \override NoteHead #'color = #red
           c'8
           cs'8
           \override NoteHead #'color = #blue
           d'8
           ef'8
           e'8
           f'8
           \revert NoteHead #'color
           fs'8
           g'8
           \revert NoteHead #'color
   }
   '''


def test_override_overlap_03( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Override(t[ : ], 'NoteHead', 'color', 'red')
   Override(t[4], 'NoteHead', 'color', 'blue')

   assert check(t)
   assert t.format == "\\new Staff {\n\t\\override NoteHead #'color = #red\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\once \\override NoteHead #'color = #blue\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\t\\revert NoteHead #'color\n}"

#   assert [leaf.spanners.find('NoteHead', 'color') for leaf in t] == \
#      ['red', 'red', 'red', 'red', 'blue', 'red', 'red', 'red']

   r'''
   \new Staff {
           \override NoteHead #'color = #red
           c'8
           cs'8
           d'8
           ef'8
           \once \override NoteHead #'color = #blue
           e'8
           f'8
           fs'8
           g'8
           \revert NoteHead #'color
   }
   '''
