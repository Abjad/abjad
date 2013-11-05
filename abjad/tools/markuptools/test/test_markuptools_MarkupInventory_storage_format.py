# -*- encoding: utf-8 -*-
from abjad import *


def test_markuptools_MarkupInventory_storage_format_01():

    inventory = markuptools.MarkupInventory(['foo', 'bar'])
    
    assert testtools.compare(
        inventory.storage_format,
        r'''
        markuptools.MarkupInventory([
            markuptools.Markup((
                'foo',
                )),
            markuptools.Markup((
                'bar',
                )),
            ])
        ''',
        )
