from abjad import *


def test_Chord___init___01():
    '''Init empty chord.
    '''

    t = Chord([], (1, 4))
    assert t.lilypond_format == "<>4"


def test_Chord___init___02():
    '''Init chord with numbers.
    '''

    t = Chord([2, 4, 5], (1, 4))
    assert t.lilypond_format == "<d' e' f'>4"


def test_Chord___init___03():
    '''Init chord with pitch tokens.
    '''

    t = Chord([('ds', 4), ('ef', 4)], (1, 4))
    assert t.lilypond_format == "<ds' ef'>4"


def test_Chord___init___04():
    '''Init chord with pitches.
    '''

    t = Chord([pitchtools.NamedChromaticPitch('ds', 4), pitchtools.NamedChromaticPitch('ef', 4)], (1, 4))
    assert t.lilypond_format == "<ds' ef'>4"


def test_Chord___init___05():
    '''Init chord with pitch token and pitch together.
    '''

    t = Chord([2, ('ef', 4), pitchtools.NamedChromaticPitch(4)], (1, 4))
    assert t.lilypond_format == "<d' ef' e'>4"


def test_Chord___init___06():
    '''Init chord with list of pitch names.
    '''

    t = Chord(["d'", "ef'", "e'"], (1, 4))
    assert t.lilypond_format == "<d' ef' e'>4"


def test_Chord___init___07():
    '''Init chord with LilyPond input string.
    '''

    t = Chord("<d' ef' e'>4")
    assert t.lilypond_format == "<d' ef' e'>4"


def test_Chord___init___08():
    '''Init chord from skip.
    '''

    s = skiptools.Skip((1, 8))
    d = s.written_duration
    c = Chord(s)
    assert isinstance(c, Chord)
    assert dir(s) == dir(skiptools.Skip((1, 4)))
    assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
    assert c._parent is None
    assert c.written_duration == d


def test_Chord___init___09():
    '''Init chord from skip.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), skiptools.Skip((1, 8)) * 3)
    d = t[0].written_duration
    chord = Chord(t[0])
    assert isinstance(t[0], skiptools.Skip)
    assert isinstance(chord, Chord)
    assert t[0]._parent is t
    assert t[0].written_duration == d
    assert chord._parent is None


def test_Chord___init___10():
    '''Init chord from containerized skip.
    '''

    v = Voice(skiptools.Skip((1, 8)) * 3)
    d = v[0].written_duration
    chord = Chord(v[0])
    assert isinstance(v[0], skiptools.Skip)
    assert isinstance(chord, Chord)
    assert v[0]._parent is v
    assert v[0].written_duration == d
    assert chord._parent is None


def test_Chord___init___11():
    '''Init chord from beamed skip.
    '''

    t = Staff([Note(0, (1, 8)), skiptools.Skip((1, 8)), Note(0, (1, 8))])
    beamtools.BeamSpanner(t[:])
    chord = Chord(t[1])
    assert isinstance(t[1], skiptools.Skip)
    assert isinstance(chord, Chord)
    assert t[1]._parent is t


def test_Chord___init___12():
    '''Init chord from rest.
    '''

    r = Rest((1, 8))
    d = r.written_duration
    c = Chord(r)
    assert isinstance(c, Chord)
    assert dir(r) == dir(Rest((1, 4)))
    assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
    assert c._parent is None
    assert c.written_duration == d


def test_Chord___init___13():
    '''Init chord from tupletized rest.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), Rest((1, 8)) * 3)
    d = t[0].written_duration
    chord = Chord(t[0])
    assert isinstance(t[0], Rest)
    assert isinstance(chord, Chord)
    assert t[0]._parent is t
    assert t[0].written_duration == d
    assert chord._parent is None


def test_Chord___init___14():
    '''Init chord from rest.
    '''

    t = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
    beamtools.BeamSpanner(t[:])
    chord = Chord(t[1])
    assert isinstance(t[1], Rest)
    assert isinstance(chord, Chord)
    assert t[1]._parent is t
    assert chord._parent is None


def test_Chord___init___15():
    '''Init chord from note.
    '''

    n = Note(2, (1, 8))
    h, p, d = n.note_head, n.written_pitch, n.written_duration
    c = Chord(n)
    assert isinstance(c, Chord)
    assert dir(n) == dir(Note("c'4"))
    assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
    assert c.lilypond_format == "<d'>8"
    assert c._parent is None
    assert c.note_heads[0] is not h
    assert c.written_pitches[0] == p
    assert c.written_duration == d


def test_Chord___init___16():
    '''Init chord from tupletized note.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3)
    h, p, d = t[0].note_head, t[0].written_pitch, t[0].written_duration
    chord = Chord(t[0])
    assert isinstance(t[0], Note)
    assert isinstance(chord, Chord)
    assert chord.lilypond_format == "<c'>8"
    assert t[0]._parent is t
    assert chord.note_heads[0] is not h
    assert chord.written_pitches[0] == p
    assert chord.written_duration == d


def test_Chord___init___17():
    '''Init chord from beamed note.
    '''

    t = Staff(Note(0, (1, 8)) * 3)
    beamtools.BeamSpanner(t[:])
    chord = Chord(t[0])
    assert isinstance(t[0], Note)
    assert isinstance(chord, Chord)
    assert t[0]._parent is t


def test_Chord___init___18():
    '''Init empty chord from LilyPond input string.
    '''

    chord = Chord('<>8.')
    assert isinstance(chord, Chord)
    assert len(chord) == 0


def test_Chord___init___19():
    '''Init with forced and cautionary accidentals.
    '''

    chord = Chord('<c!? e? g! b>4')
    assert chord.lilypond_format == '<c!? e? g! b>4'


def test_Chord___init___20():
    '''Init from Note with forced and cautionary accidentals.
    '''

    note = Note("c'!?4")
    chord = Chord(note)
    assert chord.lilypond_format == "<c'!?>4"
