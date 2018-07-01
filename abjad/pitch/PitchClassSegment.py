import inspect
from abjad import enums
from abjad.system.Signature import Signature
from abjad.top.new import new
from .Segment import Segment


class PitchClassSegment(Segment):
    r"""
    Pitch-class segment.

    ..  container:: example

        Initializes segment with numbered pitch-classes:

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example expression

            >>> expression = abjad.Expression()
            >>> expression = expression.pitch_class_segment()

            >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

    ..  container:: example

        Initializes segment with named pitch-classes:

        ..  container:: example

            >>> items = ['c', 'ef', 'bqs,', 'd']
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    c'8
                    ef'8
                    bqs'8
                    d'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example expression

            >>> expression = abjad.Expression()
            >>> expression = expression.pitch_class_segment(
            ...     item_class=abjad.NamedPitchClass,
            ...     )

            >>> segment = expression(['c', 'ef', 'bqs,', 'd'])
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    c'8
                    ef'8
                    bqs'8
                    d'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        if not items and not item_class:
            item_class = self._named_item_class
        Segment.__init__(
            self,
            items=items,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    @Signature(
        markup_maker_callback='_make___add___markup',
        string_template_callback='_make___add___string_template',
        )
    def __add__(self, argument):
        r"""
        Adds `argument` to segment.

        ..  container:: example

            Example segments:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=pitch_numbers)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> J = abjad.PitchClassSegment(items=pitch_numbers)
            >>> abjad.show(J) # doctest: +SKIP

            >>> pitch_names = ['c', 'ef', 'bqs,', 'd']
            >>> abjad.PitchClassSegment(items=pitch_names)
            PitchClassSegment("c ef bqs d")

            >>> K = abjad.PitchClassSegment(items=pitch_names)
            >>> abjad.show(K) # doctest: +SKIP

        ..  container:: example

            Adds J and K:

            ..  container:: example

                >>> J + K
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 0, 3, 11.5, 2])

                >>> segment = J + K
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        c'8
                        ef'8
                        bqs'8
                        d'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression_J = abjad.Expression(name='J')
                >>> expression_J = expression_J.pitch_class_segment()
                >>> expression_K = abjad.Expression(name='K')
                >>> expression_K = expression_K.pitch_class_segment()
                >>> expression = expression_J + expression_K

                >>> expression(pitch_numbers, pitch_names)
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 0, 3, 11.5, 2])

                >>> expression.get_string()
                'J + K'

                >>> segment = expression(pitch_numbers, pitch_names)
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \line
                                {
                                    \bold
                                        J
                                    +
                                    \bold
                                        K
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        c'8
                        ef'8
                        bqs'8
                        d'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Adds K and J:

            ..  container:: example

                >>> K + J
                PitchClassSegment("c ef bqs d bf bqf fs g bqf g")

                >>> segment = K + J
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        c'8
                        ef'8
                        bqs'8
                        d'8
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression_J = abjad.Expression(name='J')
                >>> expression_J = expression_J.pitch_class_segment()
                >>> expression_K = abjad.Expression(name='K')
                >>> expression_K = expression_K.pitch_class_segment()
                >>> expression = expression_K + expression_J

                >>> expression(pitch_names, pitch_numbers)
                PitchClassSegment("c ef bqs d bf bqf fs g bqf g")

                >>> expression.get_string()
                'K + J'

                >>> segment = expression(pitch_names, pitch_numbers)
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        c'8
                        ^ \markup {
                            \line
                                {
                                    \bold
                                        K
                                    +
                                    \bold
                                        J
                                }
                            }
                        ef'8
                        bqs'8
                        d'8
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Adds J repeatedly:

            ..  container:: example

                >>> J + J + J
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7])


                >>> segment = J + J + J
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression_J = abjad.Expression(name='J')
                >>> expression_J = expression_J.pitch_class_segment()
                >>> expression = expression_J + expression_J + expression_J

                >>> expression(pitch_numbers, pitch_numbers, pitch_numbers)
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7])

                >>> expression.get_string()
                'J + J + J'

                >>> list_ = [pitch_numbers, pitch_numbers, pitch_numbers]
                >>> segment = expression(*list_)
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \line
                                {
                                    \line
                                        {
                                            \bold
                                                J
                                            +
                                            \bold
                                                J
                                        }
                                    +
                                    \bold
                                        J
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Adds transformed segments:

            ..  container:: example

                >>> J.rotate(n=1) + K.rotate(n=2)
                PitchClassSegment([7, 10, 10.5, 6, 7, 10.5, 11.5, 2, 0, 3])

                >>> segment = J.rotate(n=1) + K.rotate(n=2)
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        g'8
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        bqs'8
                        d'8
                        c'8
                        ef'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression_J = abjad.Expression(name='J')
                >>> expression_J = expression_J.pitch_class_segment()
                >>> expression_J = expression_J.rotate(n=1)
                >>> expression_K = abjad.Expression(name='K')
                >>> expression_K = expression_K.pitch_class_segment()
                >>> expression_K = expression_K.rotate(n=2)
                >>> expression = expression_J + expression_K

                >>> expression(pitch_numbers, pitch_names)
                PitchClassSegment([7, 10, 10.5, 6, 7, 10.5, 11.5, 2, 0, 3])

                >>> expression.get_string()
                'r1(J) + r2(K)'

                >>> segment = expression(pitch_numbers, pitch_names)
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        g'8
                        ^ \markup {
                            \line
                                {
                                    \concat
                                        {
                                            r
                                            \sub
                                                1
                                            \bold
                                                J
                                        }
                                    +
                                    \concat
                                        {
                                            r
                                            \sub
                                                2
                                            \bold
                                                K
                                        }
                                }
                            }
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        bqs'8
                        d'8
                        c'8
                        ef'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Reverses result:

            ..  container:: example

                >>> segment = J.rotate(n=1) + K.rotate(n=2)
                >>> segment.retrograde()
                PitchClassSegment([3, 0, 2, 11.5, 10.5, 7, 6, 10.5, 10, 7])

                >>> segment = segment.retrograde()
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        ef'8
                        c'8
                        d'8
                        bqs'8
                        bqf'8
                        g'8
                        fs'8
                        bqf'8
                        bf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression_J = abjad.Expression(name='J')
                >>> expression_J = expression_J.pitch_class_segment()
                >>> expression_J = expression_J.rotate(n=1)
                >>> expression_K = abjad.Expression(name='K')
                >>> expression_K = expression_K.pitch_class_segment()
                >>> expression_K = expression_K.rotate(n=2)
                >>> expression = expression_J + expression_K
                >>> expression = expression.retrograde()

                >>> expression(pitch_numbers, pitch_names)
                PitchClassSegment([3, 0, 2, 11.5, 10.5, 7, 6, 10.5, 10, 7])

                >>> expression.get_string()
                'R(r1(J) + r2(K))'

                >>> segment = expression(pitch_numbers, pitch_names)
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        ef'8
                        ^ \markup {
                            \concat
                                {
                                    R
                                    \concat
                                        {
                                            (
                                            \line
                                                {
                                                    \concat
                                                        {
                                                            r
                                                            \sub
                                                                1
                                                            \bold
                                                                J
                                                        }
                                                    +
                                                    \concat
                                                        {
                                                            r
                                                            \sub
                                                                2
                                                            \bold
                                                                K
                                                        }
                                                }
                                            )
                                        }
                                }
                            }
                        c'8
                        d'8
                        bqs'8
                        bqf'8
                        g'8
                        fs'8
                        bqf'8
                        bf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example expression

            Establishes equivalence:

            >>> expression_J = abjad.Expression(name='J')
            >>> expression_J = expression_J.pitch_class_segment()
            >>> expression_J = expression_J.rotate(n=1)
            >>> expression_K = abjad.Expression(name='K')
            >>> expression_K = expression_K.pitch_class_segment()
            >>> expression_K = expression_K.rotate(n=2)
            >>> expression = expression_J + expression_K
            >>> expression = expression.establish_equivalence(name='Q')

            >>> expression(pitch_numbers, pitch_names)
            PitchClassSegment([7, 10, 10.5, 6, 7, 10.5, 11.5, 2, 0, 3])

            >>> expression.get_string()
            'Q = r1(J) + r2(K)'

            >>> segment = expression(pitch_numbers, pitch_names)
            >>> markup = expression.get_markup()
            >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__(
                ...     figure_name=markup,
                ...     )
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    g'8
                    ^ \markup {
                        \line
                            {
                                \bold
                                    Q
                                =
                                \line
                                    {
                                        \concat
                                            {
                                                r
                                                \sub
                                                    1
                                                \bold
                                                    J
                                            }
                                        +
                                        \concat
                                            {
                                                r
                                                \sub
                                                    2
                                                \bold
                                                    K
                                            }
                                    }
                            }
                        }
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    bqs'8
                    d'8
                    c'8
                    ef'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example expression

            Transforms equivalence:

            >>> expression = expression.transpose(n=1)

            >>> expression(pitch_numbers, pitch_names)
            PitchClassSegment([8, 11, 11.5, 7, 8, 11.5, 0.5, 3, 1, 4])

            >>> expression.get_string()
            'T1(Q)'

            >>> segment = expression(pitch_numbers, pitch_names)
            >>> markup = expression.get_markup()
            >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__(
                ...     figure_name=markup,
                ...     )
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    af'8
                    ^ \markup {
                        \concat
                            {
                                T
                                \sub
                                    1
                                \bold
                                    Q
                            }
                        }
                    b'8
                    bqs'8
                    g'8
                    af'8
                    bqs'8
                    cqs'8
                    ef'8
                    cs'8
                    e'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        Returns new segment.
        """
        if self._expression:
            return self._update_expresion(inspect.currentframe())
        argument = type(self)(items=argument)
        items = self.items + argument.items
        return type(self)(items=items)

    def __contains__(self, argument):
        r"""
        Is true when pitch-class segment contains `argument`.

        ..  container:: example

            Example segments:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=pitch_numbers)
            >>> segment
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> abjad.NamedPitch('bf') in segment
            True

            >>> abjad.NamedPitch('cs') in segment
            False

            >>> 'bf' in segment
            True

            >>> 'cs' in segment
            False

            >>> 10 in segment
            True

            >>> 13 in segment
            False

        Returns true or false.
        """
        return super().__contains__(argument)

    def __format__(self, format_specification=''):
        r"""
        Formats segment.

        ..  container:: example

            With numbered pitch-classes:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=pitch_numbers)

            >>> abjad.f(J)
            abjad.PitchClassSegment(
                (
                    abjad.NumberedPitchClass(10),
                    abjad.NumberedPitchClass(10.5),
                    abjad.NumberedPitchClass(6),
                    abjad.NumberedPitchClass(7),
                    abjad.NumberedPitchClass(10.5),
                    abjad.NumberedPitchClass(7),
                    ),
                item_class=abjad.NumberedPitchClass,
                )

            >>> abjad.show(J) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = J.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            With named pitch-classes:

            >>> pitch_names = ['c', 'ef', 'bqs,', 'd']
            >>> K = abjad.PitchClassSegment(
            ...     items=pitch_names,
            ...     item_class=abjad.NamedPitchClass,
            ...     )

            >>> abjad.f(K)
            abjad.PitchClassSegment(
                (
                    abjad.NamedPitchClass('c'),
                    abjad.NamedPitchClass('ef'),
                    abjad.NamedPitchClass('bqs'),
                    abjad.NamedPitchClass('d'),
                    ),
                item_class=abjad.NamedPitchClass,
                )

            >>> abjad.show(K) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = K.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    c'8
                    ef'8
                    bqs'8
                    d'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        Returns string.
        """
        return super().__format__(format_specification=format_specification)

    @Signature(
        markup_maker_callback='_make___getitem___markup',
        string_template_callback='_make___getitem___string_template',
        )
    def __getitem__(self, argument):
        r"""
        Gets `argument` from segment.

        ..  container:: example

            Example segment:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=pitch_numbers)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> J = abjad.PitchClassSegment(items=pitch_numbers)
            >>> abjad.show(J) # doctest: +SKIP

        ..  container:: example

            Gets item at nonnegative index:

            ..  container:: example

                >>> J[0]
                NumberedPitchClass(10)

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression[0]

                >>> expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                NumberedPitchClass(10)

                >>> expression.get_string()
                'J[0]'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                \bold
                                    J
                                \sub
                                    0
                            }
                        }

        ..  container:: example

            Gets item at negative index:

            ..  container:: example

                >>> J[-1]
                NumberedPitchClass(7)

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression[-1]

                >>> expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                NumberedPitchClass(7)

                >>> expression.get_string()
                'J[-1]'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                \bold
                                    J
                                \sub
                                    -1
                            }
                        }

        ..  container:: example

            Gets slice:

            ..  container:: example

                >>> J[:4]
                PitchClassSegment([10, 10.5, 6, 7])

                >>> segment = J[:4]
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression[:4]

                >>> expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7])

                >>> expression.get_string()
                'J[:4]'

                >>> segment = expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    \bold
                                        J
                                    \sub
                                        [:4]
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Gets retrograde of slice:

            ..  container:: example

                >>> J[:4].retrograde()
                PitchClassSegment([7, 6, 10.5, 10])

                >>> segment = J[:4].retrograde()
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        g'8
                        fs'8
                        bqf'8
                        bf'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression[:4]
                >>> expression = expression.retrograde()

                >>> expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([7, 6, 10.5, 10])

                >>> expression.get_string()
                'R(J[:4])'

                >>> segment = expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        g'8
                        ^ \markup {
                            \concat
                                {
                                    R
                                    \concat
                                        {
                                            \bold
                                                J
                                            \sub
                                                [:4]
                                        }
                                }
                            }
                        fs'8
                        bqf'8
                        bf'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Gets slice of retrograde:

            ..  container:: example

                >>> J.retrograde()[:4]
                PitchClassSegment([7, 10.5, 7, 6])

                >>> segment = J.retrograde()[:4]
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        g'8
                        bqf'8
                        g'8
                        fs'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.retrograde()
                >>> expression = expression[:4]

                >>> expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([7, 10.5, 7, 6])

                >>> expression.get_string()
                'R(J)[:4]'

                >>> segment = expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        g'8
                        ^ \markup {
                            \concat
                                {
                                    \concat
                                        {
                                            (
                                            \concat
                                                {
                                                    R
                                                    \bold
                                                        J
                                                }
                                            )
                                        }
                                    \sub
                                        [:4]
                                }
                            }
                        bqf'8
                        g'8
                        fs'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Returns pitch-class or pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                precedence=100,
                )
        return super().__getitem__(argument)

    def __illustrate__(self, expression_markup_direction=enums.Up, **keywords):
        r"""
        Illustrates segment.

        ..  container:: example

            Illustrates numbered segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Illustrates named segment:

            >>> items = ['c', 'ef', 'bqs,', 'd']
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NumberedPitchClass,
            ...     )
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    c'8
                    ef'8
                    bqs'8
                    d'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns LilyPond file:

            >>> prototype = abjad.LilyPondFile
            >>> isinstance(segment.__illustrate__(), prototype)
            True

        """
        return super().__illustrate__(
            expression_markup_direction=expression_markup_direction,
            **keywords
            )

    def __mul__(self, n):
        r"""
        Multiplies pitch-class segment by `n`.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> 2 * abjad.PitchClassSegment(items=items)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7])

        Returns new pitch-class segment.
        """
        return super().__mul__(n)

    def __repr__(self):
        r"""
        Gets interpreter representation.

        ..  container:: example

            Interpreter representation:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=items)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

        Returns string.
        """
        import abjad
        if self.item_class is abjad.NamedPitchClass:
            contents = ' '.join([str(_) for _ in self])
            contents = '"' + contents + '"'
        else:
            contents = ', '.join([str(_) for _ in self])
            contents = '[' + contents + ']'
        return '{}({})'.format(type(self).__name__, contents)

    def __rmul__(self, n):
        r"""
        Multiplies `n` by pitch-class segment.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=items) * 2
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7])

        Returns new pitch-class segment.
        """
        return super().__rmul__(n)

    def __str__(self):
        r"""
        Gets string representation of pitch-class segment.

        ..  container::

            Gets string represenation of numbered pitch class:

            >>> segment = abjad.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
            >>> str(segment)
            'PC<10, 10.5, 6, 7, 10.5, 7>'

        ..  container::

            Gets string represenation of named pitch class:

            >>> segment = abjad.PitchClassSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> str(segment)
            'PC<bf bqf fs g bqf g>'

        Returns string.
        """
        import abjad
        items = [str(_) for _ in self]
        separator = ' '
        if self.item_class is abjad.NumberedPitchClass:
            separator = ', '
        return 'PC<{}>'.format(separator.join(items))

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        import abjad
        return abjad.NamedPitchClass

    @property
    def _numbered_item_class(self):
        import abjad
        return abjad.NumberedPitchClass

    @property
    def _parent_item_class(self):
        import abjad
        return abjad.PitchClass

    ### PRIVATE METHODS ###

    def _get_padded_string(self, width=2):
        string = super()._get_padded_string(width=width)
        return 'PC<' + string[1:-1] + '>'

    def _is_equivalent_under_transposition(self, argument):
        import abjad
        if not isinstance(argument, type(self)):
            return False
        if not len(self) == len(argument):
            return False
        difference = -(
            abjad.NamedPitch((argument[0].name, 4)) -
            abjad.NamedPitch((self[0].name, 4))
            )
        new_pitch_classes = (x + difference for x in self)
        new_pitch_classes = new(self, items=new_pitch_classes)
        return argument == new_pitch_classes

    @staticmethod
    def _make_rotate_method_name(n=0, stravinsky=False):
        if stravinsky:
            return 'rs'
        return 'r'

    def _transpose_to_zero(self):
        numbers = [_.number for _ in self]
        first_number = self[0].number
        numbers = [pc.number - first_number for pc in self]
        pcs = [_ % 12 for _ in numbers]
        return type(self)(items=pcs, item_class=self.item_class)

    def _update_expression(self, frame, precedence=None):
        import abjad
        callback = abjad.Expression._frame_to_callback(
            frame,
            precedence=precedence,
            )
        return self._expression.append_callback(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        r"""
        Gets item class of segment.

        ..  container:: example

            Gets item class of numbered segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            >>> segment.item_class
            <class 'abjad.pitch.NumberedPitchClass.NumberedPitchClass'>

        ..  container:: example


            Gets item class of named segment:

            >>> items = ['c', 'ef', 'bqs,', 'd']
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> abjad.show(segment) # doctest: +SKIP

            >>> segment.item_class
            <class 'abjad.pitch.NamedPitchClass.NamedPitchClass'>

        ..  container:: example

            Returns class:

            >>> type(segment.item_class)
            <class 'abc.ABCMeta'>

        """
        return super().item_class

    @property
    def items(self):
        r"""
        Gets items in segment.

        ..  container:: example

            ..  container:: example

                Initializes items positionally:

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = abjad.PitchClassSegment(items)
                >>> for item in segment.items:
                ...     item
                ...
                NumberedPitchClass(10)
                NumberedPitchClass(10.5)
                NumberedPitchClass(6)
                NumberedPitchClass(7)
                NumberedPitchClass(10.5)
                NumberedPitchClass(7)

                Initializes items from keyword:

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = abjad.PitchClassSegment(items=items)
                >>> for item in segment.items:
                ...     item
                NumberedPitchClass(10)
                NumberedPitchClass(10.5)
                NumberedPitchClass(6)
                NumberedPitchClass(7)
                NumberedPitchClass(10.5)
                NumberedPitchClass(7)

            ..  container:: example expression

                Initializes items positionally:

                >>> expression = abjad.Expression()
                >>> expression = expression.pitch_class_segment()

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = expression(items)
                >>> for item in segment.items:
                ...     item
                NumberedPitchClass(10)
                NumberedPitchClass(10.5)
                NumberedPitchClass(6)
                NumberedPitchClass(7)
                NumberedPitchClass(10.5)
                NumberedPitchClass(7)

                Initializes items from keyword:

                >>> expression = abjad.Expression()
                >>> expression = expression.pitch_class_segment()

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = expression(items=items)
                >>> for item in segment.items:
                ...     item
                NumberedPitchClass(10)
                NumberedPitchClass(10.5)
                NumberedPitchClass(6)
                NumberedPitchClass(7)
                NumberedPitchClass(10.5)
                NumberedPitchClass(7)

        ..  container:: example

            Returns list:

            >>> isinstance(segment.items, list)
            True

        """
        return super().items

    ### PUBLIC METHODS ###

    def count(self, item):
        """
        Counts `item` in segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

        ..  container:: example

            Counts existing item in segment:

            >>> segment.count(-1.5)
            2

        ..  container:: example

            Counts nonexisting item in segment:

            >>> segment.count('text')
            0

        ..  container:: example

            Returns nonnegative integer:

            >>> isinstance(segment.count('text'), int)
            True

        """
        return super().count(item)

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Initializes segment from `selection`.

        ..  container:: example

            Initializes from selection:

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> staff_group = abjad.StaffGroup([staff_1, staff_2])
            >>> abjad.show(staff_group) # doctest: +SKIP

            >>> selection = abjad.select((staff_1, staff_2))
            >>> segment = abjad.PitchClassSegment.from_selection(selection)
            >>> abjad.show(segment) # doctest: +SKIP

        ..  container:: example

            Returns pitch-class segment:

            >>> segment
            PitchClassSegment("c d fs a b c g")

        """
        import abjad
        pitch_segment = abjad.PitchSegment.from_selection(selection)
        return class_(
            items=pitch_segment,
            item_class=item_class,
            )

    def has_duplicates(self):
        """
        Is true when segment contains duplicate items.

        ..  container:: example

            Has duplicates:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            >>> segment.has_duplicates()
            True

        ..  container:: example

            Has no duplicates:

            >>> items = "c d e f g a b"
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            >>> segment.has_duplicates()
            False

        Returns true or false.
        """
        import abjad
        return len(abjad.PitchClassSet(self)) < len(self)

    def index(self, item):
        """
        Gets index of `item` in segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

        ..  container:: example

            Gets index of first item in segment:

            >>> segment.index(-2)
            0

        ..  container:: example

            Gets index of second item in segment:

            >>> segment.index(-1.5)
            1

        ..  container:: example

            Returns nonnegative integer:

            >>> isinstance(segment.index(-1.5), int)
            True

        """
        return super().index(item)

    @Signature(
        is_operator=True,
        method_name='I',
        subscript='axis',
        )
    def invert(self, axis=None):
        r"""
        Inverts segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> abjad.show(J) # doctest: +SKIP

        ..  container:: example

            Inverts segment:

            ..  container:: example

                >>> J.invert()
                PitchClassSegment([2, 1.5, 6, 5, 1.5, 5])

                >>> segment = J.invert()
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        d'8
                        dqf'8
                        fs'8
                        f'8
                        dqf'8
                        f'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.invert()

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([2, 1.5, 6, 5, 1.5, 5])

                >>> expression.get_string()
                'I(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        d'8
                        ^ \markup {
                            \concat
                                {
                                    I
                                    \bold
                                        J
                                }
                            }
                        dqf'8
                        fs'8
                        f'8
                        dqf'8
                        f'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Inverts inversion of segment:

            ..  container:: example

                >>> J.invert().invert()
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> segment = J.invert().invert()
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.invert()
                >>> expression = expression.invert()

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> expression.get_string()
                'I(I(J))'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    I
                                    \concat
                                        {
                                            I
                                            \bold
                                                J
                                        }
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        items = [_.invert(axis=axis) for _ in self]
        return type(self)(items=items)

    def make_notes(self, n=None, written_duration=None):
        r"""
        Makes first `n` notes in segment.

        ..  container:: example

            Example segment:

            >>> items = [2, 4.5, 6, 11, 4.5, 10]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

        ..  container:: example

            Makes eighth notes:

            >>> notes = segment.make_notes()
            >>> staff = abjad.Staff(notes)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    d'8
                    eqs'8
                    fs'8
                    b'8
                    eqs'8
                    bf'8
                }

        ..  container:: example

            Makes notes with nonassignable durations:

            >>> notes = segment.make_notes(4, abjad.Duration(5, 16))
            >>> staff = abjad.Staff(notes)
            >>> time_signature = abjad.TimeSignature((5, 4))
            >>> abjad.attach(time_signature, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 5/4
                    d'4
                    ~
                    d'16
                    eqs'4
                    ~
                    eqs'16
                    fs'4
                    ~
                    fs'16
                    b'4
                    ~
                    b'16
                }

        Interprets none-valued `n` equal to length of segment.

        Interprets none-valued `written_duration` equal to 1/8.

        ..  container:: example

            Returns selection:

            >>> isinstance(segment.make_notes(), abjad.Selection)
            True

        """
        import abjad
        n = n or len(self)
        written_duration = written_duration or abjad.Duration(1, 8)
        maker = abjad.NoteMaker()
        result = maker([0] * n, [written_duration])
        logical_ties = abjad.iterate(result).logical_ties()
        for i, logical_tie in enumerate(logical_ties):
            pitch_class = abjad.NamedPitchClass(self[i % len(self)])
            pitch = abjad.NamedPitch((pitch_class.name, 4))
            for note in logical_tie:
                note.written_pitch = pitch
        return result

    @Signature(
        is_operator=True,
        method_name='M',
        subscript='n',
        )
    def multiply(self, n=1):
        r"""
        Multiplies pitch-classes in segment by `n`.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> abjad.show(J) # doctest: +SKIP

        ..  container:: example

            Multiplies pitch-classes in segment by 1:

            ..  container:: example

                >>> J.multiply(n=1)
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> segment = J.multiply(n=1)
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.multiply(n=1)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> expression.get_string()
                'M1(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    M
                                    \sub
                                        1
                                    \bold
                                        J
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Multiplies pitch-classes in segment by 5:

            ..  container:: example

                >>> J.multiply(n=5)
                PitchClassSegment([2, 4.5, 6, 11, 4.5, 11])

                >>> segment = J.multiply(n=5)
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        d'8
                        eqs'8
                        fs'8
                        b'8
                        eqs'8
                        b'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.multiply(n=5)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([2, 4.5, 6, 11, 4.5, 11])

                >>> expression.get_string()
                'M5(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        d'8
                        ^ \markup {
                            \concat
                                {
                                    M
                                    \sub
                                        5
                                    \bold
                                        J
                                }
                            }
                        eqs'8
                        fs'8
                        b'8
                        eqs'8
                        b'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Multiplies pitch-classes in segment by 7:

            ..  container:: example

                >>> J.multiply(n=7)
                PitchClassSegment([10, 1.5, 6, 1, 1.5, 1])

                >>> segment = J.multiply(n=7)
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        dqf'8
                        fs'8
                        cs'8
                        dqf'8
                        cs'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.multiply(n=7)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 1.5, 6, 1, 1.5, 1])

                >>> expression.get_string()
                'M7(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    M
                                    \sub
                                        7
                                    \bold
                                        J
                                }
                            }
                        dqf'8
                        fs'8
                        cs'8
                        dqf'8
                        cs'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Multiplies pitch-classes in segment by 11:

            ..  container:: example

                >>> segment = J.multiply(n=11)
                >>> segment
                PitchClassSegment([2, 7.5, 6, 5, 7.5, 5])

                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        d'8
                        gqs'8
                        fs'8
                        f'8
                        gqs'8
                        f'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.multiply(n=11)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([2, 7.5, 6, 5, 7.5, 5])

                >>> expression.get_string()
                'M11(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        d'8
                        ^ \markup {
                            \concat
                                {
                                    M
                                    \sub
                                        11
                                    \bold
                                        J
                                }
                            }
                        gqs'8
                        fs'8
                        f'8
                        gqs'8
                        f'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        items = [abjad.NumberedPitchClass(_) for _ in self]
        items = [_.multiply(n) for _ in items]
        return type(self)(items=items)

    @Signature()
    def permute(self, row=None):
        r"""
        Permutes segment by twelve-tone `row`.

        ..  container:: example

            >>> abjad.PitchClassSegment([-2, -1, 6, 7, -1, 7])
            PitchClassSegment([10, 11, 6, 7, 11, 7])

            >>> segment = abjad.PitchClassSegment([-2, -1, 6, 7, -1, 7])
            >>> abjad.show(segment) # doctest: +SKIP

            ..  doctest:

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    bf'8
                    b'8
                    fs'8
                    g'8
                    b'8
                    g'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.permute([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
            PitchClassSegment([4, 11, 5, 3, 11, 3])

            >>> segment = segment.permute([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    e'8
                    b'8
                    f'8
                    ef'8
                    b'8
                    ef'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example expression

            >>> expression = abjad.Expression(name='J')
            >>> expression = expression.pitch_class_segment()
            >>> row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
            >>> expression = expression.permute(row)

            >>> expression([-2, -1, 6, 7, -1, 7])
            PitchClassSegment([4, 11, 5, 3, 11, 3])

            >>> expression.get_string()
            'permute(J, row=[10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])'

            >>> segment = expression([-2, -1, 6, 7, -1, 7])
            >>> markup = expression.get_markup()
            >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

            ..  doctest:

                >>> lilypond_file = segment.__illustrate__(
                ...     figure_name=markup,
                ...     )
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    e'8
                    ^ \markup {
                        \concat
                            {
                                permute(
                                \bold
                                    J
                                ", row=[10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])"
                            }
                        }
                    b'8
                    f'8
                    ef'8
                    b'8
                    ef'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        Returns new segment.
        """
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        row = abjad.TwelveToneRow(items=row)
        items = row(self)
        return type(self)(items=items)

    @Signature(is_operator=True, method_name='R')
    def retrograde(self):
        r"""
        Gets retrograde of segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> abjad.show(J) # doctest: +SKIP

        ..  container:: example

            Gets retrograde of segment:

            ..  container:: example

                >>> segment = J.retrograde()
                >>> segment
                PitchClassSegment([7, 10.5, 7, 6, 10.5, 10])

                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        g'8
                        bqf'8
                        g'8
                        fs'8
                        bqf'8
                        bf'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.retrograde()

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([7, 10.5, 7, 6, 10.5, 10])

                >>> expression.get_string()
                'R(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        g'8
                        ^ \markup {
                            \concat
                                {
                                    R
                                    \bold
                                        J
                                }
                            }
                        bqf'8
                        g'8
                        fs'8
                        bqf'8
                        bf'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Gets retrograde of retrograde of segment:

            ..  container:: example

                >>> segment = J.retrograde().retrograde()
                >>> segment
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.retrograde()
                >>> expression = expression.retrograde()

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> expression.get_string()
                'R(R(J))'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    R
                                    \concat
                                        {
                                            R
                                            \bold
                                                J
                                        }
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return type(self)(items=reversed(self))

    @Signature(
        is_operator=True,
        method_name_callback='_make_rotate_method_name',
        subscript='n',
        )
    def rotate(self, n=0, stravinsky=False):
        r"""
        Rotates segment by index `n`.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> abjad.show(J) # doctest: +SKIP

        ..  container:: example

            Rotates segment to the right:

            ..  container:: example

                >>> J.rotate(n=1)
                PitchClassSegment([7, 10, 10.5, 6, 7, 10.5])

                >>> segment = J.rotate(n=1)
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        g'8
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.rotate(n=1)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([7, 10, 10.5, 6, 7, 10.5])

                >>> expression.get_string()
                'r1(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        g'8
                        ^ \markup {
                            \concat
                                {
                                    r
                                    \sub
                                        1
                                    \bold
                                        J
                                }
                            }
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Rotates segment to the left:

            ..  container:: example

                >>> J.rotate(n=-1)
                PitchClassSegment([10.5, 6, 7, 10.5, 7, 10])

                >>> segment = J.rotate(n=-1)
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        bf'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.rotate(n=-1)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10.5, 6, 7, 10.5, 7, 10])

                >>> expression.get_string()
                'r-1(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bqf'8
                        ^ \markup {
                            \concat
                                {
                                    r
                                    \sub
                                        -1
                                    \bold
                                        J
                                }
                            }
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        bf'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Rotates segment by zero:

            ..  container:: example

                >>> J.rotate(n=0)
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> segment = J.rotate(n=0)
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.rotate(n=0)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> expression.get_string()
                'r0(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    r
                                    \sub
                                        0
                                    \bold
                                        J
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

        ..  container:: example

            Stravinsky-style rotation back-transposes segment to
            begin at zero:

            ..  container:: example

                >>> J.rotate(n=1, stravinsky=True)
                PitchClassSegment([0, 3, 3.5, 11, 0, 3.5])

                >>> segment = J.rotate(n=1, stravinsky=True)
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        c'8
                        ef'8
                        eqf'8
                        b'8
                        c'8
                        eqf'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.rotate(n=1, stravinsky=True)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([0, 3, 3.5, 11, 0, 3.5])

                >>> expression.get_string()
                'rs1(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        c'8
                        ^ \markup {
                            \concat
                                {
                                    rs
                                    \sub
                                        1
                                    \bold
                                        J
                                }
                            }
                        ef'8
                        eqf'8
                        b'8
                        c'8
                        eqf'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        items = abjad.sequence(self._collection).rotate(n=n)
        if stravinsky:
            n = 0 - float(items[0].number)
            segment = new(self, items=items)
            segment = segment.transpose(n=n)
            items = segment.items[:]
        return type(self)(items=items)

    def to_pitch_classes(self):
        r"""
        Changes to pitch-classes.

        ..  container:: example

            To numbered pitch-class segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> segment
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitch_classes()
            >>> segment
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            To named pitch-class segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> segment
            PitchClassSegment("bf bqf fs g bqf g")

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitch_classes()
            >>> segment
            PitchClassSegment("bf bqf fs g bqf g")

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        Returns new segment.
        """
        return new(self)

    def to_pitches(self):
        r"""
        Changes to pitches.

        ..  container:: example

            To numbered pitch segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> segment
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitches()
            >>> segment
            PitchSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        bqf'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            To named pitch segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> segment
            PitchClassSegment("bf bqf fs g bqf g")

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitches()
            >>> segment
            PitchSegment("bf' bqf' fs' g' bqf' g'")

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        bqf'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new segment.
        """
        import abjad
        class_ = abjad.Pitch
        item_class = class_._to_pitch_item_class(self.item_class)
        return abjad.PitchSegment(items=self.items, item_class=item_class)

    @Signature(
        is_operator=True,
        method_name='T',
        subscript='n',
        )
    def transpose(self, n=0):
        r"""
        Transposes segment by index `n`.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> abjad.show(J) # doctest: +SKIP

        ..  container:: example

            Transposes segment by positive index:

            ..  container:: example

                >>> J.transpose(n=13)
                PitchClassSegment([11, 11.5, 7, 8, 11.5, 8])

                >>> segment = J.transpose(n=13)
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        b'8
                        bqs'8
                        g'8
                        af'8
                        bqs'8
                        af'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.transpose(n=13)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([11, 11.5, 7, 8, 11.5, 8])

                >>> expression.get_string()
                'T13(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        b'8
                        ^ \markup {
                            \concat
                                {
                                    T
                                    \sub
                                        13
                                    \bold
                                        J
                                }
                            }
                        bqs'8
                        g'8
                        af'8
                        bqs'8
                        af'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Transposes segment by negative index:

            ..  container:: example

                >>> J.transpose(n=-13)
                PitchClassSegment([9, 9.5, 5, 6, 9.5, 6])

                >>> segment = J.transpose(n=-13)
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        a'8
                        aqs'8
                        f'8
                        fs'8
                        aqs'8
                        fs'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.transpose(n=-13)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([9, 9.5, 5, 6, 9.5, 6])

                >>> expression.get_string()
                'T-13(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        a'8
                        ^ \markup {
                            \concat
                                {
                                    T
                                    \sub
                                        -13
                                    \bold
                                        J
                                }
                            }
                        aqs'8
                        f'8
                        fs'8
                        aqs'8
                        fs'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Transposes segment by zero index:

            ..  container:: example

                >>> J.transpose(n=0)
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> segment = J.transpose(n=0)
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.transpose(n=0)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> expression.get_string()
                'T0(J)'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    T
                                    \sub
                                        0
                                    \bold
                                        J
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        items = [_.transpose(n=n) for _ in self]
        return type(self)(items=items)

    def voice_horizontally(self, initial_octave=4):
        r"""
        Voices segment with each pitch as close to the previous pitch as
        possible.

        ..  todo:: Should be implemented somewhere else.

        ..  container:: example

            Voices horizontally:

            >>> items = "c b d e f g e b a c"
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            >>> voiced_segment = segment.voice_horizontally()
            >>> abjad.show(voiced_segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = voiced_segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score])
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble Staff"
                        {
                            \clef "treble"
                            c'1 * 1/8
                            b1 * 1/8
                            d'1 * 1/8
                            e'1 * 1/8
                            f'1 * 1/8
                            g'1 * 1/8
                            e'1 * 1/8
                            b1 * 1/8
                            r1 * 1/8
                            c'1 * 1/8
                        }
                        \context Staff = "Bass Staff"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            a1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        ..  container:: example

            Returns pitch segment:

            >>> voiced_segment
            PitchSegment("c' b d' e' f' g' e' b a c'")

        """
        import abjad
        initial_octave = abjad.Octave(initial_octave)
        pitches = []
        if self:
            pitch_class = abjad.NamedPitchClass(self[0])
            pitch = abjad.NamedPitch((pitch_class.name, initial_octave))
            pitches.append(pitch)
            for pitch_class in self[1:]:
                pitch_class = abjad.NamedPitchClass(pitch_class)
                pitch = abjad.NamedPitch((pitch_class.name, initial_octave))
                semitones = abs((pitch - pitches[-1]).semitones)
                while 6 < semitones:
                    if pitch < pitches[-1]:
                        pitch += 12
                    else:
                        pitch -= 12
                    semitones = abs((pitch - pitches[-1]).semitones)
                pitches.append(pitch)
        if self.item_class is abjad.NamedPitchClass:
            item_class = abjad.NamedPitch
        else:
            item_class = abjad.NumberedPitch
        return abjad.PitchSegment(
            items=pitches,
            item_class=item_class,
            )

    def voice_vertically(self, initial_octave=4):
        r"""
        Voices segment with each pitch higher than the previous.

        ..  todo:: Should be implemented somewhere else.

        ..  container:: example

            Voices vertically:

            >>> string = "c' ef' g' bf' d'' f'' af''"
            >>> segment = abjad.PitchClassSegment(string)
            >>> abjad.show(segment) # doctest: +SKIP

            >>> voiced_segment = segment.voice_vertically()
            >>> abjad.show(voiced_segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = voiced_segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score])
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble Staff"
                        {
                            \clef "treble"
                            c'1 * 1/8
                            ef'1 * 1/8
                            g'1 * 1/8
                            bf'1 * 1/8
                            d''1 * 1/8
                            f''1 * 1/8
                            af''1 * 1/8
                        }
                        \context Staff = "Bass Staff"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        ..  container:: example

            Returns pitch segment:

            >>> voiced_segment
            PitchSegment("c' ef' g' bf' d'' f'' af''")

        """
        import abjad
        initial_octave = abjad.Octave(initial_octave)
        pitches = []
        if self:
            pitch_class = abjad.NamedPitchClass(self[0])
            pitch = abjad.NamedPitch((pitch_class.name, initial_octave))
            pitches.append(pitch)
            for pitch_class in self[1:]:
                pitch_class = abjad.NamedPitchClass(pitch_class)
                pitch = abjad.NamedPitch((pitch_class.name, initial_octave))
                while pitch < pitches[-1]:
                    pitch += 12
                pitches.append(pitch)
        if self.item_class is abjad.NamedPitchClass:
            item_class = abjad.NamedPitch
        else:
            item_class = abjad.NumberedPitch
        return abjad.PitchSegment(
            items=pitches,
            item_class=item_class,
            )
