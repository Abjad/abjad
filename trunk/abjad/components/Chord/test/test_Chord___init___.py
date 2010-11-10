from abjad import *


def test_Chord___init____01( ):
   '''Init empty chord.
   '''

   t = Chord([ ], (1, 4))
   assert t.format == "<>4"


def test_Chord___init____02( ):
   '''Init chord with numbers.
   '''

   t = Chord([2, 4, 5], (1, 4))
   assert t.format == "<d' e' f'>4"


def test_Chord___init____03( ):
   '''Init chord with pitch tokens.
   '''

   t = Chord([('ds', 4), ('ef', 4)], (1, 4))
   assert t.format == "<ds' ef'>4"


def test_Chord___init____04( ):
   '''Init chord with pitches.
   '''

   t = Chord([pitchtools.NamedChromaticPitch('ds', 4), pitchtools.NamedChromaticPitch('ef', 4)], (1, 4))
   assert t.format == "<ds' ef'>4"


def test_Chord___init____05( ):
   '''Init chord with pitch token and pitch together.
   '''

   t = Chord([2, ('ef', 4), pitchtools.NamedChromaticPitch(4)], (1, 4))
   assert t.format == "<d' ef' e'>4"


def test_Chord___init____06( ):
   '''Init chord with list of pitch names.
   '''

   t = Chord(["d'", "ef'", "e'"], (1, 4))
   assert t.format == "<d' ef' e'>4"


def test_Chord___init____07( ):
   '''Init chord with LilyPond input string.
   '''

   t = Chord("<d' ef' e'>4")
   assert t.format == "<d' ef' e'>4"


def test_Chord___init____08( ):
   '''Init chord from skip.
   '''

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


def test_Chord___init____12( ):
   '''Init chord from rest.
   '''

   r = Rest((1, 8))
   d = r.duration.written
   c = Chord(r)
   assert isinstance(c, Chord)
   assert dir(r) == dir(Rest((1, 4)))
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert c._parentage.parent is None
   assert c.duration.written == d


def test_Chord___init____13( ):
   '''Init chord from tupletized rest.
   '''

   t = tuplettools.FixedDurationTuplet((2, 8), Rest((1, 8)) * 3)
   d = t[0].duration.written
   chord = Chord(t[0])
   assert isinstance(t[0], Rest)
   assert isinstance(chord, Chord)
   assert t[0]._parentage.parent is t
   assert t[0].duration.written == d
   assert chord._parentage.parent is None


def test_Chord___init____14( ):
   '''Init chord from rest.
   '''

   t = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
   spannertools.BeamSpanner(t[:])
   chord = Chord(t[1])
   assert isinstance(t[1], Rest)
   assert isinstance(chord, Chord)
   assert t[1]._parentage.parent is t
   assert chord._parentage.parent is None


def test_Chord___init____15( ):
   '''Init chord from note.
   '''

   n = Note(2, (1, 8))
   h, p, d = n.note_head, n.pitch, n.duration.written
   c = Chord(n)
   assert isinstance(c, Chord)
   assert dir(n) == dir(Note(0, (1, 4)))
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert c.format == "<d'>8"
   assert c._parentage.parent is None
   assert c.note_heads[0] is not h
   assert c.pitches[0] == p
   assert c.duration.written == d


def test_Chord___init____16( ):
   '''Init chord from tupletized note.
   '''

   t = tuplettools.FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   h, p, d = t[0].note_head, t[0].pitch, t[0].duration.written
   chord = Chord(t[0])
   assert isinstance(t[0], Note)
   assert isinstance(chord, Chord)
   assert chord.format == "<c'>8"
   assert t[0]._parentage.parent is t
   assert chord.note_heads[0] is not h
   assert chord.pitches[0] == p
   assert chord.duration.written == d


def test_Chord___init____17( ):
   '''Init chord from beamed note.
   '''

   t = Staff(Note(0, (1, 8)) * 3)
   spannertools.BeamSpanner(t[:])
   chord = Chord(t[0])
   assert isinstance(t[0], Note)
   assert isinstance(chord, Chord)
   assert t[0]._parentage.parent is t


def test_Chord___init____18( ):
   '''Init empty chord from LilyPond input string.
   '''

   chord = Chord('<>8.')
   assert isinstance(chord, Chord)
   assert len(chord) == 0
