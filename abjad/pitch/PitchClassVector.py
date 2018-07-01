from .Vector import Vector


class PitchClassVector(Vector):
    """
    Pitch-class vector.

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

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        """
        Gets format of pitch-class vector.

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
        """
        return super().__format__(format_specification=format_specification)

    def __repr__(self):
        """
        Gets interpreter representation of pitch-class vector.

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
        """
        return super().__repr__()

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        import abjad
        return abjad.NamedPitchClass

    @property
    def _numbered_item_class(self):
        import abjad
        return abjad.NumberedPitchClass

    @property
    def _parent_item_class(self):
        import abjad
        return abjad.PitchClass

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        """
        Makes pitch-class vector from `selection`.

        Returns pitch-class vector.
        """
        import abjad
        pitch_segment = abjad.PitchSegment.from_selection(selection)
        return class_(
            pitch_segment,
            item_class=item_class,
            )
