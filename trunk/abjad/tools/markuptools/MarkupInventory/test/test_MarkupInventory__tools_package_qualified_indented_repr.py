from abjad import *


def test_MarkupInventory__tools_package_qualified_indented_repr_01():

    inventory = markuptools.MarkupInventory(['foo', 'bar'])

    r'''
    markuptools.MarkupInventory([
        markuptools.Markup(
            'foo'
            ),
        markuptools.Markup(
            'bar'
            )
        ])
    '''

    assert inventory._tools_package_qualified_indented_repr == "markuptools.MarkupInventory([\n\tmarkuptools.Markup(\n\t\t'foo'\n\t\t),\n\tmarkuptools.Markup(\n\t\t'bar'\n\t\t)\n\t])"
