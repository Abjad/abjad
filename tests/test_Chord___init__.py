import abjad


def test_Chord___init___01():
    """
    Initialize empty chord.
    """

    chord = abjad.Chord([], (1, 4))
    assert abjad.lilypond(chord) == "<>4"


def test_Chord___init___02():
    """
    Initialize chord with pitch numbers.
    """

    chord = abjad.Chord([2, 4, 5], (1, 4))
    assert abjad.lilypond(chord) == "<d' e' f'>4"


def test_Chord___init___03():
    """
    Initialize chord with pitch tokens.
    """

    chord = abjad.Chord([("ds", 4), ("ef", 4)], (1, 4))
    assert abjad.lilypond(chord) == "<ds' ef'>4"


def test_Chord___init___04():
    """
    Initialize chord with pitches.
    """

    pitches = []
    pitches.append(abjad.NamedPitch("D#4"))
    pitches.append(abjad.NamedPitch("Eb4"))
    chord = abjad.Chord(pitches, (1, 4))
    assert abjad.lilypond(chord) == "<ds' ef'>4"


def test_Chord___init___05():
    """
    Initialize chord with pitches and pitch numbers together.
    """

    pitches = [2, ("ef", 4), abjad.NamedPitch(4)]
    chord = abjad.Chord(pitches, (1, 4))
    assert abjad.lilypond(chord) == "<d' ef' e'>4"


def test_Chord___init___06():
    """
    Initialize chord with list of pitch names.
    """

    pitches = ["d'", "ef'", "e'"]
    chord = abjad.Chord(pitches, (1, 4))
    assert abjad.lilypond(chord) == "<d' ef' e'>4"


def test_Chord___init___07():
    """
    Initialize chord with LilyPond input string.
    """

    chord = abjad.Chord("<d' ef' e'>4")
    assert abjad.lilypond(chord) == "<d' ef' e'>4"


def test_Chord___init___08():
    """
    Initialize chord from skip.
    """

    skip = abjad.Skip("s8")
    chord = abjad.Chord(skip)

    assert abjad.lilypond(skip) == "s8"
    assert abjad.lilypond(chord) == "<>8"

    assert abjad.wf.wellformed(skip)
    assert abjad.wf.wellformed(chord)


def test_Chord___init___09():
    """
    Initialize chord from tupletized skip.
    """

    tuplet = abjad.Tuplet((2, 3), "s8 s8 s8")
    chord = abjad.Chord(tuplet[0])

    assert abjad.lilypond(chord) == "<>8"
    assert abjad.get.parentage(chord).parent is None
    assert abjad.wf.wellformed(chord)


def test_Chord___init___10():
    """
    Initialize chord from containerized skip.
    """

    tuplet = abjad.Voice("s8 s8 s8")
    chord = abjad.Chord(tuplet[0])

    assert abjad.lilypond(chord) == "<>8"
    assert abjad.get.parentage(chord).parent is None
    assert abjad.wf.wellformed(chord)


def test_Chord___init___11():
    """
    Initialize chord from beamed skip.
    """

    staff = abjad.Staff("c'8 [ s8 c'8 ]")
    chord = abjad.Chord(staff[1])

    assert abjad.lilypond(chord) == "<>8"
    assert abjad.get.parentage(chord).parent is None
    assert abjad.wf.wellformed(chord)


def test_Chord___init___12():
    """
    Initialize chord from rest.
    """

    rest = abjad.Rest("r8")
    chord = abjad.Chord(rest)

    assert abjad.lilypond(rest) == "r8"
    assert abjad.lilypond(chord) == "<>8"
    assert abjad.wf.wellformed(rest)
    assert abjad.wf.wellformed(chord)


def test_Chord___init___13():
    """
    Initialize chord from tupletized rest.
    """

    tuplet = abjad.Tuplet((2, 3), "r8 r8 r8")
    chord = abjad.Chord(tuplet[1])

    assert abjad.lilypond(chord) == "<>8"
    assert abjad.wf.wellformed(chord)
    assert abjad.get.parentage(chord).parent is None


def test_Chord___init___14():
    """
    Initialize chord from note.
    """

    note = abjad.Note("d'8")
    chord = abjad.Chord(note)

    assert abjad.lilypond(note) == "d'8"
    assert abjad.lilypond(chord) == "<d'>8"
    assert abjad.wf.wellformed(note)
    assert abjad.wf.wellformed(chord)


def test_Chord___init___15():
    """
    Initialize chord from tupletized note.
    """

    tuplet = abjad.Tuplet((2, 3), "c'8 c'8 c'8")
    chord = abjad.Chord(tuplet[1])

    assert abjad.lilypond(chord) == "<c'>8"
    assert abjad.wf.wellformed(chord)
    assert abjad.get.parentage(chord).parent is None


def test_Chord___init___16():
    """
    Initialize chord from spanned note.
    """

    staff = abjad.Staff("c'8 ( d'8 e'8 f'8 )")
    chord = abjad.Chord(staff[1])

    assert abjad.lilypond(chord) == "<d'>8"
    assert abjad.wf.wellformed(chord)
    assert abjad.get.parentage(chord).parent is None


def test_Chord___init___17():
    """
    Initialize empty chord from LilyPond input string.
    """

    chord = abjad.Chord("<>8.")

    assert abjad.lilypond(chord) == "<>8."
    assert not len(chord.note_heads)


def test_Chord___init___18():
    """
    Initialize chord from LilyPond input string with forced and cautionary
    accidentals.
    """

    chord = abjad.Chord("<c!? e? g! b>4")

    assert abjad.lilypond(chord) == "<c!? e? g! b>4"


def test_Chord___init___19():
    """
    Initialize chord from note with forced and cautionary accidentals.
    """

    note = abjad.Note("c'!?4")
    chord = abjad.Chord(note)

    assert abjad.lilypond(chord) == "<c'!?>4"


def test_Chord___init___20():
    """
    Initialize chord from other chord.
    """

    chord_1 = abjad.Chord("<c' e' g' bf'>4")
    chord_2 = abjad.Chord(chord_1, abjad.Duration(1, 8))

    assert abjad.lilypond(chord_2) == "<c' e' g' bf'>8"


def test_Chord___init___21():
    """
    Initialize chord with drum pitches.
    """

    chord = abjad.Chord("<sn? bd! tamb>4")

    assert abjad.lilypond(chord) == "<bassdrum! snare? tambourine>4"
