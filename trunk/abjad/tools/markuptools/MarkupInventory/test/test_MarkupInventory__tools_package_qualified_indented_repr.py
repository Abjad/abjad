from abjad import *


def test_MarkupInventory__tools_package_qualified_indented_repr_01():

    inventory = markuptools.MarkupInventory(['foo', 'bar'])

    r'''
    markuptools.MarkupInventory([
        markuptools.Markup(
            'foo',
            style_string='backslash'
            ),
        markuptools.Markup(
            'bar',
            style_string='backslash'
            )
        ])
    '''

    assert inventory._tools_package_qualified_indented_repr == "markuptools.MarkupInventory([\n\tmarkuptools.Markup(\n\t\t'foo',\n\t\tstyle_string='backslash'\n\t\t),\n\tmarkuptools.Markup(\n\t\t'bar',\n\t\tstyle_string='backslash'\n\t\t)\n\t])"
