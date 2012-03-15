from abjad import *


def test_Markup__tools_package_qualified_indented_repr_01():

    markup = markuptools.Markup(r'\bold { foo }')

    assert repr(markup) == "Markup('\\\\bold { foo }')"

    assert markup._tools_package_qualified_repr == "markuptools.Markup('\\\\bold { foo }', style_string='backslash')"

    r'''
    markuptools.Markup(
        '\\bold { foo }',
        style_string='backslash'
        )
    '''

    assert markup._tools_package_qualified_indented_repr == "markuptools.Markup(\n\t'\\\\bold { foo }',\n\tstyle_string='backslash'\n\t)"
