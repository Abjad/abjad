import collections
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Transposition(AbjadValueObject):
    r'''Transposition operator.

    ..  container:: example

        ::

            >>> abjad.Transposition()
            Transposition(n=0)

    ..  container:: example

        ::

            >>> abjad.Transposition(n=2)
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
                >>> segment = abjad.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            Example operators:

            ::

                >>> T_1 = abjad.Transposition(n=1)
                >>> T_3 = abjad.Transposition(n=3)

        ..  container:: example

            Successive transposition:

            ::

                >>> operator = T_1 + T_3
                >>> str(operator)
                'T1T3'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
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

            ..  docs::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
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

    def __call__(self, argument):
        r'''Calls transposition on `argument`.

        ..  container:: example

            Transposes pitch-class:

            ::

                >>> transposition = abjad.Transposition(n=2)
                >>> pitch_class = abjad.NumberedPitchClass(1)
                >>> transposition(pitch_class)
                NumberedPitchClass(3)

        ..  container:: example

            Transposes pitch:

            ::

                >>> transposition = abjad.Transposition(n=2)
                >>> pitch = abjad.NumberedPitch(15)
                >>> transposition(pitch)
                NumberedPitch(17)

        ..  container:: example

            Transposes list of pitches:

            ::

                >>> transposition = abjad.Transposition(n=2)
                >>> pitches = [abjad.NumberedPitch(_) for _ in [15, 16]]
                >>> transposition(pitches)
                [NumberedPitch(17), NumberedPitch(18)]

        Returns new object with type equal to that of `argument`.
        '''
        if hasattr(argument, 'transpose'):
            result = argument.transpose(self.n)
        elif isinstance(argument, collections.Iterable):
            items = []
            for item in argument:
                item = item.transpose(self.n)
                items.append(item)
            result = type(argument)(items)
        else:
            message = 'do not know how to transpose: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        return result

    def __radd__(self, operator):
        r'''Right-addition not defined on transposition.

        ..  container:: example

            ::

                >>> abjad.Transposition().__radd__(abjad.Transposition())
                Traceback (most recent call last):
                ...
                NotImplementedError: right-addition not defined on Transposition.

        Raises not implemented error.
        '''
        message = 'right-addition not defined on {}.'
        message = message.format(type(self).__name__)
        raise NotImplementedError(message)

    def __str__(self):
        r'''Gets string representation of operator.

        ..  container:: example

            ::

                >>> str(abjad.Transposition())
                'T0'

        ..  container:: example

            ::

                >>> str(abjad.Transposition(n=2))
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

                >>> transposition = abjad.Transposition()
                >>> transposition.n
                0

        ..  container:: example

            ::

                >>> transposition = abjad.Transposition(n=2)
                >>> transposition.n
                2

        Set to integer, interval or none.
        '''
        return self._n
