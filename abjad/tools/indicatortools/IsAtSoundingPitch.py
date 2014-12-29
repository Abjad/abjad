# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class IsAtSoundingPitch(AbjadValueObject):
    r'''Is at sounding pitch indicator.

    ::

        >>> indicator = indicatortools.IsAtSoundingPitch()

    Attach to score selection to denote music written at sounding pitch.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()