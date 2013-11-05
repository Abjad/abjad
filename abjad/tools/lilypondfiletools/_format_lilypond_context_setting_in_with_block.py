# -*- encoding: utf-8 -*-


# TODO: make public and move to bound method of some class
def _format_lilypond_context_setting_in_with_block(name, value):
    from abjad.tools import formattools

    name = name.split('_')
    first = name[0:1]
    rest = name[1:]
    rest = [x.title() for x in rest]
    name = first + rest
    name = ''.join(name)
    value = formattools.LilyPondFormatManager.format_lilypond_value(value)
    result = r'{} = {}'.format(name, value)
    return result
