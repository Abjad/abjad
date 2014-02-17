# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class Tuning(AbjadObject):
    r'''Tuning indicator.

    ::

        >>> indicator = indicatortools.Tuning(
        ...     pitches=('G3', 'D4', 'A4', 'E5'),
        ...     )
        >>> print format(indicator)
        indicatortools.Tuning(
            pitches=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('g'),
                    pitchtools.NamedPitch("d'"),
                    pitchtools.NamedPitch("a'"),
                    pitchtools.NamedPitch("e''"),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitches',
        )

    ### INITIALIZER ###

    def __init__(self,
        pitches=None,
        ):
        from abjad.tools import pitchtools
        if pitches is not None:
            if isinstance(pitches, type(self)):
                pitches = pitches.pitches
            else:
                pitches = pitchtools.PitchSegment(
                    items=pitches,
                    item_class=pitchtools.NamedPitch,
                    )
        self._pitches = pitches

    ### PUBLIC PROPERTIES ###

    @property
    def pitches(self):
        r'''Gets tuning pitches.

        ::

            >>> pitches = indicator.pitches
            >>> print format(pitches)
            pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('g'),
                    pitchtools.NamedPitch("d'"),
                    pitchtools.NamedPitch("a'"),
                    pitchtools.NamedPitch("e''"),
                    ),
                item_class=pitchtools.NamedPitch,
                )

        Return pitch segment.
        '''
        return self._pitches
