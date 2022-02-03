import collections
import dataclasses
import typing

from . import cyclictuple as _cyclictuple
from . import pattern as _pattern
from . import pitch as _pitch
from . import sequence as _sequence
from . import typedcollections as _typedcollections


@dataclasses.dataclass(slots=True)
class CompoundOperator:
    """
    Compound operator.

    ..  container:: example

        Rotation followed by transposition:

        >>> operator = abjad.CompoundOperator()
        >>> operator = operator.rotate(n=1)
        >>> operator = operator.transpose(n=2)

        >>> str(operator)
        'T2r1'

        >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7])
        >>> operator(pitch_classes)
        PitchClassSegment(items=[9, 2, 3, 6], item_class=NumberedPitchClass)

    ..  container:: example

        Does not show identity operators:

        >>> operator = abjad.CompoundOperator()
        >>> operator = operator.transpose(n=0)
        >>> operator = operator.multiply(n=5)

        >>> str(operator)
        'M5'

    ..  container:: example

        Shows identity operators:

        >>> operator = abjad.CompoundOperator(
        ...     show_identity_operators=True,
        ...     )
        >>> operator = operator.transpose(n=0)
        >>> operator = operator.multiply(n=5)

        >>> str(operator)
        'M5T0'

    """

    operators: typing.Any = None
    show_identity_operators: bool | None = None

    def __post_init__(self):
        if self.operators is not None:
            if not isinstance(self.operators, collections.abc.Sequence):
                self.operators = (self.operators,)
            assert len(self.operators)
            self.operators = tuple(self.operators)
        assert isinstance(self.show_identity_operators, (bool, type(None))), repr(
            self.show_identity_operators
        )

    def __add__(self, operator) -> "CompoundOperator":
        """
        Composes compound operator and ``operator``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.transpose(n=1)
            >>> operator = operator.multiply(n=5)
            >>> str(operator)
            'M5T1'

        ..  container:: example

            >>> inversion = abjad.Inversion()
            >>> retrograde = abjad.Retrograde()
            >>> transposition = abjad.Transposition(n=1)

            >>> operator_1 = inversion + retrograde
            >>> str(operator_1)
            'IR'

            >>> operator_2 = inversion + transposition
            >>> str(operator_2)
            'IT1'

            >>> operator_3 = operator_1 + operator_2
            >>> str(operator_3)
            'IRIT1'

        """
        operators = list(self.operators)
        if isinstance(operator, type(self)):
            operators[0:0] = operator.operators
        else:
            operators.insert(0, operator)
        result = type(self)()
        for operator in operators:
            result = result._with_operator(operator)
        return result

    def __call__(self, argument):
        """
        Calls compound operator on ``argument``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.rotate(n=1)
            >>> operator = operator.transpose(n=2)
            >>> str(operator)
            'T2r1'

            >>> segment = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> transform = operator(segment)
            >>> lilypond_file = abjad.illustrate(transform)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> transform
            PitchClassSegment(items=[9, 2, 3, 6], item_class=NumberedPitchClass)

        Returns new object with type equal to that of ``argument``.
        """
        if self.operators is None:
            return argument
        for transform in self.operators:
            argument = transform(argument)
        return argument

    def __radd__(self, operator) -> "CompoundOperator":
        """
        Composes ``operator`` and compound operator.

        ..  container

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.transpose(n=1)
            >>> operator = operator.multiply(n=5)
            >>> str(operator)
            'M5T1'

            >>> retrograde = abjad.Retrograde()
            >>> new_operator = retrograde + operator
            >>> str(new_operator)
            'RM5T1'

            >>> new_operator = operator + retrograde
            >>> str(new_operator)
            'M5T1R'

        """
        operators = list(self.operators)
        if isinstance(operator, type(self)):
            operators.extend(operator.operators)
        else:
            operators.append(operator)
        result = type(self)()
        for operator in operators:
            result = result._with_operator(operator)
        return result

    def __str__(self) -> str:
        """
        Gets string representation of compound operator.

        ..  container:: example

            Gets string:

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.rotate(n=1)
            >>> operator = operator.transpose(n=2)

            >>> str(operator)
            'T2r1'

        ..  container:: example

            Gets string of empty operator:

            >>> operator = abjad.CompoundOperator()

            >>> str(operator)
            ''

        """
        result = []
        operators = self.operators or []
        for operator in reversed(operators):
            if operator._is_identity_operator():
                if self.show_identity_operators:
                    result.append(str(operator))
            else:
                result.append(str(operator))
        string = "".join(result)
        return string

    @staticmethod
    def _compose_operators(operator_1, operator_2):
        if isinstance(operator_1, CompoundOperator):
            result = operator_1.__add__(operator_2)
        elif isinstance(operator_2, CompoundOperator):
            result = operator_2.__radd__(operator_1)
        else:
            result = CompoundOperator()
            result = result._with_operator(operator_2)
            result = result._with_operator(operator_1)
        return result

    def _with_operator(self, operator):
        operators = list(self.operators or [])
        operators = operators + [operator]
        return type(self)(
            operators, show_identity_operators=self.show_identity_operators
        )

    def duplicate(self, counts=None, indices=None, period=None) -> "CompoundOperator":
        """
        Configures compound operator to duplicate pitches by ``counts``, with optional
        ``indices`` and ``period``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator.duplicate(counts=1)
            CompoundOperator(operators=(Duplication(counts=1, indices=None, period=None),), show_identity_operators=None)


        """
        operator = Duplication(counts=counts, indices=indices, period=period)
        return self._with_operator(operator)

    def invert(self, axis=None) -> "CompoundOperator":
        """
        Configures compound operator to invert pitches about ``axis``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator.invert(axis=2)
            CompoundOperator(operators=(Inversion(axis=NamedPitch("d'")),), show_identity_operators=None)

        """
        operator = Inversion(axis=axis)
        return self._with_operator(operator)

    def multiply(self, n=1) -> "CompoundOperator":
        """
        Configures compound operator to multiply pitch-classes by index ``n``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator.multiply(n=3)
            CompoundOperator(operators=(Multiplication(n=3),), show_identity_operators=None)

        """
        operator = Multiplication(n=n)
        return self._with_operator(operator)

    def retrograde(self, period=None) -> "CompoundOperator":
        """
        Configures compound operator to retrograde pitches.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator.retrograde()
            CompoundOperator(operators=(Retrograde(period=None),), show_identity_operators=None)

        """
        operator = Retrograde(period=period)
        return self._with_operator(operator)

    def rotate(self, n=0, period=None) -> "CompoundOperator":
        """
        Configures compound operator to rotate pitches by index ``n``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator.rotate(n=-1)
            CompoundOperator(operators=(Rotation(n=-1),), show_identity_operators=None)

        """
        operator = Rotation(n=n, period=period)
        return self._with_operator(operator)

    def transpose(self, n=0) -> "CompoundOperator":
        """
        Configures compound operator to transpose pitches by index ``n``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator.transpose(n=1)
            CompoundOperator(operators=(Transposition(n=1),), show_identity_operators=None)


        """
        operator = Transposition(n=n)
        return self._with_operator(operator)


