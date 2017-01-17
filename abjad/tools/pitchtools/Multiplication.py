# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Multiplication(AbjadValueObject):
    r'''Multiplication operator.

    ..  container:: example

        ::

            >>> Multiplication()
            Multiplication(n=1)

    ..  container:: example

        ::

            >>> Multiplication(n=5)
            Multiplication(n=5)

    Object model of twelve-tone multiplication operator.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_n',
        )

    ### INITIALIZER ###

    def __init__(self, n=1):
        self._n = n

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        r'''Composes multiplication and `operator`.

        ..  container:: example

            Example segment:

            ::

                >>> items = [0, 2, 4, 5]
                >>> segment = PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP
    
            Example operators:

            ::

                >>> multiplication = Multiplication(n=5)
                >>> transposition = Transposition(n=3)

        ..  container:: example


            Transposition followed by multiplication:

            ::

                >>> operator = multiplication + transposition
                >>> str(operator)
                'M5T3'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    ef'8
                    cs'8
                    b'8
                    e'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because multiplication and transposition commute:

            ::

                >>> operator = transposition + multiplication
                >>> str(operator)
                'T3M5'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    ef'8
                    cs'8
                    b'8
                    e'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns compound operator.
        '''
        from abjad.tools import pitchtools
        return pitchtools.CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        r'''Calls multiplication on `argument`.

        ..  container:: example

            Multiplies pitch-class:

            ::

                >>> multiplication = Multiplication(n=5)
                >>> pitch_class = NumberedPitchClass(4)
                >>> multiplication(pitch_class)
                NumberedPitchClass(8)

        ..  container:: example

            Multiplies pitch:

            ::

                >>> multiplication = Multiplication(n=7)
                >>> pitch = NamedPitch("f'")
                >>> multiplication(pitch)
                NamedPitch("b'")

        Returns new object with type equal to that of `argument`.
        '''
        if hasattr(argument, 'multiply'):
            result = argument.multiply(self.n)
        else:
            message = 'do not know how to multiply: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        return result

    def __str__(self):
        r'''Gets string representation of operator.

        ..  container:: example

            ::

                >>> str(Multiplication())
                'M1'

        ..  container:: example

            ::

                >>> str(Multiplication(n=5))
                'M5'

        '''
        string = 'M{}'
        string = string.format(self.n)
        return string

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        from abjad.tools import markuptools
        operator = markuptools.Markup('M', direction=direction)
        subscript = markuptools.Markup(self.n).sub()
        markup = markuptools.Markup.concat([operator, subscript])
        return markup

    def _is_identity_operator(self):
        if self.n == 1:
            return True
        return False 

    ### PUBLIC PROPERTIES ###

    @property
    def n(self):
        r'''Gets index of multiplication.

        ..  container:: example

            ::

                >>> multiplication = Multiplication()
                >>> multiplication.n
                1

        ..  container:: example

            ::

                >>> multiplication = Multiplication(n=5)
                >>> multiplication.n
                5

        Set to integer or none.
        '''
        return self._n
