from abjad import *
from py.test import raises


### TEST DEMO PUBLIC NOTEHEAD INTERFACE ###

def test_demo_public_notehead_interface_01( ):
   t = Note(13, (1, 4))
   assert repr(t.notehead) == "_NoteHead(cs'')"
   assert str(t.notehead) == "cs''"
   assert t.notehead.format == "cs''"
   assert t.notehead.pitch == Pitch(13)

def test_demo_public_notehead_interface_02( ):
   t = Note(14, (1, 4))
   assert repr(t.notehead) == "_NoteHead(d'')"
   assert str(t.notehead) == "d''"
   assert t.notehead.format == "d''"
   assert t.notehead.pitch == Pitch(14)


### TEST CHANGE NOTEHEAD PITCH ###

def test_change_notehead_pitch_01( ):
   t = Note(13, (1, 4))
   t.notehead.pitch = 14
   assert repr(t.notehead) == "_NoteHead(d'')"
   assert str(t.notehead) == "d''"
   assert t.notehead.format == "d''"
   assert t.notehead.pitch == Pitch(14)

def test_change_notehead_pitch_02( ):
   t = Note(13, (1, 4))
   t.notehead.pitch = Pitch(14)
   assert repr(t.notehead) == "_NoteHead(d'')"
   assert str(t.notehead) == "d''"
   assert t.notehead.format == "d''"
   assert t.notehead.pitch == Pitch(14)


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
   t = Note(13, (1, 4))
   t.notehead.style = 'harmonic'
   assert t.notehead.style == 'harmonic'
   assert t.notehead.format == "\\once \\override NoteHead #'style = #'harmonic\ncs''"
   t.notehead.style = None
   assert t.notehead.format == "cs''"


### TEST SET NOTEHEAD TRANSPARENT ###

def test_set_notehead_transparent_01( ):
   t = Note(13, (1, 4))
   t.notehead.transparent = True
   assert t.notehead.transparent
   assert t.notehead.format == "\\once \\override NoteHead #'transparent = ##t\ncs''"
   t.notehead.transparent = None
   assert t.notehead.format == "cs''"