class Duplication:
    """
    Duplication.

    ..  container:: example:

        >>> abjad.Duplication(counts=2, period=4)
        Duplication(counts=2, indices=None, period=4)


    """

    __slots__ = ("_counts", "_indices", "_period")

    def __init__(self, *, counts=None, indices=None, period=None):
        if counts is not None:
            if isinstance(counts, collections.abc.Sequence):
                assert len(counts)
                counts = tuple(int(_) for _ in counts)
                assert all(0 <= _ for _ in counts)
            else:
                counts = int(counts)
                assert 0 <= counts
        self._counts = counts
        if indices is not None:
            assert all(isinstance(_, int) for _ in indices), repr(indices)
            indices = tuple(indices)
        self._indices = indices
        if period is not None:
            period = int(period)
            assert 0 < period
        self._period = period

    def __call__(self, argument):
        """
        Calls rotation on ``argument``.

        ..  container:: example

            Duplicates once without period:

            >>> operator_ = abjad.Duplication(counts=1)
            >>> numbers = [1, 2, 3, 4]
            >>> operator_(numbers)
            [1, 2, 3, 4, 1, 2, 3, 4]

        ..  container:: example

            Duplicates twice without period:

            >>> operator_ = abjad.Duplication(counts=2)
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> operator_(pitch_classes)
            PitchClassSegment(items=[0, 1, 4, 7, 0, 1, 4, 7, 0, 1, 4, 7], item_class=NumberedPitchClass)

        ..  container:: example

            Duplicates periodically:

            >>> operator_ = abjad.Duplication(counts=1, period=3)
            >>> pitches = abjad.PitchSegment("c' d' e' f' g' a' b' c''")
            >>> for pitch in operator_(pitches):
            ...     pitch
            ...
            NamedPitch("c'")
            NamedPitch("d'")
            NamedPitch("e'")
            NamedPitch("c'")
            NamedPitch("d'")
            NamedPitch("e'")
            NamedPitch("f'")
            NamedPitch("g'")
            NamedPitch("a'")
            NamedPitch("f'")
            NamedPitch("g'")
            NamedPitch("a'")
            NamedPitch("b'")
            NamedPitch("c''")
            NamedPitch("b'")
            NamedPitch("c''")

        ..  container:: example

            Duplicate indices:

            >>> operator_ = abjad.Duplication(
            ...     counts=1,
            ...     indices=(0, -1),
            ...     )
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> operator_(pitch_classes)
            PitchClassSegment(items=[0, 0, 1, 4, 7, 7], item_class=NumberedPitchClass)

        ..  container:: example

            Duplicate indices periodically:

            >>> operator_ = abjad.Duplication(
            ...     counts=1,
            ...     indices=(0,),
            ...     period=2,
            ...     )
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7, 9])
            >>> operator_(pitch_classes)
            PitchClassSegment(items=[0, 0, 1, 4, 4, 7, 9, 9], item_class=NumberedPitchClass)

        ..  container:: example

            Duplicate indices periodically with different counts:

            >>> operator_ = abjad.Duplication(
            ...     counts=(1, 2),
            ...     indices=(0,),
            ...     period=2,
            ...     )
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7, 9])
            >>> operator_(pitch_classes)
            PitchClassSegment(items=[0, 0, 1, 4, 4, 4, 7, 9, 9], item_class=NumberedPitchClass)

        ..  container:: example

            Cyclic counts:

            >>> operator_ = abjad.Duplication(counts=(0, 1, 2, 3))
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7, 9])
            >>> operator_(pitch_classes)
            PitchClassSegment(items=[0, 1, 1, 4, 4, 4, 7, 7, 7, 7, 9], item_class=NumberedPitchClass)

        Returns new object with type equal to that of ``argument``.
        """
        if not isinstance(argument, collections.abc.Sequence):
            argument = (argument,)

        counts = self.counts
        if isinstance(counts, int):
            counts = counts + 1
        else:
            counts = [_ + 1 for _ in counts]

        if not self.period and not self.indices:
            if isinstance(counts, int):
                return type(argument)(argument * counts)
            else:
                counts = _cyclictuple.CyclicTuple(counts)
                result = []
                for i, x in enumerate(argument):
                    count = counts[i]
                    result.extend([x] * count)
                if isinstance(argument, _typedcollections.TypedCollection):
                    result = dataclasses.replace(argument, items=result)
                else:
                    result = type(argument)(result)
                return result

        if isinstance(counts, int):
            counts = [counts]
        counts = _cyclictuple.CyclicTuple(counts)

        if not self.indices:
            if isinstance(argument, _typedcollections.TypedCollection):
                result = dataclasses.replace(argument, items=())
            else:
                result = type(argument)()
            iterator = _sequence.Sequence(argument).partition_by_counts(
                [self.period], cyclic=True, overhang=True
            )
            for i, shard in enumerate(iterator):
                shard = type(argument)(shard) * counts[i]
                result = result + shard
            return result

        pattern = _pattern.Pattern(indices=self.indices, period=self.period)
        result = []
        length = len(argument)
        j = 0
        for i, x in enumerate(argument):
            if pattern.matches_index(i, length):
                count = counts[j]
                result.extend([x] * count)
                j += 1
            else:
                result.append(x)
        if isinstance(argument, _typedcollections.TypedCollection):
            result = dataclasses.replace(argument, items=result)
        else:
            result = type(argument)(result)
        return result

    def __eq__(self, argument) -> bool:
        """
        Compares ``counts``, ``indices``, ``period``.
        """
        if isinstance(argument, type(self)):
            return (
                self.counts == argument.counts
                and self.indices == argument.indices
                and self.period == argument.period
            )
        return False

    def __hash__(self) -> int:
        """
        Hashes duplication.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(counts={self.counts!r}, indices={self.indices!r}, period={self.period!r})"

    @property
    def counts(self) -> int | None:
        """
        Gets counts of duplication.

        ..  container:: example

            >>> operator_ = abjad.Duplication(counts=1, period=3)
            >>> operator_.counts
            1

        """
        return self._counts

    @property
    def indices(self) -> tuple[int] | None:
        """
        Gets indices of duplication.

        ..  container:: example

            >>> operator_ = abjad.Duplication(
            ...     counts=1,
            ...     indices=(0, -1),
            ... )
            >>> operator_.indices
            (0, -1)

        """
        return self._indices

    @property
    def period(self) -> int | None:
        """
        Gets period of duplication.

        ..  container:: example

            >>> abjad.Duplication(counts=1, period=3).period
            3

        """
        return self._period


class Inversion:
    """
    Inversion operator.

    ..  container:: example

        >>> abjad.Inversion()
        Inversion(axis=None)

        >>> abjad.Inversion(axis=15)
        Inversion(axis=NamedPitch("ef''"))

    """

    __slots__ = ("_axis",)

    def __init__(self, *, axis=None):
        if axis is not None:
            axis = _pitch.NamedPitch(axis)
        self._axis = axis

    def __add__(self, operator) -> "CompoundOperator":
        r"""
        Composes inversion and ``operator``.

        ..  container:: example

            Example segment:

            >>> items = [0, 2, 4, 5]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Example operators:

            >>> inversion = abjad.Inversion()
            >>> transposition = abjad.Transposition(n=3)

        ..  container:: example

            Transposition followed by inversion:

            >>> operator = inversion + transposition
            >>> str(operator)
            'IT3'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    a'8
                    g'8
                    f'8
                    e'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Inversion followed by transposition:

            >>> operator = transposition + inversion
            >>> str(operator)
            'T3I'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    ef'8
                    cs'8
                    b'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        return CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        """
        Calls inversion on ``argument``.

        ..  container:: example

            Inverts numbered pitch-class:

            >>> inversion = abjad.Inversion()
            >>> pitch_class = abjad.NumberedPitchClass(1)
            >>> inversion(pitch_class)
            NumberedPitchClass(11)

            Inverts numbered pitch:

            >>> inversion = abjad.Inversion()
            >>> pitch = abjad.NumberedPitch(15)
            >>> inversion(pitch)
            NumberedPitch(-15)

            Inverts named pitch:

            >>> inversion = abjad.Inversion()
            >>> pitch = abjad.NamedPitch("d'")
            >>> inversion(pitch)
            NamedPitch('bf')

            Inverts named pitch class:

            >>> inversion = abjad.Inversion()
            >>> pitch_class = abjad.NamedPitchClass('d')
            >>> inversion(pitch_class)
            NamedPitchClass('bf')

            Inverts pitch segment:

            >>> inversion = abjad.Inversion()
            >>> segment = abjad.PitchSegment("c' d' e'")
            >>> inversion(segment)
            PitchSegment(items="c' bf af", item_class=NamedPitch)

            Inverts pitch class segment:

            >>> inversion = abjad.Inversion()
            >>> segment = abjad.PitchClassSegment("c d e")
            >>> inversion(segment)
            PitchClassSegment(items="c bf af", item_class=NamedPitchClass)

            Inverts pitch class set:

            >>> inversion = abjad.Inversion()
            >>> setting = abjad.PitchClassSet("c d e")
            >>> inversion(setting)
            PitchClassSet(items=['c', 'af', 'bf'], item_class=abjad.NamedPitchClass)

        Returns new object with type equal to that of ``argument``.
        """
        if hasattr(argument, "invert"):
            result = argument.invert(axis=self.axis)
        else:
            raise TypeError(f"do not know how to invert: {argument!r}.")
        return result

    def __eq__(self, argument) -> bool:
        """
        Compares ``axis``.
        """
        if isinstance(argument, type(self)):
            return self.axis == argument.axis
        return False

    def __hash__(self) -> int:
        """
        Hashes inversion.
        """
        return hash(self.__class__.__name__ + str(self))

    def __radd__(self, operator):
        """
        Right-addition not defined on inversion.

        ..  container:: example

            >>> abjad.Inversion().__radd__(abjad.Inversion())
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on Inversion.

        Raises not implemented error.
        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(axis={self.axis!r})"

    def __str__(self) -> str:
        """
        Gets string representation of operator.

        ..  container:: example

            >>> str(abjad.Inversion())
            'I'

        ..  container:: example

            >>> str(abjad.Inversion(axis=15))
            'I(Eb5)'

        """
        if self.axis is None:
            return "I"
        axis = self.axis.get_name(locale="us")
        string = f"I({axis})"
        return string

    def _is_identity_operator(self):
        return False

    @property
    def axis(self) -> typing.Optional["_pitch.NamedPitch"]:
        """
        Gets axis of inversion.

        ..  container:: example

            >>> inversion = abjad.Inversion()
            >>> inversion.axis is None
            True

            >>> inversion = abjad.Inversion(axis=15)
            >>> inversion.axis
            NamedPitch("ef''")

        """
        return self._axis


