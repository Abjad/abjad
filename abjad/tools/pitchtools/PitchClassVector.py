from abjad.tools.pitchtools.Vector import Vector


class PitchClassVector(Vector):
    '''A pitch-class vector.

    ..  container:: example

        ::

            >>> vector = pitchtools.PitchClassVector(
            ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
            ...     item_class=pitchtools.NumberedPitchClass,
            ...     )

        ::
            
            >>> items = list(vector.items())
            >>> items.sort(key=lambda x: x[0].pitch_class_number)
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

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of pitch-class vector.

        ..  container:: example

            **Example 1.** Gets interpreter representation of pitch-class
            vector:

            ::

                >>> vector = pitchtools.PitchClassVector(
                ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
                ...     item_class=pitchtools.NumberedPitchClass,
                ...     )

            ::

                >>> vector
                PitchClassVector({'0': 1, '1': 1, '10': 1, '2': 1, '3': 1, '4': 2, '6': 1, '7': 1, '9': 2}, item_class=NumberedPitchClass)

        ..  container:: example

            **Example 2.** Initializes from interpreter representation of
            pitch-class vector:


                >>> pitchtools.PitchClassVector(vector)
                PitchClassVector({'0': 1, '1': 1, '10': 1, '2': 1, '3': 1, '4': 2, '6': 1, '7': 1, '9': 2}, item_class=NumberedPitchClass)

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
        cls,
        selection,
        item_class=None,
        ):
        r'''Makes pitch-class vector from `selection`.

        Returns pitch-class vector.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return cls(
            pitch_segment,
            item_class=item_class,
            )