from abjad import *


def test_Markup_contents_string_01():

    markup = markuptools.Markup('foo')

    assert markup.contents_string == 'foo'