class Multiplication:
    """
    Multiplication operator.

    ..  container:: example

        >>> abjad.Multiplication()
        Multiplication(n=1)

        >>> abjad.Multiplication(n=5)
        Multiplication(n=5)

    """

    __slots__ = ("_n",)

    def __init__(self, *, n=1):
        self._n = n

    def __add__(self, operator) -> CompoundOperator:
        r"""
        Composes multiplication and ``operator``.

        ..  container:: example

            Example segment:

            >>> items = [0, 2, 4, 5]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Example operators:

            >>> multiplication = abjad.Multiplication(n=5)
            >>> transposition = abjad.Transposition(n=3)

        ..  container:: example

            Transposition followed by multiplication:

            >>> operator = multiplication + transposition
            >>> str(operator)
            'M5T3'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    ef'8
                    cs'8
                    b'8
                    e'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because multiplication and transposition commute:

            >>> operator = transposition + multiplication
            >>> str(operator)
            'T3M5'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    ef'8
                    cs'8
                    b'8
                    e'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        return CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        """
        Calls multiplication on ``argument``.

        ..  container:: example

            Multiplies pitch-class:

            >>> multiplication = abjad.Multiplication(n=5)
            >>> pitch_class = abjad.NumberedPitchClass(4)
            >>> multiplication(pitch_class)
            NumberedPitchClass(8)

            Multiplies pitch:

            >>> multiplication = abjad.Multiplication(n=7)
            >>> pitch = abjad.NamedPitch("f'")
            >>> multiplication(pitch)
            NamedPitch("b'''")

        Returns new object with type equal to that of ``argument``.
        """
        if hasattr(argument, "multiply"):
            result = argument.multiply(self.n)
        else:
            raise TypeError(f"do not know how to multiply: {argument!r}.")
        return result

    def __eq__(self, argument) -> bool:
        """
        Compares ``n``.
        """
        if isinstance(argument, type(self)):
            return self.n == argument.n
        return False

    def __hash__(self) -> int:
        """
        Hashes multiplication.
        """
        return hash(self.__class__.__name__ + str(self))

    def __radd__(self, operator):
        """
        Right-addition not defined on multiplication.

        ..  container:: example

            >>> abjad.Multiplication().__radd__(abjad.Multiplication())
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on Multiplication.

        Raises not implemented error.
        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(n={self.n!r})"

    def __str__(self) -> str:
        """
        Gets string representation of operator.

        ..  container:: example

            >>> str(abjad.Multiplication())
            'M1'

        ..  container:: example

            >>> str(abjad.Multiplication(n=5))
            'M5'

        """
        string = f"M{self.n}"
        return string

    def _is_identity_operator(self):
        if self.n == 1:
            return True
        return False

    @property
    def n(self) -> int | None:
        """
        Gets index of multiplication.

        ..  container:: example

            >>> multiplication = abjad.Multiplication()
            >>> multiplication.n
            1

            >>> multiplication = abjad.Multiplication(n=5)
            >>> multiplication.n
            5

        """
        return self._n


