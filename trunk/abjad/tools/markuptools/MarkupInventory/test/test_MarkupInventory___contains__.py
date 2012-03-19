from abjad import *


def test_MarkupInventory___contains___01():

    inventory = markuptools.MarkupInventory(['foo', 'bar'])

    assert 'foo' in inventory
    assert markuptools.Markup('foo') in inventory

    assert 'bar' in inventory
    assert markuptools.Markup('bar') in inventory
