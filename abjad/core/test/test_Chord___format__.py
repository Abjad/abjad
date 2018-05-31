import abjad


def test_Chord___format___01():
    """
    Format chord with one note-head.
    """

    chord = abjad.Chord("<cqs'>4")

    assert str(chord) == "<cqs'>4"
    assert format(chord) == "<cqs'>4"
    assert len(chord.note_heads) == 1
    assert len(chord.written_pitches) == 1


def test_Chord___format___02():
    """
    Format chord with LilyPond command.
    """

    chord = abjad.Chord("<d' ef' e'>4")
    command = abjad.LilyPondLiteral(r'\glissando', 'right')
    abjad.attach(command, chord)

    assert format(chord) == "<d' ef' e'>4\n\\glissando"


def test_Chord___format___03():
    """
    Formats tweaked chord with LilyPond command.
    """

    chord = abjad.Chord("<d' ef' e'>4")
    chord.note_heads[0].tweaks.color = 'red'
    command = abjad.LilyPondLiteral(r'\glissando', 'right')
    abjad.attach(command, chord)

    assert format(chord) == abjad.String.normalize(
        r"""
        <
            \tweak color #red
            d'
            ef'
            e'
        >4
        \glissando
        """
        )

    assert abjad.inspect(chord).is_well_formed()


def test_Chord___format___04():
    """
    Format tweaked chord.
    """

    chord = abjad.Chord("<d' ef' e'>4")
    chord.note_heads[0].tweaks.transparent = True

    assert format(chord) == abjad.String.normalize(
        r"""
        <
            \tweak transparent ##t
            d'
            ef'
            e'
        >4
        """
        )


def test_Chord___format___05():
    """
    Formats tweaked chord.
    """

    chord = abjad.Chord("<d' ef' e'>4")
    chord.note_heads[0].tweaks.style = 'harmonic'

    assert format(chord) == abjad.String.normalize(
        r"""
        <
            \tweak style #'harmonic
            d'
            ef'
            e'
        >4
        """
        )
