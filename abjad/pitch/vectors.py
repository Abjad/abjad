import abc
import collections
import types

from .. import enumerate, math
from ..storage import FormatSpecification
from ..typedcollections import TypedCollection, TypedCounter
from .intervalclasses import IntervalClass, NamedIntervalClass, NumberedIntervalClass
from .intervals import Interval, NamedInterval, NumberedInterval
from .pitchclasses import NamedPitchClass, NumberedPitchClass, PitchClass
from .pitches import NamedPitch, NumberedPitch, Pitch
from .segments import PitchClassSegment, PitchSegment
from .sets import PitchClassSet, PitchSet


class Vector(TypedCounter):
    """
    Abstract vector.
    """

    ### CLASS VARIABLES ##

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        prototype_1 = (collections.abc.Iterator, types.GeneratorType)
        prototype_2 = (TypedCounter, collections.Counter)
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, prototype_1):
            items = [item for item in items]
        elif isinstance(items, dict):
            items = self._dictionary_to_items(items, item_class)
        if isinstance(items, prototype_2):
            new_tokens = []
            for item, count in items.items():
                new_tokens.extend(count * [item])
            items = new_tokens
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
                    if isinstance(items, dict):
                        item_class = self._dictionary_to_item_class(items)
                    elif isinstance(items[0], str):
                        item_class = self._named_item_class
                    elif isinstance(items[0], (int, float)):
                        item_class = self._numbered_item_class
                    elif isinstance(items[0], self._parent_item_class):
                        item_class = type(items[0])
        assert issubclass(item_class, self._parent_item_class)
        TypedCounter.__init__(self, items=items, item_class=item_class)

    ### SPECIAL METHODS ###

    def __str__(self):
        """
        String representation of vector.

        Returns string.
        """
        parts = [f"{key}: {value}" for key, value in self.items()]
        string = ", ".join(parts)
        return f"<{string}>"

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

    def _dictionary_to_item_class(self, dictionary):
        if not len(dictionary):
            return self._named_item_class
        keys = dictionary.keys()
        first_key = keys[0]
        assert isinstance(first_key, str), repr(first_key)
        try:
            float(first_key)
            item_class = self._numbered_item_class
        except ValueError:
            item_class = self._named_item_class
        return item_class

    def _dictionary_to_items(self, dictionary, item_class):
        items = []
        for initializer_token, count in dictionary.items():
            for _ in range(count):
                item = item_class(initializer_token)
                items.append(item)
        return items

    def _get_format_specification(self):
        if self.item_class.__name__.startswith("Named"):
            repr_items = {str(k): v for k, v in self.items()}
        else:
            repr_items = {
                math.integer_equivalent_number_to_integer(float(k.number)): v
                for k, v in self.items()
            }
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_args_values=[repr_items],
            storage_format_args_values=[self._collection],
        )

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes vector from ``selection``.

        Returns vector.
        """
        raise NotImplementedError


class IntervalVector(Vector):
    """
    Interval vector.

    ..  container:: example

        Initializes from pitch segment:

        >>> pitch_segment = abjad.PitchSegment(
        ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
        ...     )
        >>> numbered_interval_vector = abjad.IntervalVector(
        ...     items=pitch_segment,
        ...     item_class=abjad.NumberedInterval,
        ...     )
        >>> for interval, count in sorted(numbered_interval_vector.items(),
        ...     key=lambda x: (x[0].direction_number, x[0].number)):
        ...     print(interval, count)
        ...
        -11 1
        -10 1
        -9 1
        -8 2
        -7 3
        -6 3
        -5 4
        -4 4
        -3 4
        -2 5
        -1 6
        +1 5
        +2 5
        +3 5
        +4 4
        +5 3
        +6 3
        +7 2
        +8 2
        +9 2
        +10 1

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        if isinstance(
            items,
            (
                PitchSegment,
                PitchSet,
                PitchClassSegment,
                PitchClassSet,
            ),
        ):
            intervals = []
            pairs = enumerate.yield_pairs(items)
            for first, second in pairs:
                intervals.append(second - first)
            items = intervals
        Vector.__init__(self, items=items, item_class=item_class)

    ### SPECIAL METHODS ###

    def __repr__(self):
        """
        Gets interpret representation of interval vector.

        ..  container:: example

            Gets interpreter representation of interval vector:

            >>> pitch_segment = abjad.PitchSegment(
            ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
            ...     )
            >>> vector = abjad.IntervalVector(
            ...     items=pitch_segment,
            ...     item_class=abjad.NumberedInterval,
            ...     )

            >>> vector
            IntervalVector({-11: 1, -10: 1, -9: 1, -8: 2, -7: 3, -6: 3, -5: 4, -4: 4, -3: 4, -2: 5, -1: 6, 1: 5, 2: 5, 3: 5, 4: 4, 5: 3, 6: 3, 7: 2, 8: 2, 9: 2, 10: 1}, item_class=NumberedInterval)

        ..  container:: example

            Initializes from interpreter representation of interval vector:

            >>> abjad.IntervalVector(vector)
            IntervalVector({-11: 1, -10: 1, -9: 1, -8: 2, -7: 3, -6: 3, -5: 4, -4: 4, -3: 4, -2: 5, -1: 6, 1: 5, 2: 5, 3: 5, 4: 4, 5: 3, 6: 3, 7: 2, 8: 2, 9: 2, 10: 1}, item_class=NumberedInterval)

        Returns string.
        """
        return super().__repr__()

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
        Makes interval vector from ``selection``.

        Returns interval vector.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(pitch_segment, item_class=item_class)


