# -*- encoding: utf-8 -*-


def select(expr=None, contiguous=False):
    r'''Select `expr`.

    Return selection.
    '''
    from abjad.tools import componenttools
    from abjad.tools import selectiontools
    from abjad.tools import spannertools
    Selection = selectiontools.Selection
    if contiguous:
        if isinstance(expr, (list, tuple)):
            assert Selection._all_are_contiguous_components_in_same_logical_voice(expr)
        return selectiontools.ContiguousSelection(expr)
    elif isinstance(expr, componenttools.Component):
        return selectiontools.Selection(expr)
    elif hasattr(expr, '_music'):
        music = expr._music
        return selectiontools.Selection(music)
    elif isinstance(expr, spannertools.Spanner):
        music = expr._components
        return selectiontools.Selection(music)
    elif expr is None:
        return selectiontools.Selection()
    else:
        return selectiontools.Selection(expr)
