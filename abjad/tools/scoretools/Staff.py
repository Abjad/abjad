# -*- coding: utf-8 -*-
from abjad.tools.scoretools.Context import Context


class Staff(Context):
    r'''Staff.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Contexts'

    __slots__ = (
        )

    _default_context_name = 'Staff'

    ### INITIALIZER ###

    def __init__(
        self,
        music=None,
        context_name='Staff',
        is_simultaneous=None,
        name=None,
        ):
        Context.__init__(
            self,
            music=music,
            context_name=context_name,
            is_simultaneous=is_simultaneous,
            name=name,
            )
