# -*- coding: utf-8 -*-
import collections
from abjad.tools import pitchtools
from abjad.tools.abctools import AbjadValueObject


class PitchSelectorCallback(AbjadValueObject):
    r'''Pitch selector callback.

    ::

        >>> import abjad

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_pitches',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pitches=None,
        ):
        if pitches is not None:
            if not isinstance(pitches, collections.Iterable):
                pitches = [pitches]
            pitches = pitchtools.PitchSet(
                items=pitches,
                item_class=pitchtools.NumberedPitch,
                )
        self._pitches = pitches

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Iterates tuple `argument`.

        Returns tuple in which each item is a selection or component.
        '''
        if not self.pitches:
            return ()
        result = []
        for subexpr in argument:
            pitch_set = pitchtools.PitchSet.from_selection(
                subexpr,
                item_class=pitchtools.NumberedPitch,
                )
            if self.pitches.intersection(pitch_set):
                result.append(subexpr)
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def pitches(self):
        r'''Gets pitch set of pitch selector callback.

        Returns pitch set.
        '''
        return self._pitches
