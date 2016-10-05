# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Inversion(AbjadValueObject):
    r'''Inversion operator.

    ..  container:: example

        ::

            >>> pitchtools.Inversion()
            Inversion()

    ..  container:: example

        ::

            >>> pitchtools.Inversion(axis=15)
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
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            Example operators:

            ::

                >>> inversion = pitchtools.Inversion()
                >>> transposition = pitchtools.Transposition(n=3)

        ..  container:: example

            **Example 1:**

            ::

                >>> operator = inversion + transposition
                >>> str(operator)
                'IT3'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    a'8
                    g'8
                    f'8
                    e'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> operator = transposition + inversion
                >>> str(operator)
                'T3I'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
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

                >>> print(format(operator))
                pitchtools.CompoundOperator(
                    operators=(
                        pitchtools.Inversion(),
                        pitchtools.Transposition(
                            n=3,
                            ),
                        ),
                    )

        '''
        from abjad.tools import pitchtools
        return pitchtools.CompoundOperator._compose_operators(self, operator)

    def __call__(self, expr):
        r'''Calls inversion on `expr`.

        ..  container:: example

            Inverts numbered pitch-class:

            ::

                >>> inversion = pitchtools.Inversion()
                >>> pitch_class = pitchtools.NumberedPitchClass(1)
                >>> inversion(pitch_class)
                NumberedPitchClass(11)

        ..  container:: example

            Inverts numbered pitch:

            ::

                >>> inversion = pitchtools.Inversion()
                >>> pitch = pitchtools.NumberedPitch(15)
                >>> inversion(pitch)
                NumberedPitch(-15)

        ..  container:: example

            Inverts named pitch:

            ::

                >>> inversion = pitchtools.Inversion()
                >>> pitch = pitchtools.NamedPitch("d'")
                >>> inversion(pitch)
                NamedPitch('bf')

        ..  container:: example

            Inverts named pitch class:

            ::

                >>> inversion = pitchtools.Inversion()
                >>> pitch_class = pitchtools.NamedPitchClass('d')
                >>> inversion(pitch_class)
                NamedPitchClass('bf')

        ..  container:: example

            Inverts pitch segment:

            ::

                >>> inversion = pitchtools.Inversion()
                >>> segment = pitchtools.PitchSegment("c' d' e'")
                >>> inversion(segment)
                PitchSegment(["c'", 'bf', 'af'])

        ..  container:: example

            Inverts pitch class segment:

            ::

                >>> inversion = pitchtools.Inversion()
                >>> segment = pitchtools.PitchClassSegment("c d e")
                >>> inversion(segment)
                PitchClassSegment(['c', 'bf', 'af'])

        ..  container:: example
        
            Inverts pitch class set:

            ::

                >>> inversion = pitchtools.Inversion()
                >>> set_ = pitchtools.PitchClassSet("c d e")
                >>> inversion(set_)
                PitchClassSet(['c', 'af', 'bf'])

        Returns new object with type equal to that of `expr`.
        '''
        if hasattr(expr, 'invert'):
            result = expr.invert(axis=self.axis)
        else:
            message = 'do not know how to invert: {!r}.'
            message = message.format(expr)
            raise TypeError(message)
        return result

    def __str__(self):
        r'''Gets string representation of operator.

        ..  container:: example

            ::

                >>> str(pitchtools.Inversion())
                'I'

        ..  container:: example

            ::

                >>> str(pitchtools.Inversion(axis=15))
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

                >>> inversion = pitchtools.Inversion()
                >>> inversion.axis is None
                True

        ..  container:: example

            ::

                >>> inversion = pitchtools.Inversion(axis=15)
                >>> inversion.axis
                NamedPitch("ef''")

        Returns named pitch or none.
        '''
        return self._axis
