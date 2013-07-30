def select(expr):
    '''Select `expr`.

    Return selection.
    '''
    from abjad.tools import componenttools
    from abjad.tools import selectiontools
    if isinstance(expr, componenttools.Component):
        return selectiontools.ComponentSelection(expr)
    elif hasattr(expr, '_music'):
        music = expr._music
        return selectiontools.ComponentSelection(music)
    else:
        return selectiontools.ComponentSelection(expr)