class Retrograde:
    """
    Retrograde operator.

    ..  container:: example:

        >>> abjad.Retrograde()
        Retrograde(period=None)

    """

    __slots__ = ("_period",)

    def __init__(self, period=None):
        if period is not None:
            period = abs(int(period))
            assert 0 < period
        self._period = period

    def __add__(self, operator) -> CompoundOperator:
        r"""
        Composes retrograde and ``operator``.

        ..  container:: example

            Example segment:

            >>> items = [0, 2, 4, 5]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Example operators:

            >>> retrograde = abjad.Retrograde()
            >>> transposition = abjad.Transposition(n=3)

        ..  container:: example

            Transposition followed by retrograde:

            >>> operator = retrograde + transposition
            >>> str(operator)
            'RT3'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    af'8
                    g'8
                    f'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because retrograde and transposition commute:

            >>> operator = transposition + retrograde
            >>> str(operator)
            'T3R'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    af'8
                    g'8
                    f'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        return CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        """
        Calls retrograde on ``argument``.

        ..  container:: example

            Gets retrograde pitch classes:

            >>> retrograde = abjad.Retrograde()
            >>> segment = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> retrograde(segment)
            PitchClassSegment(items=[7, 4, 1, 0], item_class=NumberedPitchClass)

            Does not retrograde single pitches or pitch-classes:

            >>> retrogresion = abjad.Retrograde()
            >>> pitch_class = abjad.NumberedPitchClass(6)
            >>> retrograde(pitch_class)
            NumberedPitchClass(6)

            Periodic retrograde:

            ..  todo:: Deprecated.

            >>> retrograde = abjad.Retrograde(period=3)
            >>> segment = abjad.PitchSegment("c' d' e' f' g' a' b' c''")
            >>> retrograde(segment)
            PitchSegment(items="e' d' c' a' g' f' c'' b'", item_class=NamedPitch)

        Returns new object with type equal to that of ``argument``.
        """
        if isinstance(argument, (_pitch.Pitch, _pitch.PitchClass)):
            return argument
        if not isinstance(argument, (_pitch.PitchSegment, _pitch.PitchClassSegment)):
            argument = _pitch.PitchSegment(argument)
        if not self.period:
            return type(argument)(reversed(argument))
        result = dataclasses.replace(argument, items=())
        for shard in _sequence.Sequence(argument).partition_by_counts(
            [self.period], cyclic=True, overhang=True
        ):
            shard = type(argument)(shard)
            shard = type(argument)(reversed(shard))
            result = result + shard
        return result

    def __eq__(self, argument) -> bool:
        """
        Compares ``period``.
        """
        if isinstance(argument, type(self)):
            return self.period == argument.period
        return False

    def __hash__(self) -> int:
        """
        Hashes retrograde.
        """
        return hash(self.__class__.__name__ + str(self))

    def __radd__(self, operator):
        """
        Right-addition not defined on retrograde.

        ..  container:: example

            >>> abjad.Retrograde().__radd__(abjad.Retrograde())
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on Retrograde.

        Raises not implemented error.
        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(period={self.period!r})"

    def __str__(self) -> str:
        """
        Gets string representation of operator.

        ..  container:: example

            >>> str(abjad.Retrograde())
            'R'

        """
        return "R"

    def _is_identity_operator(self):
        return False

    @property
    def period(self) -> int | None:
        """
        Gets optional period of retrograde.

        ..  todo:: Deprecated.

        ..  container:: example

            >>> abjad.Retrograde(period=3).period
            3

        """
        return self._period


