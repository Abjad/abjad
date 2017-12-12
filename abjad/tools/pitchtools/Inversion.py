from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Inversion(AbjadValueObject):
    r'''Inversion operator.

    ..  container:: example

        >>> abjad.Inversion()
        Inversion()

    ..  container:: example

        >>> abjad.Inversion(axis=15)
        Inversion(axis=NamedPitch("ef''"))

    Object model of twelve-tone inversion operator.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_axis',
        )

    ### INITIALIZER ###

    def __init__(self, axis=None):
        from abjad.tools import pitchtools
        if axis is not None:
            axis = pitchtools.NamedPitch(axis)
        self._axis = axis

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        r'''Composes inversion and `operator`.

        ..  container:: example

            Example segment:

            >>> items = [0, 2, 4, 5]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            Example operators:

            >>> inversion = abjad.Inversion()
            >>> transposition = abjad.Transposition(n=3)

        ..  container:: example

            Transposition followed by inversion:

            >>> operator = inversion + transposition
            >>> str(operator)
            'IT3'

            >>> segment_ = operator(segment)
            >>> abjad.show(segment_) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment_.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice {
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
            >>> abjad.show(segment_) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment_.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice {
                    ef'8
                    cs'8
                    b'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns compound operator:

            >>> abjad.f(operator)
            abjad.CompoundOperator(
                operators=[
                    abjad.Inversion(),
                    abjad.Transposition(
                        n=3,
                        ),
                    ],
                )

        '''
        from abjad.tools import pitchtools
        return pitchtools.CompoundOperator._compose_operators(self, operator)

    def __call__(self, argument):
        r'''Calls inversion on `argument`.

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

        Returns new object with type equal to that of `argument`.
        '''
        if hasattr(argument, 'invert'):
            result = argument.invert(axis=self.axis)
        else:
            message = 'do not know how to invert: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        return result

    def __radd__(self, operator):
        r'''Right-addition not defined on inversion.

        ..  container:: example

            >>> abjad.Inversion().__radd__(abjad.Inversion())
            Traceback (most recent call last):
            ...
            NotImplementedError: right-addition not defined on Inversion.

        Raises not implemented error.
        '''
        message = 'right-addition not defined on {}.'
        message = message.format(type(self).__name__)
        raise NotImplementedError(message)

    def __str__(self):
        r'''Gets string representation of operator.

        ..  container:: example

            >>> str(abjad.Inversion())
            'I'

        ..  container:: example

            >>> str(abjad.Inversion(axis=15))
            'I(Eb5)'

        '''
        if self.axis is None:
            return 'I'
        string = 'I({})'
        string = string.format(self.axis.get_name(locale='us'))
        return string

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        from abjad.tools import markuptools
        markup = markuptools.Markup('I', direction=direction)
        if self.axis is not None:
            axis = self.axis.get_name(locale='us')
            subscript = markuptools.Markup(axis).sub()
            markup = markuptools.Markup.concat([markup, subscript])
        return markup

    def _is_identity_operator(self):
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def axis(self):
        r'''Gets axis of inversion.

        ..  container:: example

            >>> inversion = abjad.Inversion()
            >>> inversion.axis is None
            True

        ..  container:: example

            >>> inversion = abjad.Inversion(axis=15)
            >>> inversion.axis
            NamedPitch("ef''")

        Returns named pitch or none.
        '''
        return self._axis
