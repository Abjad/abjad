import collections

from .. import markups
from ..cyclictuple import CyclicTuple
from ..new import new
from ..pattern import Pattern
from ..sequence import Sequence
from ..storage import StorageFormatManager
from ..typedcollections import TypedCollection
from .pitchclasses import PitchClass
from .pitches import NamedPitch, Pitch
from .segments import PitchClassSegment, PitchSegment


class CompoundOperator:
    """
    Compound operator.

    ..  container:: example

        Rotation followed by transposition:

        >>> operator = abjad.CompoundOperator()
        >>> operator = operator.rotate(n=1, stravinsky=True)
        >>> operator = operator.transpose(n=2)

        >>> str(operator)
        'T2rs1'

        >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7])
        >>> operator(pitch_classes)
        PitchClassSegment([2, 7, 8, 11])

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_operators", "_show_identity_operators")

    ### INITIALIZER ###

    def __init__(self, operators=None, *, show_identity_operators=None):
        if operators is not None:
            if not isinstance(operators, collections.abc.Sequence):
                operators = (operators,)
            assert len(operators)
            operators = tuple(operators)
        self._operators = operators
        assert isinstance(show_identity_operators, (bool, type(None)))
        self._show_identity_operators = show_identity_operators

    ### SPECIAL METHODS ###

    def __add__(self, operator):
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

            >>> string = abjad.storage(operator_3)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Transposition(n=1),
                    Inversion(),
                    Retrograde(),
                    Inversion(),
                    ],
                )

        Returns new compound operator.
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
            >>> operator = operator.rotate(n=1, stravinsky=True)
            >>> operator = operator.transpose(n=2)
            >>> str(operator)
            'T2rs1'

            >>> segment = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> transform = operator(segment)
            >>> lilypond_file = abjad.illustrate(transform)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> transform
            PitchClassSegment([2, 7, 8, 11])

        Returns new object with type equal to that of ``argument``.
        """
        if self.operators is None:
            return argument
        for transform in self.operators:
            argument = transform(argument)
        return argument

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __radd__(self, operator):
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

        Returns new compound operator.
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

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
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

        Returns string.
        """
        result = []
        operators = self.operators or []
        for operator in reversed(operators):
            if operator._is_identity_operator():
                if self.show_identity_operators:
                    result.append(str(operator))
            else:
                result.append(str(operator))
        result = "".join(result)
        return result

    ### PRIVATE METHODS ###

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

    def _get_markup(self, direction=None):
        markups = []
        operators = self.operators or []
        for operator in operators:
            markup = operator._get_markup(direction=direction)
            if self.show_identity_operators or not operator._is_identity_operator():
                markups.append(markup)
        if len(markups) == 0:
            return
        elif len(markups) == 1:
            markup = markups[0]
        else:
            markup = markups.Markup.concat(markups, direction=direction)
        return markup

    def _with_operator(self, operator):
        operators = self.operators or []
        operators = operators + [operator]
        return type(self)(
            operators, show_identity_operators=self.show_identity_operators
        )

    ### PUBLIC PROPERTIES ###

    @property
    def operators(self):
        """
        Gets operators.

        ..  container:: example

            Gets operators:

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.rotate(n=1)
            >>> operator = operator.transpose(n=2)

            >>> for operator_ in operator.operators:
            ...     operator_
            ...
            Rotation(n=1)
            Transposition(n=2)

        Returns list of operators.
        """
        if self._operators is not None:
            return list(self._operators)

    @property
    def show_identity_operators(self):
        """
        Is true when string representation of operator should show identity
        operators.

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

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._show_identity_operators

    ### PUBLIC METHODS ###

    def duplicate(self, counts=None, indices=None, period=None):
        """
        Configures compound operator to duplicate pitches by ``counts``, with
        optional ``indices`` and ``period``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.duplicate(counts=1)
            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Duplication(counts=1),
                    ],
                )

        Returns new compound operator.
        """
        operator = Duplication(counts=counts, indices=indices, period=period)
        return self._with_operator(operator)

    def invert(self, axis=None):
        """
        Configures compound operator to invert pitches about ``axis``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.invert(axis=2)
            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Inversion(axis=NamedPitch("d'")),
                    ],
                )

        Returns new compound operator.
        """
        operator = Inversion(axis=axis)
        return self._with_operator(operator)

    def multiply(self, n=1):
        """
        Configures compound operator to multiply pitch-classes by index ``n``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.multiply(n=3)
            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Multiplication(n=3),
                    ],
                )

        Returns new compound operator.
        """
        operator = Multiplication(n=n)
        return self._with_operator(operator)

    def retrograde(self, period=None):
        """
        Configures compound operator to retrograde pitches.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.retrograde()
            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Retrograde(),
                    ],
                )

        Returns new compound operator.
        """
        operator = Retrograde(period=period)
        return self._with_operator(operator)

    def rotate(self, n=0, period=None, stravinsky=None):
        """
        Configures compound operator to rotate pitches by index ``n``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.rotate(n=-1)
            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Rotation(n=-1),
                    ],
                )

        Returns new compound operator.
        """
        operator = Rotation(n=n, period=period, stravinsky=stravinsky)
        return self._with_operator(operator)

    def transpose(self, n=0):
        """
        Configures compound operator to transpose pitches by index ``n``.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.transpose(n=1)

            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Transposition(n=1),
                    ],
                )

        Returns new compound operator.
        """
        operator = Transposition(n=n)
        return self._with_operator(operator)