class Rotation:
    """
    Rotation operator.

    ..  container:: example:

        >>> abjad.Rotation()
        Rotation(n=0)

        >>> abjad.Rotation(n=1)
        Rotation(n=1)

    """

    __slots__ = ("_n", "_period")

    def __init__(self, *, n=0, period=None):
        self._n = int(n)
        if period is not None:
            period = abs(int(period))
            assert 0 < period
        self._period = period

    def __add__(self, operator) -> "CompoundOperator":
        r"""
        Composes rotation and ``operator``.

        ..  container:: example

            Example segment:

            >>> items = [0, 2, 4, 5]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Example operators:

            >>> rotation = abjad.Rotation(n=-1)
            >>> transposition = abjad.Transposition(n=3)

        ..  container:: example

            Transposition followed by rotation:

            >>> operator = rotation + transposition
            >>> str(operator)
            'r-1T3'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    f'8
                    g'8
                    af'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because rotation and transposition commute:

            >>> operator = transposition + rotation
            >>> str(operator)
            'T3r-1'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    f'8
                    g'8
                    af'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        return CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        """
        Calls rotation on ``argument``.

        ..  container:: example

            Rotates pitch classes:

            >>> rotation = abjad.Rotation(n=1)
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> rotation(pitch_classes)
            PitchClassSegment(items=[7, 0, 1, 4], item_class=NumberedPitchClass)

            Does not rotate single pitches or pitch-classes:

            >>> rotation = abjad.Rotation(n=1)
            >>> pitch_class = abjad.NumberedPitchClass(6)
            >>> rotation(pitch_class)
            NumberedPitchClass(6)

            Periodic rotation:

            ..  todo:: Deprecated.

            >>> rotation = abjad.Rotation(n=1, period=3)
            >>> pitches = abjad.PitchSegment("c' d' e' f' g' a' b' c''")
            >>> rotation(pitches)
            PitchSegment(items="e' c' d' a' f' g' c'' b'", item_class=NamedPitch)

        Returns new object with type equal to that of ``argument``.
        """
        if isinstance(argument, (_pitch.Pitch, _pitch.PitchClass)):
            return argument
        if not isinstance(argument, (_pitch.PitchSegment, _pitch.PitchClassSegment)):
            argument = _pitch.PitchSegment(argument)
        if not self.period:
            return argument.rotate(self.n)
        result = dataclasses.replace(argument, items=())
        for shard in _sequence.Sequence(argument).partition_by_counts(
            [self.period], cyclic=True, overhang=True
        ):
            shard = type(argument)(shard)
            shard = shard.rotate(self.n)
            result = result + shard
        return result

    def __eq__(self, argument) -> bool:
        """
        Compares ``n``, ``period``.
        """
        if isinstance(argument, type(self)):
            return self.n == argument.n and self.period == argument.period
        return False

    def __hash__(self) -> int:
        """
        Hashes rotation.
        """
        return hash(self.__class__.__name__ + str(self))

    def __radd__(self, operator):
        """
        Right-addition not defined on rotation.

        ..  container:: example

            >>> abjad.Rotation().__radd__(abjad.Rotation())
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on Rotation.

        Raises not implemented error.
        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(n={self.n!r})"

    def __str__(self) -> str:
        """
        Gets string representation of operator.

        ..  container:: example

            >>> str(abjad.Rotation())
            'r0'

        ..  container:: example

            >>> str(abjad.Rotation(n=1))
            'r1'

        """
        string = f"r{self.n}"
        return string

    def _is_identity_operator(self):
        if self.n == 0:
            return True
        return False

    @property
    def n(self) -> int:
        """
        Gets index of rotation.

        ..  container:: example

            >>> rotation = abjad.Rotation()
            >>> rotation.n
            0

            >>> rotation = abjad.Rotation(n=2)
            >>> rotation.n
            2

        """
        return self._n

    @property
    def period(self) -> int | None:
        """
        Gets period of rotation.

        ..  todo:: Deprecated.

        ..  container:: example

            >>> abjad.Rotation(n=2, period=3).period
            3

        """
        return self._period


