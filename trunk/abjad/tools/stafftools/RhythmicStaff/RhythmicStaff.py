from abjad.tools.stafftools.Staff import Staff


class RhythmicStaff(Staff):
    r'''Abjad model of a rhythmic staff:

    ::

        >>> staff = stafftools.RhythmicStaff("c'8 d'8 e'8 f'8")

    ::

        >>> f(staff)
        \new RhythmicStaff {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Return RhythmicStaff instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, music=None, context_name='RhythmicStaff', name=None):
        Staff.__init__(self, music=music, context_name=context_name, name=name)
