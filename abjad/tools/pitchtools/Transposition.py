# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Transposition(AbjadValueObject):
    r'''Transposition operator.

    ..  container:: example

        ::

            >>> pitchtools.Transposition()
            Transposition(n=0)

    ..  container:: example

        ::

            >>> pitchtools.Transposition(n=2)
            Transposition(n=2)

    Object model of twelve-tone transposition operator.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_n',
        )

    ### INITIALIZER ###

    def __init__(self, n=0):
        self._n = n

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        r'''Composes transposition and `operator`.

        ..  container:: example

            Example segment:

            ::

                >>> items = [0, 2, 4, 5]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP
    
            Example operators:

            ::

                >>> T_1 = pitchtools.Transposition(n=1)
                >>> T_3 = pitchtools.Transposition(n=3)

        ..  container:: example

            Successive transposition:

            ::

                >>> operator = T_1 + T_3
                >>> str(operator)
                'T1T3'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    e'8
                    fs'8
                    af'8
                    a'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because transposition commutes:

            ::

                >>> operator = T_3 + T_1
                >>> str(operator)
                'T3T1'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    e'8
                    fs'8
                    af'8
                    a'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns compound operator.
        '''
        from abjad.tools import pitchtools
        return pitchtools.CompoundOperator._compose_operators(self, operator)

    def __call__(self, expr):
        r'''Calls transposition on `expr`.

        ..  container:: example

            Transposes pitch-class:

            ::

                >>> transposition = pitchtools.Transposition(n=2)
                >>> pitch_class = pitchtools.NumberedPitchClass(1)
                >>> transposition(pitch_class)
                NumberedPitchClass(3)

        ..  container:: example

            Transposes pitch:

            ::

                >>> transposition = pitchtools.Transposition(n=2)
                >>> pitch = pitchtools.NumberedPitch(15)
                >>> transposition(pitch)
                NumberedPitch(17)

        Returns new object with type equal to that of `expr`.
        '''
        if hasattr(expr, 'transpose'):
            result = expr.transpose(self.n)
        else:
            message = 'do not know how to transpose: {!r}.'
            message = message.format(expr)
            raise TypeError(message)
        return result

    def __str__(self):
        r'''Gets string representation of operator.

        ..  container:: example

            ::

                >>> str(pitchtools.Transposition())
                'T0'

        ..  container:: example

            ::

                >>> str(pitchtools.Transposition(n=2))
                'T2'

        '''
        string = 'T{}'
        string = string.format(self.n)
        return string

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        from abjad.tools import markuptools
        operator = markuptools.Markup('T', direction=None)
        subscript = markuptools.Markup(self.n).sub()
        markup = markuptools.Markup.concat([operator, subscript])
        return markup

    def _is_identity_operator(self):
        if self.n == 0:
            return True
        return False
        
    ### PUBLIC PROPERTIES ###

    @property
    def n(self):
        r'''Gets index of transposition.

        ..  container:: example

            ::

                >>> transposition = pitchtools.Transposition()
                >>> transposition.n
                0

        ..  container:: example

            ::

                >>> transposition = pitchtools.Transposition(n=2)
                >>> transposition.n
                2

        Set to integer, interval or none.
        '''
        return self._n
