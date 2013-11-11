# -*- encoding: utf-8 -*-
from abjad.tools.scoretools.StaffGroup import StaffGroup


class GrandStaff(StaffGroup):
    r'''Abjad model of grand staff:

    ::

        >>> staff_1 = Staff("c'4 d'4 e'4 f'4 g'1")
        >>> staff_2 = Staff("g2 f2 e1")

    ::

        >>> grand_staff = scoretools.GrandStaff([staff_1, staff_2])

    ..  doctest::

        >>> print format(grand_staff)
        \new GrandStaff <<
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

    Returns grand staff.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, music, context_name='GrandStaff', name=None):
        StaffGroup.__init__(
            self, 
            music=music, 
            context_name=context_name, 
            name=name,
            )
