import abjad


def test_LilyPondParser__functions__transpose_01():

    pitches = ["e'", "gs'", "b'", "e''"]
    maker = abjad.NoteMaker()
    target = abjad.Staff(maker(pitches, (1, 4)))
    key_signature = abjad.KeySignature("e", "major")
    abjad.attach(key_signature, target[0])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \key e \major
            e'4
            gs'4
            b'4
            e''4
        }
        """
    )

    string = r"\transpose d e \relative c' \new Staff { \key d \major d4 fs a d }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__transpose_02():

    pitches = ["ef'", "f'", "g'", "bf'"]
    maker = abjad.NoteMaker()
    target = abjad.Staff(maker(pitches, (1, 4)))
    key_signature = abjad.KeySignature("ef", "major")
    abjad.attach(key_signature, target[0])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \key ef \major
            ef'4
            f'4
            g'4
            bf'4
        }
        """
    )

    string = r"\transpose a c' \relative c' \new Staff { \key c \major c4 d e g }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__transpose_03():

    maker = abjad.NoteMaker()
    target = abjad.Staff(
        [
            abjad.Container(maker(["cs'", "ds'", "es'", "fs'"], (1, 4))),
            abjad.Container(maker(["df'", "ef'", "f'", "gf'"], (1, 4))),
        ]
    )

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            {
                cs'4
                ds'4
                es'4
                fs'4
            }
            {
                df'4
                ef'4
                f'4
                gf'4
            }
        }
        """
    )

    string = r"""music = \relative c' { c d e f }
    \new Staff {
        \transpose c cs \music
        \transpose c df \music
    }
    """

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
