# TODO: make public and bind to some class somewhere
def _format_note_head(note_head):
    from abjad.tools.lilypondfiletools._format_lilypond_attribute import _format_lilypond_attribute
    from abjad.tools.lilypondfiletools._format_lilypond_value import _format_lilypond_value
    from abjad.tools import chordtools

    # make sure note head has pitch
    assert note_head.written_pitch
    result = []

    # format chord note head with optional tweaks
    if isinstance(note_head._client, chordtools.Chord):
        for key, value in vars(note_head.tweak).iteritems():
            if not key.startswith('_'):
                result.append(r'\tweak %s %s' % (
                    _format_lilypond_attribute(key),
                    _format_lilypond_value(value)))

    # format note head pitch
    kernel = note_head.written_pitch.lilypond_format
    if note_head.is_forced:
        kernel += '!'
    if note_head.is_cautionary:
        kernel += '?'
    result.append(kernel)
    result = '\n'.join(result)

    # return formatted note head
    return result
