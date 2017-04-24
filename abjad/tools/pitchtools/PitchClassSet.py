# -*- coding: utf-8 -*-
import copy
from abjad.tools import mathtools
from abjad.tools.pitchtools.Set import Set
from abjad.tools.topleveltools import new


class PitchClassSet(Set):
    '''Pitch-class set.

    ..  container:: example

        Initializes numbered pitch-class set:

        ::

            >>> numbered_pitch_class_set = PitchClassSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=NumberedPitchClass,
            ...     )
            >>> numbered_pitch_class_set
            PitchClassSet([6, 7, 10, 10.5])

    ..  container:: example

        Initializes named pitch-class set:

        ::

            >>> named_pitch_class_set = PitchClassSet(
            ...     items=['c', 'ef', 'bqs,', 'd'],
            ...     item_class=NamedPitchClass,
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

    def __illustrate__(self):
        r'''Illustrates pitch-class set.

        ..  container:: example

            Illustrates numbered segment:

            ::

                >>> set_ = PitchClassSet([-2, -1.5, 6, 7, -1.5, 7])
                >>> show(set_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = set_.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    <fs' g' bf' bqf'>1
                }

        ..  container:: example

            Illustrates named set:

            ::

                >>> items = ['c', 'ef', 'bqs,', 'd']
                >>> set_ = PitchClassSet(
                ...     items=items,
                ...     item_class=NamedPitchClass,
                ...     )
                >>> show(set_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = set_.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    <c' d' ef' bqs'>1
                }

        ..  container:: example

            Returns LilyPond file:

            ::

                >>> prototype = lilypondfiletools.LilyPondFile
                >>> isinstance(set_.__illustrate__(), prototype)
                True

        '''
        import abjad
        chord = abjad.Chord(self, abjad.Duration(1))
        voice = abjad.Voice([chord])
        staff = abjad.Staff([voice])
        score = abjad.Score([staff])
        lilypond_file = abjad.LilyPondFile.new(score)
        lilypond_file.header_block.tagline = False
        return lilypond_file

    def __str__(self):
        r'''Gets string representation of pitch-class set.

        ..  container:: example

            Gets string of set sorted at initialization:

            ::

                >>> pc_set = PitchClassSet([6, 7, 10, 10.5])
                >>> str(pc_set)
                'PC{6, 7, 10, 10.5}'

        ..  container:: example

            Gets string of set not sorted at initialization:

            ::

                >>> pc_set = PitchClassSet([10.5, 10, 7, 6])
                >>> str(pc_set)
                'PC{6, 7, 10, 10.5}'

        Returns string.
        '''
        import abjad
        items = [str(_) for _ in sorted(self)]
        separator = ' '
        if self.item_class is abjad.NumberedPitchClass:
            separator = ', '
        return 'PC{{{}}}'.format(separator.join(items))

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

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_most_compact_ordering(candidates):
        from abjad.tools import pitchtools
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
            segment = pitchtools.PitchClassSegment(
                items=segment,
                item_class=pitchtools.NumberedPitchClass,
                )
            return segment
        for i in range(len(candidates[0]) - 1):
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
            >>> PitchClassSet.from_selection(selection)
            PitchClassSet(['c', 'd', 'fs', 'g', 'a', 'b'])

        Returns pitch-class set.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return class_(
            items=pitch_segment,
            item_class=item_class,
            )

    def get_normal_order(self):
        r'''Gets normal order.

        ..  container:: example

            Gets normal order of empty pitch-class set:

            ::

                >>> pc_set = PitchClassSet()
                >>> pc_set.get_normal_order()
                PitchClassSegment([])

        ..  container:: example

            Gets normal order:

            ::

                >>> pc_set = PitchClassSet([0, 1, 10, 11])
                >>> pc_set.get_normal_order()
                PitchClassSegment([10, 11, 0, 1])

        ..  container:: example

            Gets normal order:

            ::

                >>> pc_set = PitchClassSet([2, 8, 9])
                >>> pc_set.get_normal_order()
                PitchClassSegment([8, 9, 2])

        ..  container:: example

            Gets normal order of pitch-class set with degree of symmetry equal
            to 2:

            ::

                >>> pc_set = PitchClassSet([1, 2, 7, 8])
                >>> pc_set.get_normal_order()
                PitchClassSegment([1, 2, 7, 8])

        ..  container:: example

            Gets normal order of pitch-class set with degree of symmetry equal
            to 4:

            ::

                >>> pc_set = PitchClassSet([0, 3, 6, 9])
                >>> pc_set.get_normal_order()
                PitchClassSegment([0, 3, 6, 9])

        Returns pitch-class segment.
        '''
        from abjad.tools import pitchtools
        from abjad.tools import sequencetools
        if not len(self):
            return pitchtools.PitchClassSegment(
                items=None,
                item_class=pitchtools.NumberedPitchClass,
                )
        pitch_classes = list(self)
        pitch_classes.sort()
        candidates = []
        for i in range(self.cardinality):
            candidate = [pitchtools.NumberedPitch(_) for _ in pitch_classes]
            candidate = sequencetools.Sequence(candidate).rotate(n=-i)
            candidates.append(candidate)
        return self._get_most_compact_ordering(candidates)

    def get_prime_form(self, transposition_only=False):
        r'''Gets prime form.

        ..  container:: example

            Gets prime form of empty pitch-class set:

            ::

                >>> pc_set = PitchClassSet()
                >>> pc_set.get_prime_form()
                PitchClassSet([])

            ::

                >>> pc_set = PitchClassSet()
                >>> pc_set.get_prime_form(transposition_only=True)
                PitchClassSet([])

        ..  container:: example

            Gets prime form:

            ::

                >>> pc_set = PitchClassSet([0, 1, 10, 11])
                >>> pc_set.get_prime_form()
                PitchClassSet([0, 1, 2, 3])

            ::

                >>> pc_set = PitchClassSet([0, 1, 10, 11])
                >>> pc_set.get_prime_form(transposition_only=True)
                PitchClassSet([0, 1, 2, 3])

        ..  container:: example

            Gets prime form:

            ::

                >>> pc_set = PitchClassSet([2, 8, 9])
                >>> pc_set.get_prime_form()
                PitchClassSet([0, 1, 6])

            ::

                >>> pc_set = PitchClassSet([2, 8, 9])
                >>> pc_set.get_prime_form(transposition_only=True)
                PitchClassSet([0, 1, 6])

        ..  container:: example

            Gets prime form of pitch-class set with degree of symmetry equal to
            2:

            ::

                >>> pc_set = PitchClassSet([1, 2, 7, 8])
                >>> pc_set.get_prime_form()
                PitchClassSet([0, 1, 6, 7])

            ::

                >>> pc_set = PitchClassSet([1, 2, 7, 8])
                >>> pc_set.get_prime_form(transposition_only=True)
                PitchClassSet([0, 1, 6, 7])

        ..  container:: example

            Gets prime form of pitch-class set with degree of symmetry equal to
            4:

            ::

                >>> pc_set = PitchClassSet([0, 3, 6, 9])
                >>> pc_set.get_prime_form()
                PitchClassSet([0, 3, 6, 9])

            ::

                >>> pc_set = PitchClassSet([0, 3, 6, 9])
                >>> pc_set.get_prime_form(transposition_only=True)
                PitchClassSet([0, 3, 6, 9])

        ..  container:: example

            Gets prime form of pitch-class that is not inversion-equivalent:

            ::

                >>> pc_set = PitchClassSet([0, 4, 6, 7])
                >>> pc_set.get_prime_form()
                PitchClassSet([0, 1, 3, 7])

            ::

                >>> pc_set = PitchClassSet([0, 4, 6, 7])
                >>> pc_set.get_prime_form(transposition_only=True)
                PitchClassSet([0, 4, 6, 7])

        Returns new pitch-class set.
        '''
        from abjad.tools import pitchtools
        if not len(self):
            return copy.copy(self)
        normal_orders = [self.get_normal_order()]
        if not transposition_only:
            inversion = self.invert()
            normal_order = inversion.get_normal_order()
            normal_orders.append(normal_order)
        normal_order = self._get_most_compact_ordering(normal_orders)
        pcs = [int(_) for _ in normal_order]
        first_pc = pcs[0]
        pcs = [pc - first_pc for pc in pcs]
        prime_form = type(self)(
            items=pcs,
            item_class=pitchtools.NumberedPitchClass,
            )
        return prime_form

    def invert(self, axis=None):
        r'''Inverts pitch-class set.

        ::

            >>> PitchClassSet(
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

            >>> pitch_class_set_1 = PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     )
            >>> pitch_class_set_2 = PitchClassSet(
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

            >>> pitch_class_set_1 = PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     )
            >>> pitch_class_set_2 = PitchClassSet(
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

            >>> PitchClassSet(
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
        enumeration = sequencetools.Enumeration(self)
        for pitch_classes in enumeration.yield_permutations():
            candidate_pitch_class_segment = \
                pitchtools.PitchClassSegment(pitch_classes)
            if candidate_pitch_class_segment._is_equivalent_under_transposition(
                pitch_class_segment):
                return candidate_pitch_class_segment
        message = 'named pitch-class set {} can not order by '
        message += 'named pitch-class segment {}.'
        message = message.format(self, pitch_class_segment)
        raise ValueError(message)

    def transpose(self, n=0):
        r'''Transposes all pitch-classes in pitch-class set by index `n`.

        Returns new pitch-class set.
        '''
        items = (pitch_class + n for pitch_class in self)
        return new(self, items=items)

    @staticmethod
    def yield_all_pitch_class_sets():
        '''Yields all pitch-class sets.

        ..  container:: example

            Yields all pitch-class sets:

            ::


                >>> class_ = PitchClassSet
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
