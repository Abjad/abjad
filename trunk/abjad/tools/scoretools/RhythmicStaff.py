# -*- encoding: utf-8 -*-
from abjad.tools.scoretools.Staff import Staff


class RhythmicStaff(Staff):
    r'''A rhythmic staff.

    ::

        >>> staff = scoretools.RhythmicStaff("c'8 d'8 e'8 f'8")

    ..  doctest::

        >>> f(staff)
        \new RhythmicStaff {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns RhythmicStaff instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, music=None, context_name='RhythmicStaff', name=None):
        Staff.__init__(
            self,
            music=music,
            context_name=context_name,
            name=name,
            )
