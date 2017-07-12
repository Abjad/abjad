# -*- coding: utf-8 -*-
import abjad


def test_lilypondparsertools_LilyPondParser__indicators__StemTremolo_01():

    target = abjad.Staff([abjad.Note(0, 1)])
    stem_tremolo = abjad.StemTremolo(4)
    abjad.attach(stem_tremolo, target[0])

    assert format(target) == abjad.String.normalize(
        r'''
        \new Staff {
            c'1 :4
        }
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    stem_tremolos = abjad.inspect(result[0]).get_indicators(abjad.StemTremolo)
    assert 1 == len(stem_tremolos)
