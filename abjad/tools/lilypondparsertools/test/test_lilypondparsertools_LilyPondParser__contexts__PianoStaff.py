import abjad


def test_lilypondparsertools_LilyPondParser__contexts__PianoStaff_01():

    maker = abjad.NoteMaker()
    target = abjad.StaffGroup([
        abjad.Staff(maker([0, 2, 4, 5, 7], (1, 8))),
        abjad.Staff(maker([0, 2, 4, 5, 7], (1, 8)))
    ])
    target.context_name = 'PianoStaff'

    assert format(target) == abjad.String.normalize(
        r'''
        \new PianoStaff <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
                g'8
            }
            \new Staff {
                c'8
                d'8
                e'8
                f'8
                g'8
            }
        >>
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
