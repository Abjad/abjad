# -*- coding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.topleveltools import new
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Rotation(AbjadValueObject):
    r'''Rotation operator.

    ..  container:: example:

        ::

            >>> Rotation()
            Rotation(n=0)

    ..  container:: example

        ::

            >>> Rotation(n=1)
            Rotation(n=1)

    Object model of the twelve-tone rotation operator.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_n',
        '_period',
        '_stravinsky',
        )

    ### INITIALIZER ###

    def __init__(self, n=0, period=None, stravinsky=None):
        self._n = int(n)
        if period is not None:
            period = abs(int(period))
            assert 0 < period
        self._period = period
        assert isinstance(stravinsky, (bool, type(None))), repr(stravinsky)
        self._stravinsky = stravinsky

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        r'''Composes rotation and `operator`.

        ..  container:: example

            Example segment:

            ::

                >>> items = [0, 2, 4, 5]
                >>> segment = PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP
    
            Example operators:

            ::

                >>> rotation = Rotation(n=-1)
                >>> transposition = Transposition(n=3)

        ..  container:: example

            Transposition followed by rotation:

            ::

                >>> operator = rotation + transposition
                >>> str(operator)
                'r-1T3'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    f'8
                    g'8
                    af'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because rotation and transposition commute:

            ::

                >>> operator = transposition + rotation
                >>> str(operator)
                'T3r-1'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    f'8
                    g'8
                    af'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }
                
        ..  container:: example

            Returns compound operator:

            ::

                >>> f(operator)
                pitchtools.CompoundOperator(
                    operators=[
                        pitchtools.Rotation(
                            n=-1,
                            ),
                        pitchtools.Transposition(
                            n=3,
                            ),
                        ],
                    )

        '''
        from abjad.tools import pitchtools
        return pitchtools.CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        r'''Calls rotation on `argument`.

        ..  container:: example

            Rotates pitch classes:

            ::

                >>> rotation = Rotation(n=1)
                >>> pitch_classes = PitchClassSegment([0, 1, 4, 7])
                >>> rotation(pitch_classes)
                PitchClassSegment([7, 0, 1, 4])

        ..  container:: example

            Rotates pitch classes with Stravinsky-style back-transposition to
            zero:

            ::

                >>> rotation = Rotation(n=1, stravinsky=True)
                >>> pitch_classes = PitchClassSegment([0, 1, 4, 7])
                >>> rotation(pitch_classes)
                PitchClassSegment([0, 5, 6, 9])

        ..  container:: example

            Does not rotate single pitches or pitch-classes:

            ::

                >>> rotation = Rotation(n=1)
                >>> pitch_class = NumberedPitchClass(6)
                >>> rotation(pitch_class)
                NumberedPitchClass(6)

        ..  container:: example

            Periodic rotation:

            ..  todo:: Deprecated.

            ::

                >>> rotation = Rotation(n=1, period=3)
                >>> pitches = PitchSegment("c' d' e' f' g' a' b' c''")
                >>> rotation(pitches)
                PitchSegment("e' c' d' a' f' g' c'' b'")

        ..  container:: example

            Stravinsky-style periodic rotation:

            ..  todo:: Deprecated.

            ::

                >>> rotation = Rotation(
                ...     n=1,
                ...     period=3,
                ...     stravinsky=True,
                ...     )
                >>> pitches = PitchSegment("c' d' e' f' g' a' b' c''")
                >>> rotation(pitches)
                PitchSegment("c' af bf f' df' ef' b' as'")

        Returns new object with type equal to that of `argument`.
        '''
        from abjad.tools import pitchtools
        if isinstance(argument, (pitchtools.Pitch, pitchtools.PitchClass)):
            return argument
        if not isinstance(argument, (
            pitchtools.PitchSegment,
            pitchtools.PitchClassSegment,
            )):
            argument = pitchtools.PitchSegment(argument)
        if not self.period:
            return argument.rotate(self.n, stravinsky=self.stravinsky)
        result = new(argument, items=())
        for shard in sequencetools.Sequence(argument).partition_by_counts(
            [self.period],
            cyclic=True,
            overhang=True,
            ):
            shard = type(argument)(shard)
            shard = shard.rotate(self.n, stravinsky=self.stravinsky)
            result = result + shard
        return result

    def __str__(self):
        r'''Gets string representation of operator.

        ..  container:: example

            ::

                >>> str(Rotation())
                'r0'

        ..  container:: example

            ::

                >>> str(Rotation(n=1))
                'r1'

        ..  container:: example

            ::

                >>> str(Rotation(stravinsky=True))
                'rs0'

        ..  container:: example

            ::

                >>> str(Rotation(n=1, stravinsky=True))
                'rs1'

        '''
        string = 'r{}'
        if self.stravinsky:
            string = 'rs{}'
        string = string.format(self.n)
        return string

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        from abjad.tools import markuptools
        operator = markuptools.Markup('r', direction=direction)
        subscript = markuptools.Markup(self.n).sub()
        hspace = markuptools.Markup.hspace(-0.25)
        markup = markuptools.Markup.concat([operator, hspace, subscript])
        return markup

    def _is_identity_operator(self):
        if self.n == 0:
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def n(self):
        r'''Gets index of rotation.

        ..  container:: example

            ::

                >>> rotation = Rotation()
                >>> rotation.n
                0

        ..  container:: example

            ::

                >>> rotation = Rotation(n=2)
                >>> rotation.n
                2

        Returns integer.
        '''
        return self._n

    @property
    def period(self):
        r'''Gets period of rotation.

        ..  todo:: Deprecated.

        ..  container:: example

            ::

                >>> rotation = Rotation(n=2, period=3)
                >>> rotation.period
                3

        Returns integer or none.
        '''
        return self._period

    @property
    def stravinsky(self):
        r'''Is true when rotation uses Stravinsky-style back-transposition to
        zero. Otherwise false.

        ..  container:: example

            ::

                >>> rotation = Rotation(n=2, stravinsky=False)
                >>> rotation.stravinsky
                False

        Returns true or false.
        '''
        return self._stravinsky
