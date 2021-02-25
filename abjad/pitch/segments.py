import abc
import collections
import importlib
import inspect
import types

from .. import math
from ..duration import Multiplier
from ..expression import Expression, Signature
from ..new import new
from ..sequence import Sequence
from ..storage import FormatSpecification
from ..typedcollections import TypedCollection, TypedTuple
from .Octave import Octave
from .intervalclasses import (
    IntervalClass,
    NamedIntervalClass,
    NamedInversionEquivalentIntervalClass,
    NumberedIntervalClass,
)
from .intervals import Interval, NamedInterval, NumberedInterval
from .pitchclasses import NamedPitchClass, NumberedPitchClass, PitchClass
from .pitches import NamedPitch, NumberedPitch, Pitch


class Segment(TypedTuple):
    """
    Abstract segment.
    """

    ### CLASS VARIABLES ##

    __slots__ = ("_equivalence_markup", "_expression")

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        prototype = (collections.abc.Iterator, types.GeneratorType)
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, prototype):
            items = [_ for _ in items]
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
        if isinstance(item_class, str):
            abjad = importlib.import_module("abjad")
            globals_ = {"abjad": abjad}
            globals_.update(abjad.__dict__.copy())
            item_class = eval(item_class, globals_)
        assert issubclass(item_class, self._parent_item_class)
        TypedTuple.__init__(self, items=items, item_class=item_class)
        self._equivalence_markup = None
        self._expression = None

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        """
        Gets string representation of segment.
        """
        items = [str(_) for _ in self]
        string = ", ".join(items)
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

    def _coerce_item(self, item):
        return self._item_class(item)

    def _get_format_specification(self):
        items = []
        if self.item_class.__name__.startswith("Named"):
            items = [str(x) for x in self]
        elif hasattr(self.item_class, "pitch_number"):
            items = [x.pitch_number for x in self]
        elif hasattr(self.item_class, "pitch_class_number"):
            items = [x.pitch_class_number for x in self]
        elif self.item_class.__name__.startswith("Numbered"):
            items = [
                math.integer_equivalent_number_to_integer(float(x.number)) for x in self
            ]
        elif hasattr(self.item_class, "__abs__"):
            items = [abs(x) for x in self]
        else:
            raise ValueError(f"invalid item class: {self.item_class!r}.")
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_keyword_names=["name"],
            repr_args_values=[items],
            storage_format_args_values=[tuple(self._collection)],
        )

    def _get_padded_string(self, width=2):
        strings = []
        for item in self:
            string = f"{item!s:>{width}}"
            strings.append(string)
        string = ", ".join(strings)
        return f"<{string}>"

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes segment from ``selection``.

        Returns new segment.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def has_duplicates(self):
        """
        Is true when segment has duplicates.

        Returns true or false.
        """
        raise NotImplementedError


