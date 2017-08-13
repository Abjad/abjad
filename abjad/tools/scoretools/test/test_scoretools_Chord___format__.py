import abjad


def test_scoretools_Chord___format___01():
    r'''Format chord with one note-head.
    '''

    chord = abjad.Chord("<cqs'>4")

    assert str(chord) == "<cqs'>4"
    assert format(chord) == "<cqs'>4"
    assert len(chord.note_heads) == 1
    assert len(chord.written_pitches) == 1


def test_scoretools_Chord___format___02():
    r'''Format chord with LilyPond command.
    '''

    chord = abjad.Chord("<d' ef' e'>4")
    command = abjad.LilyPondCommand('glissando', 'right')
    abjad.attach(command, chord)

    assert format(chord) == "<d' ef' e'>4 \\glissando"


def test_scoretools_Chord___format___03():
    r'''Format tweaked chord with LilyPond command.
    '''

    chord = abjad.Chord("<d' ef' e'>4")
    chord.note_heads[0].tweak.color = 'red'
    command = abjad.LilyPondCommand('glissando', 'right')
    abjad.attach(command, chord)

    assert format(chord) == abjad.String.normalize(
        r'''
        <
            \tweak color #red
            d'
            ef'
            e'
        >4 \glissando
        '''
        )

    assert abjad.inspect(chord).is_well_formed()


def test_scoretools_Chord___format___04():
    '''Format tweaked chord.
    '''

    chord = abjad.Chord("<d' ef' e'>4")
    chord.note_heads[0].tweak.transparent = True

    assert format(chord) == abjad.String.normalize(
        r'''
        <
            \tweak transparent ##t
            d'
            ef'
            e'
        >4
        '''
        )


def test_scoretools_Chord___format___05():
    r'''Formats tweaked chord.
    '''

    chord = abjad.Chord("<d' ef' e'>4")
    chord.note_heads[0].tweak.style = 'harmonic'

    assert format(chord) == abjad.String.normalize(
        r'''
        <
            \tweak style #'harmonic
            d'
            ef'
            e'
        >4
        '''
        )
