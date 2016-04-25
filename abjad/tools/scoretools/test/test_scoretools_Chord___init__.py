# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Chord___init___01():
    r'''Initialize empty chord.
    '''

    chord = Chord([], (1, 4))
    assert format(chord) == "<>4"


def test_scoretools_Chord___init___02():
    r'''Initialize chord with pitch numbers.
    '''

    chord = Chord([2, 4, 5], (1, 4))
    assert format(chord) == "<d' e' f'>4"


def test_scoretools_Chord___init___03():
    r'''Initialize chord with pitch tokens.
    '''

    chord = Chord([('ds', 4), ('ef', 4)], (1, 4))
    assert format(chord) == "<ds' ef'>4"


def test_scoretools_Chord___init___04():
    r'''Initialize chord with pitches.
    '''

    pitches = []
    pitches.append(NamedPitch('ds', 4))
    pitches.append(NamedPitch('ef', 4))
    chord = Chord(pitches, (1, 4))
    assert format(chord) == "<ds' ef'>4"


def test_scoretools_Chord___init___05():
    r'''Initialize chord with pitches and pitch numbers together.
    '''

    pitches = [2, ('ef', 4), NamedPitch(4)]
    chord = Chord(pitches, (1, 4))
    assert format(chord) == "<d' ef' e'>4"


def test_scoretools_Chord___init___06():
    r'''Initialize chord with list of pitch names.
    '''

    pitches = ["d'", "ef'", "e'"]
    chord = Chord(pitches, (1, 4))
    assert format(chord) == "<d' ef' e'>4"


def test_scoretools_Chord___init___07():
    r'''Initialize chord with LilyPond input string.
    '''

    chord = Chord("<d' ef' e'>4")
    assert format(chord) == "<d' ef' e'>4"


def test_scoretools_Chord___init___08():
    r'''Initialize chord from skip.
    '''

    skip = scoretools.Skip('s8')
    chord = Chord(skip)

    assert format(skip) == 's8'
    assert format(chord) == '<>8'

    assert inspect_(skip).is_well_formed()
    assert inspect_(chord).is_well_formed()


def test_scoretools_Chord___init___09():
    r'''Initialize chord from tupletized skip.
    '''

    tuplet = Tuplet((2, 3), 's8 s8 s8')
    chord = Chord(tuplet[0])

    assert format(chord) == '<>8'
    assert inspect_(chord).get_parentage().parent is None
    assert inspect_(chord).is_well_formed()


def test_scoretools_Chord___init___10():
    r'''Initialize chord from containerized skip.
    '''

    tuplet = Voice('s8 s8 s8')
    chord = Chord(tuplet[0])

    assert format(chord) == '<>8'
    assert inspect_(chord).get_parentage().parent is None
    assert inspect_(chord).is_well_formed()



def test_scoretools_Chord___init___11():
    r'''Initialize chord from beamed skip.
    '''

    staff = Staff("c'8 [ s8 c'8 ]")
    chord = Chord(staff[1])

    assert format(chord) == '<>8'
    assert inspect_(chord).get_parentage().parent is None
    assert inspect_(chord).is_well_formed()


def test_scoretools_Chord___init___12():
    r'''Initialize chord from rest.
    '''

    rest = Rest('r8')
    chord = Chord(rest)

    assert format(rest) == 'r8'
    assert format(chord) == '<>8'
    assert inspect_(rest).is_well_formed()
    assert inspect_(chord).is_well_formed()


def test_scoretools_Chord___init___13():
    r'''Initialize chord from tupletized rest.
    '''

    tuplet = Tuplet((2, 3), 'r8 r8 r8')
    chord = Chord(tuplet[1])

    assert format(chord) == '<>8'
    assert inspect_(chord).is_well_formed()
    assert inspect_(chord).get_parentage().parent is None


def test_scoretools_Chord___init___14():
    r'''Initialize chord from note.
    '''

    note = Note("d'8")
    chord = Chord(note)

    assert format(note) == "d'8"
    assert format(chord) == "<d'>8"
    assert inspect_(note).is_well_formed()
    assert inspect_(chord).is_well_formed()


def test_scoretools_Chord___init___15():
    r'''Initialize chord from tupletized note.
    '''

    tuplet = Tuplet((2, 3), "c'8 c'8 c'8")
    chord = Chord(tuplet[1])

    assert format(chord) == "<c'>8"
    assert inspect_(chord).is_well_formed()
    assert inspect_(chord).get_parentage().parent is None


def test_scoretools_Chord___init___16():
    r'''Initialize chord from spanned note.
    '''

    staff = Staff("c'8 ( d'8 e'8 f'8 )")
    chord = Chord(staff[1])

    assert format(chord) == "<d'>8"
    assert inspect_(chord).is_well_formed()
    assert inspect_(chord).get_parentage().parent is None


def test_scoretools_Chord___init___17():
    r'''Initialize empty chord from LilyPond input string.
    '''

    chord = Chord('<>8.')

    assert format(chord) == '<>8.'
    assert not len(chord.note_heads)


def test_scoretools_Chord___init___18():
    r'''Initialize chord from LilyPond input string with forced and
    cautionary accidentals.
    '''

    chord = Chord('<c!? e? g! b>4')

    assert format(chord) == '<c!? e? g! b>4'


def test_scoretools_Chord___init___19():
    r'''Initialize chord from note with forced and cautionary accidentals.
    '''

    note = Note("c'!?4")
    chord = Chord(note)

    assert format(chord) == "<c'!?>4"


def test_scoretools_Chord___init___20():
    r'''Initialize chord from other chord.
    '''

    chord_1 = Chord("<c' e' g' bf'>4")
    chord_2 = Chord(chord_1, Duration(1, 8))

    assert format(chord_2) == "<c' e' g' bf'>8"


def test_scoretools_Chord___init___21():
    r'''Initialize chord with drum pitches.
    '''

    chord = Chord("<sn? bd! tamb>4")

    assert format(chord) == '<bassdrum! snare? tambourine>4'
