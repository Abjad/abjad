# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Retrograde(AbjadValueObject):
    r'''Retrograde operator.

    ::

        >>> import abjad
        >>> import pytest

    ..  container:: example:

        ::

            >>> abjad.Retrograde()
            Retrograde()

    Object model of twelve-tone retrograde operator.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_period',
        )

    ### INITIALIZER ###

    def __init__(self, period=None):
        if period is not None:
            period = abs(int(period))
            assert 0 < period
        self._period = period

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        r'''Composes retrograde and `operator`.

        ..  container:: example

            Example segment:

            ::

                >>> items = [0, 2, 4, 5]
                >>> segment = abjad.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP
    
            Example operators:

            ::

                >>> retrograde = abjad.Retrograde()
                >>> transposition = abjad.Transposition(n=3)

        ..  container:: example

            Transposition followed by retrograde:

            ::

                >>> operator = retrograde + transposition
                >>> str(operator)
                'RT3'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
                \new Voice {
                    af'8
                    g'8
                    f'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because retrograde and transposition commute:

            ::

                >>> operator = transposition + retrograde
                >>> str(operator)
                'T3R'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
                \new Voice {
                    af'8
                    g'8
                    f'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns compound operator:

            ::

                >>> f(operator)
                abjad.CompoundOperator(
                    operators=[
                        abjad.Retrograde(),
                        abjad.Transposition(
                            n=3,
                            ),
                        ],
                    )

        '''
        from abjad.tools import pitchtools
        return pitchtools.CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        r'''Calls retrograde on `argument`.

        ..  container:: example

            Gets retrograde pitch classes:

            ::

                >>> retrograde = abjad.Retrograde()
                >>> segment = abjad.PitchClassSegment([0, 1, 4, 7])
                >>> retrograde(segment)
                PitchClassSegment([7, 4, 1, 0])

        ..  container:: example

            Does not retrograde single pitches or pitch-classes:

            ::

                >>> retrogresion = abjad.Retrograde()
                >>> pitch_class = abjad.NumberedPitchClass(6)
                >>> retrograde(pitch_class)
                NumberedPitchClass(6)

        ..  container:: example

            Periodic retrograde:

            ..  todo:: Deprecated.

            ::

                >>> retrograde = abjad.Retrograde(period=3)
                >>> segment = abjad.PitchSegment("c' d' e' f' g' a' b' c''")
                >>> retrograde(segment)
                PitchSegment("e' d' c' a' g' f' c'' b'")

        Returns new object with type equal to that of `argument`.
        '''
        import abjad
        if isinstance(argument, (abjad.Pitch, abjad.PitchClass)):
            return argument
        if not isinstance(argument, (
            abjad.PitchSegment, abjad.PitchClassSegment,
            )):
            argument = abjad.PitchSegment(argument)
        if not self.period:
            return type(argument)(reversed(argument))
        result = abjad.new(argument, items=())
        for shard in abjad.Sequence(argument).partition_by_counts(
            [self.period],
            cyclic=True,
            overhang=True,
            ):
            shard = type(argument)(shard)
            shard = type(argument)(reversed(shard))
            result = result + shard
        return result

    def __radd__(self, operator):
        r'''Right-addition not defined on retrograde.
        
        ..  container:: example

            ::

                >>> string = 'abjad.Retrograde().__radd__(abjad.Retrograde())'
                >>> pytest.raises(NotImplementedError, string)
                <ExceptionInfo NotImplementedError ...>

        Raises not implemented error.
        '''
        message = 'right-addition not defined on {}.'
        message = message.format(type(self).__name__)
        raise NotImplementedError(message)

    def __str__(self):
        r'''Gets string representation of operator.

        ..  container:: example

            ::

                >>> str(abjad.Retrograde())
                'R'

        '''
        return 'R'

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        from abjad.tools import markuptools
        return markuptools.Markup('R', direction=direction)

    def _is_identity_operator(self):
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def period(self):
        r'''Gets optional period of retrograde.

        ..  todo:: Deprecated. Use Expression followed by Retrograde instead.

        ..  container:: example

            ::

                >>> retrograde = abjad.Retrograde(period=3)
                >>> retrograde.period
                3

        Returns integer or none.
        '''
        return self._period
