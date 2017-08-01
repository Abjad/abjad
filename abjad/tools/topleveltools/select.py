# -*- coding: utf-8 -*-


def select(argument=None):
    r'''Selects `argument` or makes empty selector.

    ::

        >>> import abjad

    ..  container:: example

        Selects first two notes in staff:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> selection = abjad.select(staff[:2])
            >>> for note in selection:
            ...     abjad.override(note).note_head.color = 'red'

        ::

            >>> show(staff) # doctest: +SKIP

        ..  docs::

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

            >>> abjad.select()
            Selector()

    Returns selection when `argument` is not none.

    Returns selector when `argument` is none.
    '''
    from abjad.tools import scoretools
    from abjad.tools import selectiontools
    from abjad.tools import selectortools
    from abjad.tools import spannertools
    if argument is None:
        return selectortools.Selector()
    elif isinstance(argument, scoretools.Component):
        return selectiontools.Selection(argument)
    elif hasattr(argument, '_music'):
        music = argument._music
        return selectiontools.Selection(music)
    elif isinstance(argument, spannertools.Spanner):
        music = argument._components
        return selectiontools.Selection(music)
    return selectiontools.Selection(argument)
