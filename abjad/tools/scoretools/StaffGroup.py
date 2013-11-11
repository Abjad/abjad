# -*- encoding: utf-8 -*-
from abjad.tools.scoretools.Context import Context


class StaffGroup(Context):
    r'''Abjad model of staff group:

    ::

        >>> staff_1 = Staff("c'4 d'4 e'4 f'4 g'1")
        >>> staff_2 = Staff("g2 f2 e1")

    ::

        >>> staff_group = scoretools.StaffGroup([staff_1, staff_2])

    ..  doctest::

        >>> print format(staff_group)
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

    Returns staff group.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, music=None, context_name='StaffGroup', name=None):
        Context.__init__(
            self,
            music=music,
            context_name=context_name,
            name=name,
            )
        self.is_simultaneous = True
