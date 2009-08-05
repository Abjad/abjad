from abjad import *
from py.test import raises


## TEST DEMO PUBLIC CHORD INTERFACE ##

def test_demo_public_chord_interface_01( ):
   t = Chord([2, 3, 4], (1, 4))
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert str(t) == "<d' ef' e'>4"
   assert t.format == "<d' ef' e'>4"
   assert len(t) == 3
   assert len(t.noteheads) == 3
   assert len(t.pitches) == 3
   assert t.duration.written == t.duration.prolated == Rational(1, 4)


## TEST TWEAKED CHORD ##

def test_tweaked_chord_01( ):
   t = Chord([2, 3, 4], (1, 4))
   t[0].style = 'harmonic'
   assert t.format == "<\n\t\\tweak #'style #'harmonic\n\td'\n\tef'\n\te'\n>4"

def test_tweaked_chord_02( ):
   t = Chord([2, 3, 4], (1, 4))
   t[0].transparent = True
   assert t.format == "<\n\t\\tweak #'transparent ##t\n\td'\n\tef'\n\te'\n>4"


## TEST ONE-NOTE CHORD ##
## the point here is that one-note chords ##
## format as chords and not as single notes ##

def test_one_note_chord_01( ):
   t = Chord([0], (1, 4))
   assert repr(t) == "Chord(c', 4)"
   assert str(t) == "<c'>4"
   assert t.format == "<c'>4"
   assert len(t) == 1
   assert len(t.noteheads) == 1
   assert len(t.pitches) == 1

def test_one_note_chord_02( ):
   t = Chord([0.5], (1, 4))
   assert repr(t) == "Chord(cqs', 4)"
   assert str(t) == "<cqs'>4"
   assert t.format == "<cqs'>4"
   assert len(t) == 1
   assert len(t.noteheads) == 1
   assert len(t.pitches) == 1


## TEST CHORD FORMAT RIGHT ##

#def test_chord_format_right_01( ):
#   '''Untweaked chords format right.'''
#   t = Chord([2, 3, 4], (1, 4))
#   t.glissando.set = True
#   assert t.format == "<d' ef' e'>4 \\glissando"
#   '''
#   <d' ef' e'>4 \glissando
#   '''
#
#
#def test_chord_format_right_02( ):
#   '''Tweaked chords format right.'''
#   t = Chord([2, 3, 4], (1, 4))
#   t[0].color = 'red'
#   t.glissando.set = True
#   assert t.format == "<\n\t\\tweak #'color #red\n\td'\n\tef'\n\te'\n>4 \\glissando"
#   '''
#   <
#           \tweak #'color #red
#           d'
#           ef'
#           e'
#   >4 \glissando
#   '''


## TEST MANAGED ATTRIBUTES ##

def test_chord_set_pitches_01( ):
   '''Chord pitches can be set as list or tuple of numbers.'''
   t = Chord([], (1,4))
   t.pitches = [4, 3, 2]
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"
   t.pitches = (4, 3, 2)
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"


def test_chord_set_pitches_02( ):
   '''Chord pitches can be set as list or tuple of Pitches.'''
   t = Chord([], (1,4))
   t.pitches = [Pitch(4), Pitch(3), Pitch(2)]
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"


def test_chord_set_pitches_03( ):
   '''Chord pitches can be set as list or tuple of both numbers and Pitches.'''
   t = Chord([], (1,4))
   t.pitches = [4, Pitch(3), Pitch(2)]
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"


def test_chord_set_noteheads_01( ):
   '''Chord noteheads can be set as list or tuple of numbers.'''
   t = Chord([], (1,4))
   t.noteheads = [4, 3, 2]
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"
   

def test_chord_set_noteheads_02( ):
   '''Chord noteheads can be set as list or tuple of Pitches.'''
   t = Chord([], (1,4))
   t.noteheads = [Pitch(4), Pitch(3), Pitch(2)]
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"


def test_chord_set_noteheads_03( ):
   '''Chord noteheads can be set as list or tuple of both numbers and Pitches.'''
   t = Chord([], (1,4))
   t.noteheads = [Pitch(4), 3, Pitch(2)]
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"


## TEST CHORD SPECIAL METHODS ##

def test_chord_setitem_01( ):
   '''Noteheads can be replaced. Noteheads are sorted.'''
   t = Chord([2, 4], (1,4))
   t[0] = Pitch(5)
   assert repr(t) == "Chord(e' f', 4)"
   assert t.format == "<e' f'>4"
   t[0] = 7
   assert repr(t) == "Chord(f' g', 4)"
   assert t.format == "<f' g'>4"
