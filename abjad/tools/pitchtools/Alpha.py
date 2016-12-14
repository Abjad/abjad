# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Alpha(AbjadValueObject):
    r'''Alpha operator.

    ..  container:: example:

        ::

            >>> pitchtools.Alpha()
            Alpha()

    Object model of twelve-tone alpha operator.

    Alpha operator switches between the two whole-tone sets:
    ``(1 0 3 2 5 4 7 6 9 8 11 10)``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _permutation = (1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10)

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        r'''Composes alpha and `operator`.

        ..  container:: example

            Example segment:

            ::

                >>> items = [0, 2, 4, 5]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP
    
            Example operators:

            ::

                >>> alpha = pitchtools.Alpha()
                >>> transposition = pitchtools.Transposition(n=3)

        ..  container:: example

            Transposition followed by alpha:

            ::

                >>> operator = alpha + transposition
                >>> str(operator)
                'AT3'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    d'8
                    e'8
                    fs'8
                    a'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Alpha followed by transposition:

            ::

                >>> operator = transposition + alpha
                >>> str(operator)
                'T3A'

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
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns compound operator:

            ::

                >>> print(format(operator))
                pitchtools.CompoundOperator(
                    operators=(
                        pitchtools.Alpha(),
                        pitchtools.Transposition(
                            n=3,
                            ),
                        ),
                    )

        '''
        from abjad.tools import pitchtools
        return pitchtools.CompoundOperator._compose_operators(self, operator)

    def __call__(self, expr):
        r'''Calls alpha on `expr`.

        ..  container:: example

            Calls alpha on pitch-class:

            ::

                >>> alpha = pitchtools.Alpha()
                >>> alpha(pitchtools.NumberedPitchClass(6))
                NumberedPitchClass(7)

        ..  container:: example

            Calls alpha on pitch-class segment:

            ::

                >>> pitch_classes = pitchtools.PitchClassSegment([0, 1, 4, 7])
                >>> alpha(pitch_classes)
                PitchClassSegment([1, 0, 5, 6])

        Returns new object of `expr` type.
        '''
        from abjad.tools import pitchtools
        row = pitchtools.TwelveToneRow(items=self._permutation)
        if isinstance(expr, pitchtools.PitchClass):
            expr = pitchtools.NumberedPitchClass(expr)
            return row([expr])[0]
        elif isinstance(expr, pitchtools.Pitch):
            expr = pitchtools.NumberedPitch(expr)
            return row([expr])[0]
        else:
            return row(expr)

    def __str__(self):
        r'''Gets string representation of operator.

        ..  container:: example

            ::

                >>> str(pitchtools.Alpha())
                'A'

        '''
        return 'A'

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        from abjad.tools import markuptools
        return markuptools.Markup('A', direction=direction)

    def _is_identity_operator(self):
        return False
