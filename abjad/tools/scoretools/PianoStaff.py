# -*- encoding: utf-8 -*-
from abjad.tools.scoretools.StaffGroup import StaffGroup


class PianoStaff(StaffGroup):
    r'''Abjad model of piano staff:

    ::

        >>> staff_1 = Staff("c'4 d'4 e'4 f'4 g'1")
        >>> staff_2 = Staff("g2 f2 e1")

    ::

        >>> piano_staff = scoretools.PianoStaff([staff_1, staff_2])

    ..  doctest::

        >>> print format(piano_staff)
        \new PianoStaff <<
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

    Returns piano staff.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, music=None, context_name='PianoStaff', name=None):
        StaffGroup.__init__(
            self, 
            music=music, 
            context_name=context_name, 
            name=name,
            )
