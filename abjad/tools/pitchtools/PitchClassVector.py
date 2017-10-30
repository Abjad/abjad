from abjad.tools.pitchtools.Vector import Vector


class PitchClassVector(Vector):
    '''Pitch-class vector.

    ..  container:: example

        Pitch-class vector:

        >>> vector = abjad.PitchClassVector(
        ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
        ...     item_class=abjad.NumberedPitchClass,
        ...     )

        >>> items = sorted(vector.items())
        >>> for pitch_class, count in items:
        ...     print(pitch_class, count)
        0 1
        1 1
        2 1
        3 1
        4 2
        6 1
        7 1
        9 2
        10 1

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Gets format of pitch-class vector.

        ..  container:: example

            >>> vector = abjad.PitchClassVector(
            ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
            ...     item_class=abjad.NumberedPitchClass,
            ...     )

            >>> abjad.f(vector)
            abjad.PitchClassVector(
                {
                    abjad.NumberedPitchClass(0): 1,
                    abjad.NumberedPitchClass(1): 1,
                    abjad.NumberedPitchClass(2): 1,
                    abjad.NumberedPitchClass(3): 1,
                    abjad.NumberedPitchClass(4): 2,
                    abjad.NumberedPitchClass(6): 1,
                    abjad.NumberedPitchClass(7): 1,
                    abjad.NumberedPitchClass(9): 2,
                    abjad.NumberedPitchClass(10): 1,
                    },
                item_class=abjad.NumberedPitchClass,
                )

        Returns string.
        '''
        superclass = super(PitchClassVector, self)
        return superclass.__format__(format_specification=format_specification)

    def __repr__(self):
        r'''Gets interpreter representation of pitch-class vector.

        ..  container:: example

            Gets interpreter representation of pitch-class vector:

            >>> vector = abjad.PitchClassVector(
            ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
            ...     item_class=abjad.NumberedPitchClass,
            ...     )

            >>> vector
            PitchClassVector({0: 1, 1: 1, 2: 1, 3: 1, 4: 2, 6: 1, 7: 1, 9: 2, 10: 1}, item_class=NumberedPitchClass)

        ..  container:: example

            Initializes from interpreter representation of pitch-class vector:


                >>> abjad.PitchClassVector(vector)
                PitchClassVector({0: 1, 1: 1, 2: 1, 3: 1, 4: 2, 6: 1, 7: 1, 9: 2, 10: 1}, item_class=NumberedPitchClass)

        Returns string.
        '''
        superclass = super(PitchClassVector, self)
        return superclass.__repr__()

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchClass

    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.PitchClass

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        r'''Makes pitch-class vector from `selection`.

        Returns pitch-class vector.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return class_(
            pitch_segment,
            item_class=item_class,
            )
