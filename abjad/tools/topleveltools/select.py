# -*- coding: utf-8 -*-


def select(expr=None):
    r'''Selects `expr` or makes empty selector.

    ..  container:: example

        Selects first two notes in staff:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> selection = select(staff[:2])
            >>> for note in selection:
            ...     override(note).note_head.color = 'red'

        ::

            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \once \override NoteHead.color = #red
                c'4
                \once \override NoteHead.color = #red
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Initializes empty selector:

        ::

            >>> select()
            Selector()

    Returns selection when `expr` is not none.

    Returns selector when `expr` is none.
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