class IntervalClassSegment(Segment):
    """
    Interval-class segment.

    ..  container:: example

        An interval-class segment:

        >>> intervals = 'm2 M10 -aug4 P5'
        >>> abjad.IntervalClassSegment(intervals)
        IntervalClassSegment(['+m2', '+M3', '-A4', '+P5'])

    ..  container:: example

        Another interval-class segment:

        >>> intervals = 'P4 P5 P11 P12'
        >>> abjad.IntervalClassSegment(intervals)
        IntervalClassSegment(['+P4', '+P5', '+P4', '+P5'])

    Returns interval-class segment.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

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

    ### PUBLIC PROPERTIES ###

    @property
    def is_tertian(self):
        """
        Is true when all named interval-classes in segment are tertian.

        ..  container:: example

            >>> interval_class_segment = abjad.IntervalClassSegment(
            ...     items=[('major', 3), ('minor', 6), ('major', 6)],
            ...     item_class=abjad.NamedIntervalClass,
            ...     )
            >>> interval_class_segment.is_tertian
            True

        Returns true or false.
        """
        inversion_equivalent_interval_class_segment = new(
            self, item_class=NamedInversionEquivalentIntervalClass
        )
        for interval in inversion_equivalent_interval_class_segment:
            if not interval.number == 3:
                return False
        return True

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Initializes interval-class segment from component selection.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> abjad.IntervalClassSegment.from_selection(selection)
            IntervalClassSegment(['-M2', '-M3', '-m3', '+m7', '+M7', '-P5'])

        Returns interval-class segment.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        pitches = [_ for _ in pitch_segment]
        intervals = math.difference_series(pitches)
        return class_(items=intervals, item_class=item_class)

    def has_duplicates(self) -> bool:
        """
        Is true when segment contains duplicates.

        ..  container:: example

            >>> intervals = 'm2 M3 -aug4 m2 P5'
            >>> segment = abjad.IntervalClassSegment(intervals)
            >>> segment.has_duplicates()
            True

            >>> intervals = 'M3 -aug4 m2 P5'
            >>> segment = abjad.IntervalClassSegment(intervals)
            >>> segment.has_duplicates()
            False

        """
        return len(set(self)) < len(self)


class IntervalSegment(Segment):
    """
    Interval segment.

    ..  container:: example

        Initializes from string:

        >>> intervals = 'm2 M10 -aug4 P5'
        >>> abjad.IntervalSegment(intervals)
        IntervalSegment(['+m2', '+M10', '-A4', '+P5'])

    ..  container:: example

        Initializes from pitch segment:

        >>> pitch_segment = abjad.PitchSegment("c d e f g a b c'")
        >>> abjad.IntervalSegment(pitch_segment)
        IntervalSegment(['+M2', '+M2', '+m2', '+M2', '+M2', '+M2', '+m2'])

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        if isinstance(items, PitchSegment):
            intervals = []
            for one, two in Sequence(items).nwise():
                intervals.append(one - two)
            items = intervals
        Segment.__init__(self, items=items, item_class=item_class)

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

    ### PUBLIC PROPERTIES ###

    @property
    def slope(self):
        """
        Gets slope of interval segment.

        ..  container:: example

            The slope of a interval segment is the sum of its
            intervals divided by its length:

            >>> abjad.IntervalSegment([1, 2]).slope
            Multiplier(3, 2)

        Returns multiplier.
        """
        result = sum([x.number for x in self]) / len(self)
        return Multiplier.from_float(result)

    @property
    def spread(self):
        """
        Gets spread of interval segment.

        ..  container:: example

            The maximum interval spanned by any combination of
            the intervals within a numbered interval segment.

            >>> abjad.IntervalSegment([1, 2, -3, 1, -2, 1]).spread
            NumberedInterval(4)

            >>> abjad.IntervalSegment([1, 1, 1, 2, -3, -2]).spread
            NumberedInterval(5)

        Returns numbered interval.
        """
        current = maximum = minimum = 0
        for x in self:
            current += float(x.number)
            if maximum < current:
                maximum = current
            if current < minimum:
                minimum = current
        return NumberedInterval(maximum - minimum)

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes interval segment from component ``selection``.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
            >>> abjad.IntervalSegment.from_selection(
            ...     abjad.select(staff),
            ...     item_class=abjad.NumberedInterval,
            ...     )
            IntervalSegment([2, 2, 1, 2, 2, 2, 1])

        Returns interval segment.
        """
        pitch_segment = PitchSegment.from_selection(selection)
        pitches = [_ for _ in pitch_segment]
        intervals = (-x for x in math.difference_series(pitches))
        return class_(items=intervals, item_class=item_class)

    def has_duplicates(self) -> bool:
        """
        Is true if segment has duplicate items.

        ..  container:: example

            >>> intervals = 'm2 M3 -aug4 m2 P5'
            >>> segment = abjad.IntervalSegment(intervals)
            >>> segment.has_duplicates()
            True

            >>> intervals = 'M3 -aug4 m2 P5'
            >>> segment = abjad.IntervalSegment(intervals)
            >>> segment.has_duplicates()
            False

        """
        return len(set(self)) < len(self)

    def rotate(self, n=0):
        """
        Rotates interval segment by index ``n``.

        Returns new interval segment.
        """
        return new(self, self[-n:] + self[:-n])


class PitchClassSegment(Segment):
    r"""
    Pitch-class segment.

    ..  container:: example

        Initializes segment with numbered pitch-classes:

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example expression

            >>> expression = abjad.Expression()
            >>> expression = abjad.pitch_class_segment()

            >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

    ..  container:: example

        Initializes segment with named pitch-classes:

        ..  container:: example

            >>> items = ['c', 'ef', 'bqs,', 'd']
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    c'8
                    ef'8
                    bqs'8
                    d'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example expression

            >>> expression = abjad.Expression()
            >>> expression = abjad.pitch_class_segment(
            ...     item_class=abjad.NamedPitchClass,
            ...     )

            >>> segment = expression(['c', 'ef', 'bqs,', 'd'])
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    c'8
                    ef'8
                    bqs'8
                    d'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        if not items and not item_class:
            item_class = self._named_item_class
        Segment.__init__(self, items=items, item_class=item_class)

    ### SPECIAL METHODS ###

    @Signature(
        markup_maker_callback="_make___add___markup",
        string_template_callback="_make___add___string_template",
    )
    def __add__(self, argument):
        r"""
        Adds ``argument`` to segment.

        ..  container:: example

            Example segments:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=pitch_numbers)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> J = abjad.PitchClassSegment(items=pitch_numbers)
            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> pitch_names = ['c', 'ef', 'bqs,', 'd']
            >>> abjad.PitchClassSegment(items=pitch_names)
            PitchClassSegment("c ef bqs d")

            >>> K = abjad.PitchClassSegment(items=pitch_names)
            >>> lilypond_file = abjad.illustrate(K)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Adds J and K:

            ..  container:: example

                >>> J + K
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 0, 3, 11.5, 2])

                >>> segment = J + K
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        c'8
                        ef'8
                        bqs'8
                        d'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression + pitch_names

                >>> expression(pitch_numbers)
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 0, 3, 11.5, 2])

                >>> expression.get_string()
                "J + ['c', 'ef', 'bqs,', 'd']"

                >>> segment = expression(pitch_names)
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        c'8
                        ^ \markup {
                            \line
                                {
                                    \bold
                                        J
                                    +
                                    "['c', 'ef', 'bqs,', 'd']"
                                }
                            }
                        ef'8
                        bqs'8
                        d'8
                        c'8
                        ef'8
                        bqs'8
                        d'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Adds J repeatedly:

            ..  container:: example

                >>> J + J + J
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7])


                >>> segment = J + J + J
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression_J = abjad.pitch_class_segment(name="J")
                >>> expression = expression_J + expression_J + expression_J

                >>> expression(pitch_numbers)
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7])

                >>> expression.get_string()
                'J + J + J'

                >>> segment = expression(pitch_numbers)
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \line
                                {
                                    \line
                                        {
                                            \bold
                                                J
                                            +
                                            \bold
                                                J
                                        }
                                    +
                                    \bold
                                        J
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Adds transformed segments:

            ..  container:: example

                >>> J.rotate(n=1) + K.rotate(n=2)
                PitchClassSegment([7, 10, 10.5, 6, 7, 10.5, 11.5, 2, 0, 3])

                >>> segment = J.rotate(n=1) + K.rotate(n=2)
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        g'8
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        bqs'8
                        d'8
                        c'8
                        ef'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.rotate(n=1)
                >>> expression = expression + K.rotate(n=2)

                >>> expression(pitch_numbers)
                PitchClassSegment([7, 10, 10.5, 6, 7, 10.5, 11.5, 2, 0, 3])

                >>> expression.get_string()
                'r1(J) + PC<bqs d c ef>'

                >>> segment = expression(pitch_numbers)
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        g'8
                        ^ \markup {
                            \line
                                {
                                    \concat
                                        {
                                            r
                                            \sub
                                                1
                                            \bold
                                                J
                                        }
                                    +
                                    "PC<bqs d c ef>"
                                }
                            }
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        bqs'8
                        d'8
                        c'8
                        ef'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Reverses result:

            ..  container:: example

                >>> segment = J.rotate(n=1) + K.rotate(n=2)
                >>> segment.retrograde()
                PitchClassSegment([3, 0, 2, 11.5, 10.5, 7, 6, 10.5, 10, 7])

                >>> segment = segment.retrograde()
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        ef'8
                        c'8
                        d'8
                        bqs'8
                        bqf'8
                        g'8
                        fs'8
                        bqf'8
                        bf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.rotate(n=1)
                >>> expression = expression + K.rotate(n=2)
                >>> expression = expression.retrograde()

                >>> expression(pitch_numbers)
                PitchClassSegment([3, 0, 2, 11.5, 10.5, 7, 6, 10.5, 10, 7])

                >>> expression.get_string()
                'R(r1(J) + PC<bqs d c ef>)'

                >>> segment = expression(pitch_numbers)
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        ef'8
                        ^ \markup {
                            \concat
                                {
                                    R
                                    \line
                                        {
                                            \concat
                                                {
                                                    r
                                                    \sub
                                                        1
                                                    \bold
                                                        J
                                                }
                                            +
                                            "PC<bqs d c ef>"
                                        }
                                }
                            }
                        c'8
                        d'8
                        bqs'8
                        bqf'8
                        g'8
                        fs'8
                        bqf'8
                        bf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example expression

            Establishes equivalence:

            >>> expression = abjad.pitch_class_segment(name="J")
            >>> expression = expression.rotate(n=1)
            >>> expression = expression + K.rotate(n=2)
            >>> expression = expression.establish_equivalence(name='Q')

            >>> expression(pitch_numbers)
            PitchClassSegment([7, 10, 10.5, 6, 7, 10.5, 11.5, 2, 0, 3])

            >>> expression.get_string()
            'Q = r1(J) + PC<bqs d c ef>'

            >>> segment = expression(pitch_numbers)
            >>> markup = expression.get_markup()
            >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    g'8
                    ^ \markup {
                        \line
                            {
                                \bold
                                    Q
                                =
                                \line
                                    {
                                        \concat
                                            {
                                                r
                                                \sub
                                                    1
                                                \bold
                                                    J
                                            }
                                        +
                                        "PC<bqs d c ef>"
                                    }
                            }
                        }
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    bqs'8
                    d'8
                    c'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example expression

            Transforms equivalence:

            >>> expression = expression.transpose(n=1)

            >>> expression(pitch_numbers)
            PitchClassSegment([8, 11, 11.5, 7, 8, 11.5, 0.5, 3, 1, 4])

            >>> expression.get_string()
            'T1(Q)'

            >>> segment = expression(pitch_numbers)
            >>> markup = expression.get_markup()
            >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    af'8
                    ^ \markup {
                        \concat
                            {
                                T
                                \sub
                                    1
                                \bold
                                    Q
                            }
                        }
                    b'8
                    bqs'8
                    g'8
                    af'8
                    bqs'8
                    cqs'8
                    ef'8
                    cs'8
                    e'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns new segment.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        argument = type(self)(items=argument)
        items = self.items + argument.items
        return type(self)(items=items)

    def __contains__(self, argument):
        r"""
        Is true when pitch-class segment contains ``argument``.

        ..  container:: example

            Example segments:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=pitch_numbers)
            >>> segment
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> abjad.NamedPitch('bf') in segment
            True

            >>> abjad.NamedPitch('cs') in segment
            False

            >>> 'bf' in segment
            True

            >>> 'cs' in segment
            False

            >>> 10 in segment
            True

            >>> 13 in segment
            False

        Returns true or false.
        """
        return super().__contains__(argument)

    @Signature(
        markup_maker_callback="_make___getitem___markup",
        string_template_callback="_make___getitem___string_template",
    )
    def __getitem__(self, argument):
        r"""
        Gets ``argument`` from segment.

        ..  container:: example

            Example segment:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=pitch_numbers)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> J = abjad.PitchClassSegment(items=pitch_numbers)
            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets item at nonnegative index:

            ..  container:: example

                >>> J[0]
                NumberedPitchClass(10)

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression[0]

                >>> expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                NumberedPitchClass(10)

                >>> expression.get_string()
                'J[0]'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \concat
                            {
                                \bold
                                    J
                                \sub
                                    0
                            }
                        }

        ..  container:: example

            Gets item at negative index:

            ..  container:: example

                >>> J[-1]
                NumberedPitchClass(7)

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression[-1]

                >>> expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                NumberedPitchClass(7)

                >>> expression.get_string()
                'J[-1]'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \concat
                            {
                                \bold
                                    J
                                \sub
                                    -1
                            }
                        }

        ..  container:: example

            Gets slice:

            ..  container:: example

                >>> J[:4]
                PitchClassSegment([10, 10.5, 6, 7])

                >>> segment = J[:4]
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression[:4]

                >>> expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7])

                >>> expression.get_string()
                'J[:4]'

                >>> segment = expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    \bold
                                        J
                                    \sub
                                        [:4]
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Gets retrograde of slice:

            ..  container:: example

                >>> J[:4].retrograde()
                PitchClassSegment([7, 6, 10.5, 10])

                >>> segment = J[:4].retrograde()
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        g'8
                        fs'8
                        bqf'8
                        bf'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression[:4]
                >>> expression = expression.retrograde()

                >>> expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([7, 6, 10.5, 10])

                >>> expression.get_string()
                'R(J[:4])'

                >>> segment = expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        g'8
                        ^ \markup {
                            \concat
                                {
                                    R
                                    \concat
                                        {
                                            \bold
                                                J
                                            \sub
                                                [:4]
                                        }
                                }
                            }
                        fs'8
                        bqf'8
                        bf'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Gets slice of retrograde:

            ..  container:: example

                >>> J.retrograde()[:4]
                PitchClassSegment([7, 10.5, 7, 6])

                >>> segment = J.retrograde()[:4]
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        g'8
                        bqf'8
                        g'8
                        fs'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.retrograde()
                >>> expression = expression[:4]

                >>> expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([7, 10.5, 7, 6])

                >>> expression.get_string()
                'R(J)[:4]'

                >>> segment = expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        g'8
                        ^ \markup {
                            \concat
                                {
                                    \concat
                                        {
                                            (
                                            \concat
                                                {
                                                    R
                                                    \bold
                                                        J
                                                }
                                            )
                                        }
                                    \sub
                                        [:4]
                                }
                            }
                        bqf'8
                        g'8
                        fs'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Returns pitch-class or pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), precedence=100)
        return super().__getitem__(argument)

    def __mul__(self, n):
        r"""
        Multiplies pitch-class segment by ``n``.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> 2 * abjad.PitchClassSegment(items=items)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7])

        Returns new pitch-class segment.
        """
        return super().__mul__(n)

    def __repr__(self):
        r"""
        Gets interpreter representation.

        ..  container:: example

            Interpreter representation:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=items)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

        Returns string.
        """
        if self.item_class is NamedPitchClass:
            contents = " ".join([str(_) for _ in self])
            contents = '"' + contents + '"'
        else:
            contents = ", ".join([str(_) for _ in self])
            contents = "[" + contents + "]"
        return f"{type(self).__name__}({contents})"

    def __rmul__(self, n):
        r"""
        Multiplies ``n`` by pitch-class segment.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=items) * 2
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7])

        Returns new pitch-class segment.
        """
        return super().__rmul__(n)

    def __str__(self):
        r"""
        Gets string representation of pitch-class segment.

        ..  container::

            Gets string represenation of numbered pitch class:

            >>> segment = abjad.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
            >>> str(segment)
            'PC<10, 10.5, 6, 7, 10.5, 7>'

        ..  container::

            Gets string represenation of named pitch class:

            >>> segment = abjad.PitchClassSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> str(segment)
            'PC<bf bqf fs g bqf g>'

        Returns string.
        """
        items = [str(_) for _ in self]
        separator = " "
        if self.item_class is NumberedPitchClass:
            separator = ", "
        return f"PC<{separator.join(items)}>"

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

    def _get_padded_string(self, width=2):
        string = super()._get_padded_string(width=width)
        return "PC<" + string[1:-1] + ">"

    def _is_equivalent_under_transposition(self, argument):
        if not isinstance(argument, type(self)):
            return False
        if not len(self) == len(argument):
            return False
        difference = -(
            NamedPitch((argument[0].name, 4)) - NamedPitch((self[0].name, 4))
        )
        new_pitch_classes = (x + difference for x in self)
        new_pitch_classes = new(self, items=new_pitch_classes)
        return argument == new_pitch_classes

    @staticmethod
    def _make_rotate_method_name(n=0, stravinsky=False):
        if stravinsky:
            return "rs"
        return "r"

    def _transpose_to_zero(self):
        numbers = [_.number for _ in self]
        first_number = self[0].number
        numbers = [pc.number - first_number for pc in self]
        pcs = [_ % 12 for _ in numbers]
        return type(self)(items=pcs, item_class=self.item_class)

    def _update_expression(self, frame, precedence=None):
        callback = Expression._frame_to_callback(frame, precedence=precedence)
        return self._expression.append_callback(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        r"""
        Gets item class of segment.

        ..  container:: example

            Gets item class of numbered segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment.item_class.__name__
            'NumberedPitchClass'

        ..  container:: example


            Gets item class of named segment:

            >>> items = ['c', 'ef', 'bqs,', 'd']
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment.item_class.__name__
            'NamedPitchClass'

        """
        return super().item_class

    @property
    def items(self):
        r"""
        Gets items in segment.

        ..  container:: example

            ..  container:: example

                Initializes items positionally:

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = abjad.PitchClassSegment(items)
                >>> for item in segment.items:
                ...     item
                ...
                NumberedPitchClass(10)
                NumberedPitchClass(10.5)
                NumberedPitchClass(6)
                NumberedPitchClass(7)
                NumberedPitchClass(10.5)
                NumberedPitchClass(7)

                Initializes items from keyword:

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = abjad.PitchClassSegment(items=items)
                >>> for item in segment.items:
                ...     item
                NumberedPitchClass(10)
                NumberedPitchClass(10.5)
                NumberedPitchClass(6)
                NumberedPitchClass(7)
                NumberedPitchClass(10.5)
                NumberedPitchClass(7)

            ..  container:: example expression

                Initializes items positionally:

                >>> expression = abjad.Expression()
                >>> expression = abjad.pitch_class_segment()

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = expression(items)
                >>> for item in segment.items:
                ...     item
                NumberedPitchClass(10)
                NumberedPitchClass(10.5)
                NumberedPitchClass(6)
                NumberedPitchClass(7)
                NumberedPitchClass(10.5)
                NumberedPitchClass(7)

                Initializes items from keyword:

                >>> expression = abjad.Expression()
                >>> expression = abjad.pitch_class_segment()

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = expression(items=items)
                >>> for item in segment.items:
                ...     item
                NumberedPitchClass(10)
                NumberedPitchClass(10.5)
                NumberedPitchClass(6)
                NumberedPitchClass(7)
                NumberedPitchClass(10.5)
                NumberedPitchClass(7)

        ..  container:: example

            Returns list:

            >>> isinstance(segment.items, list)
            True

        """
        return super().items

    ### PUBLIC METHODS ###

    def count(self, item):
        """
        Counts ``item`` in segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Counts existing item in segment:

            >>> segment.count(-1.5)
            2

        ..  container:: example

            Counts nonexisting item in segment:

            >>> segment.count('text')
            0

        ..  container:: example

            Returns nonnegative integer:

            >>> isinstance(segment.count('text'), int)
            True

        """
        return super().count(item)

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Initializes segment from ``selection``.

        ..  container:: example

            Initializes from selection:

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> staff_group = abjad.StaffGroup([staff_1, staff_2])
            >>> abjad.show(staff_group) # doctest: +SKIP

            >>> selection = abjad.select((staff_1, staff_2))
            >>> segment = abjad.PitchClassSegment.from_selection(selection)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Returns pitch-class segment:

            >>> segment
            PitchClassSegment("c d fs a b c g")

        """
        pitch_segment = PitchSegment.from_selection(selection)
        return class_(items=pitch_segment, item_class=item_class)

    def has_duplicates(self):
        """
        Is true when segment contains duplicate items.

        ..  container:: example

            Has duplicates:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment.has_duplicates()
            True

        ..  container:: example

            Has no duplicates:

            >>> items = "c d e f g a b"
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment.has_duplicates()
            False

        Returns true or false.
        """
        return len(set(self)) < len(self)

    def index(self, item):
        """
        Gets index of ``item`` in segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets index of first item in segment:

            >>> segment.index(-2)
            0

        ..  container:: example

            Gets index of second item in segment:

            >>> segment.index(-1.5)
            1

        ..  container:: example

            Returns nonnegative integer:

            >>> isinstance(segment.index(-1.5), int)
            True

        """
        return super().index(item)

    @Signature(is_operator=True, method_name="I", subscript="axis")
    def invert(self, axis=None):
        r"""
        Inverts segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Inverts segment:

            ..  container:: example

                >>> J.invert()
                PitchClassSegment([2, 1.5, 6, 5, 1.5, 5])

                >>> segment = J.invert()
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        d'8
                        dqf'8
                        fs'8
                        f'8
                        dqf'8
                        f'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.invert()

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([2, 1.5, 6, 5, 1.5, 5])

                >>> expression.get_string()
                'I(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        d'8
                        ^ \markup {
                            \concat
                                {
                                    I
                                    \bold
                                        J
                                }
                            }
                        dqf'8
                        fs'8
                        f'8
                        dqf'8
                        f'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Inverts inversion of segment:

            ..  container:: example

                >>> J.invert().invert()
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> segment = J.invert().invert()
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.invert()
                >>> expression = expression.invert()

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> expression.get_string()
                'I(I(J))'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    I
                                    \concat
                                        {
                                            I
                                            \bold
                                                J
                                        }
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        items = [_.invert(axis=axis) for _ in self]
        return type(self)(items=items)

    @Signature(is_operator=True, method_name="M", subscript="n")
    def multiply(self, n=1):
        r"""
        Multiplies pitch-classes in segment by ``n``.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Multiplies pitch-classes in segment by 1:

            ..  container:: example

                >>> J.multiply(n=1)
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> segment = J.multiply(n=1)
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.multiply(n=1)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> expression.get_string()
                'M1(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    M
                                    \sub
                                        1
                                    \bold
                                        J
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Multiplies pitch-classes in segment by 5:

            ..  container:: example

                >>> J.multiply(n=5)
                PitchClassSegment([2, 4.5, 6, 11, 4.5, 11])

                >>> segment = J.multiply(n=5)
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        d'8
                        eqs'8
                        fs'8
                        b'8
                        eqs'8
                        b'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.multiply(n=5)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([2, 4.5, 6, 11, 4.5, 11])

                >>> expression.get_string()
                'M5(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        d'8
                        ^ \markup {
                            \concat
                                {
                                    M
                                    \sub
                                        5
                                    \bold
                                        J
                                }
                            }
                        eqs'8
                        fs'8
                        b'8
                        eqs'8
                        b'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Multiplies pitch-classes in segment by 7:

            ..  container:: example

                >>> J.multiply(n=7)
                PitchClassSegment([10, 1.5, 6, 1, 1.5, 1])

                >>> segment = J.multiply(n=7)
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        dqf'8
                        fs'8
                        cs'8
                        dqf'8
                        cs'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.multiply(n=7)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 1.5, 6, 1, 1.5, 1])

                >>> expression.get_string()
                'M7(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    M
                                    \sub
                                        7
                                    \bold
                                        J
                                }
                            }
                        dqf'8
                        fs'8
                        cs'8
                        dqf'8
                        cs'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Multiplies pitch-classes in segment by 11:

            ..  container:: example

                >>> segment = J.multiply(n=11)
                >>> segment
                PitchClassSegment([2, 7.5, 6, 5, 7.5, 5])

                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        d'8
                        gqs'8
                        fs'8
                        f'8
                        gqs'8
                        f'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.multiply(n=11)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([2, 7.5, 6, 5, 7.5, 5])

                >>> expression.get_string()
                'M11(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        d'8
                        ^ \markup {
                            \concat
                                {
                                    M
                                    \sub
                                        11
                                    \bold
                                        J
                                }
                            }
                        gqs'8
                        fs'8
                        f'8
                        gqs'8
                        f'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        items = [NumberedPitchClass(_) for _ in self]
        items = [_.multiply(n) for _ in items]
        return type(self)(items=items)

    @Signature()
    def permute(self, row=None):
        r"""
        Permutes segment by twelve-tone ``row``.

        ..  container:: example

            >>> abjad.PitchClassSegment([-2, -1, 6, 7, -1, 7])
            PitchClassSegment([10, 11, 6, 7, 11, 7])

            >>> segment = abjad.PitchClassSegment([-2, -1, 6, 7, -1, 7])
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  doctest:

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    bf'8
                    b'8
                    fs'8
                    g'8
                    b'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.permute([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
            PitchClassSegment([4, 11, 5, 3, 11, 3])

            >>> segment = segment.permute([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    e'8
                    b'8
                    f'8
                    ef'8
                    b'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example expression

            >>> expression = abjad.pitch_class_segment(name="J")
            >>> row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
            >>> expression = expression.permute(row)

            >>> expression([-2, -1, 6, 7, -1, 7])
            PitchClassSegment([4, 11, 5, 3, 11, 3])

            >>> expression.get_string()
            'permute(J, row=[10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])'

            >>> segment = expression([-2, -1, 6, 7, -1, 7])
            >>> markup = expression.get_markup()
            >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  doctest:

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    e'8
                    ^ \markup {
                        \concat
                            {
                                permute(
                                \bold
                                    J
                                ", row=[10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])"
                            }
                        }
                    b'8
                    f'8
                    ef'8
                    b'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns new segment.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        row = TwelveToneRow(items=row)
        items = row(self)
        return type(self)(items=items)

    @Signature(is_operator=True, method_name="R")
    def retrograde(self):
        r"""
        Gets retrograde of segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets retrograde of segment:

            ..  container:: example

                >>> segment = J.retrograde()
                >>> segment
                PitchClassSegment([7, 10.5, 7, 6, 10.5, 10])

                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        g'8
                        bqf'8
                        g'8
                        fs'8
                        bqf'8
                        bf'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.retrograde()

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([7, 10.5, 7, 6, 10.5, 10])

                >>> expression.get_string()
                'R(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        g'8
                        ^ \markup {
                            \concat
                                {
                                    R
                                    \bold
                                        J
                                }
                            }
                        bqf'8
                        g'8
                        fs'8
                        bqf'8
                        bf'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Gets retrograde of retrograde of segment:

            ..  container:: example

                >>> segment = J.retrograde().retrograde()
                >>> segment
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.retrograde()
                >>> expression = expression.retrograde()

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> expression.get_string()
                'R(R(J))'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    R
                                    \concat
                                        {
                                            R
                                            \bold
                                                J
                                        }
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return type(self)(items=reversed(self))

    @Signature(
        is_operator=True,
        method_name_callback="_make_rotate_method_name",
        subscript="n",
    )
    def rotate(self, n=0, stravinsky=False):
        r"""
        Rotates segment by index ``n``.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Rotates segment to the right:

            ..  container:: example

                >>> J.rotate(n=1)
                PitchClassSegment([7, 10, 10.5, 6, 7, 10.5])

                >>> segment = J.rotate(n=1)
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        g'8
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.rotate(n=1)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([7, 10, 10.5, 6, 7, 10.5])

                >>> expression.get_string()
                'r1(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        g'8
                        ^ \markup {
                            \concat
                                {
                                    r
                                    \sub
                                        1
                                    \bold
                                        J
                                }
                            }
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Rotates segment to the left:

            ..  container:: example

                >>> J.rotate(n=-1)
                PitchClassSegment([10.5, 6, 7, 10.5, 7, 10])

                >>> segment = J.rotate(n=-1)
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        bf'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.rotate(n=-1)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10.5, 6, 7, 10.5, 7, 10])

                >>> expression.get_string()
                'r-1(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bqf'8
                        ^ \markup {
                            \concat
                                {
                                    r
                                    \sub
                                        -1
                                    \bold
                                        J
                                }
                            }
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        bf'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Rotates segment by zero:

            ..  container:: example

                >>> J.rotate(n=0)
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> segment = J.rotate(n=0)
                >>> lilypond_file = abjad.illustrate(J)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.rotate(n=0)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> expression.get_string()
                'r0(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    r
                                    \sub
                                        0
                                    \bold
                                        J
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

        ..  container:: example

            Stravinsky-style rotation back-transposes segment to
            begin at zero:

            ..  container:: example

                >>> J.rotate(n=1, stravinsky=True)
                PitchClassSegment([0, 3, 3.5, 11, 0, 3.5])

                >>> segment = J.rotate(n=1, stravinsky=True)
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        c'8
                        ef'8
                        eqf'8
                        b'8
                        c'8
                        eqf'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.rotate(n=1, stravinsky=True)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([0, 3, 3.5, 11, 0, 3.5])

                >>> expression.get_string()
                'rs1(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        c'8
                        ^ \markup {
                            \concat
                                {
                                    rs
                                    \sub
                                        1
                                    \bold
                                        J
                                }
                            }
                        ef'8
                        eqf'8
                        b'8
                        c'8
                        eqf'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        items = Sequence(self._collection).rotate(n=n)
        if stravinsky:
            n = 0 - float(items[0].number)
            segment = new(self, items=items)
            segment = segment.transpose(n=n)
            items = segment.items[:]
        return type(self)(items=items)

    def to_pitch_classes(self):
        r"""
        Changes to pitch-classes.

        ..  container:: example

            To numbered pitch-class segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> segment
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitch_classes()
            >>> segment
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            To named pitch-class segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> segment
            PitchClassSegment("bf bqf fs g bqf g")

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitch_classes()
            >>> segment
            PitchClassSegment("bf bqf fs g bqf g")

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns new segment.
        """
        return new(self)

    def to_pitches(self):
        r"""
        Changes to pitches.

        ..  container:: example

            To numbered pitch segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> segment
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitches()
            >>> segment
            PitchSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        bqf'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            To named pitch segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> segment
            PitchClassSegment("bf bqf fs g bqf g")

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitches()
            >>> segment
            PitchSegment("bf' bqf' fs' g' bqf' g'")

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        bqf'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new segment.
        """
        class_ = Pitch
        item_class = class_._to_pitch_item_class(self.item_class)
        return PitchSegment(items=self.items, item_class=item_class)

    @Signature(is_operator=True, method_name="T", subscript="n")
    def transpose(self, n=0):
        r"""
        Transposes segment by index ``n``.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Transposes segment by positive index:

            ..  container:: example

                >>> J.transpose(n=13)
                PitchClassSegment([11, 11.5, 7, 8, 11.5, 8])

                >>> segment = J.transpose(n=13)
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        b'8
                        bqs'8
                        g'8
                        af'8
                        bqs'8
                        af'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.transpose(n=13)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([11, 11.5, 7, 8, 11.5, 8])

                >>> expression.get_string()
                'T13(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        b'8
                        ^ \markup {
                            \concat
                                {
                                    T
                                    \sub
                                        13
                                    \bold
                                        J
                                }
                            }
                        bqs'8
                        g'8
                        af'8
                        bqs'8
                        af'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Transposes segment by negative index:

            ..  container:: example

                >>> J.transpose(n=-13)
                PitchClassSegment([9, 9.5, 5, 6, 9.5, 6])

                >>> segment = J.transpose(n=-13)
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        a'8
                        aqs'8
                        f'8
                        fs'8
                        aqs'8
                        fs'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.transpose(n=-13)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([9, 9.5, 5, 6, 9.5, 6])

                >>> expression.get_string()
                'T-13(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        a'8
                        ^ \markup {
                            \concat
                                {
                                    T
                                    \sub
                                        -13
                                    \bold
                                        J
                                }
                            }
                        aqs'8
                        f'8
                        fs'8
                        aqs'8
                        fs'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Transposes segment by zero index:

            ..  container:: example

                >>> J.transpose(n=0)
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> segment = J.transpose(n=0)
                >>> lilypond_file = abjad.illustrate(segment)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

            ..  container:: example expression

                >>> expression = abjad.pitch_class_segment(name="J")
                >>> expression = expression.transpose(n=0)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> expression.get_string()
                'T0(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> lilypond_file = abjad.illustrate(segment, figure_name=markup)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                ..  docs::

                    >>> voice = lilypond_file[abjad.Score][0][0]
                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    T
                                    \sub
                                        0
                                    \bold
                                        J
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        items = [_.transpose(n=n) for _ in self]
        return type(self)(items=items)

    def voice_horizontally(self, initial_octave=4):
        r"""
        Voices segment with each pitch as close to the previous pitch as
        possible.

        ..  todo:: Should be implemented somewhere else.

        ..  container:: example

            Voices horizontally:

            >>> items = "c b d e f g e b a c"
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> voiced_segment = segment.voice_horizontally()
            >>> lilypond_file = abjad.illustrate(voiced_segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file[abjad.Score]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            c'1 * 1/8
                            b1 * 1/8
                            d'1 * 1/8
                            e'1 * 1/8
                            f'1 * 1/8
                            g'1 * 1/8
                            e'1 * 1/8
                            b1 * 1/8
                            r1 * 1/8
                            c'1 * 1/8
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            a1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        ..  container:: example

            Returns pitch segment:

            >>> voiced_segment
            PitchSegment("c' b d' e' f' g' e' b a c'")

        """
        initial_octave = Octave(initial_octave)
        pitches = []
        if self:
            pitch_class = NamedPitchClass(self[0])
            pitch = NamedPitch((pitch_class.name, initial_octave))
            pitches.append(pitch)
            for pitch_class in self[1:]:
                pitch_class = NamedPitchClass(pitch_class)
                pitch = NamedPitch((pitch_class.name, initial_octave))
                semitones = abs((pitch - pitches[-1]).semitones)
                while 6 < semitones:
                    if pitch < pitches[-1]:
                        pitch += 12
                    else:
                        pitch -= 12
                    semitones = abs((pitch - pitches[-1]).semitones)
                pitches.append(pitch)
        if self.item_class is NamedPitchClass:
            item_class = NamedPitch
        else:
            item_class = NumberedPitch
        return PitchSegment(items=pitches, item_class=item_class)

    def voice_vertically(self, initial_octave=4):
        r"""
        Voices segment with each pitch higher than the previous.

        ..  todo:: Should be implemented somewhere else.

        ..  container:: example

            Voices vertically:

            >>> string = "c' ef' g' bf' d'' f'' af''"
            >>> segment = abjad.PitchClassSegment(string)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> voiced_segment = segment.voice_vertically()
            >>> lilypond_file = abjad.illustrate(voiced_segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file[abjad.Score]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            c'1 * 1/8
                            ef'1 * 1/8
                            g'1 * 1/8
                            bf'1 * 1/8
                            d''1 * 1/8
                            f''1 * 1/8
                            af''1 * 1/8
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        ..  container:: example

            Returns pitch segment:

            >>> voiced_segment
            PitchSegment("c' ef' g' bf' d'' f'' af''")

        """
        initial_octave = Octave(initial_octave)
        pitches = []
        if self:
            pitch_class = NamedPitchClass(self[0])
            pitch = NamedPitch((pitch_class.name, initial_octave))
            pitches.append(pitch)
            for pitch_class in self[1:]:
                pitch_class = NamedPitchClass(pitch_class)
                pitch = NamedPitch((pitch_class.name, initial_octave))
                while pitch < pitches[-1]:
                    pitch += 12
                pitches.append(pitch)
        if self.item_class is NamedPitchClass:
            item_class = NamedPitch
        else:
            item_class = NumberedPitch
        return PitchSegment(items=pitches, item_class=item_class)


class PitchSegment(Segment):
    r"""
    Pitch segment.

    ..  container:: example

        Numbered pitch segment:

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

        >>> str(segment)
        '<-2, -1.5, 6, 7, -1.5, 7>'

        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file[abjad.Score][0]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    r1 * 1/8
                    r1 * 1/8
                    fs'1 * 1/8
                    g'1 * 1/8
                    r1 * 1/8
                    g'1 * 1/8
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    bf1 * 1/8
                    bqf1 * 1/8
                    r1 * 1/8
                    r1 * 1/8
                    bqf1 * 1/8
                    r1 * 1/8
                }
            >>

    ..  container:: example

        Named pitch segment:

        >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

        >>> str(segment)
        "<bf, aqs fs' g' bqf g'>"

        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file[abjad.Score][0]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    r1 * 1/8
                    r1 * 1/8
                    fs'1 * 1/8
                    g'1 * 1/8
                    r1 * 1/8
                    g'1 * 1/8
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    bf,1 * 1/8
                    aqs1 * 1/8
                    r1 * 1/8
                    r1 * 1/8
                    bqf1 * 1/8
                    r1 * 1/8
                }
            >>

    ..  container:: example

        Built-in max() works:

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> max(segment)
        NumberedPitch(7)

        Built-in min() works:

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> min(segment)
        NumberedPitch(-2)

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        if not items and not item_class:
            item_class = self._named_item_class
        Segment.__init__(self, items=items, item_class=item_class)

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        """
        Is true when pitch segment contains ``argument``.

        ..  container:: example

            Numbered pitch segment:

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.NamedPitch('fs') in segment
            False

            >>> 6 in segment
            True

            >>> abjad.NamedPitch('f') in segment
            False

            >>> 5 in segment
            False

        Returns true or false.
        """
        return super().__contains__(argument)

    def __repr__(self):
        """
        Gets interpreter representation of segment.

        Returns string.
        """
        if self.item_class is NamedPitch:
            contents = " ".join([str(_) for _ in self])
            contents = '"' + contents + '"'
        else:
            contents = ", ".join([str(_) for _ in self])
            contents = "[" + contents + "]"
        return f"{type(self).__name__}({contents})"

    def __str__(self):
        """
        Gets pitch segment string.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> str(segment)
            '<-2, -1.5, 6, 7, -1.5, 7>'

        ..  container:: example

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> str(segment)
            "<bf, aqs fs' g' bqf g'>"

        Returns string.
        """
        items = [str(_) for _ in self]
        separator = " "
        if self.item_class is NumberedPitch:
            separator = ", "
        return f"<{separator.join(items)}>"

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
        if not isinstance(argument, type(self)):
            return False
        if not len(self) == len(argument):
            return False
        difference = -(NamedPitch(argument[0], 4) - NamedPitch(self[0], 4))
        new_pitches = (x + difference for x in self)
        new_pitches = new(self, items=new_pitches)
        return argument == new_pitches

    ### PUBLIC PROPERTIES ###

    @property
    def hertz(self):
        """
        Gets Hertz of pitches in segment.

        ..  container:: example

            >>> segment = abjad.PitchSegment('c e g b')
            >>> segment.hertz
            [130.81..., 164.81..., 195.99..., 246.94...]

        Returns list.
        """
        return [_.hertz for _ in self]

    @property
    def inflection_point_count(self):
        r"""
        Gets segment inflection point count.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.inflection_point_count
            2

        Returns nonnegative integer.
        """
        return len(self.local_minima) + len(self.local_maxima)

    @property
    def local_maxima(self):
        r"""
        Gets segment local maxima.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.local_maxima
            [NumberedPitch(7)]

        Returns list.
        """
        result = []
        if 3 <= len(self):
            for i in range(1, len(self) - 1):
                left, middle, right = self[i - 1], self[i], self[i + 1]
                if left < middle and right < middle:
                    result.append(middle)
        return result

    @property
    def local_minima(self):
        r"""
        Gets segment local minima.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.local_minima
            [NumberedPitch(-1.5)]

        Returns list.
        """
        result = []
        if 3 <= len(self):
            for i in range(1, len(self) - 1):
                left, middle, right = self[i - 1], self[i], self[i + 1]
                if middle < left and middle < right:
                    result.append(middle)
        return result

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None) -> "PitchSegment":
        r"""
        Makes pitch segment from ``selection``.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> segment = abjad.PitchSegment.from_selection(selection)

            >>> str(segment)
            "<c' d' fs' a' b c g>"

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        c'1 * 1/8
                        d'1 * 1/8
                        fs'1 * 1/8
                        a'1 * 1/8
                        b1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        c1 * 1/8
                        g1 * 1/8
                    }
                >>

        """
        assert hasattr(selection, "_pitch_segment"), repr(selection)
        pitch_segment = selection._pitch_segment()
        return class_(items=pitch_segment, item_class=item_class)

    def has_duplicates(self) -> bool:
        """
        Is true when segment has duplicates.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
            >>> segment.has_duplicates()
            True

        ..  container:: example

            >>> segment = abjad.PitchSegment("c d e f g a b")
            >>> segment.has_duplicates()
            False

        """
        return len(set(self)) < len(self)

    def invert(self, axis=None):
        r"""
        Inverts pitch segment about ``axis``.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.invert(axis=0)

            >>> str(segment)
            '<2, 1.5, -6, -7, 1.5, -7>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        d'1 * 1/8
                        dqf'1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        dqf'1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        fs1 * 1/8
                        f1 * 1/8
                        r1 * 1/8
                        f1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        items = [_.invert(axis=axis) for _ in self]
        return new(self, items=items)

    def multiply(self, n=1):
        r"""
        Multiplies pitch segment by index ``n``.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.multiply(n=3)

            >>> str(segment)
            '<-6, -4.5, 18, 21, -4.5, 21>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs''1 * 1/8
                        a''1 * 1/8
                        r1 * 1/8
                        a''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        fs1 * 1/8
                        gqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        gqs1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        items = [_.multiply(n=n) for _ in self]
        return new(self, items=items)

    def retrograde(self):
        r"""
        Retrograde of pitch segment.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.retrograde()

            >>> str(segment)
            '<7, -1.5, 7, 6, -1.5, -2>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                        fs'1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        bf1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        return new(self, items=reversed(self))

    def rotate(self, n=0, stravinsky=False):
        r"""
        Rotates pitch segment by index ``n``.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.rotate(n=1)

            >>> str(segment)
            '<7, -2, -1.5, 6, 7, -1.5>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        g'1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        rotated_pitches = Sequence(self._collection).rotate(n=n)
        new_segment = new(self, items=rotated_pitches)
        if stravinsky:
            if self[0] != new_segment[0]:
                interval = new_segment[0] - self[0]
                new_segment = new_segment.transpose(interval)
        return new_segment

    def to_pitch_classes(self):
        r"""
        Changes to pitch-classes.

        ..  container:: example

            To numbered pitch-class segment:

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitch_classes()

            >>> str(segment)
            'PC<10, 10.5, 6, 7, 10.5, 7>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            To named pitch-class segment:

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitch_classes()

            >>> str(segment)
            'PC<bf aqs fs g bqf g>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    bf'8
                    aqs'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns new segment.
        """
        class_ = Pitch
        item_class = class_._to_pitch_class_item_class(self.item_class)
        return PitchClassSegment(items=self.items, item_class=item_class)

    def to_pitches(self):
        r"""
        Changes to pitches.

        ..  container:: example

            To numbered pitch segment:

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitches()

            >>> str(segment)
            '<-2, -1.5, 6, 7, -1.5, 7>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            To named pitch segment:

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitches()

            >>> str(segment)
            "<bf, aqs fs' g' bqf g'>"

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new segment.
        """
        return new(self)

    def transpose(self, n=0):
        r"""
        Transposes pitch segment by index ``n``.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.transpose(n=11)

            >>> str(segment)
            '<9, 9.5, 17, 18, 9.5, 18>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file[abjad.Score][0]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        a'1 * 1/8
                        aqs'1 * 1/8
                        f''1 * 1/8
                        fs''1 * 1/8
                        aqs'1 * 1/8
                        fs''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        items = [_.transpose(n=n) for _ in self]
        return new(self, items=items)


class TwelveToneRow(PitchClassSegment):
    """
    Twelve-tone row.

    ..  container:: example

        Initializes from defaults:

        >>> row = abjad.TwelveToneRow()
        >>> lilypond_file = abjad.illustrate(row)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  container:: example

        Initializes from integers:

        >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
        >>> row = abjad.TwelveToneRow(numbers)
        >>> lilypond_file = abjad.illustrate(row)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  container:: example

        Interpreter representation:

        >>> row
        TwelveToneRow([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)):
        assert items is not None
        PitchClassSegment.__init__(self, items=items, item_class=NumberedPitchClass)
        self._validate_pitch_classes(self)

    ### SPECIAL METHODS ###

    def __call__(self, pitch_classes):
        r"""
        Calls row on ``pitch_classes``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Permutes pitch-classes:

            >>> row([abjad.NumberedPitchClass(2)])
            [NumberedPitchClass(9)]

            >>> row([abjad.NumberedPitchClass(3)])
            [NumberedPitchClass(3)]

            >>> row([abjad.NumberedPitchClass(4)])
            [NumberedPitchClass(6)]

        ..  container:: example

            Permutes pitch-class segment:

            >>> items = [-2, -1, 6, 7, -1, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment_ = row(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    af'8
                    c'8
                    f'8
                    e'8
                    c'8
                    e'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Permutes row:

            >>> numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            >>> row_2 = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row_2)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> row_3 = row(row_2)
            >>> lilypond_file = abjad.illustrate(row_3)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Permutes row:

            >>> numbers = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
            >>> row_2 = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row_2)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    b'8
                    bf'8
                    a'8
                    af'8
                    g'8
                    fs'8
                    f'8
                    e'8
                    ef'8
                    d'8
                    cs'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> row_3 = row(row_2)
            >>> lilypond_file = abjad.illustrate(row_3)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    c'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    f'8
                    g'8
                    fs'8
                    ef'8
                    a'8
                    b'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Permutes row:

            >>> numbers = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
            >>> row_2 = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row_2)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    bf'8
                    c'8
                    d'8
                    fs'8
                    af'8
                    g'8
                    f'8
                    ef'8
                    cs'8
                    a'8
                    e'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> row_3 = row(row_2)
            >>> lilypond_file = abjad.illustrate(row_3)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    af'8
                    cs'8
                    a'8
                    f'8
                    bf'8
                    e'8
                    g'8
                    ef'8
                    b'8
                    d'8
                    fs'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns permuted pitch-classes in object of type ``pitch_classes``.
        """
        new_pitch_classes = []
        for pitch_class in pitch_classes:
            pitch_class = NumberedPitchClass(pitch_class)
            i = pitch_class.number
            new_pitch_class = self[i]
            new_pitch_classes.append(new_pitch_class)
        result = type(pitch_classes)(new_pitch_classes)
        return result

    def __getitem__(self, argument):
        r"""
        Gets item or slice identified by ``argument``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets first hexachord:

            >>> lilypond_file = abjad.illustrate(row[:6])
            >>> abjad.show(lilypond_file) # doctest: +SKIP
            PitchClassSegment([0, 1, 11, 9, 3, 6])

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets second hexachord:

            >>> lilypond_file = abjad.illustrate(row[-6:])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns pitch-class segment:

            >>> row[-6:]
            PitchClassSegment([5, 4, 10, 2, 8, 0])

        """
        item = self._collection.__getitem__(argument)
        try:
            return PitchClassSegment(items=item, item_class=NumberedPitchClass)
        except TypeError:
            return item

    def __mul__(self, argument):
        r"""
        Multiplies row by ``argument``.

        ..  container:: example

            Multiplies row:

            >>> row = abjad.TwelveToneRow()
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment = 2 * row
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment = 2 * row
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP


            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns pitch-class segment:

            >>> segment
            PitchClassSegment([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        Returns pitch-class segment.
        """
        return PitchClassSegment(self) * argument

    def __rmul__(self, argument):
        r"""
        Multiplies ``argument`` by row.

        ..  container:: example

            Multiplies integer by row:

            >>> row = abjad.TwelveToneRow()
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment = row * 2
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies integer by row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment = row * 2
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns pitch-class segment:

            >>> segment
            PitchClassSegment([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        """
        return PitchClassSegment(self) * argument

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_string(self):
        return ", ".join([str(abs(pc)) for pc in self])

    ### PRIVATE METHODS ###

    @staticmethod
    def _validate_pitch_classes(pitch_classes):
        numbers = [pc.number for pc in pitch_classes]
        numbers.sort()
        if not numbers == list(range(12)):
            message = f"must contain all twelve pitch-classes: {pitch_classes!r}."
            raise ValueError(message)

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        """
        Gets item class of row.

        ..  container:: example

            Gets item class:

            >>> row = abjad.TwelveToneRow()
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> row.item_class.__name__
            'NumberedPitchClass'

        ..  container:: example

            Gets item class:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> row.item_class.__name__
            'NumberedPitchClass'

        """
        return super().item_class

    @property
    def items(self):
        """
        Gets items in row.

        ..  container:: example

            Gets items in row:

            >>> row = abjad.TwelveToneRow()
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP


            >>> for item in row.items:
            ...     item
            ...
            NumberedPitchClass(0)
            NumberedPitchClass(1)
            NumberedPitchClass(2)
            NumberedPitchClass(3)
            NumberedPitchClass(4)
            NumberedPitchClass(5)
            NumberedPitchClass(6)
            NumberedPitchClass(7)
            NumberedPitchClass(8)
            NumberedPitchClass(9)
            NumberedPitchClass(10)
            NumberedPitchClass(11)

        ..  container:: example

            Gets items in row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> for item in row.items:
            ...     item
            ...
            NumberedPitchClass(1)
            NumberedPitchClass(11)
            NumberedPitchClass(9)
            NumberedPitchClass(3)
            NumberedPitchClass(6)
            NumberedPitchClass(7)
            NumberedPitchClass(5)
            NumberedPitchClass(4)
            NumberedPitchClass(10)
            NumberedPitchClass(2)
            NumberedPitchClass(8)
            NumberedPitchClass(0)

        ..  container:: example

            Returns list:

            >>> isinstance(row.items, list)
            True

        """
        return super().items

    ### PUBLIC METHODS ###

    def count(self, item):
        """
        Counts ``item`` in row.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Counts pitch-class 11 in row:

            >>> row.count(11)
            1

        ..  container:: example

            Counts pitch-class 9 in row:

            >>> row.count(9)
            1

        ..  container:: example

            Counts string in row:

            >>> row.count('text')
            0

        ..  container:: example

            Returns nonnegative integer equal to 0 or 1:

            >>> isinstance(row.count('text'), int)
            True

        """
        return super().count(item)

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Makes row from ``selection``.

        Not yet implemented.

        Returns twelve-tone row.
        """
        raise NotImplementedError

    def has_duplicates(self):
        """
        Is false for all rows.

        ..  container:: example

            Is false:

            >>> row = abjad.TwelveToneRow()
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> row.has_duplicates()
            False

        ..  container:: example

            Is false:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> row.has_duplicates()
            False

        Twelve-tone rows have no duplicates.

        Returns false.
        """
        return super().has_duplicates()

    def index(self, item):
        """
        Gets index of ``item`` in row.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets index of pitch-class 11:

            >>> row.index(11)
            1

        ..  container:: example

            Gets index of pitch-class 9:

            >>> row.index(9)
            2

        ..  container:: example

            Returns nonnegative integer less than 12:

            >>> isinstance(row.index(9), int)
            True

        """
        return super().index(item)

    def invert(self, axis=None):
        r"""
        Inverts row about optional ``axis``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Inverts row about first pitch-class when ``axis`` is none:

            >>> inversion = row.invert()
            >>> lilypond_file = abjad.illustrate(inversion)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    cs'8
                    ef'8
                    f'8
                    b'8
                    af'8
                    g'8
                    a'8
                    bf'8
                    e'8
                    c'8
                    fs'8
                    d'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            First pitch-classes are equal:

            >>> row[0] == inversion[0]
            True

        ..  container:: example

            Inverts row about pitch-class 1:

            >>> inversion = row.invert(axis=1)
            >>> lilypond_file = abjad.illustrate(inversion)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    cs'8
                    ef'8
                    f'8
                    b'8
                    af'8
                    g'8
                    a'8
                    bf'8
                    e'8
                    c'8
                    fs'8
                    d'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Same result as above.

        ..  container:: example

            Inverts row about pitch-class 0:

            >>> inversion = row.invert(axis=0)
            >>> lilypond_file = abjad.illustrate(inversion)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    b'8
                    cs'8
                    ef'8
                    a'8
                    fs'8
                    f'8
                    g'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Inverts row about pitch-class 5:

            >>> inversion = row.invert(axis=5)
            >>> lilypond_file = abjad.illustrate(inversion)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    a'8
                    b'8
                    cs'8
                    g'8
                    e'8
                    ef'8
                    f'8
                    fs'8
                    c'8
                    af'8
                    d'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns twelve-tone row:

            >>> inversion
            TwelveToneRow([9, 11, 1, 7, 4, 3, 5, 6, 0, 8, 2, 10])

        """
        if axis is None:
            axis = self[0]
        items = [pc.invert(axis=axis) for pc in self]
        return new(self, items=items)

    def multiply(self, n=1):
        r"""
        Multiplies pitch-classes in row by ``n``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Multiplies pitch-classes in row by 5:

            >>> multiplication = row.multiply(n=5)
            >>> lilypond_file = abjad.illustrate(multiplication)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    f'8
                    g'8
                    a'8
                    ef'8
                    fs'8
                    b'8
                    cs'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies pitch-classes in row by 7:

            >>> multiplication = row.multiply(n=7)
            >>> lilypond_file = abjad.illustrate(multiplication)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    g'8
                    f'8
                    ef'8
                    a'8
                    fs'8
                    cs'8
                    b'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies pitch-classes in row by 1:

            >>> multiplication = row.multiply(n=1)
            >>> lilypond_file = abjad.illustrate(multiplication)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns twelve-tone row:

            >>> multiplication
            TwelveToneRow([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        """
        return super().multiply(n=n)

    def retrograde(self):
        r"""
        Gets retrograde of row.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets retrograde of row:

            >>> retrograde = row.retrograde()
            >>> lilypond_file = abjad.illustrate(retrograde)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    c'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    f'8
                    g'8
                    fs'8
                    ef'8
                    a'8
                    b'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets retrograde of retrograde of row:

            >>> retrograde = row.retrograde().retrograde()
            >>> lilypond_file = abjad.illustrate(retrograde)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> retrograde == row
            True

        ..  container:: example

            Returns row:

            >>> retrograde
            TwelveToneRow([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        """
        return super().retrograde()

    def rotate(self, n=0, stravinsky=False):
        r"""
        Rotates row by index ``n``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Rotates row to the right:

            >>> rotation = row.rotate(n=1)
            >>> lilypond_file = abjad.illustrate(rotation)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    c'8
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Rotates row to the left:

            >>> rotation = row.rotate(n=-1)
            >>> lilypond_file = abjad.illustrate(rotation)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Rotates row by zero:

            >>> rotation = row.rotate(n=0)
            >>> lilypond_file = abjad.illustrate(rotation)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> rotation == row
            True

        ..  container:: example

            Stravinsky-style rotation back-transposes row to zero:

            >>> rotation = row.rotate(n=-1, stravinsky=True)
            >>> lilypond_file = abjad.illustrate(rotation)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    c'8
                    bf'8
                    e'8
                    g'8
                    af'8
                    fs'8
                    f'8
                    b'8
                    ef'8
                    a'8
                    cs'8
                    d'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns row:

            >>> rotation
            TwelveToneRow([0, 10, 4, 7, 8, 6, 5, 11, 3, 9, 1, 2])

        """
        return super().rotate(n=n, stravinsky=stravinsky)

    def transpose(self, n=0):
        r"""
        Transposes row by index ``n``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Transposes row by positive index:

            >>> transposition = row.transpose(n=13)
            >>> lilypond_file = abjad.illustrate(transposition)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    d'8
                    c'8
                    bf'8
                    e'8
                    g'8
                    af'8
                    fs'8
                    f'8
                    b'8
                    ef'8
                    a'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes row by negative index:

            >>> transposition = row.transpose(n=-13)
            >>> lilypond_file = abjad.illustrate(transposition)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    c'8
                    bf'8
                    af'8
                    d'8
                    f'8
                    fs'8
                    e'8
                    ef'8
                    a'8
                    cs'8
                    g'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes row by zero index:

            >>> transposition = row.transpose(n=0)
            >>> lilypond_file = abjad.illustrate(transposition)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> transposition == row
            True

        ..  container:: example

            Returns row:

            >>> transposition
            TwelveToneRow([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        """
        return super().transpose(n=n)


### FUNCTIONS ###


def pitch_class_segment(items=None, item_class=None, **keywords):
    """
    Makes pitch-class segment or pitch-class segment expression.
    """
    if items is not None:
        return PitchClassSegment(items=items, item_class=item_class)
    name = keywords.pop("name", None)
    expression = Expression(name=name, proxy_class=PitchClassSegment)
    callback = Expression._make_initializer_callback(
        PitchClassSegment, string_template="{}", **keywords
    )
    expression = expression.append_callback(callback)
    return expression
