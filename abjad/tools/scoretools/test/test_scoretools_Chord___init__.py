import abjad


def test_scoretools_Chord___init___01():
    r'''Initialize empty chord.
    '''

    chord = abjad.Chord([], (1, 4))
    assert format(chord) == "<>4"


def test_scoretools_Chord___init___02():
    r'''Initialize chord with pitch numbers.
    '''

    chord = abjad.Chord([2, 4, 5], (1, 4))
    assert format(chord) == "<d' e' f'>4"


def test_scoretools_Chord___init___03():
    r'''Initialize chord with pitch tokens.
    '''

    chord = abjad.Chord([('ds', 4), ('ef', 4)], (1, 4))
    assert format(chord) == "<ds' ef'>4"


def test_scoretools_Chord___init___04():
    r'''Initialize chord with pitches.
    '''

    pitches = []
    pitches.append(abjad.NamedPitch('D#4'))
    pitches.append(abjad.NamedPitch('Eb4'))
    chord = abjad.Chord(pitches, (1, 4))
    assert format(chord) == "<ds' ef'>4"


def test_scoretools_Chord___init___05():
    r'''Initialize chord with pitches and pitch numbers together.
    '''

    pitches = [2, ('ef', 4), abjad.NamedPitch(4)]
    chord = abjad.Chord(pitches, (1, 4))
    assert format(chord) == "<d' ef' e'>4"


def test_scoretools_Chord___init___06():
    r'''Initialize chord with list of pitch names.
    '''

    pitches = ["d'", "ef'", "e'"]
    chord = abjad.Chord(pitches, (1, 4))
    assert format(chord) == "<d' ef' e'>4"


def test_scoretools_Chord___init___07():
    r'''Initialize chord with LilyPond input string.
    '''

    chord = abjad.Chord("<d' ef' e'>4")
    assert format(chord) == "<d' ef' e'>4"


def test_scoretools_Chord___init___08():
    r'''Initialize chord from skip.
    '''

    skip = abjad.Skip('s8')
    chord = abjad.Chord(skip)

    assert format(skip) == 's8'
    assert format(chord) == '<>8'

    assert abjad.inspect(skip).is_well_formed()
    assert abjad.inspect(chord).is_well_formed()


def test_scoretools_Chord___init___09():
    r'''Initialize chord from tupletized skip.
    '''

    tuplet = abjad.Tuplet((2, 3), 's8 s8 s8')
    chord = abjad.Chord(tuplet[0])

    assert format(chord) == '<>8'
    assert abjad.inspect(chord).get_parentage().parent is None
    assert abjad.inspect(chord).is_well_formed()


def test_scoretools_Chord___init___10():
    r'''Initialize chord from containerized skip.
    '''

    tuplet = abjad.Voice('s8 s8 s8')
    chord = abjad.Chord(tuplet[0])

    assert format(chord) == '<>8'
    assert abjad.inspect(chord).get_parentage().parent is None
    assert abjad.inspect(chord).is_well_formed()



def test_scoretools_Chord___init___11():
    r'''Initialize chord from beamed skip.
    '''

    staff = abjad.Staff("c'8 [ s8 c'8 ]")
    chord = abjad.Chord(staff[1])

    assert format(chord) == '<>8'
    assert abjad.inspect(chord).get_parentage().parent is None
    assert abjad.inspect(chord).is_well_formed()


def test_scoretools_Chord___init___12():
    r'''Initialize chord from rest.
    '''

    rest = abjad.Rest('r8')
    chord = abjad.Chord(rest)

    assert format(rest) == 'r8'
    assert format(chord) == '<>8'
    assert abjad.inspect(rest).is_well_formed()
    assert abjad.inspect(chord).is_well_formed()


def test_scoretools_Chord___init___13():
    r'''Initialize chord from tupletized rest.
    '''

    tuplet = abjad.Tuplet((2, 3), 'r8 r8 r8')
    chord = abjad.Chord(tuplet[1])

    assert format(chord) == '<>8'
    assert abjad.inspect(chord).is_well_formed()
    assert abjad.inspect(chord).get_parentage().parent is None


def test_scoretools_Chord___init___14():
    r'''Initialize chord from note.
    '''

    note = abjad.Note("d'8")
    chord = abjad.Chord(note)

    assert format(note) == "d'8"
    assert format(chord) == "<d'>8"
    assert abjad.inspect(note).is_well_formed()
    assert abjad.inspect(chord).is_well_formed()


def test_scoretools_Chord___init___15():
    r'''Initialize chord from tupletized note.
    '''

    tuplet = abjad.Tuplet((2, 3), "c'8 c'8 c'8")
    chord = abjad.Chord(tuplet[1])

    assert format(chord) == "<c'>8"
    assert abjad.inspect(chord).is_well_formed()
    assert abjad.inspect(chord).get_parentage().parent is None


def test_scoretools_Chord___init___16():
    r'''Initialize chord from spanned note.
    '''

    staff = abjad.Staff("c'8 ( d'8 e'8 f'8 )")
    chord = abjad.Chord(staff[1])

    assert format(chord) == "<d'>8"
    assert abjad.inspect(chord).is_well_formed()
    assert abjad.inspect(chord).get_parentage().parent is None


def test_scoretools_Chord___init___17():
    r'''Initialize empty chord from LilyPond input string.
    '''

    chord = abjad.Chord('<>8.')

    assert format(chord) == '<>8.'
    assert not len(chord.note_heads)


def test_scoretools_Chord___init___18():
    r'''Initialize chord from LilyPond input string with forced and
    cautionary accidentals.
    '''

    chord = abjad.Chord('<c!? e? g! b>4')

    assert format(chord) == '<c!? e? g! b>4'


def test_scoretools_Chord___init___19():
    r'''Initialize chord from note with forced and cautionary accidentals.
    '''

    note = abjad.Note("c'!?4")
    chord = abjad.Chord(note)

    assert format(chord) == "<c'!?>4"


def test_scoretools_Chord___init___20():
    r'''Initialize chord from other chord.
    '''

    chord_1 = abjad.Chord("<c' e' g' bf'>4")
    chord_2 = abjad.Chord(chord_1, abjad.Duration(1, 8))

    assert format(chord_2) == "<c' e' g' bf'>8"


def test_scoretools_Chord___init___21():
    r'''Initialize chord with drum pitches.
    '''

    chord = abjad.Chord("<sn? bd! tamb>4")

    assert format(chord) == '<bassdrum! snare? tambourine>4'
