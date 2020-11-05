import abjad


def test_LilyPondParser__indicators__StemTremolo_01():

    target = abjad.Staff([abjad.Note(0, 1)])
    stem_tremolo = abjad.StemTremolo(4)
    abjad.attach(stem_tremolo, target[0])

    assert abjad.lilypond(target) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            :4
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    stem_tremolos = abjad.get.indicators(result[0], abjad.StemTremolo)
    assert 1 == len(stem_tremolos)
