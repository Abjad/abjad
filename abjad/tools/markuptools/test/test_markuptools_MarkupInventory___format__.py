# -*- encoding: utf-8 -*-
from abjad import *


def test_markuptools_MarkupInventory___format___01():

    inventory = markuptools.MarkupInventory(['foo', 'bar'])
    
    assert systemtools.TestManager.compare(
        format(inventory),
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
