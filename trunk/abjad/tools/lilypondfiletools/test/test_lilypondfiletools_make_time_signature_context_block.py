from abjad import *


def test_lilypondfiletools_make_time_signature_context_block_01():

    context_block = lilypondfiletools.make_time_signature_context_block()
    
    r'''
    \context {
        \type Engraver_group
        \name TimeSignatureContext
        \consists Axis_group_engraver
        \consists Time_signature_engraver
        \override TimeSignature #'X-extent = #'(0 . 0)
        \override TimeSignature #'X-offset = #ly:self-alignment-interface::x-aligned-on-self
        \override TimeSignature #'Y-extent = #'(0 . 0)
        \override TimeSignature #'break-align-symbol = ##f
        \override TimeSignature #'break-visibility = #end-of-line-invisible
        \override TimeSignature #'font-size = #3
        \override TimeSignature #'self-alignment-X = #center
        \override VerticalAxisGroup #'default-staff-staff-spacing = #'((basic_distance . 0) (minimum_distance . 0) (padding . 4) (stretchability . 0))
    }
    '''

    assert context_block.lilypond_format == "\\context {\n\t\\type Engraver_group\n\t\\name TimeSignatureContext\n\t\\consists Axis_group_engraver\n\t\\consists Time_signature_engraver\n\t\\override TimeSignature #'X-extent = #'(0 . 0)\n\t\\override TimeSignature #'X-offset = #ly:self-alignment-interface::x-aligned-on-self\n\t\\override TimeSignature #'Y-extent = #'(0 . 0)\n\t\\override TimeSignature #'break-align-symbol = ##f\n\t\\override TimeSignature #'break-visibility = #end-of-line-invisible\n\t\\override TimeSignature #'font-size = #3\n\t\\override TimeSignature #'self-alignment-X = #center\n\t\\override VerticalAxisGroup #'default-staff-staff-spacing = #'((basic_distance . 0) (minimum_distance . 0) (padding . 4) (stretchability . 0))\n}"
