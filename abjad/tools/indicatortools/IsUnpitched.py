# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class IsUnpitched(AbjadValueObject):
    r'''Is unpitched indicator.

    ::

        >>> indicator = indicatortools.IsUnpitched()

    Attach to score selection to denote unpitched music.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()