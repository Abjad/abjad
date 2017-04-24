# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Inversion(AbjadValueObject):
    r'''Inversion operator.

    ..  container:: example

        ::

            >>> Inversion()
            Inversion()

    ..  container:: example

        ::

            >>> Inversion(axis=15)
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

            ::

                >>> items = [0, 2, 4, 5]
                >>> segment = PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            Example operators:

            ::

                >>> inversion = Inversion()
                >>> transposition = Transposition(n=3)

        ..  container:: example

            Transposition followed by inversion:

            ::

                >>> operator = inversion + transposition
                >>> str(operator)
                'IT3'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file[Voice])
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

            ::

                >>> operator = transposition + inversion
                >>> str(operator)
                'T3I'

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
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns compound operator:

            ::

                >>> f(operator)
                pitchtools.CompoundOperator(
                    operators=[
                        pitchtools.Inversion(),
                        pitchtools.Transposition(
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

            ::

                >>> inversion = Inversion()
                >>> pitch_class = NumberedPitchClass(1)
                >>> inversion(pitch_class)
                NumberedPitchClass(11)

        ..  container:: example

            Inverts numbered pitch:

            ::

                >>> inversion = Inversion()
                >>> pitch = NumberedPitch(15)
                >>> inversion(pitch)
                NumberedPitch(-15)

        ..  container:: example

            Inverts named pitch:

            ::

                >>> inversion = Inversion()
                >>> pitch = NamedPitch("d'")
                >>> inversion(pitch)
                NamedPitch('bf')

        ..  container:: example

            Inverts named pitch class:

            ::

                >>> inversion = Inversion()
                >>> pitch_class = NamedPitchClass('d')
                >>> inversion(pitch_class)
                NamedPitchClass('bf')

        ..  container:: example

            Inverts pitch segment:

            ::

                >>> inversion = Inversion()
                >>> segment = PitchSegment("c' d' e'")
                >>> inversion(segment)
                PitchSegment("c' bf af")

        ..  container:: example

            Inverts pitch class segment:

            ::

                >>> inversion = Inversion()
                >>> segment = PitchClassSegment("c d e")
                >>> inversion(segment)
                PitchClassSegment("c bf af")

        ..  container:: example
        
            Inverts pitch class set:

            ::

                >>> inversion = Inversion()
                >>> set_ = PitchClassSet("c d e")
                >>> inversion(set_)
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

    def __str__(self):
        r'''Gets string representation of operator.

        ..  container:: example

            ::

                >>> str(Inversion())
                'I'

        ..  container:: example

            ::

                >>> str(Inversion(axis=15))
                'I(Eb5)'

        '''
        if self.axis is None:
            return 'I'
        string = 'I({})'
        string = string.format(self.axis.pitch_class_octave_label)
        return string

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        from abjad.tools import markuptools
        markup = markuptools.Markup('I', direction=direction)
        if self.axis is not None:
            axis = self.axis.pitch_class_octave_label
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

            ::

                >>> inversion = Inversion()
                >>> inversion.axis is None
                True

        ..  container:: example

            ::

                >>> inversion = Inversion(axis=15)
                >>> inversion.axis
                NamedPitch("ef''")

        Returns named pitch or none.
        '''
        return self._axis
