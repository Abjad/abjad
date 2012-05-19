from abjad import *


def test_Markup_contents_01():

    markup = markuptools.Markup('foo')

    assert markup.contents == ('foo',)


def test_Markup_contents_02():

    markup = markuptools.Markup(['foo', 'bar', 'baz'])

    assert markup.contents == ('foo', 'bar', 'baz')
