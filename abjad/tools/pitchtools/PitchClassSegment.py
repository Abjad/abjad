# -* coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import expressiontools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.pitchtools.Segment import Segment
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import new


class PitchClassSegment(Segment):
    r'''Pitch-class segment.

    ..  container:: example

        With numbered pitch-classes:

        ::

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = pitchtools.PitchClassSegment(items=items)
            >>> show(segment) # doctest: +SKIP

        ..  doctest::

            >>> lilypond_file = segment.__illustrate__()
            >>> f(lilypond_file[Voice])
            \new Voice {
                bf'8
                bqf'8
                fs'8
                g'8
                bqf'8
                g'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

    ..  container:: example

        With named pitch-classes:

        ::

            >>> items = ['c', 'ef', 'bqs,', 'd']
            >>> segment = pitchtools.PitchClassSegment(
            ...     items=items,
            ...     item_class=pitchtools.NamedPitchClass,
            ...     )
            >>> show(segment) # doctest: +SKIP

        ..  doctest::

            >>> lilypond_file = segment.__illustrate__()
            >>> f(lilypond_file[Voice])
            \new Voice {
                c'8
                ef'8
                bqs'8
                d'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

    ..  container:: example

        Interpreter representation:

        ::

            >>> segment
            PitchClassSegment(['c', 'ef', 'bqs', 'd'])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        name=None,
        name_markup=None,
        ):
        if not items and not item_class:
            item_class = self._named_item_class
        Segment.__init__(
            self,
            items=items,
            item_class=item_class,
            name=name,
            name_markup=name_markup,
            )

    ### SPECIAL METHODS ###

    def __add__(self, segment):
        r'''Adds `segment` to segment.

        ..  container:: example

            Example segments:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> J = pitchtools.PitchClassSegment(items=items, name='J')
                >>> J
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='J')

            ::

                >>> show(J) # doctest: +SKIP

            ::

                >>> items = ['c', 'ef', 'bqs,', 'd']
                >>> K = pitchtools.PitchClassSegment(items=items, name='K')
                >>> K
                PitchClassSegment(['c', 'ef', 'bqs', 'd'], name='K')

            ::

                >>> show(K) # doctest: +SKIP

        ..  container:: example

            Adds J and K:

            ::

                >>> segment = J + K
                >>> segment
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 0, 3, 11.5, 2], name='J + K')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    bf'8
                        ^ \markup {
                            \bold
                                J
                            +
                            \bold
                                K
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
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Adds K and J:

            ::

                >>> segment = K + J
                >>> segment
                PitchClassSegment(['c', 'ef', 'bqs', 'd', 'bf', 'bqf', 'fs', 'g', 'bqf', 'g'], name='K + J')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    c'8
                        ^ \markup {
                            \bold
                                K
                            +
                            \bold
                                J
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
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Adds J repeatedly:

            ::

                >>> segment = J + J + J
                >>> segment
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7], name='J + J + J')


            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    bf'8
                        ^ \markup {
                            \bold
                                J
                            +
                            \bold
                                J
                            +
                            \bold
                                J
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
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Adds transformed segments:

            ::

                >>> segment = J.rotate(n=1) + K.rotate(n=2)
                >>> segment
                PitchClassSegment([7, 10, 10.5, 6, 7, 10.5, 11.5, 2, 0, 3], name='r1(J) + r2(K)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    g'8
                        ^ \markup {
                            \concat
                                {
                                    r
                                    \hspace
                                        #-0.2
                                    \sub
                                        1
                                    \concat
                                        {
                                            \hspace
                                                #0.4
                                            \bold
                                                J
                                        }
                                }
                            +
                            \concat
                                {
                                    r
                                    \hspace
                                        #-0.2
                                    \sub
                                        2
                                    \concat
                                        {
                                            \hspace
                                                #0.4
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
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Establishes equivalence after add:

            ::

                >>> segment = J.rotate(n=1) + K.rotate(n=2)
                >>> segment
                PitchClassSegment([7, 10, 10.5, 6, 7, 10.5, 11.5, 2, 0, 3], name='r1(J) + r2(K)')

            ::

                >>> segment = expressiontools.Expression.establish_equivalence(segment, 'Q')
                >>> segment
                PitchClassSegment([7, 10, 10.5, 6, 7, 10.5, 11.5, 2, 0, 3], name='Q')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    g'8
                        ^ \markup {
                            \line
                                {
                                    \bold
                                        Q
                                    =
                                    \concat
                                        {
                                            r
                                            \hspace
                                                #-0.2
                                            \sub
                                                1
                                            \concat
                                                {
                                                    \hspace
                                                        #0.4
                                                    \bold
                                                        J
                                                }
                                        }
                                    +
                                    \concat
                                        {
                                            r
                                            \hspace
                                                #-0.2
                                            \sub
                                                2
                                            \concat
                                                {
                                                    \hspace
                                                        #0.4
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
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Transforms equivalence:

            ::

                >>> segment = segment.transpose(n=1)
                >>> segment
                PitchClassSegment([8, 11, 11.5, 7, 8, 11.5, 0.5, 3, 1, 4], name='T1(Q)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    af'8
                        ^ \markup {
                            \concat
                                {
                                    T
                                    \hspace
                                        #-0.2
                                    \sub
                                        1
                                    \concat
                                        {
                                            \hspace
                                                #0.4
                                            \bold
                                                Q
                                        }
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
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns new segment.
        '''
        if not isinstance(segment, type(self)):
            message = 'must be pitch-class segment: {!r}.'
            message = message.format(segment)
            raise TypeError(message)
        items = self.items + segment.items
        string_expression = '{{}} + {}'.format(segment.name)
        markup_expression = expressiontools.Expression()
        markup_expression = markup_expression.make_callback(
            'Markup({})'
            )
        segment_expression_markup = \
            expressiontools.Expression._get_expression_markup(segment)
        if segment_expression_markup is None:
            segment_expression_markup = '?'
        else:
            segment_expression_markup = format(
                segment_expression_markup,
                'storage',
                )
        markup_expression = markup_expression.make_callback(
            "{{}} + Markup('+') + {}".format(segment_expression_markup)
            )
        segment = new(self, items=items, name=self._name)
        expressiontools.Expression._track_expression(
            self,
            segment,
            '__add__',
            direction=Right,
            markup_expression=markup_expression,
            string_expression=string_expression,
            )
        return segment

    def __format__(self, format_specification=''):
        r'''Formats segment.

        ..  container:: example

            With numbered pitch-classes:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> J = pitchtools.PitchClassSegment(items=items, name='J')

            ::

                >>> f(J)
                pitchtools.PitchClassSegment(
                    (
                        pitchtools.NumberedPitchClass(10),
                        pitchtools.NumberedPitchClass(10.5),
                        pitchtools.NumberedPitchClass(6),
                        pitchtools.NumberedPitchClass(7),
                        pitchtools.NumberedPitchClass(10.5),
                        pitchtools.NumberedPitchClass(7),
                        ),
                    item_class=pitchtools.NumberedPitchClass,
                    name='J',
                    )

            ::

                >>> show(J) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = J.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    bf'8
                        ^ \markup {
                            \bold
                                J
                            }
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            With named pitch-classes:

            ::

                >>> items = ['c', 'ef', 'bqs,', 'd']
                >>> K = pitchtools.PitchClassSegment(
                ...     items=items,
                ...     item_class=pitchtools.NamedPitchClass,
                ...     name='K',
                ...     )

            ::

                >>> f(K)
                pitchtools.PitchClassSegment(
                    (
                        pitchtools.NamedPitchClass('c'),
                        pitchtools.NamedPitchClass('ef'),
                        pitchtools.NamedPitchClass('bqs'),
                        pitchtools.NamedPitchClass('d'),
                        ),
                    item_class=pitchtools.NamedPitchClass,
                    name='K',
                    )

            ::

                >>> show(K) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = K.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    c'8
                        ^ \markup {
                            \bold
                                K
                            }
                    ef'8
                    bqs'8
                    d'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns string.
        '''
        superclass = super(PitchClassSegment, self)
        return superclass.__format__(format_specification=format_specification)

    def __getitem__(self, i):
        r'''Gets `i` from segment.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> J = pitchtools.PitchClassSegment(items=items, name='J')
                >>> J
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='J')

            ::

                >>> show(J) # doctest: +SKIP

        ..  container:: example

            Gets item at nonnegative index:

            ::

                >>> pitch_class = J[0]
                >>> pitch_class
                NumberedPitchClass(10)

        ..  container:: example

            Gets item at negative index:

            ::

                >>> pitch_class = J[-1]
                >>> pitch_class
                NumberedPitchClass(7)

        ..  container:: example

            Gets slice:

            ::

                >>> segment = J[:4]
                >>> segment
                PitchClassSegment([10, 10.5, 6, 7], name='J[:4]')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
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
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets retrograde of slice:

            ::

                >>> segment = J[:4]
                >>> segment = segment.retrograde()
                >>> segment
                PitchClassSegment([7, 6, 10.5, 10], name='R(J[:4])')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
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
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets slice of retrograde:

            ::

                >>> segment = J.retrograde()
                >>> segment = segment[:4]
                >>> segment
                PitchClassSegment([7, 10.5, 7, 6], name='R(J)[:4]')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    g'8
                        ^ \markup {
                            \concat
                                {
                                    \parenthesize
                                        \concat
                                            {
                                                R
                                                \concat
                                                    {
                                                        \hspace
                                                            #0.4
                                                        \bold
                                                            J
                                                    }
                                            }
                                    \sub
                                        [:4]
                                }
                            }
                    bqf'8
                    g'8
                    fs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns pitch-class or pitch-class segment:

            ::

                >>> isinstance(segment, pitchtools.PitchClassSegment)
                True

        '''
        import abjad
        superclass = super(PitchClassSegment, self)
        result = superclass.__getitem__(i)
        if isinstance(result, Segment):
            result._name = self._name
            if isinstance(i, int):
                subscript_string = '[{i}]'
                start = stop = step = None
            elif isinstance(i, slice):
                if i.step is not None:
                    raise NotImplementedError
                if i.start is None and i.stop is None:
                    subscript_string = '[:]'
                elif i.start is None:
                    subscript_string = '[:{stop}]'
                elif i.stop is None:
                    subscript_string = '[{start}:]'
                else:
                    subscript_string = '[{start}:{stop}]'
                start = i.start
                stop = i.stop
                step = i.step
            else:
                message = 'must be integer or slice: {!r}.'
                message = message.format(i)
                raise TypeError(message)
            subscript_string = subscript_string.format(
                i=i,
                start=start,
                stop=stop,
                step=step,
                )
            string_expression = '{}' + subscript_string
            markup_expression = expressiontools.Expression()
            markup_expression = markup_expression.make_callback(
                'Markup({})',
                )
            subscript_markup = abjad.Markup(subscript_string).sub()
            template = 'Markup.concat([{{}}, Markup({!r}).sub()])'
            template = template.format(subscript_string)
            markup_expression = markup_expression.make_callback(template)
            expressiontools.Expression._track_expression(
                self,
                result,
                '__getitem__',
                direction=Right,
                markup_expression=markup_expression,
                precedence=100,
                string_expression=string_expression,
                )
        return result

    def __illustrate__(self, expression_markup_direction=Up, **kwargs):
        r'''Illustrates segment.

        ..  container:: example

            Illustrates numbered segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Illustrates named segment:

            ::

                >>> items = ['c', 'ef', 'bqs,', 'd']
                >>> segment = pitchtools.PitchClassSegment(
                ...     items=items,
                ...     item_class=pitchtools.NumberedPitchClass,
                ...     )
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    c'8
                    ef'8
                    bqs'8
                    d'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns LilyPond file:

            ::

                >>> isinstance(segment.__illustrate__(), lilypondfiletools.LilyPondFile)
                True

        '''
        superclass = super(PitchClassSegment, self)
        return superclass.__illustrate__(
            expression_markup_direction=expression_markup_direction,
            **kwargs
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchClass

    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.PitchClass

    ### PRIVATE METHODS ###

    def _is_equivalent_under_transposition(self, expr):
        r'''Is true when `expr` is equivalent to segment under transposition.
        
        Otherwise False.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        if not isinstance(expr, type(self)):
            return False
        if not len(self) == len(expr):
            return False
        difference = -(pitchtools.NamedPitch(expr[0], 4) -
            pitchtools.NamedPitch(self[0], 4))
        new_pitch_classes = (x + difference for x in self)
        new_pitch_classes = new(self, items=new_pitch_classes)
        return expr == new_pitch_classes

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        r'''Gets item class of segment.

        ..  container:: example

            Gets item class of numbered segment:
        
            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            ::

                >>> segment.item_class
                <class 'abjad.tools.pitchtools.NumberedPitchClass.NumberedPitchClass'>

        ..  container:: example


            Gets item class of named segment:

            ::

                >>> items = ['c', 'ef', 'bqs,', 'd']
                >>> segment = pitchtools.PitchClassSegment(
                ...     items=items,
                ...     item_class=pitchtools.NamedPitchClass,
                ...     )
                >>> show(segment) # doctest: +SKIP

            ::
                
                >>> segment.item_class
                <class 'abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass'>

        ..  container:: example

            Returns class:

            ::

                >>> type(segment.item_class)
                <class 'abc.ABCMeta'>

        '''
        superclass = super(PitchClassSegment, self)
        return superclass.item_class

    @property
    def items(self):
        r'''Gets items in segment.

        ..  container:: example

            Gets items in numbered segment:
        
            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            ::

                >>> for item in segment.items:
                ...     item
                NumberedPitchClass(10)
                NumberedPitchClass(10.5)
                NumberedPitchClass(6)
                NumberedPitchClass(7)
                NumberedPitchClass(10.5)
                NumberedPitchClass(7)

        ..  container:: example

            Gets items in named segment:

            ::

                >>> items = ['c', 'ef', 'bqs,', 'd']
                >>> segment = pitchtools.PitchClassSegment(
                ...     items=items,
                ...     item_class=pitchtools.NamedPitchClass,
                ...     )
                >>> show(segment) # doctest: +SKIP

            ::
                
                >>> for item in segment.items:
                ...     item
                NamedPitchClass('c')
                NamedPitchClass('ef')
                NamedPitchClass('bqs')
                NamedPitchClass('d')

        ..  container:: example

            Returns list:

            ::

                >>> isinstance(segment.items, list)
                True

        '''
        superclass = super(PitchClassSegment, self)
        return superclass.items

    @property
    def name(self):
        r'''Gets name of segment.

        ..  container:: example

            Gets name:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items, name='J')
                >>> segment
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='J')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    bf'8
                        ^ \markup {
                            \bold
                                J
                            }
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

                >>> segment.name
                'J'

        ..  container:: example

            Defaults to none:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> segment
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

                >>> segment.name is None
                True

        Set to string or none.

        Returns string or none.
        '''
        superclass = super(PitchClassSegment, self)
        return superclass.name

    ### PUBLIC METHODS ###

    def alpha(self):
        r'''Gets alpha transform of segment.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> J = pitchtools.PitchClassSegment(items=items, name='J')
                >>> J
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='J')

            ::

                >>> show(J) # doctest: +SKIP

        ..  container:: example

            Gets alpha transform of segment:

            ::

                >>> segment = J.alpha()
                >>> segment
                PitchClassSegment([11, 11.5, 7, 6, 11.5, 6], name='A(J)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    b'8
                        ^ \markup {
                            \concat
                                {
                                    A
                                    \concat
                                        {
                                            \hspace
                                                #0.4
                                            \bold
                                                J
                                        }
                                }
                            }
                    bqs'8
                    g'8
                    fs'8
                    bqs'8
                    fs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets alpha transform of alpha transform of segment:

            ::

                >>> segment = J.alpha().alpha()
                >>> segment
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='A(A(J))')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    bf'8
                        ^ \markup {
                            \concat
                                {
                                    A
                                    \concat
                                        {
                                            A
                                            \concat
                                                {
                                                    \hspace
                                                        #0.4
                                                    \bold
                                                        J
                                                }
                                        }
                                }
                            }
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

                >>> segment == J
                True

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> isinstance(segment, pitchtools.PitchClassSegment)
                True

        '''
        numbers = []
        for pc in self:
            pc = abs(float(pc))
            is_integer = True
            if not mathtools.is_integer_equivalent_number(pc):
                is_integer = False
                fraction_part = pc - int(pc)
                pc = int(pc)
            if abs(pc) % 2 == 0:
                number = (abs(pc) + 1) % 12
            else:
                number = abs(pc) - 1
            if not is_integer:
                number += fraction_part
            else:
                number = int(number)
            numbers.append(number)
        string_expression = 'A({})'
        markup_expression = expressiontools.Expression()
        markup_expression = markup_expression.make_callback(
            'Markup({})'
            )
        markup_expression = markup_expression.make_callback(
            "Markup.concat([Markup('A'), {}])",
            )
        segment = new(self, items=numbers, name=self._name)
        expressiontools.Expression._track_expression(
            self,
            segment,
            'alpha',
            markup_expression=markup_expression,
            string_expression=string_expression,
            )
        return segment

    def count(self, item):
        r'''Counts `item` in segment.

        ..  container:: example

            Example segment:
        
            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Counts existing item in segment:

            ::
                
                >>> segment.count(-1.5)
                2

        ..  container:: example

            Counts nonexisting item in segment:

            ::
                
                >>> segment.count('text')
                0

        ..  container:: example

            Returns nonnegative integer:

            ::

                >>> isinstance(segment.count('text'), int)
                True

        '''
        superclass = super(PitchClassSegment, self)
        return superclass.count(item)

    @classmethod
    def from_selection(class_, selection, item_class=None):
        r'''Initializes segment from `selection`.

        ..  container:: example

            itializes from selection:

            ::

                >>> staff_1 = Staff("c'4 <d' fs' a'>4 b2")
                >>> staff_2 = Staff("c4. r8 g2")
                >>> staff_group = StaffGroup([staff_1, staff_2])
                >>> show(staff_group) # doctest: +SKIP

            ::

                >>> selection = select((staff_1, staff_2))
                >>> segment = pitchtools.PitchClassSegment.from_selection(selection)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> segment
                PitchClassSegment(['c', 'd', 'fs', 'a', 'b', 'c', 'g'])

        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return class_(
            items=pitch_segment,
            item_class=item_class,
            )

    def has_duplicates(self):
        r'''Is true when segment contains duplicate items. Otherwise false.

        ..  container:: example

            Has duplicates:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            ::

                >>> segment.has_duplicates()
                True

        ..  container:: example

            Has no duplicates:

            ::

                >>> items = "c d e f g a b"
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            ::

                >>> segment.has_duplicates()
                False

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        return len(pitchtools.PitchClassSet(self)) < len(self)

    def index(self, item):
        r'''Gets index of `item` in segment.

        ..  container:: example

            Example segment:
        
            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Gets index of first item in segment:
        
            ::

                >>> segment.index(-2)
                0

        ..  container:: example

            Gets index of second item in segment:

            ::
                
                >>> segment.index(-1.5)
                1

        ..  container:: example

            Returns nonnegative integer:

            ::
                
                >>> isinstance(segment.index(-1.5), int)
                True

        '''
        superclass = super(PitchClassSegment, self)
        return superclass.index(item)

    def invert(self, axis=None):
        r'''Inverts segment.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> J = pitchtools.PitchClassSegment(items=items, name='J')
                >>> J
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='J')

            ::

                >>> show(J) # doctest: +SKIP

        ..  container:: example

            Inverts segment:

            ::

                >>> segment = J.invert()
                >>> segment
                PitchClassSegment([2, 1.5, 6, 5, 1.5, 5], name='I(J)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    d'8
                        ^ \markup {
                            \concat
                                {
                                    I
                                    \concat
                                        {
                                            \hspace
                                                #0.4
                                            \bold
                                                J
                                        }
                                }
                            }
                    dqf'8
                    fs'8
                    f'8
                    dqf'8
                    f'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Inverts inversion of segment:

            ::

                >>> segment = J.invert().invert()
                >>> segment
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='I(I(J))')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    bf'8
                        ^ \markup {
                            \concat
                                {
                                    I
                                    \concat
                                        {
                                            I
                                            \concat
                                                {
                                                    \hspace
                                                        #0.4
                                                    \bold
                                                        J
                                                }
                                        }
                                }
                            }
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

                >>> segment == J
                True

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> isinstance(segment, pitchtools.PitchClassSegment)
                True

        '''
        items = (pc.invert(axis=axis) for pc in self)
        markup_expression = expressiontools.Expression()
        markup_expression = markup_expression.make_callback(
            'Markup({})',
            )
        if axis is None:
            string_expression = 'I({})'
            template = "Markup.concat(['I', {}])"
        else:
            string_expression = 'I{}({{}})'
            string_expression = string_expression.format(axis)
            template = "Markup.concat(['I', Markup({}).sub() {{}}])"
            template = template.format(axis)
        markup_expression = markup_expression.make_callback(template)
        segment = new(self, items=items, name=self._name)
        expressiontools.Expression._track_expression(
            self,
            segment,
            'invert',
            markup_expression=markup_expression,
            string_expression=string_expression,
            )
        return segment

    def make_notes(self, n=None, written_duration=None):
        r'''Makes first `n` notes in segment.

        ..  container:: example

            Example segment:

            ::

                >>> items = [2, 4.5, 6, 11, 4.5, 10]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Makes eighth notes:

            ::

                >>> notes = segment.make_notes()
                >>> staff = Staff(notes)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    d'8
                    eqs'8
                    fs'8
                    b'8
                    eqs'8
                    bf'8
                }

        ..  container:: example

            Makes notes with nonassignable durations:

            ::

                >>> notes = segment.make_notes(4, Duration(5, 16))
                >>> staff = Staff(notes)
                >>> time_signature = TimeSignature((5, 4))
                >>> attach(time_signature, staff)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \time 5/4
                    d'4 ~
                    d'16
                    eqs'4 ~
                    eqs'16
                    fs'4 ~
                    fs'16
                    b'4 ~
                    b'16
                }

        Interprets none-valued `n` equal to length of segment.

        Interprets none-valued `written_duration` equal to 1/8.

        ..  container:: example

            Returns selection:

            ::

                >>> isinstance(segment.make_notes(), selectiontools.Selection)
                True

        '''
        from abjad.tools import scoretools
        from abjad.tools import pitchtools
        n = n or len(self)
        written_duration = written_duration or durationtools.Duration(1, 8)
        result = scoretools.make_notes([0] * n, [written_duration])
        for i, logical_tie in enumerate(iterate(result).by_logical_tie()):
            pitch_class = pitchtools.NamedPitchClass(self[i % len(self)])
            pitch = pitchtools.NamedPitch(pitch_class, 4)
            for note in logical_tie:
                note.written_pitch = pitch
        return result

    def multiply(self, n=1):
        r'''Multiplies pitch-classes in segment by `n`.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> J = pitchtools.PitchClassSegment(items=items, name='J')
                >>> J
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='J')

            ::

                >>> show(J) # doctest: +SKIP

        ..  container:: example

            Multiplies pitch-classes in segment by 1:

            ::

                >>> segment = J.multiply(n=1)
                >>> segment
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='M1(J)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    bf'8
                        ^ \markup {
                            \concat
                                {
                                    M
                                    \sub
                                        1
                                    \concat
                                        {
                                            \hspace
                                                #0.4
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
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies pitch-classes in segment by 5:

            ::

                >>> segment = J.multiply(n=5)
                >>> segment
                PitchClassSegment([2, 4.5, 6, 11, 4.5, 11], name='M5(J)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    d'8
                        ^ \markup {
                            \concat
                                {
                                    M
                                    \sub
                                        5
                                    \concat
                                        {
                                            \hspace
                                                #0.4
                                            \bold
                                                J
                                        }
                                }
                            }
                    eqs'8
                    fs'8
                    b'8
                    eqs'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies pitch-classes in segment by 7:

            ::

                >>> segment = J.multiply(n=7)
                >>> segment
                PitchClassSegment([10, 1.5, 6, 1, 1.5, 1], name='M7(J)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    bf'8
                        ^ \markup {
                            \concat
                                {
                                    M
                                    \sub
                                        7
                                    \concat
                                        {
                                            \hspace
                                                #0.4
                                            \bold
                                                J
                                        }
                                }
                            }
                    dqf'8
                    fs'8
                    cs'8
                    dqf'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies pitch-classes in segment by 11:

            ::

                >>> segment = J.multiply(n=11)
                >>> segment
                PitchClassSegment([2, 7.5, 6, 5, 7.5, 5], name='M11(J)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    d'8
                        ^ \markup {
                            \concat
                                {
                                    M
                                    \sub
                                        11
                                    \concat
                                        {
                                            \hspace
                                                #0.4
                                            \bold
                                                J
                                        }
                                }
                            }
                    gqs'8
                    fs'8
                    f'8
                    gqs'8
                    f'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> isinstance(segment, pitchtools.PitchClassSegment)
                True

        '''
        from abjad.tools import pitchtools
        items = [
            pitchtools.NumberedPitchClass(pc).multiply(n)
            for pc in self
            ]

        string_expression = 'M{n}({{}})'
        string_expression = string_expression.format(n=n)
        markup_expression = expressiontools.Expression()
        markup_expression = markup_expression.make_callback(
            'Markup({})',
            )
        template = "Markup.concat(['M', Markup({n}).sub(), {{}}])"
        template = template.format(n=n)
        markup_expression = markup_expression.make_callback(template)
        segment = new(self, items=items, name=self._name)
        expressiontools.Expression._track_expression(
            self,
            segment,
            'multiply',
            markup_expression=markup_expression,
            string_expression=string_expression,
            )
        return segment

    def retrograde(self):
        r'''Gets retrograde of segment.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> J = pitchtools.PitchClassSegment(items=items, name='J')
                >>> J
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='J')

            ::

                >>> show(J) # doctest: +SKIP

        ..  container:: example

            Gets retrograde of segment:

            ::

                >>> segment = J.retrograde()
                >>> segment
                PitchClassSegment([7, 10.5, 7, 6, 10.5, 10], name='R(J)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    g'8
                        ^ \markup {
                            \concat
                                {
                                    R
                                    \concat
                                        {
                                            \hspace
                                                #0.4
                                            \bold
                                                J
                                        }
                                }
                            }
                    bqf'8
                    g'8
                    fs'8
                    bqf'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets retrograde of retrograde of segment:

            ::

                >>> segment = J.retrograde().retrograde()
                >>> segment
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='R(R(J))')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    bf'8
                        ^ \markup {
                            \concat
                                {
                                    R
                                    \concat
                                        {
                                            R
                                            \concat
                                                {
                                                    \hspace
                                                        #0.4
                                                    \bold
                                                        J
                                                }
                                        }
                                }
                            }
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

                >>> segment == J
                True

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> isinstance(segment, pitchtools.PitchClassSegment)
                True

        '''
        items = reversed(self)
        string_expression = 'R({})'
        markup_expression = expressiontools.Expression()
        markup_expression = markup_expression.make_callback(
            'Markup({})',
            )
        markup_expression = markup_expression.make_callback(
            "Markup.concat(['R', {}])",
            )
        segment = new(self, items=items, name=self._name)
        expressiontools.Expression._track_expression(
            self,
            segment,
            'retrograde',
            markup_expression=markup_expression,
            string_expression=string_expression,
            )
        return segment

    def rotate(self, n=0, stravinsky=False):
        r'''Rotates segment.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> J = pitchtools.PitchClassSegment(items=items, name='J')
                >>> J
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='J')

            ::

                >>> show(J) # doctest: +SKIP

        ..  container:: example

            Rotates segment to the right:

            ::

                >>> segment = J.rotate(n=1)
                >>> segment
                PitchClassSegment([7, 10, 10.5, 6, 7, 10.5], name='r1(J)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    g'8
                        ^ \markup {
                            \concat
                                {
                                    r
                                    \hspace
                                        #-0.2
                                    \sub
                                        1
                                    \concat
                                        {
                                            \hspace
                                                #0.4
                                            \bold
                                                J
                                        }
                                }
                            }
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Rotates segment to the left:

            ::

                >>> segment = J.rotate(n=-1)
                >>> segment
                PitchClassSegment([10.5, 6, 7, 10.5, 7, 10], name='r-1(J)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    bqf'8
                        ^ \markup {
                            \concat
                                {
                                    r
                                    \hspace
                                        #-0.7
                                    \sub
                                        -1
                                    \concat
                                        {
                                            \hspace
                                                #0.4
                                            \bold
                                                J
                                        }
                                }
                            }
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Rotates segment by zero:

            ::

                >>> segment = J.rotate(n=0)
                >>> segment
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='r0(J)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    bf'8
                        ^ \markup {
                            \concat
                                {
                                    r
                                    \hspace
                                        #-0.2
                                    \sub
                                        0
                                    \concat
                                        {
                                            \hspace
                                                #0.4
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
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

                >>> segment == J
                True

        ..  container:: example

            Stravinsky-style rotation back-transposes segment to
            begin at zero:

            ::

                >>> segment = J.rotate(n=1, stravinsky=True)
                >>> segment
                PitchClassSegment([0, 3, 3.5, 11, 0, 3.5], name='rs1(J)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    c'8
                        ^ \markup {
                            \concat
                                {
                                    rs
                                    \hspace
                                        #-0.2
                                    \sub
                                        1
                                    \concat
                                        {
                                            \hspace
                                                #0.4
                                            \bold
                                                J
                                        }
                                }
                            }
                    ef'8
                    eqf'8
                    b'8
                    c'8
                    eqf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> isinstance(segment, pitchtools.PitchClassSegment)
                True

        '''
        original_n = n
        items = sequencetools.rotate_sequence(self._collection, n)
        if stravinsky:
            n = 0 - float(items[0])
            segment = new(self, items=items)
            segment = segment.transpose(n=n)
            items = segment.items[:]
        if stravinsky:
            abbreviation = 'rs'
        else:
            abbreviation = 'r'
        string_expression = '{abbreviation}{n}({{}})'
        string_expression = string_expression.format(
            abbreviation=abbreviation,
            n=original_n,
            )
        markup_expression = expressiontools.Expression()
        markup_expression = markup_expression.make_callback('Markup({})')
        if 0 <= original_n:
            hspace = 'Markup.hspace(-0.2)'
        else:
            hspace = 'Markup.hspace(-0.7)'
        subscript = 'Markup({n}).sub()'
        subscript = subscript.format(n=original_n)
        template = \
            "Markup.concat([{abbreviation!r}, {hspace}, {subscript}, {{}}])"
        template = template.format(
            abbreviation=abbreviation,
            hspace=hspace,
            subscript=subscript,
            )
        markup_expression = markup_expression.make_callback(template)
        segment = new(self, items=items, name=self._name)
        expressiontools.Expression._track_expression(
            self,
            segment,
            'rotate',
            markup_expression=markup_expression,
            string_expression=string_expression,
            )
        return segment

    def transpose(self, n=0):
        r'''Transposes segment by index `n`.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> J = pitchtools.PitchClassSegment(items=items, name='J')
                >>> J
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='J')

            ::

                >>> show(J) # doctest: +SKIP

        ..  container:: example

            Transposes segment by positive index:

            ::

                >>> segment = J.transpose(n=13)
                >>> segment
                PitchClassSegment([11, 11.5, 7, 8, 11.5, 8], name='T13(J)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    b'8
                        ^ \markup {
                            \concat
                                {
                                    T
                                    \hspace
                                        #-0.2
                                    \sub
                                        13
                                    \concat
                                        {
                                            \hspace
                                                #0.4
                                            \bold
                                                J
                                        }
                                }
                            }
                    bqs'8
                    g'8
                    af'8
                    bqs'8
                    af'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes segment by negative index:

            ::

                >>> segment = J.transpose(n=-13)
                >>> segment
                PitchClassSegment([9, 9.5, 5, 6, 9.5, 6], name='T-13(J)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    a'8
                        ^ \markup {
                            \concat
                                {
                                    T
                                    \hspace
                                        #-0.7
                                    \sub
                                        -13
                                    \concat
                                        {
                                            \hspace
                                                #0.4
                                            \bold
                                                J
                                        }
                                }
                            }
                    aqs'8
                    f'8
                    fs'8
                    aqs'8
                    fs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes segment by zero index:

            ::

                >>> segment = J.transpose(n=0)
                >>> segment
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='T0(J)')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    bf'8
                        ^ \markup {
                            \concat
                                {
                                    T
                                    \hspace
                                        #-0.2
                                    \sub
                                        0
                                    \concat
                                        {
                                            \hspace
                                                #0.4
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
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

                >>> segment == J
                True

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> isinstance(segment, pitchtools.PitchClassSegment)
                True

        '''
        items = (pitch_class.transpose(n=n) for pitch_class in self)
        string_expression = 'T{n}({{}})'
        string_expression = string_expression.format(n=n)
        markup_expression = expressiontools.Expression()
        markup_expression = markup_expression.make_callback(
            'Markup({})',
            )
        if 0 <= n:
            hspace = 'Markup.hspace(-0.2)'
        else:
            hspace = 'Markup.hspace(-0.7)'
        subscript = 'Markup({n}).sub()'
        subscript = subscript.format(n=n)
        template = "Markup.concat(['T', {hspace}, {subscript}, {{}}])"
        template = template.format(hspace=hspace, subscript=subscript) 
        markup_expression = markup_expression.make_callback(template)
        segment = new(self, items=items, name=self._name)
        expressiontools.Expression._track_expression(
            self,
            segment,
            'transpose',
            markup_expression=markup_expression,
            string_expression=string_expression,
            )
        return segment

    def voice_horizontally(self, initial_octave=4):
        r'''Voices segment with each pitch as close to the previous pitch as
        possible.

        ..  todo:: Should be implemented somewhere else.

        ..  container:: example

            Voices horizontally:

            ::

                >>> items = "c b d e f g e b a c"
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            ::

                >>> voiced_segment = segment.voice_horizontally()
                >>> show(voiced_segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = voiced_segment.__illustrate__()
                >>> f(lilypond_file[Score])
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "treble" {
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
                        \context Staff = "bass" {
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

            ::

                >>> voiced_segment
                PitchSegment(["c'", 'b', "d'", "e'", "f'", "g'", "e'", 'b', 'a', "c'"])

        '''
        from abjad.tools import pitchtools
        initial_octave = pitchtools.Octave(initial_octave)
        pitches = []
        if self:
            pitch_class = pitchtools.NamedPitchClass(self[0])
            pitch = pitchtools.NamedPitch(pitch_class, initial_octave)
            pitches.append(pitch)
            for pitch_class in self[1:]:
                pitch_class = pitchtools.NamedPitchClass(pitch_class)
                pitch = pitchtools.NamedPitch(pitch_class, initial_octave)
                semitones = abs((pitch - pitches[-1]).semitones)
                while 6 < semitones:
                    if pitch < pitches[-1]:
                        pitch += 12
                    else:
                        pitch -= 12
                    semitones = abs((pitch - pitches[-1]).semitones)
                pitches.append(pitch)
        if self.item_class is pitchtools.NamedPitchClass:
            item_class = pitchtools.NamedPitch
        else:
            item_class = pitchtools.NumberedPitch
        return pitchtools.PitchSegment(
            items=pitches,
            item_class=item_class,
            )

    def voice_vertically(self, initial_octave=4):
        r'''Voices segment with each pitch higher than the previous.

        ..  todo:: Should be implemented somewhere else.

        ..  container:: example

            Voices vertically:

            ::

                >>> scale_degree_numbers = [1, 3, 5, 7, 9, 11, 13]
                >>> scale = tonalanalysistools.Scale('c', 'minor')
                >>> segment = pitchtools.PitchClassSegment((
                ...     scale.scale_degree_to_named_pitch_class(x)
                ...     for x in scale_degree_numbers))
                >>> show(segment) # doctest: +SKIP

            ::

                >>> voiced_segment = segment.voice_vertically()
                >>> show(voiced_segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = voiced_segment.__illustrate__()
                >>> f(lilypond_file[Score])
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "treble" {
                            \clef "treble"
                            c'1 * 1/8
                            ef'1 * 1/8
                            g'1 * 1/8
                            bf'1 * 1/8
                            d''1 * 1/8
                            f''1 * 1/8
                            af''1 * 1/8
                        }
                        \context Staff = "bass" {
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

            ::

                >>> voiced_segment
                PitchSegment(["c'", "ef'", "g'", "bf'", "d''", "f''", "af''"])

        '''
        from abjad.tools import pitchtools
        initial_octave = pitchtools.Octave(initial_octave)
        pitches = []
        if self:
            pitch_class = pitchtools.NamedPitchClass(self[0])
            pitch = pitchtools.NamedPitch(pitch_class, initial_octave)
            pitches.append(pitch)
            for pitch_class in self[1:]:
                pitch_class = pitchtools.NamedPitchClass(pitch_class)
                pitch = pitchtools.NamedPitch(pitch_class, initial_octave)
                while pitch < pitches[-1]:
                    pitch += 12
                pitches.append(pitch)
        if self.item_class is pitchtools.NamedPitchClass:
            item_class = pitchtools.NamedPitch
        else:
            item_class = pitchtools.NumberedPitch
        return pitchtools.PitchSegment(
            items=pitches,
            item_class=item_class,
            )
