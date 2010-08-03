from abjad import *


def test_Chord___init____01( ):
   '''Chord initializes empty.'''
   t = Chord([ ], (1, 4))
   assert repr(t) == "Chord(, 4)"
   assert t.format == "<>4"


def test_Chord___init____02( ):
   '''Chord initializes with numeric pitch token input.'''
   t = Chord([2, 4, 5], (1, 4))
   assert repr(t) == "Chord(d' e' f', 4)"
   assert t.format == "<d' e' f'>4"


def test_Chord___init____03( ):
   '''Chord initializes with pair pitch token input.'''
   t = Chord([('ds', 4), ('ef', 4)], (1, 4))
   assert repr(t) == "Chord(ds' ef', 4)"
   assert t.format == "<ds' ef'>4"


def test_Chord___init____04( ):
   '''Chord initializes with pitch instance pitch token input.'''
   t = Chord([Pitch('ds', 4), Pitch('ef', 4)], (1, 4))
   assert repr(t) == "Chord(ds' ef', 4)"
   assert t.format == "<ds' ef'>4"


def test_Chord___init____05( ):
   '''Chord initializes with mixed pitch token input.'''
   t = Chord([2, ('ef', 4), Pitch(4)], (1, 4))
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"


def test_Chord___init____06( ):
   '''Init chord with LilyPond-style pitch name strings.'''
   t = Chord(["d'", "ef'", "e'"], (1, 4))
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"


def test_Chord___init____07( ):
   '''Init chord with complete LilyPond-style chord string.'''
   t = Chord("<d' ef' e'>4")
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert t.format == "<d' ef' e'>4"
