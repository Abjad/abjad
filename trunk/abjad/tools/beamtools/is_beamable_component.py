from abjad.tools import chordtools
from abjad.tools import durationtools
from abjad.tools import notetools


def is_beamable_component(expr):
    '''.. versionadded:: 1.1

    True when `expr` is a beamable component. Otherwise false:

    ::

        >>> staff = Staff(r"r32 a'32 ( [ gs'32 fs''32 \staccato f''8 ) ]")
        >>> staff.extend(r"r8 e''8 ( ef'2 )")

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> for leaf in staff.leaves:
        ...     result = beamtools.is_beamable_component(leaf)
        ...     print '{:<8}{}'.format(leaf, result)
        ...
        r32     False
        a'32    True
        gs'32   True
        fs''32  True
        f''8    True
        r8      False
        e''8    True
        ef'2    False

    Return boolean.
    '''

    if isinstance(expr, (notetools.Note, chordtools.Chord)):
        if 0 < expr.written_duration.flag_count:
            return True
    return False
