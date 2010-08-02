from abjad import *


def test_leaf_cast_01( ):
   '''Containerized notes can reinitialize to a rest.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Rest(t[0])

   r'''
   \new Staff {
           r8
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\tr8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"


def test_leaf_cast_02( ):
   '''Round-trip (re)initialization from note to rest to note again
      does not preserve note_head.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Rest(t[0])
   Note(t[0])

   r'''
   \new Staff {
           8
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"

   
def test_leaf_cast_03( ):
   '''Round-trip (re)initialization from (pitched) chord to
      rest (or skip) and back again strips pitch.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   t[0] = Chord([2, 3, 4], (1, 8))
   Rest(t[0])
   Chord(t[0])

   r'''
   \new Staff {
           <>8
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''

   assert t.format == "\\new Staff {\n\t<>8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   

def test_leaf_cast_04( ):
   '''Casting does *not* preserve Formatter instance;
      but casting *does* preserve Formatter before, after, left right.
      Works casting to note / rest / skip.'''

   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].directives.before.append(r"\override NoteHead #'color = #red")
   staff[0].directives.after.append(r"\revert NoteHead #'color")
   #staff[0].directives.left.append(r'\beam #0 #1')

   staff[0].directives.right.append(r'\staccato')

   r'''
   \new Staff {
           \override NoteHead #'color = #red
           c'8 \staccato
           \revert NoteHead #'color
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''

   assert staff.format == "\\new Staff {\n\t\\override NoteHead #'color = #red\n\tc'8 \\staccato\n\t\\revert NoteHead #'color\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"

   Rest(staff[0])

   r'''
   \new Staff {
           \override NoteHead #'color = #red
           r8 \staccato
           \revert NoteHead #'color
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''

   assert staff.format == "\\new Staff {\n\t\\override NoteHead #'color = #red\n\tr8 \\staccato\n\t\\revert NoteHead #'color\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"


def test_leaf_cast_05( ):
   '''Casting does *not* preserve Formatter instance;
      but casting *does* preserve Formatter before, after, left right.
      Works casting to chord.'''

   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].directives.before.append(r"\override NoteHead #'color = #red")
   staff[0].directives.after.append(r"\revert NoteHead #'color")
   #staff[0].directives.left.append(r'\beam #0 #1')
   staff[0].directives.right.append(r'\staccato')

   assert staff.format == "\\new Staff {\n\t\\override NoteHead #'color = #red\n\tc'8 \\staccato\n\t\\revert NoteHead #'color\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"

   Chord(staff[0])

   r'''
   \new Staff {
           \override NoteHead #'color = #red
           <c'>8 \staccato
           \revert NoteHead #'color
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''

   assert staff.format == "\\new Staff {\n\t\\override NoteHead #'color = #red\n\t<c'>8 \\staccato\n\t\\revert NoteHead #'color\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
