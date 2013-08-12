# -*- encoding: utf-8 -*-


def select(expr=None, contiguous=False):
    r'''Select `expr`.

    Return selection.
    '''
    from abjad.tools import componenttools
    from abjad.tools import selectiontools
    if contiguous:
        assert componenttools.all_are_thread_contiguous_components(expr)
        return selectiontools.ContiguousSelection(expr)
    elif isinstance(expr, componenttools.Component):
        return selectiontools.FreeComponentSelection(expr)
    elif hasattr(expr, '_music'):
        music = expr._music
        return selectiontools.FreeComponentSelection(music)
    elif expr is None:
        return selectiontools.FreeComponentSelection()
    else:
        return selectiontools.FreeComponentSelection(expr)
