# -*- coding: utf-8 -*-


def select(expr=None):
    r'''Selects `expr`.


    ..  container:: example

        **Example 1.** Returns selection when `expr` is not none:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> select(staff[:2])
            Selection([Note("c'8"), Note("d'8")])

    ..  container:: example

        **Example 2.** Returns selector when `expr` is none:

        ::

            >>> select()
            Selector()

    Returns selection.
    '''
    from abjad.tools import scoretools
    from abjad.tools import selectiontools
    from abjad.tools import selectortools
    from abjad.tools import spannertools
    if expr is None:
        return selectortools.Selector()
    elif isinstance(expr, scoretools.Component):
        return selectiontools.Selection(expr)
    elif hasattr(expr, '_music'):
        music = expr._music
        return selectiontools.Selection(music)
    elif isinstance(expr, spannertools.Spanner):
        music = expr._components
        return selectiontools.Selection(music)
    return selectiontools.Selection(expr)
