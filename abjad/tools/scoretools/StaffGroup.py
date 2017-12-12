from .Context import Context


class StaffGroup(Context):
    r'''Staff group.

    ..  container:: example

        ::

            >>> staff_1 = abjad.Staff("c'4 d'4 e'4 f'4 g'1")
            >>> staff_2 = abjad.Staff("g2 f2 e1")
            >>> staff_group = abjad.StaffGroup([staff_1, staff_2])
            >>> show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> f(staff_group)
            \new StaffGroup <<
                \new Staff {
                    c'4
                    d'4
                    e'4
                    f'4
                    g'1
                }
                \new Staff {
                    g2
                    f2
                    e1
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Contexts'

    __slots__ = ()

    _default_context_name = 'StaffGroup'

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        context_name='StaffGroup',
        is_simultaneous=True,
        name=None,
        ):
        Context.__init__(
            self,
            components=components,
            context_name=context_name,
            is_simultaneous=is_simultaneous,
            name=name,
            )
