def _grob_attribute_and_value_to_lilypond_override(grob, attribute, value):
    from abjad.tools.lilypondfiletools._format_lilypond_attribute import _format_lilypond_attribute
    from abjad.tools.lilypondfiletools._format_lilypond_value import _format_lilypond_value
    attribute = _format_lilypond_attribute(attribute)
    value = _format_lilypond_value(value)
    return r'\once \override %s %s = %s' % (grob, attribute, value)
