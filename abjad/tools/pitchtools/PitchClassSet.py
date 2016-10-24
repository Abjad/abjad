# -*- coding: utf-8 -*-
import copy
from abjad.tools import mathtools
from abjad.tools.pitchtools.Set import Set
from abjad.tools.topleveltools import new


class PitchClassSet(Set):
    '''Pitch-class set.

    ..  container:: example

        **Example 1.** Initializes numbered pitch-class set:

        ::

            >>> numbered_pitch_class_set = pitchtools.PitchClassSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=pitchtools.NumberedPitchClass,
            ...     )
            >>> numbered_pitch_class_set
            PitchClassSet([6, 7, 10, 10.5])

    ..  container:: example

        **Example 2.** Initializes named pitch-class set:

        ::

            >>> named_pitch_class_set = pitchtools.PitchClassSet(
            ...     items=['c', 'ef', 'bqs,', 'd'],
            ...     item_class=pitchtools.NamedPitchClass,
            ...     )
            >>> named_pitch_class_set
            PitchClassSet(['c', 'd', 'ef', 'bqs'])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __hash__(self):
        r'''Hashes pitch-class set.

        Returns integer.
        '''
        return hash(repr(self))

    def __str__(self):
        r'''Gets string representation of pitch-class set.

        ..  container:: example

            **Example 1.** Gets string of set sorted at initialization:

            ::

                >>> pc_set = pitchtools.PitchClassSet([6, 7, 10, 10.5])
                >>> str(pc_set)
                '{6, 7, 10, 10.5}'

        ..  container:: example

            **Example 2.** Gets string of set not sorted at initialization:

            ::

                >>> pc_set = pitchtools.PitchClassSet([10.5, 10, 7, 6])
                >>> str(pc_set)
                '{6, 7, 10, 10.5}'

        Returns string.
        '''
        superclass = super(PitchClassSet, self)
        return superclass.__str__()

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

    ### PUBLIC PROPERTIES ###

    @property
    def normal_order(self):
        r'''Gets normal order.

        ..  container:: example

            **Example 1.** Gets normal order:

            ::

                >>> pc_set = pitchtools.PitchClassSet([0, 1, 10, 11])
                >>> pc_set.normal_order
                PitchClassSegment([10, 11, 0, 1])

        ..  container:: example

            **Example 2.** Gets normal order:

            ::

                >>> pc_set = pitchtools.PitchClassSet([2, 8, 9])
                >>> pc_set.normal_order
                PitchClassSegment([8, 9, 2])

        ..  container:: example

            **Example 3.** Gets normal order of pitch-class set with degree of
            symmetry equal to 2:

            ::

                >>> pc_set = pitchtools.PitchClassSet([1, 2, 7, 8])
                >>> pc_set.normal_order
                PitchClassSegment([1, 2, 7, 8])

        ..  container:: example

            **Example 4.** Gets normal order of pitch-class set with degree of
            symmetry equal to 4:

            ::

                >>> pc_set = pitchtools.PitchClassSet([0, 3, 6, 9])
                >>> pc_set.normal_order
                PitchClassSegment([0, 3, 6, 9])

        Returns pitch-class segment.
        '''
        from abjad.tools import pitchtools
        from abjad.tools import sequencetools
        pitch_classes = list(self)
        pitch_classes.sort()
        candidates = []
        widths = []
        for i in range(self.cardinality):
            candidate = [pitchtools.NumberedPitch(_) for _ in pitch_classes]
            candidate = sequencetools.rotate_sequence(candidate, -i)
            candidates.append(candidate)
            if candidate[0] < candidate[-1]:
                width = abs(candidate[-1] - candidate[0])
            else:
                width = abs(candidate[-1] + 12 - candidate[0])
            widths.append(width)
        minimum_width = min(widths)
        candidates_ = []
        for candidate, width in zip(candidates, widths):
            if width == minimum_width:
                candidates_.append(candidate)
        candidates = candidates_
        assert 1 <= len(candidates)
        if len(candidates) == 1:
            segment = candidates[0]
            segment = pitchtools.PitchClassSegment(
                items=segment,
                item_class=pitchtools.NumberedPitchClass,
                )
            return segment
        for i in range(self.cardinality - 1):
            widths = []
            for candidate in candidates:
                if candidate[0] < candidate[i+1]:
                    width = abs(candidate[i+1] - candidate[0])
                else:
                    width = abs(candidate[i+1] + 12 - candidate[0])
                widths.append(width)
            minimum_width = min(widths)
            candidates_ = []
            for candidate, width in zip(candidates, widths):
                if width == minimum_width:
                    candidates_.append(candidate)
            candidates = candidates_
            if len(candidates) == 1:
                segment = candidates[0]
                segment = pitchtools.PitchClassSegment(
                    items=segment,
                    item_class=pitchtools.NumberedPitchClass,
                    )
                return segment
        candidates.sort(key=lambda x: x[0])
        segment = candidates[0]
        segment = pitchtools.PitchClassSegment(
            items=segment,
            item_class=pitchtools.NumberedPitchClass,
            )
        return segment

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        r'''Makes pitch-class set from `selection`.

        ::

            >>> staff_1 = Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = Staff("c4. r8 g2")
            >>> selection = select((staff_1, staff_2))
            >>> pitchtools.PitchClassSet.from_selection(selection)
            PitchClassSet(['c', 'd', 'fs', 'g', 'a', 'b'])

        Returns pitch-class set.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return class_(
            items=pitch_segment,
            item_class=item_class,
            )

    def invert(self, axis=None):
        r'''Inverts pitch-class set.

        ::

            >>> pitchtools.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     ).invert()
            PitchClassSet([1.5, 2, 5, 6])

        Returns numbered pitch-class set.
        '''
        return type(self)([pc.invert(axis=axis) for pc in self])

    def is_transposed_subset(self, pcset):
        r'''Is true when pitch-class set is transposed subset of `pcset`.
        Otherwise false:

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

        Returns true or false.
        '''
        for n in range(12):
            if self.transpose(n).issubset(pcset):
                return True
        return False

    def is_transposed_superset(self, pcset):
        r'''Is true when pitch-class set is transposed superset of `pcset`.
        Otherwise false:

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

        Returns true or false.
        '''
        for n in range(12):
            if self.transpose(n).issuperset(pcset):
                return True
        return False

    def multiply(self, n):
        r'''Multiplies pitch-class set by `n`.

        ::

            >>> pitchtools.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     ).multiply(5)
            PitchClassSet([2, 4.5, 6, 11])

        Returns new pitch-class set.
        '''
        items = (pitch_class.multiply(n) for pitch_class in self)
        return new(self, items=items)

    def order_by(self, pitch_class_segment):
        r'''Orders pitch-class set by `pitch_class_segment`.

        Returns pitch-class segment.
        '''
        from abjad.tools import pitchtools
        from abjad.tools import sequencetools
        if not len(self) == len(pitch_class_segment):
            message = 'set and segment must be on equal length.'
            raise ValueError(message)
        for pitch_classes in sequencetools.yield_all_permutations_of_sequence(
            tuple(self)):
            candidate_pitch_class_segment = \
                pitchtools.PitchClassSegment(pitch_classes)
            if candidate_pitch_class_segment.is_equivalent_under_transposition(
                pitch_class_segment):
                return candidate_pitch_class_segment
        message = 'named pitch-class set {} can not order by '
        message += 'named pitch-class segment {}.'
        message = message.format(self, pitch_class_segment)
        raise ValueError(message)

    def transpose(self, expr):
        r'''Transposes all pitch-classes in pitch-class set by `expr`.

        Returns new pitch-class set.
        '''
        items = (pitch_class + expr for pitch_class in self)
        return new(self, items=items)

    @staticmethod
    def yield_all_pitch_class_sets():
        '''Yields all pitch-class sets.

        ..  container:: example

            **Example 1.** Yields all pitch-class sets:

            ::


                >>> class_ = pitchtools.PitchClassSet
                >>> pcsets = list(class_.yield_all_pitch_class_sets())
                >>> len(pcsets)
                4096

            ::

                >>> for pcset in pcsets[:20]:
                ...   pcset
                PitchClassSet([])
                PitchClassSet([0])
                PitchClassSet([1])
                PitchClassSet([0, 1])
                PitchClassSet([2])
                PitchClassSet([0, 2])
                PitchClassSet([1, 2])
                PitchClassSet([0, 1, 2])
                PitchClassSet([3])
                PitchClassSet([0, 3])
                PitchClassSet([1, 3])
                PitchClassSet([0, 1, 3])
                PitchClassSet([2, 3])
                PitchClassSet([0, 2, 3])
                PitchClassSet([1, 2, 3])
                PitchClassSet([0, 1, 2, 3])
                PitchClassSet([4])
                PitchClassSet([0, 4])
                PitchClassSet([1, 4])
                PitchClassSet([0, 1, 4])

        There are 4096 pitch-class sets.

        This is ``U*`` in [Morris 1987].

        Returns generator.
        '''
        from abjad.tools import pitchtools
        def _helper(binary_string):
            result = zip(binary_string, range(len(binary_string)))
            result = [string[1] for string in result if string[0] == '1']
            return result
        for i in range(4096):
            string = mathtools.integer_to_binary_string(i).zfill(12)
            subset = ''.join(list(reversed(string)))
            subset = _helper(subset)
            subset = pitchtools.PitchClassSet(
                subset,
                item_class=pitchtools.NumberedPitchClass,
                )
            yield subset
