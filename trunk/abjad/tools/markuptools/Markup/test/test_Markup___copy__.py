from abjad import *
import copy


def test_Markup___copy___01():
    '''Copy keywords.
    '''

    markup_1 = markuptools.Markup('foo bar', direction=Up, markup_name='foo')
    markup_2 = copy.copy(markup_1)

    assert markup_1 == markup_2
    assert repr(markup_1) == repr(markup_2)
    assert markup_1._storage_format == markup_2._storage_format
