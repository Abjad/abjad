from abjad import *


def test_LayoutBlock_context_blocks_01():


    layout_block = lilypondfiletools.LayoutBlock()
    context_block = lilypondfiletools.ContextBlock('Score')
    context_block.override.bar_number.transparent = True
    context_block.override.time_signature.break_visibility = schemetools.Scheme('end-of-line-invisible')
    layout_block.context_blocks.append(context_block)

    r'''
    \layout {
        \context {
            \Score
            \override BarNumber #'transparent = ##t
            \override TimeSignature #'break-visibility = #end-of-line-invisible
        }
    }
    '''

    assert layout_block.format == "\\layout {\n\t\\context {\n\t\t\\Score\n\t\t\\override BarNumber #'transparent = ##t\n\t\t\\override TimeSignature #'break-visibility = #end-of-line-invisible\n\t}\n}"
