# -*- encoding: utf-8 -*-
from abjad.tools import schemetools
from abjad.tools.topleveltools import override


def make_time_signature_context_block(
    font_size=3, 
    minimum_distance=12, 
    padding=4,
    ):
    r'''Make time signature context block:

    ::

        >>> context_block = lilypondfiletools.make_time_signature_context_block()

    ..  doctest::

        >>> print format(context_block) # doctest: +SKIP
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
            \override VerticalAxisGroup #'default-staff-staff-spacing = #'(
                (basic-distance . 0) (minimum-distance . 0) (padding . 4) (stretchability . 0))
        }

    Returns context block.
    '''
    from abjad.tools import layouttools
    from abjad.tools import lilypondfiletools

    assert isinstance(font_size, (int, float))
    assert isinstance(padding, (int, float))

    context_block = lilypondfiletools.ContextBlock(
        type_='Engraver_group', 
        name='TimeSignatureContext',
        )
    context_block.engraver_consists.append('Axis_group_engraver')
    context_block.engraver_consists.append('Time_signature_engraver')
    override(context_block).time_signature.X_extent = (0, 0)
    override(context_block).time_signature.X_offset = schemetools.Scheme(
        'ly:self-alignment-interface::x-aligned-on-self')
    override(context_block).time_signature.Y_extent = (0, 0)
    override(context_block).time_signature.break_align_symbol = False
    override(context_block).time_signature.break_visibility = \
        schemetools.Scheme('end-of-line-invisible')
    override(context_block).time_signature.font_size = font_size
    override(context_block).time_signature.self_alignment_X = \
        schemetools.Scheme('center')
    spacing_vector = layouttools.make_spacing_vector(
        0, 
        minimum_distance, 
        padding, 
        0,
        )
    override(context_block).vertical_axis_group.default_staff_staff_spacing = \
        spacing_vector

    return context_block
