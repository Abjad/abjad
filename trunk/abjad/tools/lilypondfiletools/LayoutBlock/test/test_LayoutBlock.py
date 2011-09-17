from abjad import *


def test_LayoutBlock_01():

    lb = lilypondfiletools.LayoutBlock()
    lb.indent = 0
    lb.ragged_right = True

    r'''
    \layout {
        indent = #0
        ragged-right = ##t
    }
    '''

    assert lb.format == '\\layout {\n\tindent = #0\n\tragged-right = ##t\n}'
