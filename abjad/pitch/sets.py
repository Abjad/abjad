import abc
import collections
import copy
import types

from .. import enumerate
from ..expression import Expression
from ..new import new
from ..sequence import Sequence
from ..storage import FormatSpecification
from ..typedcollections import TypedCollection, TypedFrozenset
from .intervalclasses import IntervalClass, NamedIntervalClass, NumberedIntervalClass
from .intervals import Interval, NamedInterval, NumberedInterval
from .pitchclasses import NamedPitchClass, NumberedPitchClass, PitchClass
from .pitches import NamedPitch, NumberedPitch, Pitch
from .segments import PitchClassSegment, PitchSegment


class Set(TypedFrozenset):
    """
    Abstract set.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_expression",)

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, (collections.abc.Iterator, types.GeneratorType)):
            items = [item for item in items]
        if item_class is None:
            item_class = self._named_item_class
            if items is not None:
                if isinstance(items, TypedCollection) and issubclass(
                    items.item_class, self._parent_item_class
                ):
                    item_class = items.item_class
                elif len(items):
                    if isinstance(items, collections.abc.Set):
                        items = tuple(items)
                    if isinstance(items[0], str):
                        item_class = self._named_item_class
                    elif isinstance(items[0], (int, float)):
                        item_class = self._numbered_item_class
                    elif isinstance(items[0], self._parent_item_class):
                        item_class = type(items[0])
        assert issubclass(item_class, self._parent_item_class)
        TypedFrozenset.__init__(self, items=items, item_class=item_class)
        self._expression = None

    ### SPECIAL METHODS ###

    def __str__(self):
        """
        Gets string representation.

        Returns string.
        """
        items = self._get_sorted_repr_items()
        items = [str(_) for _ in items]
        string = ", ".join(items)
        return f"{{{string}}}"

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _named_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _numbered_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _parent_item_class(self):
        raise NotImplementedError

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        repr_items = self._get_sorted_repr_items()
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_args_values=[repr_items],
            storage_format_args_values=[repr_items],
            storage_format_keyword_names=[],
        )

    def _get_sorted_repr_items(self):
        items = sorted(self, key=lambda x: (float(x.number), str(x)))
        if self.item_class.__name__.startswith("Named"):
            repr_items = [str(x) for x in items]
        elif hasattr(self.item_class, "number"):
            repr_items = [x.number for x in items]
        elif hasattr(self.item_class, "pitch_class_number"):
            repr_items = [x.pitch_class_number for x in items]
        elif hasattr(self.item_class, "__abs__"):
            repr_items = [abs(x) for x in items]
        else:
            raise ValueError(f"invalid item class: {self.item_class!r}.")
        return repr_items

    def _sort_self(self):
        return tuple(self)

    ### PUBLIC PROPERTIES ###

    @property
    def cardinality(self):
        """
        Gets cardinality of set.

        Defined equal to length of set.

        Returns nonnegative integer.
        """
        return len(self)

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes set from ``selection``.

        Returns set.
        """
        raise NotImplementedError


