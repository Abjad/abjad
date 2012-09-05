from abjad.tools import schemetools


def make_time_signature_context_block(font_size=3, padding=4):
    r'''.. versionadded:: 2.9

    Make time signature context block::

        >>> context_block = lilypondfiletools.make_time_signature_context_block()

    ::

        >>> f(context_block) # doctest: +SKIP
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
                (basic_distance . 0) (minimum_distance . 0) (padding . 4) (stretchability . 0))
        }

    Return context block.
    '''
    from abjad.tools import layouttools
    from abjad.tools import lilypondfiletools

    assert isinstance(font_size, (int, float))
    assert isinstance(padding, (int, float))

    context_block = lilypondfiletools.ContextBlock()
    context_block.type = 'Engraver_group'
    context_block.engraver_consists.append('Axis_group_engraver')
    context_block.engraver_consists.append('Time_signature_engraver')
    context_block.name = 'TimeSignatureContext'
    context_block.override.time_signature.X_extent = (0, 0)
    context_block.override.time_signature.X_offset = schemetools.Scheme(
        'ly:self-alignment-interface::x-aligned-on-self')
    context_block.override.time_signature.Y_extent = (0, 0)
    context_block.override.time_signature.break_align_symbol = False
    context_block.override.time_signature.break_visibility = schemetools.Scheme('end-of-line-invisible')
    context_block.override.time_signature.font_size = font_size
    context_block.override.time_signature.self_alignment_X = schemetools.Scheme('center')
    spacing_vector = layouttools.make_spacing_vector(0, 0, padding, 0)
    context_block.override.vertical_axis_group.default_staff_staff_spacing = spacing_vector

    return context_block
