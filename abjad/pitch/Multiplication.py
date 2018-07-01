from abjad import markups
from abjad.system.AbjadValueObject import AbjadValueObject


class Multiplication(AbjadValueObject):
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

    __slots__ = (
        '_n',
        )

    ### INITIALIZER ###

    def __init__(self, *, n=1):
        self._n = n

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        r"""
        Composes multiplication and `operator`.

        ..  container:: example

            Example segment:

            >>> items = [0, 2, 4, 5]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            Example operators:

            >>> multiplication = abjad.Multiplication(n=5)
            >>> transposition = abjad.Transposition(n=3)

        ..  container:: example


            Transposition followed by multiplication:

            >>> operator = multiplication + transposition
            >>> str(operator)
            'M5T3'

            >>> segment_ = operator(segment)
            >>> abjad.show(segment_) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment_.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    ef'8
                    cs'8
                    b'8
                    e'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because multiplication and transposition commute:

            >>> operator = transposition + multiplication
            >>> str(operator)
            'T3M5'

            >>> segment_ = operator(segment)
            >>> abjad.show(segment_) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment_.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    ef'8
                    cs'8
                    b'8
                    e'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        Returns compound operator.
        """
        import abjad
        return abjad.CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        """
        Calls multiplication on `argument`.

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

        Returns new object with type equal to that of `argument`.
        """
        if hasattr(argument, 'multiply'):
            result = argument.multiply(self.n)
        else:
            message = 'do not know how to multiply: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
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
        message = 'right-addition not defined on {}.'
        message = message.format(type(self).__name__)
        raise NotImplementedError(message)

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
        string = 'M{}'
        string = string.format(self.n)
        return string

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        operator = markups.Markup('M', direction=direction)
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
