from abjad.tools.markuptools.MarkupCommand import MarkupCommand


def combine_markup_commands(*commands):
    r'''Combine MarkupCommand and/or string objects.

    LilyPond's '\combine' markup command can only take two arguments, so in order
    to combine more than two stencils, a cascade of '\combine' commands must be
    employed.  `combine_markup_commands` simplifies this process.

    ::

        abjad> from abjad.tools.markuptools import combine_markup_commands
        abjad> from abjad.tools.schemetools import SchemePair
        abjad> from abjad.tools.markuptools import MarkupCommand

    ::

        abjad> markup_a = MarkupCommand('draw-circle', 4, 0.4, False)
        abjad> markup_b = MarkupCommand('filled-box', SchemePair(-4, 4), SchemePair(-0.5, 0.5), 1)
        abjad> markup_c = "some text"
        abjad> print combine_markup_commands(markup_a, markup_b, markup_c).format
        \combine \combine \draw-circle #4 #0.4 ##f \filled-box #'(-4 . 4) #'(-0.5 . 0.5) #1 #"some text"

    Returns a MarkupCommand instance, or a string if that was the only argument.
    '''

    assert len(commands)
    assert all([isinstance(command, (MarkupCommand, str)) for command in commands])

    if 1 == len(commands):
        return commands[0]

    combined = MarkupCommand('combine', commands[0], commands[1])
    for command in commands[2:]:
        combined = MarkupCommand('combine', combined, command)
    return combined
