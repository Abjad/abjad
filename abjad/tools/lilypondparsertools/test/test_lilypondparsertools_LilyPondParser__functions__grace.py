import abjad


def test_lilypondparsertools_LilyPondParser__functions__grace_01():

    target = abjad.Container([
        abjad.Note("c'4"),
        abjad.Note("d'4"),
        abjad.Note("e'2")
    ])

    grace = abjad.GraceContainer([
        abjad.Note("g''16"),
        abjad.Note("fs''16")
    ])

    abjad.attach(grace, target[2])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c'4
            d'4
            \grace {
                g''16
                fs''16
            }
            e'2
        }
        '''
        )

    string = r"{ c'4 d'4 \grace { g''16 fs''16} e'2 }"
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
