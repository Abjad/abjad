def select(expr):
    '''Select `expr`.

    Return selection.
    '''
    from abjad.tools import componenttools
    from abjad.tools import selectiontools
    if isinstance(expr, componenttools.Component):
        return selectiontools.Selection(expr)
    elif hasattr(expr, '_music'):
        music = expr._music
        return selectiontools.Selection(music)
    else:
        return selectiontools.Selection(expr)