class Transposition:
    """
    Transposition operator.

    ..  container:: example

        >>> abjad.Transposition()
        Transposition(n=0)

        >>> abjad.Transposition(n=2)
        Transposition(n=2)

    """

    __slots__ = ("_n",)

    def __init__(self, *, n=0):
        self._n = n

    def __add__(self, operator) -> "CompoundOperator":
        r"""
        Composes transposition and ``operator``.

        ..  container:: example

            Example segment:

            >>> items = [0, 2, 4, 5]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Example operators:

            >>> T_1 = abjad.Transposition(n=1)
            >>> T_3 = abjad.Transposition(n=3)

        ..  container:: example

            Successive transposition:

            >>> operator = T_1 + T_3
            >>> str(operator)
            'T1T3'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    e'8
                    fs'8
                    af'8
                    a'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because transposition commutes:

            >>> operator = T_3 + T_1
            >>> str(operator)
            'T3T1'

            >>> segment_ = operator(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    e'8
                    fs'8
                    af'8
                    a'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        return CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        """
        Calls transposition on ``argument``.

        ..  container:: example

            Transposes pitch-class:

            >>> transposition = abjad.Transposition(n=2)
            >>> pitch_class = abjad.NumberedPitchClass(1)
            >>> transposition(pitch_class)
            NumberedPitchClass(3)

        ..  container:: example

            Transposes pitch:

            >>> transposition = abjad.Transposition(n=2)
            >>> pitch = abjad.NumberedPitch(15)
            >>> transposition(pitch)
            NumberedPitch(17)

        ..  container:: example

            Transposes list of pitches:

            >>> transposition = abjad.Transposition(n=2)
            >>> pitches = [abjad.NumberedPitch(_) for _ in [15, 16]]
            >>> transposition(pitches)
            [NumberedPitch(17), NumberedPitch(18)]

        Returns new object with type equal to that of ``argument``.
        """
        if hasattr(argument, "transpose"):
            result = argument.transpose(self.n)
        elif isinstance(argument, collections.abc.Iterable):
            items = []
            for item in argument:
                item = item.transpose(self.n)
                items.append(item)
            result = type(argument)(items)
        else:
            raise TypeError(f"do not know how to transpose: {argument!r}.")
        return result

    def __eq__(self, argument) -> bool:
        """
        Compares ``n``.
        """
        if isinstance(argument, type(self)):
            return self.n == argument.n
        return False

    def __hash__(self) -> int:
        """
        Hashes transposition.
        """
        return hash(self.__class__.__name__ + str(self))

    def __radd__(self, operator):
        """
        Right-addition not defined on transposition.

        ..  container:: example

            >>> abjad.Transposition().__radd__(abjad.Transposition())
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on Transposition.

        Raises not implemented error.
        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(n={self.n!r})"

    def __str__(self) -> str:
        """
        Gets string representation of operator.

        ..  container:: example

            >>> str(abjad.Transposition())
            'T0'

        ..  container:: example

            >>> str(abjad.Transposition(n=2))
            'T2'

        """
        string = f"T{self.n}"
        return string

    def _is_identity_operator(self):
        if self.n == 0:
            return True
        return False

    @property
    def n(self):
        """
        Gets index of transposition.

        ..  container:: example

            >>> transposition = abjad.Transposition()
            >>> transposition.n
            0

            >>> transposition = abjad.Transposition(n=2)
            >>> transposition.n
            2

        Set to integer, interval or none.
        """
        return self._n
