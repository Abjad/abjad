from abjad.tools import durationtools
from abjad.tools.marktools.Mark import Mark


class LilyPondDurationMultiplier(Mark):
    r'''A LilyPond duration multiplier.

    ::

        >>> staff = Staff("c'1 ( d'4 e'4 )")
        >>> multiplier = marktools.LilyPondDurationMultiplier((1, 2))
        >>> attach(multiplier, staff[0])
        >>> show(staff) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_multiplier',
        )

    ### INITIALIZER ###

    def __init__(self, multiplier):
        Mark.__init__(self)
        multiplier = durationtools.Multiplier(multiplier)
        self._multiplier = multiplier

    ### PUBLIC PROPERTIES ###

    @property
    def multiplier(self):
        r'''LilyPond duration multiplier.

        ::

            >>> multiplier.multiplier
            Multiplier(1, 2)

        Returns multiplier.
        '''
        return self._multiplier