class Duplication:
    """
    Duplication.

    ..  container:: example:

        >>> operator_ = abjad.Duplication(counts=2, period=4)

        >>> string = abjad.storage(operator_)
        >>> print(string)
        abjad.Duplication(
            counts=2,
            period=4,
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_counts", "_indices", "_period")

    ### INITIALIZER ###

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

    ### SPECIAL METHODS ###

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
            PitchClassSegment([0, 1, 4, 7, 0, 1, 4, 7, 0, 1, 4, 7])

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
            PitchClassSegment([0, 0, 1, 4, 7, 7])

        ..  container:: example

            Duplicate indices periodically:

            >>> operator_ = abjad.Duplication(
            ...     counts=1,
            ...     indices=(0,),
            ...     period=2,
            ...     )
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7, 9])
            >>> operator_(pitch_classes)
            PitchClassSegment([0, 0, 1, 4, 4, 7, 9, 9])

        ..  container:: example

            Duplicate indices periodically with different counts:

            >>> operator_ = abjad.Duplication(
            ...     counts=(1, 2),
            ...     indices=(0,),
            ...     period=2,
            ...     )
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7, 9])
            >>> operator_(pitch_classes)
            PitchClassSegment([0, 0, 1, 4, 4, 4, 7, 9, 9])

        ..  container:: example

            Cyclic counts:

            >>> operator_ = abjad.Duplication(counts=(0, 1, 2, 3))
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7, 9])
            >>> operator_(pitch_classes)
            PitchClassSegment([0, 1, 1, 4, 4, 4, 7, 7, 7, 7, 9])

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
                counts = CyclicTuple(counts)
                result = []
                for i, x in enumerate(argument):
                    count = counts[i]
                    result.extend([x] * count)
                if isinstance(argument, TypedCollection):
                    result = new(argument, items=result)
                else:
                    result = type(argument)(result)
                return result

        if isinstance(counts, int):
            counts = [counts]
        counts = CyclicTuple(counts)

        if not self.indices:
            if isinstance(argument, TypedCollection):
                result = new(argument, items=())
            else:
                result = type(argument)()
            iterator = Sequence(argument).partition_by_counts(
                [self.period], cyclic=True, overhang=True
            )
            for i, shard in enumerate(iterator):
                shard = type(argument)(shard) * counts[i]
                result = result + shard
            return result

        pattern = Pattern(indices=self.indices, period=self.period)
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
        if isinstance(argument, TypedCollection):
            result = new(argument, items=result)
        else:
            result = type(argument)(result)
        return result

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        """
        Gets counts of duplication.

        ..  container:: example

            >>> operator_ = abjad.Duplication(counts=1, period=3)
            >>> operator_.counts
            1

        Returns integer or none.
        """
        return self._counts

    @property
    def indices(self):
        """
        Gets indices of duplication.

        ..  container:: example

            >>> operator_ = abjad.Duplication(
            ...     counts=1,
            ...     indices=(0, -1),
            ...     )
            >>> operator_.indices
            (0, -1)

        Returns integer or none.
        """
        return self._indices

    @property
    def period(self):
        """
        Gets period of duplication.

        ..  container:: example

            >>> operator_ = abjad.Duplication(counts=1, period=3)
            >>> operator_.period
            3

        Returns integer or none.
        """
        return self._period


class Inversion:
    """
    Inversion operator.

    ..  container:: example

        >>> abjad.Inversion()
        Inversion()

    ..  container:: example

        >>> abjad.Inversion(axis=15)
        Inversion(axis=NamedPitch("ef''"))

    Object model of twelve-tone inversion operator.
    """

    ### CLASS VARIABLES ##

    __slots__ = ("_axis",)

    ### INITIALIZER ###

    def __init__(self, *, axis=None):
        if axis is not None:
            axis = NamedPitch(axis)
        self._axis = axis

    ### SPECIAL METHODS ###

    def __add__(self, operator):
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

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
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

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    ef'8
                    cs'8
                    b'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns compound operator:

            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Inversion(),
                    Transposition(n=3),
                    ],
                )

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

        ..  container:: example

            Inverts numbered pitch:

            >>> inversion = abjad.Inversion()
            >>> pitch = abjad.NumberedPitch(15)
            >>> inversion(pitch)
            NumberedPitch(-15)

        ..  container:: example

            Inverts named pitch:

            >>> inversion = abjad.Inversion()
            >>> pitch = abjad.NamedPitch("d'")
            >>> inversion(pitch)
            NamedPitch('bf')

        ..  container:: example

            Inverts named pitch class:

            >>> inversion = abjad.Inversion()
            >>> pitch_class = abjad.NamedPitchClass('d')
            >>> inversion(pitch_class)
            NamedPitchClass('bf')

        ..  container:: example

            Inverts pitch segment:

            >>> inversion = abjad.Inversion()
            >>> segment = abjad.PitchSegment("c' d' e'")
            >>> inversion(segment)
            PitchSegment("c' bf af")

        ..  container:: example

            Inverts pitch class segment:

            >>> inversion = abjad.Inversion()
            >>> segment = abjad.PitchClassSegment("c d e")
            >>> inversion(segment)
            PitchClassSegment("c bf af")

        ..  container:: example

            Inverts pitch class set:

            >>> inversion = abjad.Inversion()
            >>> setting = abjad.PitchClassSet("c d e")
            >>> inversion(setting)
            PitchClassSet(['c', 'af', 'bf'])

        Returns new object with type equal to that of ``argument``.
        """
        if hasattr(argument, "invert"):
            result = argument.invert(axis=self.axis)
        else:
            raise TypeError(f"do not know how to invert: {argument!r}.")
        return result

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

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
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
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

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        markup = markups.Markup("I", direction=direction)
        if self.axis is not None:
            axis = self.axis.get_name(locale="us")
            subscript = markups.Markup(axis).sub()
            markup = markups.Markup.concat([markup, subscript])
        return markup

    def _is_identity_operator(self):
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def axis(self):
        """
        Gets axis of inversion.

        ..  container:: example

            >>> inversion = abjad.Inversion()
            >>> inversion.axis is None
            True

        ..  container:: example

            >>> inversion = abjad.Inversion(axis=15)
            >>> inversion.axis
            NamedPitch("ef''")

        Returns named pitch or none.
        """
        return self._axis


