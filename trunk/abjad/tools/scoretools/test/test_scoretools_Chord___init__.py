# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Chord___init___01():
    r'''Initialize empty chord.
    '''

    chord = Chord([], (1, 4))
    assert chord.lilypond_format == "<>4"


def test_scoretools_Chord___init___02():
    r'''Initialize chord with pitch numbers.
    '''

    chord = Chord([2, 4, 5], (1, 4))
    assert chord.lilypond_format == "<d' e' f'>4"


def test_scoretools_Chord___init___03():
    r'''Initialize chord with pitch tokens.
    '''

    chord = Chord([('ds', 4), ('ef', 4)], (1, 4))
    assert chord.lilypond_format == "<ds' ef'>4"


def test_scoretools_Chord___init___04():
    r'''Initialize chord with pitches.
    '''

    pitches = []
    pitches.append(pitchtools.NamedPitch('ds', 4))
    pitches.append(pitchtools.NamedPitch('ef', 4))
    chord = Chord(pitches, (1, 4))
    assert chord.lilypond_format == "<ds' ef'>4"


def test_scoretools_Chord___init___05():
    r'''Initialize chord with pitches and pitch numbers together.
    '''

    pitches = [2, ('ef', 4), pitchtools.NamedPitch(4)]
    chord = Chord(pitches, (1, 4))
    assert chord.lilypond_format == "<d' ef' e'>4"


def test_scoretools_Chord___init___06():
    r'''Initialize chord with list of pitch names.
    '''

    pitches = ["d'", "ef'", "e'"]
    chord = Chord(pitches, (1, 4))
    assert chord.lilypond_format == "<d' ef' e'>4"


def test_scoretools_Chord___init___07():
    r'''Initialize chord with LilyPond input string.
    '''

    chord = Chord("<d' ef' e'>4")
    assert chord.lilypond_format == "<d' ef' e'>4"


def test_scoretools_Chord___init___08():
    r'''Initialize chord from skip.
    '''

    skip = skiptools.Skip('s8')
    chord = Chord(skip)

    assert skip.lilypond_format == 's8'
    assert chord.lilypond_format == '<>8'

    assert inspect(skip).is_well_formed()
    assert inspect(chord).is_well_formed()


def test_scoretools_Chord___init___09():
    r'''Initialize chord from tupletized skip.
    '''

    tuplet = Tuplet((2, 3), 's8 s8 s8')
    chord = Chord(tuplet[0])

    assert chord.lilypond_format == '<>8'
    assert inspect(chord).get_parentage().parent is None
    assert inspect(chord).is_well_formed()


def test_scoretools_Chord___init___10():
    r'''Initialize chord from containerized skip.
    '''

    tuplet = Voice('s8 s8 s8')
    chord = Chord(tuplet[0])

    assert chord.lilypond_format == '<>8'
    assert inspect(chord).get_parentage().parent is None
    assert inspect(chord).is_well_formed()



def test_scoretools_Chord___init___11():
    r'''Initialize chord from beamed skip.
    '''

    staff = Staff("c'8 [ s8 c'8 ]")
    chord = Chord(staff[1])

    assert chord.lilypond_format == '<>8'
    assert inspect(chord).get_parentage().parent is None
    assert inspect(chord).is_well_formed()


def test_scoretools_Chord___init___12():
    r'''Initialize chord from rest.
    '''

    rest = Rest('r8')
    chord = Chord(rest)

    assert rest.lilypond_format == 'r8'
    assert chord.lilypond_format == '<>8'
    assert inspect(rest).is_well_formed()
    assert inspect(chord).is_well_formed()


def test_scoretools_Chord___init___13():
    r'''Initialize chord from tupletized rest.
    '''

    tuplet = Tuplet((2, 3), 'r8 r8 r8')
    chord = Chord(tuplet[1])

    assert chord.lilypond_format == '<>8'
    assert inspect(chord).is_well_formed()
    assert inspect(chord).get_parentage().parent is None


def test_scoretools_Chord___init___14():
    r'''Initialize chord from note.
    '''

    note = Note("d'8")
    chord = Chord(note)
    
    assert note.lilypond_format == "d'8"
    assert chord.lilypond_format == "<d'>8"
    assert inspect(note).is_well_formed()
    assert inspect(chord).is_well_formed()


def test_scoretools_Chord___init___15():
    r'''Initialize chord from tupletized note.
    '''

    tuplet = Tuplet((2, 3), "c'8 c'8 c'8")
    chord = Chord(tuplet[1])

    assert chord.lilypond_format == "<c'>8"
    assert inspect(chord).is_well_formed()
    assert inspect(chord).get_parentage().parent is None


def test_scoretools_Chord___init___16():
    r'''Initialize chord from spanned note.
    '''

    staff = Staff("c'8 ( d'8 e'8 f'8 )")
    chord = Chord(staff[1])

    assert chord.lilypond_format == "<d'>8"
    assert inspect(chord).is_well_formed()
    assert inspect(chord).get_parentage().parent is None


def test_scoretools_Chord___init___17():
    r'''Initialize empty chord from LilyPond input string.
    '''

    chord = Chord('<>8.')

    assert chord.lilypond_format == '<>8.'
    assert not len(chord)


def test_scoretools_Chord___init___18():
    r'''Initialize chord from LilyPond input string with forced and 
    cautionary accidentals.
    '''

    chord = Chord('<c!? e? g! b>4')

    assert chord.lilypond_format == '<c!? e? g! b>4'


def test_scoretools_Chord___init___19():
    r'''Initialize chord from note with forced and cautionary accidentals.
    '''

    note = Note("c'!?4")
    chord = Chord(note)

    assert chord.lilypond_format == "<c'!?>4"
