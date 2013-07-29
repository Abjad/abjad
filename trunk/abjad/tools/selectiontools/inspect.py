def inspect(expr):
    '''Select `expr` for inspection.

    Return inspection.
    '''
    from abjad.tools import componenttools
    from abjad.tools import selectiontools
    if isinstance(expr, componenttools.Component):
        return selectiontools.Inspector(expr)
    elif hasattr(expr, '_music'):
        music = expr._music
        return selectiontools.Inspector(music)
    else:
        return selectiontools.Inspector(expr)