class Multiplication:
    """
    Multiplication operator.

    ..  container:: example

        >>> abjad.Multiplication()
        Multiplication(n=1)

    ..  container:: example

        >>> abjad.Multiplication(n=5)
        Multiplication(n=5)

    Object model of twelve-tone multiplication operator.
    """

    ### CLASS VARIABLES ##

    __slots__ = ("_n",)

    ### INITIALIZER ###

    def __init__(self, *, n=1):
        self._n = n

    ### SPECIAL METHODS ###

    def __add__(self, operator):
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

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
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

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    ef'8
                    cs'8
                    b'8
                    e'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns compound operator.
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

        ..  container:: example

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
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

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
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
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

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        operator = markups.Markup("M", direction=direction)
        subscript = markups.Markup(self.n).sub()
        markup = markups.Markup.concat([operator, subscript])
        return markup

    def _is_identity_operator(self):
        if self.n == 1:
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def n(self):
        """
        Gets index of multiplication.

        ..  container:: example

            >>> multiplication = abjad.Multiplication()
            >>> multiplication.n
            1

        ..  container:: example

            >>> multiplication = abjad.Multiplication(n=5)
            >>> multiplication.n
            5

        Set to integer or none.
        """
        return self._n


class Retrograde:
    """
    Retrograde operator.

    ..  container:: example:

        >>> abjad.Retrograde()
        Retrograde()

    Object model of twelve-tone retrograde operator.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_period",)

    ### INITIALIZER ###

    def __init__(self, period=None):
        if period is not None:
            period = abs(int(period))
            assert 0 < period
        self._period = period

    ### SPECIAL METHODS ###

    def __add__(self, operator):
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

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
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

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    af'8
                    g'8
                    f'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns compound operator:

            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Retrograde(),
                    Transposition(n=3),
                    ],
                )

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
            PitchClassSegment([7, 4, 1, 0])

        ..  container:: example

            Does not retrograde single pitches or pitch-classes:

            >>> retrogresion = abjad.Retrograde()
            >>> pitch_class = abjad.NumberedPitchClass(6)
            >>> retrograde(pitch_class)
            NumberedPitchClass(6)

        ..  container:: example

            Periodic retrograde:

            ..  todo:: Deprecated.

            >>> retrograde = abjad.Retrograde(period=3)
            >>> segment = abjad.PitchSegment("c' d' e' f' g' a' b' c''")
            >>> retrograde(segment)
            PitchSegment("e' d' c' a' g' f' c'' b'")

        Returns new object with type equal to that of ``argument``.
        """
        if isinstance(argument, (Pitch, PitchClass)):
            return argument
        if not isinstance(argument, (PitchSegment, PitchClassSegment)):
            argument = PitchSegment(argument)
        if not self.period:
            return type(argument)(reversed(argument))
        result = new(argument, items=())
        for shard in Sequence(argument).partition_by_counts(
            [self.period], cyclic=True, overhang=True
        ):
            shard = type(argument)(shard)
            shard = type(argument)(reversed(shard))
            result = result + shard
        return result

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

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
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
        """
        Gets string representation of operator.

        ..  container:: example

            >>> str(abjad.Retrograde())
            'R'

        """
        return "R"

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        return markups.Markup("R", direction=direction)

    def _is_identity_operator(self):
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def period(self):
        """
        Gets optional period of retrograde.

        ..  todo:: Deprecated. Use Expression followed by Retrograde instead.

        ..  container:: example

            >>> retrograde = abjad.Retrograde(period=3)
            >>> retrograde.period
            3

        Returns integer or none.
        """
        return self._period


