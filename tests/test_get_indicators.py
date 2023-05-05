import abjad


def test_get_indicators_01():
    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.slur(voice[:])
    command_1 = abjad.LilyPondLiteral(r"\slurDotted", site="before")
    abjad.attach(command_1, voice[0])
    command_2 = abjad.LilyPondLiteral(r"\slurUp", site="before")
    abjad.attach(command_2, voice[0])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \slurDotted
            \slurUp
            c'8
            (
            d'8
            e'8
            f'8
            )
        }
        """
    ), abjad.lilypond(voice)

    indicators = abjad.get.indicators(voice[0], abjad.LilyPondLiteral)
    assert command_1 in indicators
    assert command_2 in indicators
    assert len(indicators) == 2


def test_get_indicators_02():
    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([voice])
    clef = abjad.Clef("treble")
    abjad.attach(clef, voice[0])
    dynamic = abjad.Dynamic("p")
    abjad.attach(dynamic, voice[0])

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                \clef "treble"
                c'8
                \p
                d'8
                e'8
                f'8
            }
        }
        """
    ), abjad.lilypond(staff)

    indicators = abjad.get.indicators(voice[0])
    assert len(indicators) == 2


def test_get_indicators_03():
    note = abjad.Note("c'4")
    stem_tremolo = abjad.StemTremolo(16)
    abjad.attach(stem_tremolo, note)
    stem_tremolos = abjad.get.indicators(note, abjad.StemTremolo)

    assert stem_tremolos[0] is stem_tremolo
