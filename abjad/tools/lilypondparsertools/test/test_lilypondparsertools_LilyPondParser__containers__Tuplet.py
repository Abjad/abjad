# -*- coding: utf-8 -*-
import abjad


def test_lilypondparsertools_LilyPondParser__containers__Tuplet_01():

    maker = abjad.NoteMaker()
    notes = maker([0, 2, 4], (1, 8))
    target = abjad.Tuplet(abjad.Multiplier(2, 3), notes)

    assert format(target) == abjad.String.normalize(
        r'''
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
