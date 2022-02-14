import abjad


def test_LilyPondParser__contexts__Staff_01():

    target = abjad.Staff([])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__contexts__Staff_02():

    target = abjad.Staff([])
    target.simultaneous = True
    maker = abjad.NoteMaker()
    target.append(abjad.Voice(maker([0, 2, 4, 5, 7, 9, 11, 12], (1, 8))))
    target.append(abjad.Voice(maker([0, 2, 4, 5, 7, 9, 11, 12], (1, 8))))

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        <<
            \new Voice
            {
                c'8
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8
            }
            \new Voice
            {
                c'8
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8
            }
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
