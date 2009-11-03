from abjad import *


def test_chord_public_methods_01( ):
   '''Chords can be appended note_heads. Noteheads are sorted.'''
   t = Chord([2, 4], (1,4))
   t.append(Pitch(3))
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"
   t.append(0)
   assert repr(t) == "Chord(c' d' ef' e', 4)"
   assert t.format == "<c' d' ef' e'>4"


def test_chord_public_methods_02( ):
   '''Chords can be copied. Python ids differ.'''
   t = Chord([2, 4], (1, 4))
   new = clone.fracture([t])[0]
   assert isinstance(new, Chord)
   assert len(t) == len(new)
   assert t.pitches[0].number == new.pitches[0].number
   assert t.pitches[1].number == new.pitches[1].number
   assert id(t) != id(new)


def test_chord_public_methods_03( ):
   '''Chords can be extended. Noteheads are sorted.'''
   t = Chord([2, 4], (1,4))
   t.extend([Pitch(3)])
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"
   t.extend([0, 1])
   assert repr(t) == "Chord(c' cs' d' ef' e', 4)"
   assert t.format == "<c' cs' d' ef' e'>4"


def test_chord_public_methods_04( ):
   '''Lone chords can pop note_heads by index.'''
   t = Chord([2, 4], (1, 4))
   note_head = t.pop( )
   assert note_head.pitch.number == 4
   assert len(t) == 1
   assert t.pitches[0].number == 2
   

def test_chord_public_methods_05( ):
   '''Lone chords can remove note_heads by reference.'''
   t = Chord([2, 4], (1, 4))
   t.remove(t[0])
   assert len(t) == 1
   assert t.pitches[0].number == 4


def test_chord_public_methods_06( ):
   '''Lone chords can remove note_heads by reference.'''
   t = Chord([2, 4], (1, 4))
   t.remove(t[1])
   assert len(t) == 1
   assert t.pitches[0].number == 2