class IntervalClassSet(Set):
    """
    Interval-class set.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        prototype = (
            PitchClassSegment,
            PitchSegment,
            PitchClassSet,
            PitchSet,
        )
        if isinstance(items, prototype):
            items = list(items)
            pairs = enumerate.yield_pairs(items)
            items = [second - first for first, second in pairs]
        super().__init__(items=items, item_class=item_class)

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedIntervalClass

    @property
    def _numbered_item_class(self):
        return NumberedIntervalClass

    @property
    def _parent_item_class(self):
        return IntervalClass

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        r"""
        Initialize interval set from component selection:

        ..  container:: example

            ::

                >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
                >>> staff_2 = abjad.Staff("c4. r8 g2")
                >>> staff_group = abjad.StaffGroup([staff_1, staff_2])
                >>> abjad.show(staff_group) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new StaffGroup
                <<
                    \new Staff
                    {
                        c'4
                        <d' fs' a'>4
                        b2
                    }
                    \new Staff
                    {
                        c4.
                        r8
                        g2
                    }
                >>

            ::

                >>> selection = abjad.select(staff_group)
                >>> interval_classes = abjad.IntervalClassSet.from_selection(selection)
                >>> for interval_class in sorted(interval_classes):
                ...     interval_class
                ...
                NamedIntervalClass('-M6')
                NamedIntervalClass('-P5')
                NamedIntervalClass('-A4')
                NamedIntervalClass('-M3')
                NamedIntervalClass('-m3')
                NamedIntervalClass('-M2')
                NamedIntervalClass('+m2')
                NamedIntervalClass('+M2')
                NamedIntervalClass('+m3')
                NamedIntervalClass('+M3')
                NamedIntervalClass('+P4')
                NamedIntervalClass('+A4')
                NamedIntervalClass('+P5')
                NamedIntervalClass('+M6')
                NamedIntervalClass('+m7')
                NamedIntervalClass('+M7')
                NamedIntervalClass('+P8')

        Returns interval set.
        """
        interval_set = IntervalSet.from_selection(selection)
        return class_(items=interval_set, item_class=item_class)


class IntervalSet(Set):
    """
    Interval set.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        prototype = (
            PitchClassSegment,
            PitchClassSet,
            PitchSegment,
            PitchSet,
        )
        if isinstance(items, prototype):
            items = list(items)
            pairs = enumerate.yield_pairs(items)
            items = [second - first for first, second in pairs]
        super().__init__(items=items, item_class=item_class)

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedInterval

    @property
    def _numbered_item_class(self):
        return NumberedInterval

    @property
    def _parent_item_class(self):
        return Interval

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Initializes interval set from component selection.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> intervals = abjad.IntervalSet.from_selection(selection)
            >>> for interval in sorted(intervals):
            ...     interval
            ...
            NamedInterval('-M6')
            NamedInterval('-P5')
            NamedInterval('-A4')
            NamedInterval('-M3')
            NamedInterval('-m3')
            NamedInterval('-M2')
            NamedInterval('+m2')
            NamedInterval('+m3')
            NamedInterval('+M3')
            NamedInterval('+P4')
            NamedInterval('+P5')
            NamedInterval('+m7')
            NamedInterval('+M7')
            NamedInterval('+P8')
            NamedInterval('+M9')
            NamedInterval('+A11')
            NamedInterval('+M13')

        Returns interval set.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        pairs = enumerate.yield_pairs(pitch_segment)
        intervals = [second - first for first, second in pairs]
        return class_(items=intervals, item_class=item_class)


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
        Is true when pitch-class set contains ``argument``.

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

    def __str__(self) -> str:
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

        """
        items = [str(_) for _ in sorted(self)]
        separator = " "
        if self.item_class is NumberedPitchClass:
            separator = ", "
        return f"PC{{{separator.join(items)}}}"

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedPitchClass

    @property
    def _numbered_item_class(self):
        return NumberedPitchClass

    @property
    def _parent_item_class(self):
        return PitchClass

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_most_compact_ordering(candidates):
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
            segment = PitchClassSegment(items=segment, item_class=NumberedPitchClass)
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
                segment = PitchClassSegment(
                    items=segment, item_class=NumberedPitchClass
                )
                return segment
        candidates.sort(key=lambda x: x[0])
        segment = candidates[0]
        segment = PitchClassSegment(items=segment, item_class=NumberedPitchClass)
        return segment

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes pitch-class set from ``selection``.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> abjad.PitchClassSet.from_selection(selection)
            PitchClassSet(['c', 'd', 'fs', 'g', 'a', 'b'])

        Returns pitch-class set.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(items=pitch_segment, item_class=item_class)

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
        if not len(self):
            return PitchClassSegment(items=None, item_class=NumberedPitchClass)
        pitch_classes = list(self)
        pitch_classes.sort()
        candidates = []
        for i in range(self.cardinality):
            candidate = [NumberedPitch(_) for _ in pitch_classes]
            candidate = Sequence(candidate).rotate(n=-i)
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
        prime_form = type(self)(items=pcs, item_class=NumberedPitchClass)
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
        Is true when pitch-class set is transposed subset of ``pcset``.

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
        Is true when pitch-class set is transposed superset of ``pcset``.

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
        Multiplies pitch-class set by ``n``.

        ..  container:: example

            >>> abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ...     ).multiply(5)
            PitchClassSet([2, 4.5, 6, 11])

        Returns new pitch-class set.
        """
        items = (pitch_class.multiply(n) for pitch_class in self)
        return new(self, items=items)

    def order_by(self, segment):
        """
        Orders pitch-class set by pitch-class ``segment``.

        ..  container:: example

            >>> set_ = abjad.PitchClassSet(['c', 'e', 'b'])
            >>> segment = abjad.PitchClassSegment(['e', 'a', 'f'])
            >>> set_.order_by(segment)
            PitchClassSegment("b e c")

        Returns pitch-class segment.
        """
        if not len(self) == len(segment):
            raise ValueError("set and segment must be on equal length.")
        for pitch_classes in enumerate.yield_permutations(self):
            candidate = PitchClassSegment(pitch_classes)
            if candidate._is_equivalent_under_transposition(segment):
                return candidate
        raise ValueError(f"{self!s} can not order by {segment!s}.")

    def transpose(self, n=0):
        """
        Transposes all pitch-classes in pitch-class set by index ``n``.

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
        items = (pitch_class + n for pitch_class in self)
        return new(self, items=items)


class PitchSet(Set):
    r"""
    Pitch set.

    ..  container:: example

        Numbered pitch set:

        >>> set_ = abjad.PitchSet(
        ...     items=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=abjad.NumberedPitch,
        ...     )
        >>> set_
        PitchSet([-2, -1.5, 6, 7])

        >>> string = abjad.storage(set_)
        >>> print(string)
        abjad.PitchSet(
            [-2, -1.5, 6, 7]
            )

    ..  container:: example

        Named pitch set:

        >>> set_ = abjad.PitchSet(
        ...     ['bf,', 'aqs', "fs'", "g'", 'bqf', "g'"],
        ...     item_class=abjad.NamedPitch,
        ...     )
        >>> set_
        PitchSet(['bf,', 'aqs', 'bqf', "fs'", "g'"])

        >>> string = abjad.storage(set_)
        >>> print(string)
        abjad.PitchSet(
            ['bf,', 'aqs', 'bqf', "fs'", "g'"]
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when pitch set equals ``argument``.

        ..  container:: example

            >>> set_1 = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_2 = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_3 = abjad.PitchSet(
            ...     items=[11, 12, 12.5],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> set_1 == set_1
            True
            >>> set_1 == set_2
            True
            >>> set_1 == set_3
            False

            >>> set_2 == set_1
            True
            >>> set_2 == set_2
            True
            >>> set_2 == set_3
            False

            >>> set_3 == set_1
            False
            >>> set_3 == set_2
            False
            >>> set_3 == set_3
            True

        Return true or false.
        """
        return super().__eq__(argument)

    def __hash__(self):
        """
        Hashes pitch set.

        Returns number.
        """
        return super().__hash__()

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        return NamedPitch

    @property
    def _numbered_item_class(self):
        return NumberedPitch

    @property
    def _parent_item_class(self):
        return Pitch

    ### PRIVATE METHODS ###

    def _is_equivalent_under_transposition(self, argument):
        """
        True if pitch set is equivalent to ``argument`` under transposition.

        Returns true or false.
        """
        if not isinstance(argument, type(self)):
            return False
        if not len(self) == len(argument):
            return False
        difference = -(NamedPitch(argument[0], 4) - NamedPitch(self[0], 4))
        new_pitches = (x + difference for x in self)
        new_pitches = new(self, items=new_pitches)
        return argument == new_pitches

    def _sort_self(self):
        return sorted(PitchSegment(tuple(self)))

    ### PUBLIC PROPERTIES ###

    @property
    def duplicate_pitch_classes(self):
        """
        Gets duplicate pitch-classes in pitch set.

        ..  container:: example

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_.duplicate_pitch_classes
            PitchClassSet([])

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, 10.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_.duplicate_pitch_classes
            PitchClassSet([10.5])

        Returns pitch-class set.
        """
        pitch_classes = []
        duplicate_pitch_classes = []
        for pitch in self:
            pitch_class = NumberedPitchClass(pitch)
            if pitch_class in pitch_classes:
                duplicate_pitch_classes.append(pitch_class)
            pitch_classes.append(pitch_class)
        return PitchClassSet(duplicate_pitch_classes, item_class=NumberedPitchClass)

    @property
    def hertz(self):
        """
        Gets hertz of pitches in pitch segment.

        ..  container:: example

            >>> pitch_set = abjad.PitchSet('c e g b')
            >>> sorted(pitch_set.hertz)
            [130.81..., 164.81..., 195.99..., 246.94...]

        Returns set.
        """
        return set(_.hertz for _ in self)

    @property
    def is_pitch_class_unique(self):
        """
        Is true when pitch set is pitch-class-unique.

        ..  container:: example

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> set_.is_pitch_class_unique
            True

        ..  container:: example

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, 10.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> set_.is_pitch_class_unique
            False

        Returns true or false.
        """
        numbered_pitch_class_set = PitchClassSet(self, item_class=NumberedPitchClass)
        return len(self) == len(numbered_pitch_class_set)

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes pitch set from ``selection``.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> abjad.PitchSet.from_selection(selection)
            PitchSet(['c', 'g', 'b', "c'", "d'", "fs'", "a'"])

        Returns pitch set.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(items=pitch_segment, item_class=item_class)

    def invert(self, axis):
        """
        Inverts pitch set about ``axis``.

        Returns new pitch set.
        """
        items = (pitch.invert(axis) for pitch in self)
        return new(self, items=items)

    def issubset(self, argument):
        """
        Is true when pitch set is subset of ``argument``.

        ..  container:: example

            >>> set_1 = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_2 = abjad.PitchSet(
            ...     items=[-1.5, 6],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> set_1.issubset(set_2)
            False

            >>> set_2.issubset(set_1)
            True

        Returns true or false.
        """
        return super().issubset(argument)

    def issuperset(self, argument):
        """
        Is true when pitch set is superset of ``argument``.

        ..  container:: example

            >>> set_1 = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_2 = abjad.PitchSet(
            ...     items=[-1.5, 6],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> set_1.issuperset(set_2)
            False

            >>> set_2.issuperset(set_1)
            True

        Returns true or false.
        """
        return super().issubset(argument)

    def register(self, pitch_classes):
        """
        Registers ``pitch_classes`` by pitch set.

        ..  container:: example

            >>> pitch_set = abjad.PitchSet(
            ...     items=[10, 19, 20, 23, 24, 26, 27, 29, 30, 33, 37, 40],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> pitch_classes = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
            >>> pitches = pitch_set.register(pitch_classes)
            >>> for pitch in pitches:
            ...     pitch
            NumberedPitch(10)
            NumberedPitch(24)
            NumberedPitch(26)
            NumberedPitch(30)
            NumberedPitch(20)
            NumberedPitch(19)
            NumberedPitch(29)
            NumberedPitch(27)
            NumberedPitch(37)
            NumberedPitch(33)
            NumberedPitch(40)
            NumberedPitch(23)

        Returns list of zero or more numbered pitches.
        """
        if isinstance(pitch_classes, collections.abc.Iterable):
            result = [
                [_ for _ in self if _.number % 12 == pc]
                for pc in [x % 12 for x in pitch_classes]
            ]
            result = Sequence(result).flatten(depth=-1)
        elif isinstance(pitch_classes, int):
            result = [p for p in pitch_classes if p % 12 == pitch_classes][0]
        else:
            raise TypeError("must be pitch-class or list of pitch-classes.")
        return result

    def transpose(self, n=0):
        """
        Transposes pitch set by index ``n``.

        Returns new pitch set.
        """
        items = (pitch.transpose(n=n) for pitch in self)
        return new(self, items=items)


### FUNCTIONS ###


def pitch_set(items=None, item_class=None, **keywords):
    """
    Makes pitch set or pitch set expression.
    """
    if items is not None:
        return PitchSet(items=items, item_class=item_class)
    name = keywords.pop("name", None)
    expression = Expression(name=name, proxy_class=PitchSet)
    callback = Expression._make_initializer_callback(
        PitchSet, string_template="{}", **keywords
    )
    expression = expression.append_callback(callback)
    return expression
