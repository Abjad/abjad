import abjad


def test_lilypondparsertools_LilyPondParser__indicators__KeySignature_01():

    target = abjad.Staff([abjad.Note("fs'", 1)])
    key_signature = abjad.KeySignature('g', 'major')
    abjad.attach(key_signature, target[0])

    assert format(target) == abjad.String.normalize(
        r'''
        \new Staff {
            \key g \major
            fs'1
        }
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    key_signatures = abjad.inspect(result[0]).get_indicators(abjad.KeySignature)
    assert len(key_signatures) == 1