class IntervalClassVector(Vector):
    """
    Interval-class vector.

    ..  container:: example

        An interval-class vector:

        >>> pitch_segment = abjad.PitchSegment(
        ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
        ...     )
        >>> numbered_interval_class_vector = abjad.IntervalClassVector(
        ...     items=pitch_segment,
        ...     item_class=abjad.NumberedInversionEquivalentIntervalClass,
        ...     )

        >>> items = sorted(numbered_interval_class_vector.items())
        >>> for interval, count in items:
        ...     print(interval, count)
        ...
        1 12
        2 12
        3 12
        4 12
        5 12
        6 6

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        prototype = (
            PitchSegment,
            PitchSet,
            PitchClassSegment,
            PitchClassSet,
        )
        if isinstance(items, prototype):
            intervals = []
            items = tuple(items)
            pairs = enumerate.yield_pairs(items)
            for first, second in pairs:
                intervals.append(second - first)
            items = intervals
        Vector.__init__(self, items=items, item_class=item_class)

    ### SPECIAL METHODS ###

    def __repr__(self):
        """
        Gets interpreter representation of interval-class vector.

        ..  container:: example

            Gets interpreter representation of interval-class vector:

            >>> pitch_segment = abjad.PitchSegment(
            ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
            ...     )
            >>> vector = abjad.IntervalClassVector(
            ...     items=pitch_segment,
            ...     item_class=abjad.NumberedInversionEquivalentIntervalClass,
            ...     )

            >>> vector
            IntervalClassVector({1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 6}, item_class=NumberedInversionEquivalentIntervalClass)

        ..  container:: example

            Initializes from interpreter representation of interval-class
            vector:

            >>> abjad.IntervalClassVector(vector)
            IntervalClassVector({1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 6}, item_class=NumberedInversionEquivalentIntervalClass)

        Returns string.
        """
        return super().__repr__()

    ### PRIVATE PROPERTIES ###

    @property
    def _label(self):
        counts = []
        for i in range(7):
            counts.append(self[i])
        counts = "".join([str(x) for x in counts])
        if len(self) == 13:
            quartertones = []
            for i in range(6):
                quartertones.append(self[i + 0.5])
            quartertones = "".join([str(x) for x in quartertones])
            return r'\tiny \column { "%s" "%s" }' % (counts, quartertones)
        else:
            return r"\tiny %s" % counts

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
        """
        Makes interval-class vector from ``selection``.

        ..  container:: example

            Makes numbered inversion-equivalent interval-class vector from
            selection:

            >>> chord = abjad.Chord("<c' d' b''>4"),
            >>> vector = abjad.IntervalClassVector.from_selection(
            ...     abjad.select(chord),
            ...     item_class=abjad.NumberedInversionEquivalentIntervalClass,
            ...     )
            >>> vector
            IntervalClassVector({1: 1, 2: 1, 3: 1}, item_class=NumberedInversionEquivalentIntervalClass)

        ..  container:: example

            Makes numbered interval-class vector from selection:

            >>> chord = abjad.Chord("<c' d' b''>4")
            >>> vector = abjad.IntervalClassVector.from_selection(
            ...     abjad.select(chord),
            ...     item_class=abjad.NumberedIntervalClass,
            ...     )
            >>> vector
            IntervalClassVector({-11: 1, -9: 1, -2: 1}, item_class=NumberedIntervalClass)

            .. todo:: This should probabaly be checked. Resulting values
                should probabaly be positive (or signless) instead of negative.

        ..  container:: example

            Makes named interval-class vector from selection:

            >>> chord = abjad.Chord("<c' d' b''>4")
            >>> vector = abjad.IntervalClassVector.from_selection(
            ...     abjad.select(chord),
            ...     item_class=None,
            ...     )
            >>> vector
            IntervalClassVector({'-M2': 1, '-M6': 1, '-M7': 1}, item_class=NamedIntervalClass)

            .. todo:: This should probabaly be checked. Resulting values
                should probabaly be positive (or signless) instead of negative.

        Returns new interval-class vector.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(pitch_segment, item_class=item_class)


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
        return NamedPitchClass

    @property
    def _numbered_item_class(self):
        return NumberedPitchClass

    @property
    def _parent_item_class(self):
        return PitchClass

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes pitch-class vector from ``selection``.

        Returns pitch-class vector.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(pitch_segment, item_class=item_class)


class PitchVector(Vector):
    """
    Pitch vector.

    ..  container:: example

        >>> vector = abjad.PitchVector(
        ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
        ...     item_class=abjad.NumberedPitch,
        ...     )

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

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __repr__(self):
        """
        Gets interpreter representation of pitch vector.

        ..  container:: example

            Gets interpreter representation of pitch vector:

            >>> vector = abjad.PitchVector(
            ...     items=[7, 6, -2, -3, -3, 0, 1, 14, 15, 16, 16],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> vector
            PitchVector({-3: 2, -2: 1, 0: 1, 1: 1, 6: 1, 7: 1, 14: 1, 15: 1, 16: 2}, item_class=NumberedPitch)

        ..  container:: example

            Initializes from interpreter representation of pitch vector:

                >>> abjad.PitchVector(vector)
                PitchVector({-3: 2, -2: 1, 0: 1, 1: 1, 6: 1, 7: 1, 14: 1, 15: 1, 16: 2}, item_class=NumberedPitch)

        Returns string.
        """
        return super().__repr__()

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

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes pitch vector from ``selection``.

        Returns pitch vector.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(pitch_segment, item_class=item_class)
