# -*- coding: utf-8 -*-
import abjad


def test_lilypondparsertools_LilyPondParser__misc__variables_01():

    target = abjad.Staff([
        abjad.Container([
            abjad.Container([
                abjad.Container([
                    abjad.Container([abjad.Note(0, (1, 8))]),
                    abjad.Note(2, (1, 8)),
                    abjad.Note(4, (1, 4))
                ]),
                abjad.Note(5, (1, 4)),
                abjad.Note(7, (1, 2))
            ]),
            abjad.Note(9, (1, 2)),
            abjad.Note(11, 1)
        ]),
        abjad.Note(12, 1)
    ])

    assert format(target) == abjad.String.normalize(
        r'''
        \new Staff {
            {
                {
                    {
                        {
                            c'8
                        }
                        d'8
                        e'4
                    }
                    f'4
                    g'2
                }
                a'2
                b'1
            }
            c''1
        }
        '''
        )

    string = r'''
        foo = { c'8 }
        foo = { \foo d' e'4 }
        foo = { \foo f' g'2 }
        foo = { \foo a' b'1 }
        \new Staff { \foo c'' }
    '''

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
