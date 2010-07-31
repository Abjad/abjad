from abjad import *
from py.test import raises


## TEST DEMO PUBLIC CHORD INTERFACE ##

def test_Chord_01( ):
   t = Chord([2, 3, 4], (1, 4))
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert str(t) == "<d' ef' e'>4"
   assert t.format == "<d' ef' e'>4"
   assert len(t) == 3
   assert len(t.note_heads) == 3
   assert len(t.pitches) == 3
   assert t.duration.written == t.duration.prolated == Rational(1, 4)


## TEST TWEAKED CHORD ##

def test_Chord_02( ):
   t = Chord([2, 3, 4], (1, 4))
   t[0].style = 'harmonic'
   assert t.format == "<\n\t\\tweak #'style #'harmonic\n\td'\n\tef'\n\te'\n>4"

def test_Chord_03( ):
   t = Chord([2, 3, 4], (1, 4))
   t[0].transparent = True
   assert t.format == "<\n\t\\tweak #'transparent ##t\n\td'\n\tef'\n\te'\n>4"


## TEST ONE-NOTE CHORD ##
## the point here is that one-note chords ##
## format as chords and not as single notes ##

def test_Chord_04( ):
   t = Chord([0], (1, 4))
   assert repr(t) == "Chord(c', 4)"
   assert str(t) == "<c'>4"
   assert t.format == "<c'>4"
   assert len(t) == 1
   assert len(t.note_heads) == 1
   assert len(t.pitches) == 1

def test_Chord_05( ):
   t = Chord([0.5], (1, 4))
   assert repr(t) == "Chord(cqs', 4)"
   assert str(t) == "<cqs'>4"
   assert t.format == "<cqs'>4"
   assert len(t) == 1
   assert len(t.note_heads) == 1
   assert len(t.pitches) == 1


## TEST CHORD FORMAT RIGHT ##

#def test_Chord_06( ):
#   '''Untweaked chords format right.'''
#   t = Chord([2, 3, 4], (1, 4))
#   t.glissando.set = True
#   assert t.format == "<d' ef' e'>4 \\glissando"
#   '''
#   <d' ef' e'>4 \glissando
#   '''
#
#
#def test_Chord_07( ):
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

def test_Chord_08( ):
   '''Chord pitches can be set as list or tuple of numbers.'''
   t = Chord([], (1,4))
   t.pitches = [4, 3, 2]
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"
   t.pitches = (4, 3, 2)
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"


def test_Chord_09( ):
   '''Chord pitches can be set as list or tuple of Pitches.'''
   t = Chord([], (1,4))
   t.pitches = [Pitch(4), Pitch(3), Pitch(2)]
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"


def test_Chord_10( ):
   '''Chord pitches can be set as list or tuple of both numbers and Pitches.'''
   t = Chord([], (1,4))
   t.pitches = [4, Pitch(3), Pitch(2)]
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"


def test_Chord_11( ):
   '''Chord note_heads can be set as list or tuple of numbers.'''
   t = Chord([], (1,4))
   t.note_heads = [4, 3, 2]
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"
   

def test_Chord_12( ):
   '''Chord note_heads can be set as list or tuple of Pitches.'''
   t = Chord([], (1,4))
   t.note_heads = [Pitch(4), Pitch(3), Pitch(2)]
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"


def test_Chord_13( ):
   '''Chord note_heads can be set as list or tuple of both numbers and Pitches.'''
   t = Chord([], (1,4))
   t.note_heads = [Pitch(4), 3, Pitch(2)]
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"


## TEST CHORD SPECIAL METHODS ##

def test_Chord_14( ):
   '''Noteheads can be replaced. Noteheads are sorted.'''
   t = Chord([2, 4], (1,4))
   t[0] = Pitch(5)
   assert repr(t) == "Chord(e' f', 4)"
   assert t.format == "<e' f'>4"
   t[0] = 7
   assert repr(t) == "Chord(f' g', 4)"
   assert t.format == "<f' g'>4"
