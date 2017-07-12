# -*- coding: utf-8 -*-
import abjad


def test_lilypondparsertools_LilyPondParser__contexts__Staff_01():

    target = abjad.Staff([])

    assert format(target) == abjad.String.normalize(
        r'''
        \new Staff {
        }
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__contexts__Staff_02():

    target = abjad.Staff([])
    target.is_simultaneous = True
    maker = abjad.NoteMaker()
    target.append(abjad.Voice(maker([0, 2, 4, 5, 7, 9, 11, 12], (1, 8))))
    target.append(abjad.Voice(maker([0, 2, 4, 5, 7, 9, 11, 12], (1, 8))))

    assert format(target) == abjad.String.normalize(
        r'''
        \new Staff <<
            \new Voice {
                c'8
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8
            }
            \new Voice {
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
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
