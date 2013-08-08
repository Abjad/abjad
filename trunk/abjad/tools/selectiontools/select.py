# -*- encoding: utf-8 -*-
def select(expr=None):
    r'''Select `expr`.

    Return selection.
    '''
    from abjad.tools import componenttools
    from abjad.tools import selectiontools
    if isinstance(expr, componenttools.Component):
        return selectiontools.FreeComponentSelection(expr)
    elif hasattr(expr, '_music'):
        music = expr._music
        return selectiontools.FreeComponentSelection(music)
    elif expr is None:
        return selectiontools.FreeComponentSelection()
    else:
        return selectiontools.FreeComponentSelection(expr)
