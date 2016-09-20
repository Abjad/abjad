# -*- coding: utf-8 -*-
from abjad.tools.pitchtools.Vector import Vector


class PitchClassVector(Vector):
    '''Pitch-class vector.

    ..  container:: example

        **Example 1.**

        ::

            >>> vector = pitchtools.PitchClassVector(
            ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
            ...     item_class=pitchtools.NumberedPitchClass,
            ...     )

        ::

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

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Gets format of pitch-class vector.

        ..  container:: example

            ::

                >>> vector = pitchtools.PitchClassVector(
                ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
                ...     item_class=pitchtools.NumberedPitchClass,
                ...     )

            ::

                >>> print(format(vector))
                pitchtools.PitchClassVector(
                    {
                        pitchtools.NumberedPitchClass(0): 1,
                        pitchtools.NumberedPitchClass(1): 1,
                        pitchtools.NumberedPitchClass(2): 1,
                        pitchtools.NumberedPitchClass(3): 1,
                        pitchtools.NumberedPitchClass(4): 2,
                        pitchtools.NumberedPitchClass(6): 1,
                        pitchtools.NumberedPitchClass(7): 1,
                        pitchtools.NumberedPitchClass(9): 2,
                        pitchtools.NumberedPitchClass(10): 1,
                        },
                    item_class=pitchtools.NumberedPitchClass,
                    )

        Returns string.
        '''
        superclass = super(PitchClassVector, self)
        return superclass.__format__(format_specification=format_specification)

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
                PitchClassVector({0: 1, 1: 1, 2: 1, 3: 1, 4: 2, 6: 1, 7: 1, 9: 2, 10: 1}, item_class=NumberedPitchClass)

        ..  container:: example

            **Example 2.** Initializes from interpreter representation of
            pitch-class vector:


                >>> pitchtools.PitchClassVector(vector)
                PitchClassVector({0: 1, 1: 1, 2: 1, 3: 1, 4: 2, 6: 1, 7: 1, 9: 2, 10: 1}, item_class=NumberedPitchClass)

        Returns string.
        '''
        superclass = super(PitchClassVector, self)
        return superclass.__repr__()

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
