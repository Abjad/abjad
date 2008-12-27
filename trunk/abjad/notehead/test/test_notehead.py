from abjad import *
from py.test import raises


### TEST DEMO PUBLIC NOTEHEAD INTERFACE ###

def test_demo_public_notehead_interface_01( ):
   t = Note(13, (1, 4))
   assert repr(t.notehead) == "_NoteHead(cs'')"
   assert str(t.notehead) == "cs''"
   assert t.notehead.format == "cs''"
   #assert t.notehead.pitch == Pitch(13)
   assert t.notehead.pitch.number == 13

def test_demo_public_notehead_interface_02( ):
   t = Note(14, (1, 4))
   assert repr(t.notehead) == "_NoteHead(d'')"
   assert str(t.notehead) == "d''"
   assert t.notehead.format == "d''"
   #assert t.notehead.pitch == Pitch(14)
   assert t.notehead.pitch.number == 14


### TEST CHANGE NOTEHEAD PITCH ###

def test_change_notehead_pitch_01( ):
   t = Note(13, (1, 4))
   t.notehead.pitch = 14
   assert repr(t.notehead) == "_NoteHead(d'')"
   assert str(t.notehead) == "d''"
   assert t.notehead.format == "d''"
   #assert t.notehead.pitch == Pitch(14)
   assert t.notehead.pitch.number == 14

def test_change_notehead_pitch_02( ):
   t = Note(13, (1, 4))
   t.notehead.pitch = Pitch(14)
   assert repr(t.notehead) == "_NoteHead(d'')"
   assert str(t.notehead) == "d''"
   assert t.notehead.format == "d''"
   #assert t.notehead.pitch == Pitch(14)
   assert t.notehead.pitch.number == 14


### TEST REMOVE NOTEHEAD PITCH ###

def test_remove_notehead_pitch_01( ):
   t = Note(13, (1, 4))
   t.notehead.pitch = None
   assert t.notehead.pitch == None
   assert repr(t.notehead) == '_NoteHead( )'
   assert str(t.notehead) == ''
   assert raises(AssertionError, 't.notehead.format')

def test_remove_notehead_pitch_02( ):
   t = Note(14, (1, 4))
   t.notehead.pitch = None
   assert t.notehead.pitch == None
   assert repr(t.notehead) == '_NoteHead( )'
   assert str(t.notehead) == ''
   assert raises(AssertionError, 't.notehead.format')


### TEST SET NOTEHEAD STYLE ###

def test_set_notehead_style_01( ):
   '''Supported head styles are formated with NoteHead #'style override.'''
   t = Note(1, (1, 4))
   t.notehead.style = 'cross'
   assert t.notehead.style == 'cross'
   assert t.notehead.format == "\\once \\override NoteHead #'style = #'cross\ncs'"
   t.notehead.style = None
   assert t.notehead.format == "cs'"

def test_set_notehead_style_02( ):
   '''Unsupported noteheads are placed verbatim in front of note and 
      are assumed to be defined by user.'''
   t = Note(1, (1, 4))
   t.notehead.style = 'mystrangehead'
   assert t.notehead.style == 'mystrangehead'
   assert t.notehead.format == "\\mystrangehead\ncs'"
   t.notehead.style = None
   assert t.notehead.format == "cs'"

def test_set_notehead_style_03( ):
   '''Abjad supported head styles are translated to LilyPond style names.'''
   t = Note(1, (1, 4))
   t.notehead.style = 'triangle'
   assert t.notehead.style == 'triangle'
   assert t.notehead.format == "\\once \\override NoteHead #'style = #'do\ncs'"

def test_set_notehead_style_04( ):
   '''Notehead style formats correctly in Chords.'''
   t = Chord([1,2,3], (1, 4))
   t.noteheads[0].style = 'harmonic'
   assert t.format == "<\n\t\\tweak #'style #'harmonic\n\tcs'\n\td'\n\tef'\n>4"

   '''
   <
           \tweak #'style #'harmonic
           cs'
           d'
           ef'
   >4
   '''


### TEST SET NOTEHEAD TRANSPARENT ###

def test_set_notehead_transparent_01( ):
   t = Note(13, (1, 4))
   t.notehead.transparent = True
   assert t.notehead.transparent
   #assert t.notehead.format == "\\once \\override NoteHead #'transparent = ##t\ncs''"
   assert t.format == "\\once \\override NoteHead #'transparent = ##t\ncs''4"
   t.notehead.transparent = None
   #assert t.notehead.format == "cs''"
   assert t.format == "cs''4"
