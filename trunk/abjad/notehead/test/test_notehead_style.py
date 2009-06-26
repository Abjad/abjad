from abjad import *
import py.test


def test_notehead_style_01( ):
   '''Notehead styles are handled just like all other grob overrides.
   NOTE: Abjad previous managed notehead style differently.
   This explains the presence of this extra test file.'''

   t = Note(1, (1, 4))
   t.notehead.style = 'cross'

   assert t.notehead.style == 'cross'
   assert t.format == "\\once \\override NoteHead #'style = #'cross\ncs'4"

   t.notehead.style = None
   assert t.notehead.format == "cs'"


def test_notehead_style_02( ):
   '''Notehead styles are handled just like all other grob overrides.'''

   t = Note(1, (1, 4))
   t.notehead.style = 'mystrangehead'

   assert t.notehead.style == 'mystrangehead'
   assert t.format == "\\once \\override NoteHead #'style = #'mystrangehead\ncs'4"

   t.notehead.style = None
   assert t.notehead.format == "cs'"


def test_notehead_style_03( ):
   '''Notehead style overrides are handled just like all other
   notehead grob overrides, even for noteheads in chords.'''

   t = Chord([1, 2, 3], (1, 4))
   t.noteheads[0].style = 'harmonic'

   r'''<
           \tweak #'style #'harmonic
           cs'
           d'
           ef'
   >4'''

   assert t.format == "<\n\t\\tweak #'style #'harmonic\n\tcs'\n\td'\n\tef'\n>4"


def test_notehead_style_04( ):
   '''Notehead shape style overrides are just normal grob overrides.'''

   t = Note(1, (1, 4))
   t.notehead.style = 'triangle'

   assert t.notehead.style == 'triangle'
   assert t.format == "\\once \\override NoteHead #'style = #'triangle\ncs'4"

   t.notehead.style = None
   assert t.format == "cs'4"


def test_notehead_style_05( ):
   '''Notehead solfege style overrides are just normal grob overrides.
   Modern versions of LilyPond now handles solfege overrides correctly.'''

   t = Note(1, (1, 4))
   t.notehead.style = 'do'

   assert t.notehead.style == 'do'
   assert t.format == "\\once \\override NoteHead #'style = #'do\ncs'4"

   t.notehead.style = None
   assert t.format == "cs'4"
