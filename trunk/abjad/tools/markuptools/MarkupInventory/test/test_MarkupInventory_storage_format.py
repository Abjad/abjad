from abjad import *


def test_MarkupInventory_storage_format_01():

    inventory = markuptools.MarkupInventory(['foo', 'bar'])

    r'''
    markuptools.MarkupInventory([
        markuptools.Markup((
            'foo',
            )),
        markuptools.Markup((
            'bar',
            ))
        ])
    '''

    assert inventory.storage_format == "markuptools.MarkupInventory([\n\tmarkuptools.Markup((\n\t\t'foo',\n\t\t)),\n\tmarkuptools.Markup((\n\t\t'bar',\n\t\t))\n\t])"

