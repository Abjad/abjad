from abjad import *
import py.test


def test_note_head_style_01( ):
   '''Notehead styles are handled just like all other grob overrides.
   NOTE: Abjad previous managed note_head style differently.
   This explains the presence of this extra test file.'''

   t = Note(1, (1, 4))
   t.note_head.style = 'cross'

   assert t.note_head.style == 'cross'
   assert t.format == "\\once \\override NoteHead #'style = #'cross\ncs'4"

   t.note_head.style = None
   assert t.note_head.format == "cs'"


def test_note_head_style_02( ):
   '''Notehead styles are handled just like all other grob overrides.'''

   t = Note(1, (1, 4))
   t.note_head.style = 'mystrangehead'

   assert t.note_head.style == 'mystrangehead'
   assert t.format == "\\once \\override NoteHead #'style = #'mystrangehead\ncs'4"

   t.note_head.style = None
   assert t.note_head.format == "cs'"


def test_note_head_style_03( ):
   '''Notehead style overrides are handled just like all other
   note_head grob overrides, even for note_heads in chords.'''

   t = Chord([1, 2, 3], (1, 4))
   t.note_heads[0].style = 'harmonic'

   r'''<
           \tweak #'style #'harmonic
           cs'
           d'
           ef'
   >4'''

   assert t.format == "<\n\t\\tweak #'style #'harmonic\n\tcs'\n\td'\n\tef'\n>4"


def test_note_head_style_04( ):
   '''Notehead shape style overrides are just normal grob overrides.'''

   t = Note(1, (1, 4))
   t.note_head.style = 'triangle'

   assert t.note_head.style == 'triangle'
   assert t.format == "\\once \\override NoteHead #'style = #'triangle\ncs'4"

   t.note_head.style = None
   assert t.format == "cs'4"


def test_note_head_style_05( ):
   '''Notehead solfege style overrides are just normal grob overrides.
   Modern versions of LilyPond now handles solfege overrides correctly.'''

   t = Note(1, (1, 4))
   t.note_head.style = 'do'

   assert t.note_head.style == 'do'
   assert t.format == "\\once \\override NoteHead #'style = #'do\ncs'4"

   t.note_head.style = None
   assert t.format == "cs'4"
