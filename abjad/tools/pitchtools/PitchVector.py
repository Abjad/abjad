# -*- coding: utf-8 -*-
from abjad.tools.pitchtools.Vector import Vector


class PitchVector(Vector):
    r'''Pitch vector.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> vector = abjad.PitchVector(
            ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
            ...     item_class=abjad.NumberedPitch,
            ...     )

        ::

            >>> items = list(vector.items())
            >>> items.sort(key=lambda x: x[0].number)
            >>> for pitch_class, count in items:
            ...     print(pitch_class, count)
            -3 2
            -2 1
            0 1
            1 1
            6 1
            7 1
            14 1
            15 1
            16 2

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of pitch vector.

        ..  container:: example

            Gets interpreter representation of pitch vector:
            ::

                >>> vector = abjad.PitchVector(
                ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
                ...     item_class=abjad.NumberedPitch,
                ...     )

            ::

                >>> vector
                PitchVector({-3: 2, -2: 1, 0: 1, 1: 1, 6: 1, 7: 1, 14: 1, 15: 1, 16: 2}, item_class=NumberedPitch)

        ..  container:: example

            Initializes from interpreter representation of pitch vector:

                >>> abjad.PitchVector(vector)
                PitchVector({-3: 2, -2: 1, 0: 1, 1: 1, 6: 1, 7: 1, 14: 1, 15: 1, 16: 2}, item_class=NumberedPitch)

        Returns string.
        '''
        superclass = super(PitchVector, self)
        return superclass.__repr__()

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedPitch

    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitch

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.Pitch

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        r'''Makes pitch vector from `selection`.

        Returns pitch vector.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return class_(
            pitch_segment,
            item_class=item_class,
            )
