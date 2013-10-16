# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.Set import Set


class PitchClassSet(Set):
    '''Abjad model of a pitch-class set.

    ::

        >>> numbered_pitch_class_set = pitchtools.PitchClassSet(
        ...     tokens=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=pitchtools.NumberedPitchClass,
        ...     )
        >>> numbered_pitch_class_set
        PitchClassSet([6, 7, 10, 10.5])

    ::

        >>> named_pitch_class_set = pitchtools.PitchClassSet(
        ...     tokens=['c', 'ef', 'bqs,', 'd'],
        ...     item_class=pitchtools.NamedPitchClass,
        ...     )
        >>> named_pitch_class_set
        PitchClassSet(['c', 'd', 'ef', 'bqs'])

    Return pitch-class set.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __hash__(self):
        return hash(repr(self))

    ### PRIVATE METHODS ###

    def _sort_self(self):
        from abjad.tools import pitchtools
        def helper(x, y):
            return cmp(
                pitchtools.NamedPitch(pitchtools.NamedPitchClass(x), 0),
                pitchtools.NamedPitch(pitchtools.NamedPitchClass(y), 0)
                )
        result = list(self)
        result.sort(helper)
        return result

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
    def from_selection(cls, selection, item_class=None, name=None):
        r'''Initialize pitch-class set from component selection:

        ::

            >>> staff_1 = Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = Staff("c4. r8 g2")
            >>> selection = select((staff_1, staff_2))
            >>> pitchtools.PitchClassSet.from_selection(selection)
            PitchClassSet(['c', 'd', 'fs', 'g', 'a', 'b'])
        
        Return pitch-class set.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return cls(
            tokens=pitch_segment,
            item_class=item_class,
            name=name,
            )

    def invert(self):
        r'''Invert numbered pitch-class set:

        ::

            >>> pitchtools.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     ).invert()
            PitchClassSet([1.5, 2, 5, 6])

        Return numbered pitch-class set.
        '''
        return type(self)([pc.invert() for pc in self])

    def is_transposed_subset(self, pcset):
        r'''True when self is transposed subset of `pcset`.
        False otherwise:

        ::

            >>> pitch_class_set_1 = pitchtools.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     )
            >>> pitch_class_set_2 = pitchtools.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7, 7.5, 8],
            ...     )

        ::

            >>> pitch_class_set_1.is_transposed_subset(pitch_class_set_2)
            True

        Return boolean.
        '''
        for n in range(12):
            if self.transpose(n).issubset(pcset):
                return True
        return False

    def is_transposed_superset(self, pcset):
        r'''True when self is transposed superset of `pcset`.
        False otherwise:

        ::

            >>> pitch_class_set_1 = pitchtools.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     )
            >>> pitch_class_set_2 = pitchtools.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7, 7.5, 8],
            ...     )

        ::

            >>> pitch_class_set_2.is_transposed_superset(pitch_class_set_1)
            True

        Return boolean.
        '''
        for n in range(12):
            if self.transpose(n).issuperset(pcset):
                return True
        return False

    def multiply(self, n):
        r'''Multiply pitch-class set by `n`:

        ::

            >>> pitchtools.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     ).multiply(5)
            PitchClassSet([2, 4.5, 6, 11])

        Return numbered pitch-class set.
        '''
        tokens = (pitch_class.multiply(n) for pitch_class in self)
        return self.new(tokens=tokens)

    def order_by(self, pitch_class_segment):
        from abjad.tools import pitchtools
        from abjad.tools import sequencetools
        if not len(self) == len(pitch_class_segment):
            raise ValueError('set and segment must be of equal length.')
        for pitch_classes in sequencetools.yield_all_permutations_of_sequence(
            tuple(self)):
            candidate_pitch_class_segment = \
                pitchtools.PitchClassSegment(pitch_classes)
            if candidate_pitch_class_segment.is_equivalent_under_transposition(
                pitch_class_segment):
                return candidate_pitch_class_segment
        message = 'named pitch-class set {} can not order by '
        message += 'named pitch-class segment {}.'
        raise ValueError(message.format(self, pitch_class_segment))

    def transpose(self, expr):
        r'''Transpose all pitch classes in self by `expr`.
        '''
        tokens = (pitch_class + expr for pitch_class in self)
        return self.new(tokens=tokens)
