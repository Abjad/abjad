from .Context import Context


class Staff(Context):
    r'''Staff.

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

    __slots__ = ()

    _default_context_name = 'Staff'

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        context_name='Staff',
        is_simultaneous=None,
        name=None,
        ):
        Context.__init__(
            self,
            components=components,
            context_name=context_name,
            is_simultaneous=is_simultaneous,
            name=name,
            )
