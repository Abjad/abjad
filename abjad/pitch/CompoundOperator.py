import collections
from abjad import markups
from abjad.system.AbjadValueObject import AbjadValueObject
from .Duplication import Duplication
from .Inversion import Inversion
from .Multiplication import Multiplication
from .Retrograde import Retrograde
from .Rotation import Rotation
from .Transposition import Transposition


class CompoundOperator(AbjadValueObject):
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

    __slots__ = (
        '_operators',
        '_show_identity_operators',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, operators=None, *, show_identity_operators=None):
        if operators is not None:
            if not isinstance(operators, collections.Sequence):
                operators = (operators,)
            assert len(operators)
            operators = tuple(operators)
        self._operators = operators
        assert isinstance(show_identity_operators, (bool, type(None)))
        self._show_identity_operators = show_identity_operators

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        """
        Composes compound operator and `operator`.

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

            >>> abjad.f(operator_3)
            abjad.CompoundOperator(
                operators=[
                    abjad.Transposition(
                        n=1,
                        ),
                    abjad.Inversion(),
                    abjad.Retrograde(),
                    abjad.Inversion(),
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
        Calls compound operator on `argument`.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.rotate(n=1, stravinsky=True)
            >>> operator = operator.transpose(n=2)
            >>> str(operator)
            'T2rs1'

            >>> segment = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> abjad.show(segment) # doctest: +SKIP

            >>> transform = operator(segment)
            >>> abjad.show(transform) # doctest: +SKIP

            >>> transform
            PitchClassSegment([2, 7, 8, 11])

        Returns new object with type equal to that of `argument`.
        """
        if self.operators is None:
            return argument
        for transform in self.operators:
            argument = transform(argument)
        return argument

    def __radd__(self, operator):
        """
        Composes `operator` and compound operator.

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
        result = ''.join(result)
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
            if (self.show_identity_operators or
                not operator._is_identity_operator()):
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
            operators,
            show_identity_operators=self.show_identity_operators,
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
        Configures compound operator to duplicate pitches by `counts`, with
        optional `indices` and `period`.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.duplicate(counts=1)
            >>> abjad.f(operator)
            abjad.CompoundOperator(
                operators=[
                    abjad.Duplication(
                        counts=1,
                        ),
                    ],
                )

        Returns new compound operator.
        """
        operator = Duplication(
            counts=counts,
            indices=indices,
            period=period,
            )
        return self._with_operator(operator)

    def invert(self, axis=None):
        """
        Configures compound operator to invert pitches about `axis`.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.invert(axis=2)
            >>> abjad.f(operator)
            abjad.CompoundOperator(
                operators=[
                    abjad.Inversion(
                        axis=abjad.NamedPitch("d'"),
                        ),
                    ],
                )

        Returns new compound operator.
        """
        operator = Inversion(axis=axis)
        return self._with_operator(operator)

    def multiply(self, n=1):
        """
        Configures compound operator to multiply pitch-classes by index `n`.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.multiply(n=3)
            >>> abjad.f(operator)
            abjad.CompoundOperator(
                operators=[
                    abjad.Multiplication(
                        n=3,
                        ),
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
            >>> abjad.f(operator)
            abjad.CompoundOperator(
                operators=[
                    abjad.Retrograde(),
                    ],
                )

        Returns new compound operator.
        """
        operator = Retrograde(period=period)
        return self._with_operator(operator)

    def rotate(self, n=0, period=None, stravinsky=None):
        """
        Configures compound operator to rotate pitches by index `n`.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.rotate(n=-1)
            >>> abjad.f(operator)
            abjad.CompoundOperator(
                operators=[
                    abjad.Rotation(
                        n=-1,
                        ),
                    ],
                )

        Returns new compound operator.
        """
        operator = Rotation(
            n=n,
            period=period,
            stravinsky=stravinsky,
            )
        return self._with_operator(operator)

    def transpose(self, n=0):
        """
        Configures compound operator to transpose pitches by index `n`.

        ..  container:: example

            >>> operator = abjad.CompoundOperator()
            >>> operator = operator.transpose(n=1)

            >>> abjad.f(operator)
            abjad.CompoundOperator(
                operators=[
                    abjad.Transposition(
                        n=1,
                        ),
                    ],
                )

        Returns new compound operator.
        """
        operator = Transposition(n=n)
        return self._with_operator(operator)
