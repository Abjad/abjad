from abjad import *


def test_ArticulationsInterface_grob_handling_01( ):
   '''Articulations inteface handles the LilyPond Script grob.'''

   t = Note(0, (1, 4))
   t.articulations.append('staccato')
   #t.articulations.color = 'red'
   t.override.script.color = 'red'

   r'''
   \once \override Script #'color = #red
   c'4 -\staccato
   '''

   assert t.format == "\\once \\override Script #'color = #red\nc'4 -\\staccato"