class Rotation:
    """
    Rotation operator.

    ..  container:: example:

        >>> abjad.Rotation()
        Rotation(n=0)

    ..  container:: example

        >>> abjad.Rotation(n=1)
        Rotation(n=1)

    Object model of the twelve-tone rotation operator.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_n", "_period", "_stravinsky")

    ### INITIALIZER ###

    def __init__(self, *, n=0, period=None, stravinsky=None):
        self._n = int(n)
        if period is not None:
            period = abs(int(period))
            assert 0 < period
        self._period = period
        assert isinstance(stravinsky, (bool, type(None))), repr(stravinsky)
        self._stravinsky = stravinsky

    ### SPECIAL METHODS ###

    def __add__(self, operator):
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

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
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

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    f'8
                    g'8
                    af'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns compound operator:

            >>> string = abjad.storage(operator)
            >>> print(string)
            abjad.CompoundOperator(
                operators=[
                    Rotation(n=-1),
                    Transposition(n=3),
                    ],
                )

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
            PitchClassSegment([7, 0, 1, 4])

        ..  container:: example

            Rotates pitch classes with Stravinsky-style back-transposition to
            zero:

            >>> rotation = abjad.Rotation(n=1, stravinsky=True)
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> rotation(pitch_classes)
            PitchClassSegment([0, 5, 6, 9])

        ..  container:: example

            Does not rotate single pitches or pitch-classes:

            >>> rotation = abjad.Rotation(n=1)
            >>> pitch_class = abjad.NumberedPitchClass(6)
            >>> rotation(pitch_class)
            NumberedPitchClass(6)

        ..  container:: example

            Periodic rotation:

            ..  todo:: Deprecated.

            >>> rotation = abjad.Rotation(n=1, period=3)
            >>> pitches = abjad.PitchSegment("c' d' e' f' g' a' b' c''")
            >>> rotation(pitches)
            PitchSegment("e' c' d' a' f' g' c'' b'")

        ..  container:: example

            Stravinsky-style periodic rotation:

            ..  todo:: Deprecated.

            >>> rotation = abjad.Rotation(
            ...     n=1,
            ...     period=3,
            ...     stravinsky=True,
            ...     )
            >>> pitches = abjad.PitchSegment("c' d' e' f' g' a' b' c''")
            >>> rotation(pitches)
            PitchSegment("c' af bf f' df' ef' b' as'")

        Returns new object with type equal to that of ``argument``.
        """
        if isinstance(argument, (Pitch, PitchClass)):
            return argument
        if not isinstance(argument, (PitchSegment, PitchClassSegment)):
            argument = PitchSegment(argument)
        if not self.period:
            return argument.rotate(self.n, stravinsky=self.stravinsky)
        result = new(argument, items=())
        for shard in Sequence(argument).partition_by_counts(
            [self.period], cyclic=True, overhang=True
        ):
            shard = type(argument)(shard)
            shard = shard.rotate(self.n, stravinsky=self.stravinsky)
            result = result + shard
        return result

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

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
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
        """
        Gets string representation of operator.

        ..  container:: example

            >>> str(abjad.Rotation())
            'r0'

        ..  container:: example

            >>> str(abjad.Rotation(n=1))
            'r1'

        ..  container:: example

            >>> str(abjad.Rotation(stravinsky=True))
            'rs0'

        ..  container:: example

            >>> str(abjad.Rotation(n=1, stravinsky=True))
            'rs1'

        """
        if self.stravinsky:
            string = f"rs{self.n}"
        else:
            string = f"r{self.n}"
        return string

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        operator = markups.Markup("r", direction=direction)
        subscript = markups.Markup(self.n).sub()
        hspace = markups.Markup.hspace(-0.25)
        markup = markups.Markup.concat([operator, hspace, subscript])
        return markup

    def _is_identity_operator(self):
        if self.n == 0:
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def n(self):
        """
        Gets index of rotation.

        ..  container:: example

            >>> rotation = abjad.Rotation()
            >>> rotation.n
            0

        ..  container:: example

            >>> rotation = abjad.Rotation(n=2)
            >>> rotation.n
            2

        Returns integer.
        """
        return self._n

    @property
    def period(self):
        """
        Gets period of rotation.

        ..  todo:: Deprecated.

        ..  container:: example

            >>> rotation = abjad.Rotation(n=2, period=3)
            >>> rotation.period
            3

        Returns integer or none.
        """
        return self._period

    @property
    def stravinsky(self):
        """
        Is true when rotation uses Stravinsky-style back-transposition to zero.

        ..  container:: example

            >>> rotation = abjad.Rotation(n=2, stravinsky=False)
            >>> rotation.stravinsky
            False

        Returns true or false.
        """
        return self._stravinsky


class Transposition:
    """
    Transposition operator.

    ..  container:: example

        >>> abjad.Transposition()
        Transposition(n=0)

    ..  container:: example

        >>> abjad.Transposition(n=2)
        Transposition(n=2)

    Object model of twelve-tone transposition operator.
    """

    ### CLASS VARIABLES ##

    __slots__ = ("_n",)

    ### INITIALIZER ###

    def __init__(self, *, n=0):
        self._n = n

    ### SPECIAL METHODS ###

    def __add__(self, operator):
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

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
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

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    e'8
                    fs'8
                    af'8
                    a'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns compound operator.
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
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

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
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
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

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        operator = markups.Markup("T", direction=None)
        subscript = markups.Markup(self.n).sub()
        markup = markups.Markup.concat([operator, subscript])
        return markup

    def _is_identity_operator(self):
        if self.n == 0:
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def n(self):
        """
        Gets index of transposition.

        ..  container:: example

            >>> transposition = abjad.Transposition()
            >>> transposition.n
            0

        ..  container:: example

            >>> transposition = abjad.Transposition(n=2)
            >>> transposition.n
            2

        Set to integer, interval or none.
        """
        return self._n
