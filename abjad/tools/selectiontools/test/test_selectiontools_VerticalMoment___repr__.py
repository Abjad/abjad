# -*- coding: utf-8 -*-
import abjad


def test_selectiontools_VerticalMoment___repr___01():
    r'''Vertical moment repr returns a nonempty string.
    '''

    vertical_moment = abjad.inspect(abjad.Note('c4')).get_vertical_moment()
    representation = repr(vertical_moment)

    assert isinstance(representation, str) and 0 < len(representation)
