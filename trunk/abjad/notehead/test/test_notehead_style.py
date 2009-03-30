from abjad import *
import py.test


def test_notehead_style_01( ):
   '''Supported head styles are formated with NoteHead #'style override.'''

   t = Note(1, (1, 4))
   t.notehead.style = 'cross'
   assert t.notehead.style == 'cross'
   assert t.notehead.format == "\\once \\override NoteHead #'style = #'cross\ncs'"
   t.notehead.style = None
   assert t.notehead.format == "cs'"


def test_notehead_style_02( ):
   '''Unsupported noteheads are placed verbatim in front of note and 
      are assumed to be defined by user.'''

   t = Note(1, (1, 4))
   t.notehead.style = 'mystrangehead'
   assert t.notehead.style == 'mystrangehead'
   assert t.notehead.format == "\\mystrangehead\ncs'"
   t.notehead.style = None
   assert t.notehead.format == "cs'"


def test_notehead_style_03( ):
   '''Abjad supported head styles are translated to LilyPond style names.'''

   t = Note(1, (1, 4))
   t.notehead.style = 'triangle'
   assert t.notehead.style == 'triangle'
   assert t.notehead.format == "\\once \\override NoteHead #'style = #'do\ncs'"


def test_notehead_style_04( ):
   '''Notehead style formats correctly in Chords.'''

   t = Chord([1,2,3], (1, 4))
   t.noteheads[0].style = 'harmonic'

   r'''<
           \tweak #'style #'harmonic
           cs'
           d'
           ef'
   >4'''

   assert t.format == "<\n\t\\tweak #'style #'harmonic\n\tcs'\n\td'\n\tef'\n>4"
