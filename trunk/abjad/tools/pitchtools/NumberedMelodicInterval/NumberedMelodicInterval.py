# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.NumberedInterval import NumberedInterval


class NumberedMelodicInterval(NumberedInterval):
    '''Abjad model of melodic chromatic interval:

    ::

        >>> mci = pitchtools.NumberedMelodicInterval(-14)
        >>> mci
        NumberedMelodicInterval(-14)

    Melodic chromatic intervals are immutable.
    '''

