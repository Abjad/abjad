from abjad import markups
from abjad.system.AbjadValueObject import AbjadValueObject


class Rotation(AbjadValueObject):
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

    __slots__ = (
        '_n',
        '_period',
        '_stravinsky',
        )

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
        Composes rotation and `operator`.

        ..  container:: example

            Example segment:

            >>> items = [0, 2, 4, 5]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            Example operators:

            >>> rotation = abjad.Rotation(n=-1)
            >>> transposition = abjad.Transposition(n=3)

        ..  container:: example

            Transposition followed by rotation:

            >>> operator = rotation + transposition
            >>> str(operator)
            'r-1T3'

            >>> segment_ = operator(segment)
            >>> abjad.show(segment_) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment_.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    f'8
                    g'8
                    af'8
                    ef'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because rotation and transposition commute:

            >>> operator = transposition + rotation
            >>> str(operator)
            'T3r-1'

            >>> segment_ = operator(segment)
            >>> abjad.show(segment_) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment_.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    f'8
                    g'8
                    af'8
                    ef'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns compound operator:

            >>> abjad.f(operator)
            abjad.CompoundOperator(
                operators=[
                    abjad.Rotation(
                        n=-1,
                        ),
                    abjad.Transposition(
                        n=3,
                        ),
                    ],
                )

        """
        import abjad
        return abjad.CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        """
        Calls rotation on `argument`.

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

        Returns new object with type equal to that of `argument`.
        """
        import abjad
        if isinstance(argument, (abjad.Pitch, abjad.PitchClass)):
            return argument
        if not isinstance(argument, (
            abjad.PitchSegment,
            abjad.PitchClassSegment,
            )):
            argument = abjad.PitchSegment(argument)
        if not self.period:
            return argument.rotate(self.n, stravinsky=self.stravinsky)
        result = abjad.new(argument, items=())
        for shard in abjad.sequence(argument).partition_by_counts(
            [self.period],
            cyclic=True,
            overhang=True,
            ):
            shard = type(argument)(shard)
            shard = shard.rotate(self.n, stravinsky=self.stravinsky)
            result = result + shard
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
        message = 'right-addition not defined on {}.'
        message = message.format(type(self).__name__)
        raise NotImplementedError(message)

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
        string = 'r{}'
        if self.stravinsky:
            string = 'rs{}'
        string = string.format(self.n)
        return string

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        operator = markups.Markup('r', direction=direction)
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
