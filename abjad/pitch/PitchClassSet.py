import copy
from abjad.utilities.Enumerator import Enumerator
from .Set import Set


class PitchClassSet(Set):
    """
    Pitch-class set.

    ..  container:: example

        Initializes numbered pitch-class set:

        >>> numbered_pitch_class_set = abjad.PitchClassSet(
        ...     items=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=abjad.NumberedPitchClass,
        ...     )
        >>> numbered_pitch_class_set
        PitchClassSet([6, 7, 10, 10.5])

    ..  container:: example

        Initializes named pitch-class set:

        >>> named_pitch_class_set = abjad.PitchClassSet(
        ...     items=['c', 'ef', 'bqs,', 'd'],
        ...     item_class=abjad.NamedPitchClass,
        ...     )
        >>> named_pitch_class_set
        PitchClassSet(['c', 'd', 'ef', 'bqs'])

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        """
        Is true when pitch-class set contains `argument`.

        ..  container:: example

            Initializes numbered pitch-class set:

            >>> set_ = abjad.PitchClassSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitchClass,
            ...     )
            >>> set_
            PitchClassSet([6, 7, 10, 10.5])

            >>> abjad.NamedPitch('fs') in set_
            True

            >>> abjad.NamedPitch('f') in set_
            False

            >>> 6 in set_
            True

            >>> 5 in set_
            False

        Returns true or false.
        """
        return super().__contains__(argument)

    def __hash__(self):
        """
        Hashes pitch-class set.

        Returns integer.
        """
        return super().__hash__()

    def __illustrate__(self):
        r"""
        Illustrates pitch-class set.

        ..  container:: example

            Illustrates numbered segment:

            >>> setting = abjad.PitchClassSet([-2, -1.5, 6, 7, -1.5, 7])
            >>> abjad.show(setting) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = setting.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    <fs' g' bf' bqf'>1
                }

        ..  container:: example

            Illustrates named set:

            >>> items = ['c', 'ef', 'bqs,', 'd']
            >>> setting = abjad.PitchClassSet(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> abjad.show(setting) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = setting.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    <c' d' ef' bqs'>1
                }

        ..  container:: example

            Returns LilyPond file:

            >>> prototype = abjad.LilyPondFile
            >>> isinstance(setting.__illustrate__(), prototype)
            True

        """
        import abjad
        chord = abjad.Chord(self, abjad.Duration(1))
        voice = abjad.Voice([chord])
        staff = abjad.Staff([voice])
        score = abjad.Score([staff])
        lilypond_file = abjad.LilyPondFile.new(score)
        return lilypond_file

    def __str__(self):
        """
        Gets string representation of pitch-class set.

        ..  container:: example

            Gets string of set sorted at initialization:

            >>> pc_set = abjad.PitchClassSet([6, 7, 10, 10.5])
            >>> str(pc_set)
            'PC{6, 7, 10, 10.5}'

        ..  container:: example

            Gets string of set not sorted at initialization:

            >>> pc_set = abjad.PitchClassSet([10.5, 10, 7, 6])
            >>> str(pc_set)
            'PC{6, 7, 10, 10.5}'

        Returns string.
        """
        import abjad
        items = [str(_) for _ in sorted(self)]
        separator = ' '
        if self.item_class is abjad.NumberedPitchClass:
            separator = ', '
        return 'PC{{{}}}'.format(separator.join(items))

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

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_most_compact_ordering(candidates):
        import abjad
        widths = []
        for candidate in candidates:
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
            segment = abjad.PitchClassSegment(
                items=segment,
                item_class=abjad.NumberedPitchClass,
                )
            return segment
        for i in range(len(candidates[0]) - 1):
            widths = []
            for candidate in candidates:
                stop = i + 1
                if candidate[0] < candidate[stop]:
                    width = abs(candidate[stop] - candidate[0])
                else:
                    width = abs(candidate[stop] + 12 - candidate[0])
                widths.append(width)
            minimum_width = min(widths)
            candidates_ = []
            for candidate, width in zip(candidates, widths):
                if width == minimum_width:
                    candidates_.append(candidate)
            candidates = candidates_
            if len(candidates) == 1:
                segment = candidates[0]
                segment = abjad.PitchClassSegment(
                    items=segment,
                    item_class=abjad.NumberedPitchClass,
                    )
                return segment
        candidates.sort(key=lambda x: x[0])
        segment = candidates[0]
        segment = abjad.PitchClassSegment(
            items=segment,
            item_class=abjad.NumberedPitchClass,
            )
        return segment

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        """
        Makes pitch-class set from `selection`.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> abjad.PitchClassSet.from_selection(selection)
            PitchClassSet(['c', 'd', 'fs', 'g', 'a', 'b'])

        Returns pitch-class set.
        """
        import abjad
        pitch_segment = abjad.PitchSegment.from_selection(selection)
        return class_(
            items=pitch_segment,
            item_class=item_class,
            )

    def get_normal_order(self):
        """
        Gets normal order.

        ..  container:: example

            Gets normal order of empty pitch-class set:

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_normal_order()
            PitchClassSegment([])

        ..  container:: example

            Gets normal order:

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_normal_order()
            PitchClassSegment([10, 11, 0, 1])

        ..  container:: example

            Gets normal order:

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_normal_order()
            PitchClassSegment([8, 9, 2])

        ..  container:: example

            Gets normal order of pitch-class set with degree of symmetry equal
            to 2:

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_normal_order()
            PitchClassSegment([1, 2, 7, 8])

        ..  container:: example

            Gets normal order of pitch-class set with degree of symmetry equal
            to 4:

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_normal_order()
            PitchClassSegment([0, 3, 6, 9])

        Returns pitch-class segment.
        """
        import abjad
        if not len(self):
            return abjad.PitchClassSegment(
                items=None,
                item_class=abjad.NumberedPitchClass,
                )
        pitch_classes = list(self)
        pitch_classes.sort()
        candidates = []
        for i in range(self.cardinality):
            candidate = [abjad.NumberedPitch(_) for _ in pitch_classes]
            candidate = abjad.sequence(candidate).rotate(n=-i)
            candidates.append(candidate)
        return self._get_most_compact_ordering(candidates)

    def get_prime_form(self, transposition_only=False):
        """
        Gets prime form.

        ..  container:: example

            Gets prime form of empty pitch-class set:

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_prime_form()
            PitchClassSet([])

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([])

        ..  container:: example

            Gets prime form:

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 2, 3])

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 1, 2, 3])

        ..  container:: example

            Gets prime form:

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 6])

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 1, 6])

        ..  container:: example

            Gets prime form of pitch-class set with degree of symmetry equal to
            2:

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 6, 7])

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 1, 6, 7])

        ..  container:: example

            Gets prime form of pitch-class set with degree of symmetry equal to
            4:

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 3, 6, 9])

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 3, 6, 9])

        ..  container:: example

            Gets prime form of pitch-class that is not inversion-equivalent:

            >>> pc_set = abjad.PitchClassSet([0, 4, 6, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 3, 7])

            >>> pc_set = abjad.PitchClassSet([0, 4, 6, 7])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 4, 6, 7])

        ..  container:: example

            Gets prime form of inversionally nonequivalent pitch-class set:

            >>> pc_set = abjad.PitchClassSet([0, 4, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 3, 7])

            >>> pc_set = abjad.PitchClassSet([0, 4, 7])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 4, 7])

        ..  container:: example

            REGRESSION:

            >>> pc_set = abjad.PitchClassSet([0, 1, 2, 5, 8, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 2, 5, 6, 9])

            REGRESSION:

            >>> pc_set = abjad.PitchClassSet([0, 1, 2, 3, 6, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 2, 3, 6, 7])

        Returns new pitch-class set.
        """
        import abjad
        if not len(self):
            return copy.copy(self)
        normal_order = self.get_normal_order()
        if not transposition_only:
            normal_orders = [normal_order]
            inversion = self.invert()
            normal_order = inversion.get_normal_order()
            normal_orders.append(normal_order)
            normal_orders = [_._transpose_to_zero() for _ in normal_orders]
            assert len(normal_orders) == 2
            for left_pc, right_pc in zip(*normal_orders):
                if left_pc == right_pc:
                    continue
                if left_pc < right_pc:
                    normal_order = normal_orders[0]
                    break
                if right_pc < left_pc:
                    normal_order = normal_orders[-1]
                    break
        pcs = [_.number for _ in normal_order]
        first_pc = pcs[0]
        pcs = [pc - first_pc for pc in pcs]
        prime_form = type(self)(
            items=pcs,
            item_class=abjad.NumberedPitchClass,
            )
        return prime_form

    def invert(self, axis=None):
        """
        Inverts pitch-class set.

        ..  container:: example

            >>> abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     ).invert()
            PitchClassSet([1.5, 2, 5, 6])

        Returns numbered pitch-class set.
        """
        return type(self)([pc.invert(axis=axis) for pc in self])

    def is_transposed_subset(self, pcset):
        """
        Is true when pitch-class set is transposed subset of `pcset`.

        ..  container:: example

            >>> pitch_class_set_1 = abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     )
            >>> pitch_class_set_2 = abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7, 7.5, 8],
            ...     )

            >>> pitch_class_set_1.is_transposed_subset(pitch_class_set_2)
            True

        Returns true or false.
        """
        for n in range(12):
            if self.transpose(n).issubset(pcset):
                return True
        return False

    def is_transposed_superset(self, pcset):
        """
        Is true when pitch-class set is transposed superset of `pcset`.

        ..  container:: example

            >>> pitch_class_set_1 = abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     )
            >>> pitch_class_set_2 = abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7, 7.5, 8],
            ...     )

            >>> pitch_class_set_2.is_transposed_superset(pitch_class_set_1)
            True

        Returns true or false.
        """
        for n in range(12):
            if self.transpose(n).issuperset(pcset):
                return True
        return False

    def multiply(self, n):
        """
        Multiplies pitch-class set by `n`.

        ..  container:: example

            >>> abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     ).multiply(5)
            PitchClassSet([2, 4.5, 6, 11])

        Returns new pitch-class set.
        """
        import abjad
        items = (pitch_class.multiply(n) for pitch_class in self)
        return abjad.new(self, items=items)

    def order_by(self, segment):
        """
        Orders pitch-class set by pitch-class `segment`.

        ..  container:: example

            >>> set_ = abjad.PitchClassSet(['c', 'e', 'b'])
            >>> segment = abjad.PitchClassSegment(['e', 'a', 'f'])
            >>> set_.order_by(segment)
            PitchClassSegment("b e c")

        Returns pitch-class segment.
        """
        import abjad
        if not len(self) == len(segment):
            message = 'set and segment must be on equal length.'
            raise ValueError(message)
        enumerator = Enumerator(self)
        for pitch_classes in enumerator.yield_permutations():
            candidate = abjad.PitchClassSegment(pitch_classes)
            if candidate._is_equivalent_under_transposition(segment):
                return candidate
        message = '{!s} can not order by {!s}.'
        message = message.format(self, segment)
        raise ValueError(message)

    def transpose(self, n=0):
        """
        Transposes all pitch-classes in pitch-class set by index `n`.

        ..  container:: example

            >>> set_ = abjad.PitchClassSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitchClass,
            ...     )

            >>> for n in range(12):
            ...     print(n, set_.transpose(n))
            ...
            0 PC{6, 7, 10, 10.5}
            1 PC{7, 8, 11, 11.5}
            2 PC{0, 0.5, 8, 9}
            3 PC{1, 1.5, 9, 10}
            4 PC{2, 2.5, 10, 11}
            5 PC{0, 3, 3.5, 11}
            6 PC{0, 1, 4, 4.5}
            7 PC{1, 2, 5, 5.5}
            8 PC{2, 3, 6, 6.5}
            9 PC{3, 4, 7, 7.5}
            10 PC{4, 5, 8, 8.5}
            11 PC{5, 6, 9, 9.5}

        Returns new pitch-class set.
        """
        import abjad
        items = (pitch_class + n for pitch_class in self)
        return abjad.new(self, items=items)
