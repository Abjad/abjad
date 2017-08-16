import abjad


def test_lilypondparsertools_LilyPondParser__indicators__Clef_01():

    target = abjad.Staff([abjad.Note(0, 1)])
    clef = abjad.Clef('bass')
    abjad.attach(clef, target[0])

    assert format(target) == abjad.String.normalize(
        r'''
        \new Staff {
            \clef "bass"
            c'1
        }
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    clefs = abjad.inspect(result[0]).get_indicators(abjad.Clef)
    assert len(clefs) == 1
