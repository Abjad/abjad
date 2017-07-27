# -*- coding: utf-8 -*-
import inspect
from abjad.tools import abctools
from abjad.tools import markuptools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import new


class LabelAgent(abctools.AbjadObject):
    r'''Label agent.

    ::

        >>> import abjad

    ..  container:: example

        Labels pitch names:

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
                >>> abjad.label(staff).with_pitches()

            ::

                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'4
                        ^ \markup {
                            \small
                                c'
                            }
                    e'4
                        ^ \markup {
                            \small
                                e'
                            }
                    d'4
                        ^ \markup {
                            \small
                                d'
                            }
                    f'4
                        ^ \markup {
                            \small
                                f'
                            }
                }

        ..  container:: example expression

            ::

                >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
                >>> expression = abjad.label().with_pitches()
                >>> f(expression)
                abjad.Expression(
                    callbacks=[
                        abjad.Expression(
                            evaluation_template='abjad.LabelAgent',
                            is_initializer=True,
                            ),
                        abjad.Expression(
                            evaluation_template='{}.with_pitches()',
                            qualified_method_name='abjad.LabelAgent.with_pitches',
                            ),
                        ],
                    proxy_class=agenttools.LabelAgent,
                    )

            ::

                >>> expression(staff)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'4
                        ^ \markup {
                            \small
                                c'
                            }
                    e'4
                        ^ \markup {
                            \small
                                e'
                            }
                    d'4
                        ^ \markup {
                            \small
                                d'
                            }
                    f'4
                        ^ \markup {
                            \small
                                f'
                            }
                }

    ..  container:: example

        Labels durations:

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
                >>> abjad.label(staff).with_durations()

            ::

                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'4
                        ^ \markup {
                            \small
                                1/4
                            }
                    e'4
                        ^ \markup {
                            \small
                                1/4
                            }
                    d'4
                        ^ \markup {
                            \small
                                1/4
                            }
                    f'4
                        ^ \markup {
                            \small
                                1/4
                            }
                }

        ..  container:: example expression

            ::

                >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
                >>> expression = abjad.label().with_durations()
                >>> f(expression)
                abjad.Expression(
                    callbacks=[
                        abjad.Expression(
                            evaluation_template='abjad.LabelAgent',
                            is_initializer=True,
                            ),
                        abjad.Expression(
                            evaluation_template='{}.with_durations()',
                            qualified_method_name='abjad.LabelAgent.with_durations',
                            ),
                        ],
                    proxy_class=agenttools.LabelAgent,
                    )

            ::

                >>> expression(staff)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'4
                        ^ \markup {
                            \small
                                1/4
                            }
                    e'4
                        ^ \markup {
                            \small
                                1/4
                            }
                    d'4
                        ^ \markup {
                            \small
                                1/4
                            }
                    f'4
                        ^ \markup {
                            \small
                                1/4
                            }
                }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        '_expression',
        )

    _pc_number_to_color = {
        0: schemetools.SchemeColor('red'),
        1: schemetools.SchemeColor('MediumBlue'),
        2: schemetools.SchemeColor('orange'),
        3: schemetools.SchemeColor('LightSlateBlue'),
        4: schemetools.SchemeColor('ForestGreen'),
        5: schemetools.SchemeColor('MediumOrchid'),
        6: schemetools.SchemeColor('firebrick'),
        7: schemetools.SchemeColor('DeepPink'),
        8: schemetools.SchemeColor('DarkOrange'),
        9: schemetools.SchemeColor('IndianRed'),
        10: schemetools.SchemeColor('CadetBlue'),
        11: schemetools.SchemeColor('SeaGreen'),
        12: schemetools.SchemeColor('LimeGreen'),
        }

    ### INITIALIZER ###

    def __init__(self, client=None):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        from abjad.tools import spannertools
        prototype = (
            scoretools.Component,
            selectiontools.Selection,
            spannertools.Spanner,
            list,
            type(None),
            )
        if not isinstance(client, prototype):
            message = 'must be component, selection, spanner, list or none:'
            message += ' {!r}.'
            message = message.format(client)
            raise TypeError(message)
        self._client = client
        self._expression = None

    ### PRIVATE METHODS ###

    def _color_leaf(self, leaf, color):
        if isinstance(leaf, (scoretools.Note, scoretools.Chord)):
            override(leaf).accidental.color = color
            override(leaf).beam.color = color
            override(leaf).dots.color = color
            override(leaf).note_head.color = color
            override(leaf).stem.color = color
        elif isinstance(leaf, scoretools.Rest):
            override(leaf).dots.color = color
            override(leaf).rest.color = color
        return leaf

    def _update_expression(self, frame):
        import abjad
        callback = abjad.Expression._frame_to_callback(frame)
        return self._expression.append_callback(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Gets client of label agent.

        Returns component, selection, spanner or none.
        '''
        return self._client

    ### PUBLIC METHODS ###

    def color_alternating(self, colors=['red', 'blue']):
        r'''Colors client items in alternating `colors`.

        Returns none.
        '''
        import abjad
        colors = abjad.CyclicTuple(colors)
        if isinstance(self._client, abjad.Component):
            target = [self._client]
        elif isinstance(self._client, abjad.selectiontools.LogicalTie):
            target = [self._client]
        elif isinstance(self._client, abjad.Selection):
            target = self._client
        else:
            raise TypeError(self._client)
        for i, item in enumerate(target):
            color = colors[i]
            abjad.label(item).color_leaves(color=color)

    def color_container(self, color='red'):
        r'''Colors contents of `container`.

        ..  container:: example

            Colors measure:

            ..  container:: example

                ::

                    >>> measure = abjad.Measure((2, 8), "c'8 d'8")
                    >>> abjad.label(measure).color_container('red')
                    >>> show(measure) # doctest: +SKIP

                ..  docs::

                    >>> f(measure)
                    {
                        \override Accidental.color = #red
                        \override Beam.color = #red
                        \override Dots.color = #red
                        \override NoteHead.color = #red
                        \override Rest.color = #red
                        \override Stem.color = #red
                        \override TupletBracket.color = #red
                        \override TupletNumber.color = #red
                        \time 2/8
                        c'8
                        d'8
                        \revert Accidental.color
                        \revert Beam.color
                        \revert Dots.color
                        \revert NoteHead.color
                        \revert Rest.color
                        \revert Stem.color
                        \revert TupletBracket.color
                        \revert TupletNumber.color
                    }

            ..  container:: example expression

                ::

                    >>> measure = abjad.Measure((2, 8), "c'8 d'8")
                    >>> expression = abjad.label().color_container('red')
                    >>> expression(measure)
                    >>> show(measure) # doctest: +SKIP

                ..  docs::

                    >>> f(measure)
                    {
                        \override Accidental.color = #red
                        \override Beam.color = #red
                        \override Dots.color = #red
                        \override NoteHead.color = #red
                        \override Rest.color = #red
                        \override Stem.color = #red
                        \override TupletBracket.color = #red
                        \override TupletNumber.color = #red
                        \time 2/8
                        c'8
                        d'8
                        \revert Accidental.color
                        \revert Beam.color
                        \revert Dots.color
                        \revert NoteHead.color
                        \revert Rest.color
                        \revert Stem.color
                        \revert TupletBracket.color
                        \revert TupletNumber.color
                    }

        Returns none.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        override(self.client).accidental.color = color
        override(self.client).beam.color = color
        override(self.client).dots.color = color
        override(self.client).note_head.color = color
        override(self.client).rest.color = color
        override(self.client).stem.color = color
        override(self.client).tuplet_bracket.color = color
        override(self.client).tuplet_number.color = color

    def color_leaves(self, color='red'):
        r"""Colors leaves.

        ..  container:: example

            Colors leaves red:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("cs'8. [ r8. s8. <c' cs' a'>8. ]")
                    >>> abjad.label(staff).color_leaves('red')
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        cs'8. [
                        \once \override Dots.color = #red
                        \once \override Rest.color = #red
                        r8.
                        s8.
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        <c' cs' a'>8. ]
                    }

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff("cs'8. [ r8. s8. <c' cs' a'>8. ]")
                    >>> expression = abjad.label().color_leaves('red')
                    >>> expression(staff)
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        cs'8. [
                        \once \override Dots.color = #red
                        \once \override Rest.color = #red
                        r8.
                        s8.
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        <c' cs' a'>8. ]
                    }

        Returns none.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        for leaf in iterate(self.client).by_leaf():
            self._color_leaf(leaf, color)

    def color_note_heads(self, color_map=None):
        r'''Colors note note-heads.

        ..  container:: example

            Colors chord note-heads:

            ..  container:: example

                ::

                    >>> chord = abjad.Chord([12, 14, 18, 21, 23], (1, 4))
                    >>> pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
                    >>> colors = ['red', 'blue', 'green']
                    >>> color_map = abjad.ColorMap(colors, pitches)
                    >>> abjad.label(chord).color_note_heads(color_map)
                    >>> show(chord) # doctest: +SKIP

                ..  docs::

                    >>> f(chord)
                    <
                        \tweak color #red
                        c''
                        \tweak color #red
                        d''
                        \tweak color #green
                        fs''
                        \tweak color #green
                        a''
                        \tweak color #blue
                        b''
                    >4

            ..  container:: example expression

                ::

                    >>> chord = abjad.Chord([12, 14, 18, 21, 23], (1, 4))
                    >>> pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
                    >>> colors = ['red', 'blue', 'green']
                    >>> color_map = abjad.ColorMap(colors, pitches)
                    >>> expression = abjad.label().color_note_heads(color_map)
                    >>> expression(chord)
                    >>> show(chord) # doctest: +SKIP

                ..  docs::

                    >>> f(chord)
                    <
                        \tweak color #red
                        c''
                        \tweak color #red
                        d''
                        \tweak color #green
                        fs''
                        \tweak color #green
                        a''
                        \tweak color #blue
                        b''
                    >4

        ..  container:: example

            Colors note note-head:

            ..  container:: example

                ::

                    >>> note = abjad.Note("c'4")
                    >>> abjad.label(note).color_note_heads(color_map)
                    >>> show(note) # doctest: +SKIP

                ..  docs::

                    >>> f(note)
                    \once \override NoteHead.color = #red
                    c'4

            ..  container:: example expression

                ::

                    >>> note = abjad.Note("c'4")
                    >>> expression = abjad.label().color_note_heads(color_map)
                    >>> expression(note)
                    >>> show(note) # doctest: +SKIP

                ..  docs::

                    >>> f(note)
                    \once \override NoteHead.color = #red
                    c'4

        ..  container:: example

            Colors nothing:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff()
                    >>> abjad.label(staff).color_note_heads(color_map)

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff()
                    >>> expression = abjad.label().color_note_heads(color_map)
                    >>> expression(staff)

        ..  container:: example

            Colors note-heads:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("c'8 cs'8 d'8 ds'8 e'8 f'8 fs'8 g'8 gs'8 a'8 as'8 b'8 c''8")
                    >>> abjad.label(staff).color_note_heads()
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        \once \override NoteHead.color = #(x11-color 'red)
                        c'8
                        \once \override NoteHead.color = #(x11-color 'MediumBlue)
                        cs'8
                        \once \override NoteHead.color = #(x11-color 'orange)
                        d'8
                        \once \override NoteHead.color = #(x11-color 'LightSlateBlue)
                        ds'8
                        \once \override NoteHead.color = #(x11-color 'ForestGreen)
                        e'8
                        \once \override NoteHead.color = #(x11-color 'MediumOrchid)
                        f'8
                        \once \override NoteHead.color = #(x11-color 'firebrick)
                        fs'8
                        \once \override NoteHead.color = #(x11-color 'DeepPink)
                        g'8
                        \once \override NoteHead.color = #(x11-color 'DarkOrange)
                        gs'8
                        \once \override NoteHead.color = #(x11-color 'IndianRed)
                        a'8
                        \once \override NoteHead.color = #(x11-color 'CadetBlue)
                        as'8
                        \once \override NoteHead.color = #(x11-color 'SeaGreen)
                        b'8
                        \once \override NoteHead.color = #(x11-color 'red)
                        c''8
                    }

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff("c'8 cs'8 d'8 ds'8 e'8 f'8 fs'8 g'8 gs'8 a'8 as'8 b'8 c''8")
                    >>> expression = abjad.label().color_note_heads()
                    >>> expression(staff)
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        \once \override NoteHead.color = #(x11-color 'red)
                        c'8
                        \once \override NoteHead.color = #(x11-color 'MediumBlue)
                        cs'8
                        \once \override NoteHead.color = #(x11-color 'orange)
                        d'8
                        \once \override NoteHead.color = #(x11-color 'LightSlateBlue)
                        ds'8
                        \once \override NoteHead.color = #(x11-color 'ForestGreen)
                        e'8
                        \once \override NoteHead.color = #(x11-color 'MediumOrchid)
                        f'8
                        \once \override NoteHead.color = #(x11-color 'firebrick)
                        fs'8
                        \once \override NoteHead.color = #(x11-color 'DeepPink)
                        g'8
                        \once \override NoteHead.color = #(x11-color 'DarkOrange)
                        gs'8
                        \once \override NoteHead.color = #(x11-color 'IndianRed)
                        a'8
                        \once \override NoteHead.color = #(x11-color 'CadetBlue)
                        as'8
                        \once \override NoteHead.color = #(x11-color 'SeaGreen)
                        b'8
                        \once \override NoteHead.color = #(x11-color 'red)
                        c''8
                    }

        Returns none.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        color_map = color_map or self._pc_number_to_color
        for leaf in iterate(self.client).by_leaf():
            if isinstance(leaf, scoretools.Chord):
                for note_head in leaf.note_heads:
                    number = note_head.written_pitch.number
                    pc = abjad.NumberedPitchClass(number)
                    color = color_map.get(pc, None)
                    if color is not None:
                        note_head.tweak.color = color
            elif isinstance(leaf, scoretools.Note):
                note_head = leaf.note_head
                number = note_head.written_pitch.number
                pc = abjad.NumberedPitchClass(number)
                color = color_map[pc.number]
                if color is not None:
                    override(leaf).note_head.color = color

    def remove_markup(self):
        r'''Removes markup from leaves.

        ..  container:: example

            Removes markup:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                    >>> abjad.label(staff).with_pitches()
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        c'8
                            ^ \markup {
                                \small
                                    c'
                                }
                        d'8
                            ^ \markup {
                                \small
                                    d'
                                }
                        e'8
                            ^ \markup {
                                \small
                                    e'
                                }
                        f'8
                            ^ \markup {
                                \small
                                    f'
                                }
                    }

                ::

                    >>> abjad.label(staff).remove_markup()
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        c'8
                        d'8
                        e'8
                        f'8
                    }

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                    >>> expression = abjad.label().with_pitches()
                    >>> expression(staff)
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        c'8
                            ^ \markup {
                                \small
                                    c'
                                }
                        d'8
                            ^ \markup {
                                \small
                                    d'
                                }
                        e'8
                            ^ \markup {
                                \small
                                    e'
                                }
                        f'8
                            ^ \markup {
                                \small
                                    f'
                                }
                    }

                ::

                    >>> expression = abjad.label().remove_markup()
                    >>> expression(staff)
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        c'8
                        d'8
                        e'8
                        f'8
                    }

        Returns none.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        leaves = iterate(self.client).by_leaf()
        for leaf in leaves:
            detach(markuptools.Markup, leaf)

    def vertical_moments(self, direction=Up, prototype=None):
        r'''Labels vertical moments.

        ..  container:: example

            Labels indices:

            ..  container:: example

                ::

                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                    >>> staff_group.append(staff)
                    >>> abjad.label(staff_group).vertical_moments()
                    >>> show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> f(staff_group)
                    \new StaffGroup <<
                        \new Staff {
                            c'8
                                ^ \markup {
                                    \tiny
                                        0
                                    }
                            d'4
                                ^ \markup {
                                    \tiny
                                        1
                                    }
                            e'16
                                ^ \markup {
                                    \tiny
                                        3
                                    }
                            f'16
                                ^ \markup {
                                    \tiny
                                        4
                                    }
                        }
                        \new Staff {
                            \clef "alto"
                            g4
                            f4
                                ^ \markup {
                                    \tiny
                                        2
                                    }
                        }
                        \new Staff {
                            \clef "bass"
                            c,2
                        }
                    >>

            ..  container:: example expression

                ::

                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                    >>> staff_group.append(staff)
                    >>> expression = abjad.label().vertical_moments()
                    >>> expression(staff_group)
                    >>> show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> f(staff_group)
                    \new StaffGroup <<
                        \new Staff {
                            c'8
                                ^ \markup {
                                    \tiny
                                        0
                                    }
                            d'4
                                ^ \markup {
                                    \tiny
                                        1
                                    }
                            e'16
                                ^ \markup {
                                    \tiny
                                        3
                                    }
                            f'16
                                ^ \markup {
                                    \tiny
                                        4
                                    }
                        }
                        \new Staff {
                            \clef "alto"
                            g4
                            f4
                                ^ \markup {
                                    \tiny
                                        2
                                    }
                        }
                        \new Staff {
                            \clef "bass"
                            c,2
                        }
                    >>

        ..  container:: example

            Labels pitch numbers:

            ..  container:: example

                ::

                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                    >>> staff_group.append(staff)
                    >>> abjad.label(staff_group).vertical_moments(
                    ...     prototype=abjad.NumberedPitch,
                    ...     )
                    >>> show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> f(staff_group)
                    \new StaffGroup <<
                        \new Staff {
                            c'8
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                0
                                                -5
                                                -24
                                            }
                                    }
                            d'4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                2
                                                -5
                                                -24
                                            }
                                    }
                            e'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                4
                                                -7
                                                -24
                                            }
                                    }
                            f'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                5
                                                -7
                                                -24
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "alto"
                            g4
                            f4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                2
                                                -7
                                                -24
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "bass"
                            c,2
                        }
                    >>

            ..  container:: example expression

                ::

                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                    >>> staff_group.append(staff)
                    >>> prototype = abjad.NumberedPitch
                    >>> expression = abjad.label().vertical_moments(prototype=prototype)
                    >>> expression(staff_group)
                    >>> show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> f(staff_group)
                    \new StaffGroup <<
                        \new Staff {
                            c'8
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                0
                                                -5
                                                -24
                                            }
                                    }
                            d'4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                2
                                                -5
                                                -24
                                            }
                                    }
                            e'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                4
                                                -7
                                                -24
                                            }
                                    }
                            f'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                5
                                                -7
                                                -24
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "alto"
                            g4
                            f4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                2
                                                -7
                                                -24
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "bass"
                            c,2
                        }
                    >>

        ..  container:: example

            Labels pitch-class numbers:

            ..  container:: example

                ::

                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                    >>> staff_group.append(staff)
                    >>> prototype = abjad.NumberedPitchClass
                    >>> abjad.label(staff_group).vertical_moments(prototype=prototype)
                    >>> show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> f(staff_group)
                    \new StaffGroup <<
                        \new Staff {
                            c'8
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                7
                                                0
                                            }
                                    }
                            d'4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                7
                                                2
                                                0
                                            }
                                    }
                            e'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                5
                                                4
                                                0
                                            }
                                    }
                            f'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                5
                                                0
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "alto"
                            g4
                            f4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                5
                                                2
                                                0
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "bass"
                            c,2
                        }
                    >>

            ..  container:: example expression

                ::

                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                    >>> staff_group.append(staff)
                    >>> prototype = abjad.NumberedPitchClass
                    >>> expression = abjad.label().vertical_moments(prototype=prototype)
                    >>> expression(staff_group)
                    >>> show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> f(staff_group)
                    \new StaffGroup <<
                        \new Staff {
                            c'8
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                7
                                                0
                                            }
                                    }
                            d'4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                7
                                                2
                                                0
                                            }
                                    }
                            e'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                5
                                                4
                                                0
                                            }
                                    }
                            f'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                5
                                                0
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "alto"
                            g4
                            f4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                5
                                                2
                                                0
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "bass"
                            c,2
                        }
                    >>

        ..  container:: example

            Labels interval numbers:

            ..  container:: example

                ::

                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                    >>> staff_group.append(staff)
                    >>> prototype = abjad.NumberedInterval
                    >>> abjad.label(staff_group).vertical_moments(prototype=prototype)
                    >>> show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> f(staff_group)
                    \new StaffGroup <<
                        \new Staff {
                            c'8
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                15
                                                12
                                            }
                                    }
                            d'4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                16
                                                12
                                            }
                                    }
                            e'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                17
                                                11
                                            }
                                    }
                            f'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                18
                                                11
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "alto"
                            g4
                            f4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                16
                                                11
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "bass"
                            c,2
                        }
                    >>

            ..  container:: example expression

                ::

                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                    >>> staff_group.append(staff)
                    >>> prototype = abjad.NumberedInterval
                    >>> expression = abjad.label().vertical_moments(prototype=prototype)
                    >>> expression(staff_group)
                    >>> show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> f(staff_group)
                    \new StaffGroup <<
                        \new Staff {
                            c'8
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                15
                                                12
                                            }
                                    }
                            d'4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                16
                                                12
                                            }
                                    }
                            e'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                17
                                                11
                                            }
                                    }
                            f'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                18
                                                11
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "alto"
                            g4
                            f4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                16
                                                11
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "bass"
                            c,2
                        }
                    >>

        ..  container:: example

            Labels interval-class numbers:

            ..  container:: example

                ::

                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                    >>> staff_group.append(staff)
                    >>> prototype = abjad.NumberedIntervalClass
                    >>> abjad.label(staff_group).vertical_moments(prototype=prototype)
                    >>> show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> f(staff_group)
                    \new StaffGroup <<
                        \new Staff {
                            c'8
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                12
                                                7
                                            }
                                    }
                            d'4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                2
                                                7
                                            }
                                    }
                            e'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                4
                                                5
                                            }
                                    }
                            f'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                5
                                                5
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "alto"
                            g4
                            f4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                2
                                                5
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "bass"
                            c,2
                        }
                    >>

            ..  container:: example expression

                ::

                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                    >>> staff_group.append(staff)
                    >>> prototype = abjad.NumberedIntervalClass
                    >>> expression = abjad.label().vertical_moments(prototype=prototype)
                    >>> expression(staff_group)
                    >>> show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> f(staff_group)
                    \new StaffGroup <<
                        \new Staff {
                            c'8
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                12
                                                7
                                            }
                                    }
                            d'4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                2
                                                7
                                            }
                                    }
                            e'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                4
                                                5
                                            }
                                    }
                            f'16
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                5
                                                5
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "alto"
                            g4
                            f4
                                ^ \markup {
                                    \tiny
                                        \column
                                            {
                                                2
                                                5
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "bass"
                            c,2
                        }
                    >>

        ..  container:: example

            Labels interval-class vectors:

            ..  container:: example

                ::

                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                    >>> staff_group.append(staff)
                    >>> prototype = abjad.IntervalClassVector
                    >>> abjad.label(staff_group).vertical_moments(prototype=prototype)
                    >>> show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> f(staff_group)
                    \new StaffGroup <<
                        \new Staff {
                            c'8
                                ^ \markup {
                                    \tiny
                                        \tiny
                                            1000020
                                    }
                            d'4
                                ^ \markup {
                                    \tiny
                                        \tiny
                                            0010020
                                    }
                            e'16
                                ^ \markup {
                                    \tiny
                                        \tiny
                                            0100110
                                    }
                            f'16
                                ^ \markup {
                                    \tiny
                                        \tiny
                                            1000020
                                    }
                        }
                        \new Staff {
                            \clef "alto"
                            g4
                            f4
                                ^ \markup {
                                    \tiny
                                        \tiny
                                            0011010
                                    }
                        }
                        \new Staff {
                            \clef "bass"
                            c,2
                        }
                    >>

            ..  container:: example expression

                ::

                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                    >>> staff_group.append(staff)
                    >>> prototype = abjad.IntervalClassVector
                    >>> expression = abjad.label().vertical_moments(prototype=prototype)
                    >>> expression(staff_group)
                    >>> show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> f(staff_group)
                    \new StaffGroup <<
                        \new Staff {
                            c'8
                                ^ \markup {
                                    \tiny
                                        \tiny
                                            1000020
                                    }
                            d'4
                                ^ \markup {
                                    \tiny
                                        \tiny
                                            0010020
                                    }
                            e'16
                                ^ \markup {
                                    \tiny
                                        \tiny
                                            0100110
                                    }
                            f'16
                                ^ \markup {
                                    \tiny
                                        \tiny
                                            1000020
                                    }
                        }
                        \new Staff {
                            \clef "alto"
                            g4
                            f4
                                ^ \markup {
                                    \tiny
                                        \tiny
                                            0011010
                                    }
                        }
                        \new Staff {
                            \clef "bass"
                            c,2
                        }
                    >>

        ..  container:: example

            Labels set-classes:

            ..  container:: example

                ::

                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                    >>> staff_group.append(staff)
                    >>> prototype = abjad.SetClass()
                    >>> abjad.label(staff_group).vertical_moments(prototype=prototype)
                    >>> show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> f(staff_group)
                    \new StaffGroup <<
                        \new Staff {
                            c'8
                                ^ \markup {
                                    \tiny
                                        \line
                                            {
                                                "SC(2-5){0, 5}"
                                            }
                                    }
                            d'4
                                ^ \markup {
                                    \tiny
                                        \line
                                            {
                                                "SC(3-9){0, 2, 7}"
                                            }
                                    }
                            e'16
                                ^ \markup {
                                    \tiny
                                        \line
                                            {
                                                "SC(3-4){0, 1, 5}"
                                            }
                                    }
                            f'16
                                ^ \markup {
                                    \tiny
                                        \line
                                            {
                                                "SC(2-5){0, 5}"
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "alto"
                            g4
                            f4
                                ^ \markup {
                                    \tiny
                                        \line
                                            {
                                                "SC(3-7){0, 2, 5}"
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "bass"
                            c,2
                        }
                    >>

            ..  container:: example expression

                ::

                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                    >>> staff_group.append(staff)
                    >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                    >>> staff_group.append(staff)
                    >>> prototype = abjad.SetClass()
                    >>> expression = abjad.label().vertical_moments(prototype=prototype)
                    >>> expression(staff_group)
                    >>> show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> f(staff_group)
                    \new StaffGroup <<
                        \new Staff {
                            c'8
                                ^ \markup {
                                    \tiny
                                        \line
                                            {
                                                "SC(2-5){0, 5}"
                                            }
                                    }
                            d'4
                                ^ \markup {
                                    \tiny
                                        \line
                                            {
                                                "SC(3-9){0, 2, 7}"
                                            }
                                    }
                            e'16
                                ^ \markup {
                                    \tiny
                                        \line
                                            {
                                                "SC(3-4){0, 1, 5}"
                                            }
                                    }
                            f'16
                                ^ \markup {
                                    \tiny
                                        \line
                                            {
                                                "SC(2-5){0, 5}"
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "alto"
                            g4
                            f4
                                ^ \markup {
                                    \tiny
                                        \line
                                            {
                                                "SC(3-7){0, 2, 5}"
                                            }
                                    }
                        }
                        \new Staff {
                            \clef "bass"
                            c,2
                        }
                    >>

        Set `prototype` to one of the classes shown above.

        Returns none.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        prototype = prototype or int
        vertical_moments = iterate(self.client).by_vertical_moment()
        for index, vertical_moment in enumerate(vertical_moments):
            label = None
            if prototype is int:
                label = markuptools.Markup(index, direction=direction)
            elif prototype is pitchtools.NumberedPitch:
                leaves = vertical_moment.leaves
                pitches = pitchtools.PitchSegment.from_selection(leaves)
                if not pitches:
                    continue
                pitch_numbers = [pitch.number for pitch in pitches]
                pitch_numbers = [markuptools.Markup(_) for _ in pitch_numbers]
                label = markuptools.Markup.column(pitch_numbers, direction)
            elif prototype is pitchtools.NumberedPitchClass:
                leaves = vertical_moment.leaves
                pitches = pitchtools.PitchSegment.from_selection(leaves)
                if not pitches:
                    continue
                pitch_classes = [pitch.pitch_class.number for pitch in pitches]
                pitch_classes = list(set(pitch_classes))
                pitch_classes.sort()
                pitch_classes.reverse()
                numbers = [str(_) for _ in pitch_classes]
                markup = [markuptools.Markup(_) for _ in numbers]
                label = markuptools.Markup.column(markup, direction)
            elif prototype is pitchtools.NumberedInterval:
                leaves = vertical_moment.leaves
                notes = [_ for _ in leaves if isinstance(_, scoretools.Note)]
                if not notes:
                    continue
                notes.sort(key=lambda x: x.written_pitch.number)
                notes.reverse()
                bass_note = notes[-1]
                upper_notes = notes[:-1]
                named_intervals = []
                for upper_note in upper_notes:
                    named_interval = pitchtools.NamedInterval.from_pitch_carriers(
                        bass_note.written_pitch, upper_note.written_pitch)
                    named_intervals.append(named_interval)
                numbers = [x.number for x in named_intervals]
                markup = [markuptools.Markup(_) for _ in numbers]
                label = markuptools.Markup.column(markup, direction)
            elif prototype is pitchtools.NumberedIntervalClass:
                leaves = vertical_moment.leaves
                notes = [_ for _ in leaves if isinstance(_, scoretools.Note)]
                if not notes:
                    continue
                notes.sort(key=lambda x: x.written_pitch.number)
                notes.reverse()
                bass_note = notes[-1]
                upper_notes = notes[:-1]
                numbers = []
                for upper_note in upper_notes:
                    interval = pitchtools.NamedInterval.from_pitch_carriers(
                        bass_note.written_pitch, upper_note.written_pitch)
                    interval_class = pitchtools.NumberedIntervalClass(interval)
                    number = interval_class.number
                    numbers.append(number)
                markup = [markuptools.Markup(_) for _ in numbers]
                label = markuptools.Markup.column(markup, direction)
            elif prototype is pitchtools.IntervalClassVector:
                leaves = vertical_moment.leaves
                pitches = pitchtools.PitchSegment.from_selection(leaves)
                if not pitches:
                    continue
                interval_class_vector = pitchtools.IntervalClassVector(
                    pitches,
                    item_class=pitchtools
                        .NumberedInversionEquivalentIntervalClass,
                    )
                markup = interval_class_vector._label
                label = markuptools.Markup(markup, direction=direction)
            elif (prototype is pitchtools.SetClass or
                isinstance(prototype, pitchtools.SetClass)):
                if prototype is pitchtools.SetClass:
                    prototype = prototype()
                assert isinstance(prototype, pitchtools.SetClass)
                leaves = vertical_moment.leaves
                pitch_class_set = pitchtools.PitchClassSet.from_selection(
                    leaves)
                if not pitch_class_set:
                    continue
                set_class = pitchtools.SetClass.from_pitch_class_set(
                    pitch_class_set,
                    lex_rank=prototype.lex_rank,
                    transposition_only=prototype.transposition_only,
                    )
                string = str(set_class)
                command = markuptools.MarkupCommand('line', [string])
                label = markuptools.Markup(command, direction=direction)
            else:
                message = 'unknown prototype: {!r}.'
                message = message.format(prototype)
                raise TypeError(message)
            if label is not None:
                label = label.tiny()
                if direction is Up:
                    leaf = vertical_moment.start_leaves[0]
                else:
                    leaf = vertical_moment.start_leaves[-1]
                attach(label, leaf)

    def with_durations(self, direction=Up, preferred_denominator=None):
        r'''Labels logical ties with durations.

        ..  container:: example

            Labels logical tie durations:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")
                    >>> abjad.label(staff).with_durations()
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        c'4.
                            ^ \markup {
                                \small
                                    3/8
                                }
                        d'8 ~
                            ^ \markup {
                                \small
                                    1/2
                                }
                        d'4.
                        e'16 [
                            ^ \markup {
                                \small
                                    1/16
                                }
                        ef'16 ]
                            ^ \markup {
                                \small
                                    1/16
                                }
                    }

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")
                    >>> expression = abjad.label().with_durations()
                    >>> expression(staff)
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        c'4.
                            ^ \markup {
                                \small
                                    3/8
                                }
                        d'8 ~
                            ^ \markup {
                                \small
                                    1/2
                                }
                        d'4.
                        e'16 [
                            ^ \markup {
                                \small
                                    1/16
                                }
                        ef'16 ]
                            ^ \markup {
                                \small
                                    1/16
                                }
                    }

        ..  container:: example

            Labels logical ties with preferred denominator:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")
                    >>> abjad.label(staff).with_durations(preferred_denominator=16)
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        c'4.
                            ^ \markup {
                                \small
                                    6/16
                                }
                        d'8 ~
                            ^ \markup {
                                \small
                                    8/16
                                }
                        d'4.
                        e'16 [
                            ^ \markup {
                                \small
                                    1/16
                                }
                        ef'16 ]
                            ^ \markup {
                                \small
                                    1/16
                                }
                    }

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")
                    >>> expression = abjad.label().with_durations(preferred_denominator=16)
                    >>> expression(staff)
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        c'4.
                            ^ \markup {
                                \small
                                    6/16
                                }
                        d'8 ~
                            ^ \markup {
                                \small
                                    8/16
                                }
                        d'4.
                        e'16 [
                            ^ \markup {
                                \small
                                    1/16
                                }
                        ef'16 ]
                            ^ \markup {
                                \small
                                    1/16
                                }
                    }

        Returns none.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        logical_ties = iterate(self.client).by_logical_tie()
        for logical_tie in logical_ties:
            duration = logical_tie.get_duration()
            if preferred_denominator is not None:
                duration = mathtools.NonreducedFraction(duration)
                duration = duration.with_denominator(preferred_denominator)
            label = markuptools.Markup(str(duration), direction=direction)
            label = label.small()
            attach(label, logical_tie.head)

    def with_indices(self, direction=Up, prototype=None):
        r'''Labels logical ties with indices.

        ..  container:: example

            Labels logical tie indices:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                    >>> abjad.label(staff).with_indices()
                    >>> abjad.override(staff).text_script.staff_padding = 2
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #2
                    } {
                        <c' bf'>8
                            ^ \markup {
                                \small
                                    0
                                }
                        <g' a'>4
                            ^ \markup {
                                \small
                                    1
                                }
                        af'8 ~
                            ^ \markup {
                                \small
                                    2
                                }
                        af'8
                        gf'8 ~
                            ^ \markup {
                                \small
                                    3
                                }
                        gf'4
                    }

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                    >>> expression = abjad.label().with_indices()
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 2
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #2
                    } {
                        <c' bf'>8
                            ^ \markup {
                                \small
                                    0
                                }
                        <g' a'>4
                            ^ \markup {
                                \small
                                    1
                                }
                        af'8 ~
                            ^ \markup {
                                \small
                                    2
                                }
                        af'8
                        gf'8 ~
                            ^ \markup {
                                \small
                                    3
                                }
                        gf'4
                    }

        ..  container:: example

            Labels note indices:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                    >>> abjad.label(staff).with_indices(prototype=abjad.Note)
                    >>> abjad.override(staff).text_script.staff_padding = 2
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #2
                    } {
                        <c' bf'>8
                        <g' a'>4
                        af'8 ~
                            ^ \markup {
                                \small
                                    0
                                }
                        af'8
                            ^ \markup {
                                \small
                                    1
                                }
                        gf'8 ~
                            ^ \markup {
                                \small
                                    2
                                }
                        gf'4
                            ^ \markup {
                                \small
                                    3
                                }
                    }

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                    >>> expression = abjad.label().with_indices(
                    ...     prototype=abjad.Note,
                    ...     )
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 2
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #2
                    } {
                        <c' bf'>8
                        <g' a'>4
                        af'8 ~
                            ^ \markup {
                                \small
                                    0
                                }
                        af'8
                            ^ \markup {
                                \small
                                    1
                                }
                        gf'8 ~
                            ^ \markup {
                                \small
                                    2
                                }
                        gf'4
                            ^ \markup {
                                \small
                                    3
                                }
                    }

        ..  container:: example

            Labels chord indices:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                    >>> abjad.label(staff).with_indices(prototype=abjad.Chord)
                    >>> abjad.override(staff).text_script.staff_padding = 2
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #2
                    } {
                        <c' bf'>8
                            ^ \markup {
                                \small
                                    0
                                }
                        <g' a'>4
                            ^ \markup {
                                \small
                                    1
                                }
                        af'8 ~
                        af'8
                        gf'8 ~
                        gf'4
                    }

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                    >>> expression = abjad.label().with_indices(
                    ...     prototype=abjad.Chord,
                    ...     )
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 2
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #2
                    } {
                        <c' bf'>8
                            ^ \markup {
                                \small
                                    0
                                }
                        <g' a'>4
                            ^ \markup {
                                \small
                                    1
                                }
                        af'8 ~
                        af'8
                        gf'8 ~
                        gf'4
                    }

        ..  container:: example

            Labels leaf indices:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                    >>> abjad.label(staff).with_indices(prototype=abjad.Leaf)
                    >>> abjad.override(staff).text_script.staff_padding = 2
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #2
                    } {
                        <c' bf'>8
                            ^ \markup {
                                \small
                                    0
                                }
                        <g' a'>4
                            ^ \markup {
                                \small
                                    1
                                }
                        af'8 ~
                            ^ \markup {
                                \small
                                    2
                                }
                        af'8
                            ^ \markup {
                                \small
                                    3
                                }
                        gf'8 ~
                            ^ \markup {
                                \small
                                    4
                                }
                        gf'4
                            ^ \markup {
                                \small
                                    5
                                }
                    }

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                    >>> expression = abjad.label().with_indices(
                    ...     prototype=abjad.Leaf,
                    ...     )
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 2
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #2
                    } {
                        <c' bf'>8
                            ^ \markup {
                                \small
                                    0
                                }
                        <g' a'>4
                            ^ \markup {
                                \small
                                    1
                                }
                        af'8 ~
                            ^ \markup {
                                \small
                                    2
                                }
                        af'8
                            ^ \markup {
                                \small
                                    3
                                }
                        gf'8 ~
                            ^ \markup {
                                \small
                                    4
                                }
                        gf'4
                            ^ \markup {
                                \small
                                    5
                                }
                    }

        ..  container:: example

            Labels tuplet indices:

            ..  container:: example

                ::

                    >>> tuplet = abjad.Tuplet((2, 3), "c'8 [ d'8 e'8 ]")
                    >>> staff = abjad.Staff(4 * tuplet)
                    >>> abjad.label(staff).with_indices(prototype=abjad.Tuplet)
                    >>> abjad.override(staff).text_script.staff_padding = 2
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #2
                    } {
                        \times 2/3 {
                            c'8
                                ^ \markup {
                                    \small
                                        0
                                    }
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                                ^ \markup {
                                    \small
                                        1
                                    }
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                                ^ \markup {
                                    \small
                                        2
                                    }
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                                ^ \markup {
                                    \small
                                        3
                                    }
                            d'8
                            e'8
                        }
                    }

            ..  container:: example expression

                ::

                    >>> tuplet = abjad.Tuplet((2, 3), "c'8 [ d'8 e'8 ]")
                    >>> staff = abjad.Staff(4 * tuplet)
                    >>> expression = abjad.label().with_indices(
                    ...     prototype=abjad.Tuplet,
                    ...     )
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 2
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #2
                    } {
                        \times 2/3 {
                            c'8
                                ^ \markup {
                                    \small
                                        0
                                    }
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                                ^ \markup {
                                    \small
                                        1
                                    }
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                                ^ \markup {
                                    \small
                                        2
                                    }
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                                ^ \markup {
                                    \small
                                        3
                                    }
                            d'8
                            e'8
                        }
                    }

        Returns none.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if prototype is None:
            items = iterate(self.client).by_logical_tie()
        else:
            items = iterate(self.client).by_class(prototype=prototype)
        items = list(items)
        for index, item in enumerate(items):
            string = str(index)
            label = markuptools.Markup(string, direction=direction)
            label = label.small()
            leaves = iterate(item).by_leaf()
            first_leaf = list(leaves)[0]
            attach(label, first_leaf)

    def with_intervals(self, direction=Up, prototype=None):
        r"""Labels consecutive notes with intervals.

        ..  container:: example

            Labels consecutive notes with interval names:

            ..  container:: example

                ::

                    >>> maker = abjad.NoteMaker()
                    >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                    >>> notes = maker(pitch_numbers, [(1, 4)])
                    >>> staff = abjad.Staff(notes)
                    >>> abjad.label(staff).with_intervals(prototype=None)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        c'4 ^ \markup { +aug15 }
                        cs'''4 ^ \markup { -M9 }
                        b'4 ^ \markup { -aug9 }
                        af4 ^ \markup { -m7 }
                        bf,4 ^ \markup { +aug1 }
                        b,4 ^ \markup { +m14 }
                        a'4 ^ \markup { +m2 }
                        bf'4
                    }

            ..  container:: example expression

                ::

                    >>> maker = abjad.NoteMaker()
                    >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                    >>> notes = maker(pitch_numbers, [(1, 4)])
                    >>> staff = abjad.Staff(notes)
                    >>> expression = abjad.label().with_intervals(prototype=None)
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        c'4 ^ \markup { +aug15 }
                        cs'''4 ^ \markup { -M9 }
                        b'4 ^ \markup { -aug9 }
                        af4 ^ \markup { -m7 }
                        bf,4 ^ \markup { +aug1 }
                        b,4 ^ \markup { +m14 }
                        a'4 ^ \markup { +m2 }
                        bf'4
                    }

        ..  container:: example

            Labels consecutive notes with interval-class names:

            ..  container:: example

                ::

                    >>> maker = abjad.NoteMaker()
                    >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                    >>> notes = maker(pitch_numbers, [(1, 4)])
                    >>> staff = abjad.Staff(notes)
                    >>> prototype = abjad.NamedIntervalClass
                    >>> abjad.label(staff).with_intervals(prototype=prototype)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        c'4 ^ \markup { +aug8 }
                        cs'''4 ^ \markup { -M2 }
                        b'4 ^ \markup { -aug2 }
                        af4 ^ \markup { -m7 }
                        bf,4 ^ \markup { aug1 }
                        b,4 ^ \markup { +m7 }
                        a'4 ^ \markup { +m2 }
                        bf'4
                    }

            ..  container:: example expression

                ::

                    >>> maker = abjad.NoteMaker()
                    >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                    >>> notes = maker(pitch_numbers, [(1, 4)])
                    >>> staff = abjad.Staff(notes)
                    >>> prototype = abjad.NamedIntervalClass
                    >>> expression = abjad.label().with_intervals(prototype=prototype)
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        c'4 ^ \markup { +aug8 }
                        cs'''4 ^ \markup { -M2 }
                        b'4 ^ \markup { -aug2 }
                        af4 ^ \markup { -m7 }
                        bf,4 ^ \markup { aug1 }
                        b,4 ^ \markup { +m7 }
                        a'4 ^ \markup { +m2 }
                        bf'4
                    }

        ..  container:: example

            Labels consecutive notes with interval numbers:

            ..  container:: example

                ::

                    >>> maker = abjad.NoteMaker()
                    >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                    >>> notes = maker(pitch_numbers, [(1, 4)])
                    >>> staff = abjad.Staff(notes)
                    >>> prototype = abjad.NumberedInterval
                    >>> abjad.label(staff).with_intervals(prototype=prototype)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        c'4 ^ \markup { +25 }
                        cs'''4 ^ \markup { -14 }
                        b'4 ^ \markup { -15 }
                        af4 ^ \markup { -10 }
                        bf,4 ^ \markup { +1 }
                        b,4 ^ \markup { +22 }
                        a'4 ^ \markup { +1 }
                        bf'4
                    }

            ..  container:: example expression

                ::

                    >>> maker = abjad.NoteMaker()
                    >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                    >>> notes = maker(pitch_numbers, [(1, 4)])
                    >>> staff = abjad.Staff(notes)
                    >>> prototype = abjad.NumberedInterval
                    >>> expression = abjad.label().with_intervals(prototype=prototype)
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        c'4 ^ \markup { +25 }
                        cs'''4 ^ \markup { -14 }
                        b'4 ^ \markup { -15 }
                        af4 ^ \markup { -10 }
                        bf,4 ^ \markup { +1 }
                        b,4 ^ \markup { +22 }
                        a'4 ^ \markup { +1 }
                        bf'4
                    }


        ..  container:: example

            Labels consecutive notes with interval-class numbers:

            ..  container:: example

                ::

                    >>> maker = abjad.NoteMaker()
                    >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                    >>> notes = maker(pitch_numbers, [(1, 4)])
                    >>> staff = abjad.Staff(notes)
                    >>> prototype = abjad.NumberedIntervalClass
                    >>> abjad.label(staff).with_intervals(prototype=prototype)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        c'4 ^ \markup { +1 }
                        cs'''4 ^ \markup { -2 }
                        b'4 ^ \markup { -3 }
                        af4 ^ \markup { -10 }
                        bf,4 ^ \markup { +1 }
                        b,4 ^ \markup { +10 }
                        a'4 ^ \markup { +1 }
                        bf'4
                    }

            ..  container:: example expression

                ::

                    >>> maker = abjad.NoteMaker()
                    >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                    >>> notes = maker(pitch_numbers, [(1, 4)])
                    >>> staff = abjad.Staff(notes)
                    >>> prototype = abjad.NumberedIntervalClass
                    >>> expression = abjad.label().with_intervals(prototype=prototype)
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        c'4 ^ \markup { +1 }
                        cs'''4 ^ \markup { -2 }
                        b'4 ^ \markup { -3 }
                        af4 ^ \markup { -10 }
                        bf,4 ^ \markup { +1 }
                        b,4 ^ \markup { +10 }
                        a'4 ^ \markup { +1 }
                        bf'4
                    }

        ..  container:: example

            Labels consecutive notes with inversion-equivalent interval-class
            numbers:

            ..  container:: example

                ::

                    >>> maker = abjad.NoteMaker()
                    >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                    >>> notes = maker(pitch_numbers, [(1, 4)])
                    >>> staff = abjad.Staff(notes)
                    >>> prototype = abjad.NumberedInversionEquivalentIntervalClass
                    >>> abjad.label(staff).with_intervals(prototype=prototype)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        c'4 ^ \markup { 1 }
                        cs'''4 ^ \markup { 2 }
                        b'4 ^ \markup { 3 }
                        af4 ^ \markup { 2 }
                        bf,4 ^ \markup { 1 }
                        b,4 ^ \markup { 2 }
                        a'4 ^ \markup { 1 }
                        bf'4
                    }

            ..  container:: example expression

                ::

                    >>> maker = abjad.NoteMaker()
                    >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                    >>> notes = maker(pitch_numbers, [(1, 4)])
                    >>> staff = abjad.Staff(notes)
                    >>> prototype = abjad.NumberedInversionEquivalentIntervalClass
                    >>> expression = abjad.label().with_intervals(prototype=prototype)
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        c'4 ^ \markup { 1 }
                        cs'''4 ^ \markup { 2 }
                        b'4 ^ \markup { 3 }
                        af4 ^ \markup { 2 }
                        bf,4 ^ \markup { 1 }
                        b,4 ^ \markup { 2 }
                        a'4 ^ \markup { 1 }
                        bf'4
                    }

        Returns none.
        """
        from abjad.tools.topleveltools import inspect as abjad_inspect
        if self._expression:
            return self._update_expression(inspect.currentframe())
        prototype = prototype or pitchtools.NamedInterval
        notes = iterate(self.client).by_class(scoretools.Note)
        for note in notes:
            label = None
            next_leaf = abjad_inspect(note).get_leaf(1)
            if isinstance(next_leaf, scoretools.Note):
                interval = pitchtools.NamedInterval.from_pitch_carriers(
                    note,
                    next_leaf,
                    )
                if prototype is pitchtools.NamedInterval:
                    label = markuptools.Markup(interval, direction)
                elif prototype is pitchtools.NamedIntervalClass:
                    label = pitchtools.NamedIntervalClass(interval)
                    label = markuptools.Markup(label, direction)
                elif prototype is pitchtools.NumberedInterval:
                    label = pitchtools.NumberedInterval(interval)
                    label = markuptools.Markup(label, direction)
                elif prototype is pitchtools.NumberedIntervalClass:
                    label = pitchtools.NumberedIntervalClass(interval)
                    label = markuptools.Markup(label, direction)
                elif prototype is pitchtools.NumberedInversionEquivalentIntervalClass:
                    label = pitchtools.NumberedInversionEquivalentIntervalClass(interval)
                    label = markuptools.Markup(label, direction)
                if label is not None:
                    attach(label, note)

    def with_pitches(self, direction=Up, prototype=None):
        r'''Labels logical ties with pitches.

        ..  container:: example

            Labels logical ties with pitch names:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                    >>> abjad.label(staff).with_pitches(prototype=None)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        <a d' fs'>4
                            ^ \markup {
                                \small
                                    \column
                                        {
                                            fs'
                                            d'
                                            a
                                        }
                                }
                        g'4 ~
                            ^ \markup {
                                \small
                                    g'
                                }
                        g'8
                        r8
                        fs''4
                            ^ \markup {
                                \small
                                    fs''
                                }
                    }

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                    >>> expression = abjad.label().with_pitches(prototype=None)
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        <a d' fs'>4
                            ^ \markup {
                                \small
                                    \column
                                        {
                                            fs'
                                            d'
                                            a
                                        }
                                }
                        g'4 ~
                            ^ \markup {
                                \small
                                    g'
                                }
                        g'8
                        r8
                        fs''4
                            ^ \markup {
                                \small
                                    fs''
                                }
                    }

        ..  container:: example

            Labels logical ties with pitch numbers:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                    >>> prototype = abjad.NumberedPitch
                    >>> abjad.label(staff).with_pitches(prototype=prototype)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        <a d' fs'>4
                            ^ \markup {
                                \small
                                    \column
                                        {
                                            6
                                            2
                                            -3
                                        }
                                }
                        g'4 ~
                            ^ \markup {
                                \small
                                    7
                                }
                        g'8
                        r8
                        fs''4
                            ^ \markup {
                                \small
                                    18
                                }
                    }

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                    >>> prototype = abjad.NumberedPitch
                    >>> expression = abjad.label().with_pitches(prototype=prototype)
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        <a d' fs'>4
                            ^ \markup {
                                \small
                                    \column
                                        {
                                            6
                                            2
                                            -3
                                        }
                                }
                        g'4 ~
                            ^ \markup {
                                \small
                                    7
                                }
                        g'8
                        r8
                        fs''4
                            ^ \markup {
                                \small
                                    18
                                }
                    }

        ..  container:: example

            Labels logical ties with pitch-class numbers:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                    >>> prototype = abjad.NumberedPitchClass
                    >>> abjad.label(staff).with_pitches(prototype=prototype)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        <a d' fs'>4
                            ^ \markup {
                                \small
                                    \column
                                        {
                                            6
                                            2
                                            9
                                        }
                                }
                        g'4 ~
                            ^ \markup {
                                \small
                                    7
                                }
                        g'8
                        r8
                        fs''4
                            ^ \markup {
                                \small
                                    6
                                }
                    }

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                    >>> prototype = abjad.NumberedPitchClass
                    >>> expression = abjad.label().with_pitches(prototype=prototype)
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                    } {
                        <a d' fs'>4
                            ^ \markup {
                                \small
                                    \column
                                        {
                                            6
                                            2
                                            9
                                        }
                                }
                        g'4 ~
                            ^ \markup {
                                \small
                                    7
                                }
                        g'8
                        r8
                        fs''4
                            ^ \markup {
                                \small
                                    6
                                }
                    }

        ..  container:: example

            Labels logical ties with pitch names (filtered by selection):

            ..  container:: example

                ::

                    >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
                    >>> string = 'Horizontal_bracket_engraver'
                    >>> voice.consists_commands.append(string)
                    >>> selections = [voice[:2], voice[-2:]]
                    >>> for selection in selections:
                    ...     spanner = abjad.HorizontalBracketSpanner()
                    ...     abjad.attach(spanner, selection)
                    ...
                    >>> abjad.label(selections).with_pitches()
                    >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                    >>> abjad.override(voice).text_script.staff_padding = 2
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

                    >>> f(voice)
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    } {
                        df''4 \startGroup
                            ^ \markup {
                                \small
                                    df''
                                }
                        c''4 \stopGroup
                            ^ \markup {
                                \small
                                    c''
                                }
                        f'4
                        fs'4
                        d''4 \startGroup
                            ^ \markup {
                                \small
                                    d''
                                }
                        ds''4 \stopGroup
                            ^ \markup {
                                \small
                                    ds''
                                }
                    }

            ..  container:: example expression

                ::

                    >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
                    >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                    >>> selections = [voice[:2], voice[-2:]]
                    >>> for selection in selections:
                    ...     spanner = abjad.HorizontalBracketSpanner()
                    ...     abjad.attach(spanner, selection)
                    ...
                    >>> expression = abjad.label().with_pitches()
                    >>> expression(selections)
                    >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                    >>> abjad.override(voice).text_script.staff_padding = 2
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

                    >>> f(voice)
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    } {
                        df''4 \startGroup
                            ^ \markup {
                                \small
                                    df''
                                }
                        c''4 \stopGroup
                            ^ \markup {
                                \small
                                    c''
                                }
                        f'4
                        fs'4
                        d''4 \startGroup
                            ^ \markup {
                                \small
                                    d''
                                }
                        ds''4 \stopGroup
                            ^ \markup {
                                \small
                                    ds''
                                }
                    }

        ..  container:: example

            Labels logical ties with pitch numbers (filtered by selection):

            ..  container:: example

                ::

                    >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
                    >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                    >>> selections = [voice[:2], voice[-2:]]
                    >>> for selection in selections:
                    ...     spanner = abjad.HorizontalBracketSpanner()
                    ...     abjad.attach(spanner, selection)
                    ...
                    >>> prototype = abjad.NumberedPitch
                    >>> abjad.label(selections).with_pitches(prototype=prototype)
                    >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                    >>> abjad.override(voice).text_script.staff_padding = 2
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

                    >>> f(voice)
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    } {
                        df''4 \startGroup
                            ^ \markup {
                                \small
                                    13
                                }
                        c''4 \stopGroup
                            ^ \markup {
                                \small
                                    12
                                }
                        f'4
                        fs'4
                        d''4 \startGroup
                            ^ \markup {
                                \small
                                    14
                                }
                        ds''4 \stopGroup
                            ^ \markup {
                                \small
                                    15
                                }
                    }

            ..  container:: example expression

                ::

                    >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
                    >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                    >>> selections = [voice[:2], voice[-2:]]
                    >>> for selection in selections:
                    ...     spanner = abjad.HorizontalBracketSpanner()
                    ...     abjad.attach(spanner, selection)
                    ...
                    >>> prototype = abjad.NumberedPitch
                    >>> expression = abjad.label().with_pitches(prototype=prototype)
                    >>> expression(selections)
                    >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                    >>> abjad.override(voice).text_script.staff_padding = 2
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

                    >>> f(voice)
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    } {
                        df''4 \startGroup
                            ^ \markup {
                                \small
                                    13
                                }
                        c''4 \stopGroup
                            ^ \markup {
                                \small
                                    12
                                }
                        f'4
                        fs'4
                        d''4 \startGroup
                            ^ \markup {
                                \small
                                    14
                                }
                        ds''4 \stopGroup
                            ^ \markup {
                                \small
                                    15
                                }
                    }

        ..  container:: example

            Labels logical ties with pitch-class numbers (filtered by
            selection):

            ..  container:: example

                ::

                    >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
                    >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                    >>> selections = [voice[:2], voice[-2:]]
                    >>> for selection in selections:
                    ...     spanner = abjad.HorizontalBracketSpanner()
                    ...     abjad.attach(spanner, selection)
                    ...
                    >>> prototype = abjad.NumberedPitchClass
                    >>> abjad.label(selections).with_pitches(prototype=prototype)
                    >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                    >>> abjad.override(voice).text_script.staff_padding = 2
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

                    >>> f(voice)
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    } {
                        df''4 \startGroup
                            ^ \markup {
                                \small
                                    1
                                }
                        c''4 \stopGroup
                            ^ \markup {
                                \small
                                    0
                                }
                        f'4
                        fs'4
                        d''4 \startGroup
                            ^ \markup {
                                \small
                                    2
                                }
                        ds''4 \stopGroup
                            ^ \markup {
                                \small
                                    3
                                }
                    }

            ..  container:: example expression

                ::

                    >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
                    >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                    >>> selections = [voice[:2], voice[-2:]]
                    >>> for selection in selections:
                    ...     spanner = abjad.HorizontalBracketSpanner()
                    ...     abjad.attach(spanner, selection)
                    ...
                    >>> prototype = abjad.NumberedPitchClass
                    >>> expression = abjad.label().with_pitches(prototype=prototype)
                    >>> expression(selections)
                    >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                    >>> abjad.override(voice).text_script.staff_padding = 2
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

                    >>> f(voice)
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    } {
                        df''4 \startGroup
                            ^ \markup {
                                \small
                                    1
                                }
                        c''4 \stopGroup
                            ^ \markup {
                                \small
                                    0
                                }
                        f'4
                        fs'4
                        d''4 \startGroup
                            ^ \markup {
                                \small
                                    2
                                }
                        ds''4 \stopGroup
                            ^ \markup {
                                \small
                                    3
                                }
                    }

        Returns none.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        prototype = prototype or pitchtools.NamedPitch
        logical_ties = iterate(self.client).by_logical_tie()
        for logical_tie in logical_ties:
            leaf = logical_tie.head
            label = None
            if prototype is pitchtools.NamedPitch:
                if isinstance(leaf, scoretools.Note):
                    pitch = leaf.written_pitch
                    label = str(pitch)
                    label = markuptools.Markup(label, direction=direction)
                    label = label.small()
                elif isinstance(leaf, scoretools.Chord):
                    pitches = leaf.written_pitches
                    pitches = reversed(pitches)
                    pitches = [markuptools.Markup(_) for _ in pitches]
                    label = markuptools.Markup.column(pitches)
                    label = label.small()
            elif prototype is pitchtools.NumberedPitch:
                if isinstance(leaf, scoretools.Note):
                    pitch = leaf.written_pitch.number
                    label = str(pitch)
                    label = markuptools.Markup(label, direction=direction)
                    label = label.small()
                elif isinstance(leaf, scoretools.Chord):
                    pitches = leaf.written_pitches
                    pitches = reversed(pitches)
                    pitches = [_.number for _ in pitches]
                    pitches = [markuptools.Markup(_) for _ in pitches]
                    label = markuptools.Markup.column(pitches)
                    label = label.small()
            elif prototype is pitchtools.NumberedPitchClass:
                if isinstance(leaf, scoretools.Note):
                    pitch = leaf.written_pitch.pitch_class.number
                    label = str(pitch)
                    label = markuptools.Markup(label, direction=direction)
                    label = label.small()
                elif isinstance(leaf, scoretools.Chord):
                    pitches = leaf.written_pitches
                    pitches = reversed(pitches)
                    pitches = [_.pitch_class.number for _ in pitches]
                    pitches = [markuptools.Markup(_) for _ in pitches]
                    label = markuptools.Markup.column(pitches)
                    label = label.small()
            if label is not None:
                label = new(label, direction=direction)
                attach(label, leaf)

    def with_set_classes(self, direction=Up, prototype=None):
        r'''Labels items in client with set-classes.

        ..  container:: example

            Labels selections with Forte-ranked transposition-inversion
            set-classes:

            ..  container:: example

                ::

                    >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
                    >>> voice = abjad.Voice(string)
                    >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                    >>> selections = [voice[:4], voice[-4:]]
                    >>> for selection in selections:
                    ...     spanner = abjad.HorizontalBracketSpanner()
                    ...     abjad.attach(spanner, selection)
                    ...
                    >>> abjad.label(selections).with_set_classes()
                    >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                    >>> abjad.override(voice).text_script.staff_padding = 2
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

                    >>> f(voice)
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    } {
                        df''8 \startGroup
                            ^ \markup {
                                \tiny
                                    \line
                                        {
                                            "SC(4-3){0, 1, 3, 4}"
                                        }
                                }
                        c''8
                        bf'8
                        a'8 \stopGroup
                        f'4.
                        fs'8 \startGroup
                            ^ \markup {
                                \tiny
                                    \line
                                        {
                                            "SC(4-20){0, 1, 5, 8}"
                                        }
                                }
                        g'8
                        b'8
                        d''2. \stopGroup
                    }

            ..  container:: example expression

                ::

                    >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
                    >>> voice = abjad.Voice(string)
                    >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                    >>> selections = [voice[:4], voice[-4:]]
                    >>> for selection in selections:
                    ...     spanner = abjad.HorizontalBracketSpanner()
                    ...     abjad.attach(spanner, selection)
                    ...
                    >>> expression = abjad.label().with_set_classes()
                    >>> expression(selections)
                    >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                    >>> abjad.override(voice).text_script.staff_padding = 2
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

                    >>> f(voice)
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    } {
                        df''8 \startGroup
                            ^ \markup {
                                \tiny
                                    \line
                                        {
                                            "SC(4-3){0, 1, 3, 4}"
                                        }
                                }
                        c''8
                        bf'8
                        a'8 \stopGroup
                        f'4.
                        fs'8 \startGroup
                            ^ \markup {
                                \tiny
                                    \line
                                        {
                                            "SC(4-20){0, 1, 5, 8}"
                                        }
                                }
                        g'8
                        b'8
                        d''2. \stopGroup
                    }

        ..  container:: example

            Labels selections with lex-ranked transposition-inversion
            set-classes:

            ..  container:: example

                ::

                    >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
                    >>> voice = abjad.Voice(string)
                    >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                    >>> selections = [voice[:4], voice[-4:]]
                    >>> for selection in selections:
                    ...     spanner = abjad.HorizontalBracketSpanner()
                    ...     abjad.attach(spanner, selection)
                    ...
                    >>> prototype = abjad.SetClass(lex_rank=True)
                    >>> abjad.label(selections).with_set_classes(prototype=prototype)
                    >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                    >>> abjad.override(voice).text_script.staff_padding = 2
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

                    >>> f(voice)
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    } {
                        df''8 \startGroup
                            ^ \markup {
                                \tiny
                                    \line
                                        {
                                            "SC(4-6){0, 1, 3, 4}"
                                        }
                                }
                        c''8
                        bf'8
                        a'8 \stopGroup
                        f'4.
                        fs'8 \startGroup
                            ^ \markup {
                                \tiny
                                    \line
                                        {
                                            "SC(4-16){0, 1, 5, 8}"
                                        }
                                }
                        g'8
                        b'8
                        d''2. \stopGroup
                    }

            ..  container:: example expression

                ::

                    >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
                    >>> voice = abjad.Voice(string)
                    >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                    >>> selections = [voice[:4], voice[-4:]]
                    >>> for selection in selections:
                    ...     spanner = abjad.HorizontalBracketSpanner()
                    ...     abjad.attach(spanner, selection)
                    ...
                    >>> prototype = abjad.SetClass(lex_rank=True)
                    >>> expression = abjad.label().with_set_classes(prototype=prototype)
                    >>> expression(selections)
                    >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                    >>> abjad.override(voice).text_script.staff_padding = 2
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

                    >>> f(voice)
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    } {
                        df''8 \startGroup
                            ^ \markup {
                                \tiny
                                    \line
                                        {
                                            "SC(4-6){0, 1, 3, 4}"
                                        }
                                }
                        c''8
                        bf'8
                        a'8 \stopGroup
                        f'4.
                        fs'8 \startGroup
                            ^ \markup {
                                \tiny
                                    \line
                                        {
                                            "SC(4-16){0, 1, 5, 8}"
                                        }
                                }
                        g'8
                        b'8
                        d''2. \stopGroup
                    }

        ..  container:: example

            Labels selections with transposition-only set-classes:

            ..  container:: example

                ::

                    >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
                    >>> voice = abjad.Voice(string)
                    >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                    >>> selections = [voice[:4], voice[-4:]]
                    >>> for selection in selections:
                    ...     spanner = abjad.HorizontalBracketSpanner()
                    ...     abjad.attach(spanner, selection)
                    ...
                    >>> prototype = abjad.SetClass(transposition_only=True)
                    >>> abjad.label(selections).with_set_classes(prototype=prototype)
                    >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                    >>> abjad.override(voice).text_script.staff_padding = 2
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

                    >>> f(voice)
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    } {
                        df''8 \startGroup
                            ^ \markup {
                                \tiny
                                    \line
                                        {
                                            "SC(4-3){0, 1, 2, 5}"
                                        }
                                }
                        c''8
                        bf'8
                        a'8 \stopGroup
                        f'4.
                        fs'8 \startGroup
                            ^ \markup {
                                \tiny
                                    \line
                                        {
                                            "SC(4-20){0, 2, 3, 6}"
                                        }
                                }
                        g'8
                        b'8
                        d''2. \stopGroup
                    }

            ..  container:: example expression

                ::

                    >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
                    >>> voice = abjad.Voice(string)
                    >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                    >>> selections = [voice[:4], voice[-4:]]
                    >>> for selection in selections:
                    ...     spanner = abjad.HorizontalBracketSpanner()
                    ...     abjad.attach(spanner, selection)
                    ...
                    >>> prototype = abjad.SetClass(transposition_only=True)
                    >>> expression = abjad.label().with_set_classes(prototype=prototype)
                    >>> expression(selections)
                    >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                    >>> abjad.override(voice).text_script.staff_padding = 2
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

                    >>> f(voice)
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    } {
                        df''8 \startGroup
                            ^ \markup {
                                \tiny
                                    \line
                                        {
                                            "SC(4-3){0, 1, 2, 5}"
                                        }
                                }
                        c''8
                        bf'8
                        a'8 \stopGroup
                        f'4.
                        fs'8 \startGroup
                            ^ \markup {
                                \tiny
                                    \line
                                        {
                                            "SC(4-20){0, 2, 3, 6}"
                                        }
                                }
                        g'8
                        b'8
                        d''2. \stopGroup
                    }

        Returns none.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        prototype = prototype or pitchtools.SetClass()
        if prototype is pitchtools.SetClass:
            prototype = prototype()
        assert isinstance(prototype, pitchtools.SetClass), repr(prototype)
        for selection in self._client:
            pitch_class_set = pitchtools.PitchClassSet.from_selection(
                selection)
            if not pitch_class_set:
                continue
            set_class = pitchtools.SetClass.from_pitch_class_set(
                pitch_class_set,
                lex_rank=prototype.lex_rank,
                transposition_only=prototype.transposition_only,
                )
            string = str(set_class)
            command = markuptools.MarkupCommand('line', [string])
            label = markuptools.Markup(command, direction=direction)
            if label is not None:
                label = label.tiny()
                leaf = selection[0]
                attach(label, leaf)

    def with_start_offsets(
        self,
        clock_time=False,
        direction=Up,
        font_size=None,
        ):
        r'''Labels logical ties with start offsets.

        ..  container:: example

            Labels logical tie start offsets:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
                    >>> abjad.label(staff).with_start_offsets(direction=Up)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                        \override TupletBracket.staff-padding = #0
                    } {
                        \times 2/3 {
                            c'4 ^ \markup { 0 }
                            d'4 ^ \markup { 1/6 }
                            e'4 ~ ^ \markup { 1/3 }
                        }
                        e'4
                        ef'4 ^ \markup { 3/4 }
                    }

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
                    >>> expression = abjad.label().with_start_offsets(direction=Up)
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #4
                        \override TupletBracket.staff-padding = #0
                    } {
                        \times 2/3 {
                            c'4 ^ \markup { 0 }
                            d'4 ^ \markup { 1/6 }
                            e'4 ~ ^ \markup { 1/3 }
                        }
                        e'4
                        ef'4 ^ \markup { 3/4 }
                    }

        ..  container:: example

            Labels logical tie start offsets with clock time:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff(r"c'2 d' e' f'")
                    >>> score = abjad.Score([staff])
                    >>> mark = abjad.MetronomeMark((1, 4), 60)
                    >>> abjad.attach(mark, staff[0])
                    >>> abjad.label(staff).with_start_offsets(clock_time=True)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
                    >>> show(score) # doctest: +SKIP

                ..  docs::

                    >>> f(score)
                    \new Score <<
                        \new Staff \with {
                            \override TextScript.staff-padding = #4
                            \override TupletBracket.staff-padding = #0
                        } {
                            \tempo 4=60
                            c'2 ^ \markup { 0'00'' }
                            d'2 ^ \markup { 0'02'' }
                            e'2 ^ \markup { 0'04'' }
                            f'2 ^ \markup { 0'06'' }
                        }
                    >>

            ..  container:: example

                ::

                    >>> staff = abjad.Staff(r"c'2 d' e' f'")
                    >>> score = abjad.Score([staff])
                    >>> mark = abjad.MetronomeMark((1, 4), 60)
                    >>> abjad.attach(mark, staff[0])
                    >>> expression = abjad.label().with_start_offsets(clock_time=True)
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
                    >>> show(score) # doctest: +SKIP

                ..  docs::

                    >>> f(score)
                    \new Score <<
                        \new Staff \with {
                            \override TextScript.staff-padding = #4
                            \override TupletBracket.staff-padding = #0
                        } {
                            \tempo 4=60
                            c'2 ^ \markup { 0'00'' }
                            d'2 ^ \markup { 0'02'' }
                            e'2 ^ \markup { 0'04'' }
                            f'2 ^ \markup { 0'06'' }
                        }
                    >>

        ..  container:: example

            Labels logical tie start offsets with clock time and custom font
            size:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff(r"c'2 d' e' f'")
                    >>> score = abjad.Score([staff])
                    >>> mark = abjad.MetronomeMark((1, 4), 60)
                    >>> abjad.attach(mark, staff[0])
                    >>> abjad.label(staff).with_start_offsets(
                    ...     clock_time=True,
                    ...     font_size=-3,
                    ...     )
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
                    >>> show(score) # doctest: +SKIP

                ..  docs::

                    >>> f(score)
                    \new Score <<
                        \new Staff \with {
                            \override TextScript.staff-padding = #4
                            \override TupletBracket.staff-padding = #0
                        } {
                            \tempo 4=60
                            c'2
                                ^ \markup {
                                    \fontsize
                                        #-3
                                        0'00''
                                    }
                            d'2
                                ^ \markup {
                                    \fontsize
                                        #-3
                                        0'02''
                                    }
                            e'2
                                ^ \markup {
                                    \fontsize
                                        #-3
                                        0'04''
                                    }
                            f'2
                                ^ \markup {
                                    \fontsize
                                        #-3
                                        0'06''
                                    }
                        }
                    >>

            ..  container:: example expression

                ::

                    >>> staff = abjad.Staff(r"c'2 d' e' f'")
                    >>> score = abjad.Score([staff])
                    >>> mark = abjad.MetronomeMark((1, 4), 60)
                    >>> abjad.attach(mark, staff[0])
                    >>> expression = abjad.label().with_start_offsets(
                    ...     clock_time=True,
                    ...     font_size=-3,
                    ...     )
                    >>> expression(staff)
                    >>> abjad.override(staff).text_script.staff_padding = 4
                    >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
                    >>> show(score) # doctest: +SKIP

                ..  docs::

                    >>> f(score)
                    \new Score <<
                        \new Staff \with {
                            \override TextScript.staff-padding = #4
                            \override TupletBracket.staff-padding = #0
                        } {
                            \tempo 4=60
                            c'2
                                ^ \markup {
                                    \fontsize
                                        #-3
                                        0'00''
                                    }
                            d'2
                                ^ \markup {
                                    \fontsize
                                        #-3
                                        0'02''
                                    }
                            e'2
                                ^ \markup {
                                    \fontsize
                                        #-3
                                        0'04''
                                    }
                            f'2
                                ^ \markup {
                                    \fontsize
                                        #-3
                                        0'06''
                                    }
                        }
                    >>

        Returns none.
        '''
        from abjad.tools.topleveltools import inspect as abjad_inspect
        if self._expression:
            return self._update_expression(inspect.currentframe())
        logical_ties = iterate(self.client).by_logical_tie()
        for logical_tie in logical_ties:
            if clock_time:
                inspector = abjad_inspect(logical_tie.head)
                timespan = inspector.get_timespan(in_seconds=True)
                start_offset = timespan.start_offset
                string = start_offset.to_clock_string()
                string = '"{}"'.format(string)
            else:
                timespan = abjad_inspect(logical_tie.head).get_timespan()
                start_offset = timespan.start_offset
                string = str(start_offset)
            label = markuptools.Markup(string, direction=direction)
            if font_size is not None:
                label = label.fontsize(font_size)
            attach(label, logical_tie.head)
