# -*- coding: utf-8 -*-
from abjad import *


def test_markuptools_MarkupInventory___format___01():

    inventory = markuptools.MarkupInventory(['foo', 'bar'])

    assert format(inventory) == stringtools.normalize(
        r'''
        markuptools.MarkupInventory(
            [
                markuptools.Markup(
                    contents=('foo',),
                    ),
                markuptools.Markup(
                    contents=('bar',),
                    ),
                ]
            )
        ''',
        )
