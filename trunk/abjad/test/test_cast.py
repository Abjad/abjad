from abjad import *


def test_cast_01( ):
   '''Casting leaves inside a container works;
      a 'naked' cast works fine here;
      no need to reassign staff[0] = staff[0].caster.toRest( ).'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].caster.toRest( )
   assert staff.format == "\\new Staff {\n\tr8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert staff.tester.testAll(ret = True)
   '''
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


def test_cast_02( ):
   '''Casting from note to rest / skip to note again preserves notehead.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].caster.toRest( )
   staff[0].caster.toNote( )
   assert staff.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
   \new Staff {
           c'8
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''

   
def test_cast_03( ):
   '''Casting from chord to rest / skip to chord again preserves noteheads.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0] = Chord([2, 3, 4], (1, 8))
   assert staff.format == "\\new Staff {\n\t<d' ef' e'>8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   staff[0].caster.toRest( )
   staff[0].caster.toChord( )
   assert staff.format == "\\new Staff {\n\t<d' ef' e'>8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
   \new Staff {
           <d' ef' e'>8
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''
   

def test_cast_04( ):
   '''Casting does *not* preserve Formatter instance;
      but casting *does* preserve Formatter before, after, left right.
      Works casting to note / rest / skip.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].formatter.before.append(r"\override NoteHead #'color = #red")
   staff[0].formatter.after.append(r"\revert NoteHead #'color")
   staff[0].formatter.left.append(r'\beam #0 #1')
   staff[0].formatter.right.append(r'\staccato')
   assert staff.format == "\\new Staff {\n\t\\override NoteHead #'color = #red\n\t\\beam #0 #1 c'8 \\staccato\n\t\\revert NoteHead #'color\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   staff[0].caster.toRest( )
   assert staff.format == "\\new Staff {\n\t\\override NoteHead #'color = #red\n\t\\beam #0 #1 r8 \\staccato\n\t\\revert NoteHead #'color\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
   \new Staff {
           \override NoteHead #'color = #red
           \beam #0 #1 r8 \staccato
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


def test_cast_05( ):
   '''Casting does *not* preserve Formatter instance;
      but casting *does* preserve Formatter before, after, left right.
      Works casting to chord.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].formatter.before.append(r"\override NoteHead #'color = #red")
   staff[0].formatter.after.append(r"\revert NoteHead #'color")
   staff[0].formatter.left.append(r'\beam #0 #1')
   staff[0].formatter.right.append(r'\staccato')
   assert staff.format == "\\new Staff {\n\t\\override NoteHead #'color = #red\n\t\\beam #0 #1 c'8 \\staccato\n\t\\revert NoteHead #'color\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   staff[0].caster.toChord( )
   assert staff.format == "\\new Staff {\n\t\\override NoteHead #'color = #red\n\t\\beam #0 #1 <c'>8 \\staccato\n\t\\revert NoteHead #'color\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
   \new Staff {
           \override NoteHead #'color = #red
           \beam #0 #1 <c'>8 \staccato
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
