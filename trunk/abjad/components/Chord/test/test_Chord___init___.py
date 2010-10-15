from abjad import *


def test_Chord___init____01( ):
   '''Chord initializes empty.'''
   t = Chord([ ], (1, 4))
   assert t.format == "<>4"


def test_Chord___init____02( ):
   '''Chord initializes with numeric pitch token input.'''
   t = Chord([2, 4, 5], (1, 4))
   assert t.format == "<d' e' f'>4"


def test_Chord___init____03( ):
   '''Chord initializes with pair pitch token input.'''
   t = Chord([('ds', 4), ('ef', 4)], (1, 4))
   assert t.format == "<ds' ef'>4"


def test_Chord___init____04( ):
   '''Chord initializes with pitch instance pitch token input.'''
   t = Chord([pitchtools.NamedChromaticPitch('ds', 4), pitchtools.NamedChromaticPitch('ef', 4)], (1, 4))
   assert t.format == "<ds' ef'>4"


def test_Chord___init____05( ):
   '''Chord initializes with mixed pitch token input.'''
   t = Chord([2, ('ef', 4), pitchtools.NamedChromaticPitch(4)], (1, 4))
   assert t.format == "<d' ef' e'>4"


def test_Chord___init____06( ):
   '''Init chord with LilyPond-style pitch name strings.'''
   t = Chord(["d'", "ef'", "e'"], (1, 4))
   assert t.format == "<d' ef' e'>4"


def test_Chord___init____07( ):
   '''Init chord with complete LilyPond-style chord string.'''
   t = Chord("<d' ef' e'>4")
   assert t.format == "<d' ef' e'>4"


def test_Chord___init____08( ):
   '''Cast skip as chord.'''
   s = skiptools.Skip((1, 8))
   d = s.duration.written
   c = Chord(s)
   assert isinstance(c, Chord)
   assert dir(s) == dir(skiptools.Skip((1, 4)))
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert c._parentage.parent is None
   assert c.duration.written == d


def test_Chord___init____09( ):
   '''Init chord from skip.
   '''

   t = tuplettools.FixedDurationTuplet((2, 8), skiptools.Skip((1, 8)) * 3)
   d = t[0].duration.written
   chord = Chord(t[0])
   assert isinstance(t[0], skiptools.Skip)
   assert isinstance(chord, Chord)
   assert t[0]._parentage.parent is t
   assert t[0].duration.written == d
   assert chord._parentage.parent is None


def test_Chord___init____10( ):
   '''Init chord from containerized skip.
   '''

   v = Voice(skiptools.Skip((1, 8)) * 3)
   d = v[0].duration.written
   chord = Chord(v[0])
   assert isinstance(v[0], skiptools.Skip)
   assert isinstance(chord, Chord)
   assert v[0]._parentage.parent is v
   assert v[0].duration.written == d
   assert chord._parentage.parent is None


def test_Chord___init____11( ):
   '''Init chord from beamed skip.
   '''

   t = Staff([Note(0, (1, 8)), skiptools.Skip((1, 8)), Note(0, (1, 8))])
   spannertools.BeamSpanner(t[:])
   chord = Chord(t[1])
   assert isinstance(t[1], skiptools.Skip)
   assert isinstance(chord, Chord)
   assert t[1]._parentage.parent is t
