# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import markuptools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import new


class LabelAgent(abctools.AbjadObject):
    r'''Label agent.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> label(staff)
            LabelAgent(client=Staff("c'4 e'4 d'4 f'4"))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
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
            type(None),
            )
        assert isinstance(client, prototype), repr(client)
        self._client = client

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

    def _format_interval_class_vector(self, interval_class_vector):
        counts = []
        for i in range(7):
            counts.append(interval_class_vector[i])
        counts = ''.join([str(x) for x in counts])
        if len(interval_class_vector) == 13:
            quartertones = []
            for i in range(6):
                quartertones.append(interval_class_vector[i + 0.5])
            quartertones = ''.join([str(x) for x in quartertones])
            return r'\tiny \column { "%s" "%s" }' % (counts, quartertones)
        else:
            return r'\tiny %s' % counts

    ### PUBLIC METHODS ###

    def color_container(self, color='red'):
        r'''Colors contents of `container`.

        ..  container:: example

            **Example 1.** Colors measure:

            ::

                >>> measure = Measure((2, 8), "c'8 d'8")
                >>> label(measure).color_container('red')
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
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

            **Example 1.** Colors leaves red:

            ::

                >>> staff = Staff("cs'8. [ r8. s8. <c' cs' a'>8. ]")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    cs'8. [
                    r8.
                    s8.
                    <c' cs' a'>8. ]
                }

            ::

                >>> label(staff).color_leaves('red')
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
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
        for leaf in iterate(self.client).by_class(scoretools.Leaf):
            self._color_leaf(leaf, color)

    def color_note_heads(self, color_map=None):
        r'''Colors note note heads.

        ..  container:: example

            **Example 1.** Colors chord note heads:

            ::

                >>> chord = Chord([12, 14, 18, 21, 23], (1, 4))
                >>> pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
                >>> colors = ['red', 'blue', 'green']
                >>> color_map = pitchtools.NumberedPitchClassColorMap(pitches, colors)
                >>> label(chord).color_note_heads(color_map)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
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

            **Example 2.** Colors note note head:

            ::

                >>> note = Note("c'4")
                >>> label(note).color_note_heads(color_map)
                >>> show(note) # doctest: +SKIP

            ..  doctest::

                >>> print(format(note))
                \once \override NoteHead.color = #red
                c'4

        ..  container:: example

            **Example 3.** Colors nothing:

            ::

                >>> staff = Staff([])
                >>> label(staff).color_note_heads(color_map)

        ..  container:: example

            **Example 4.** Colors note heads:

            ::

                >>> staff = Staff("c'8 cs'8 d'8 ds'8 e'8 f'8 fs'8 g'8 gs'8 a'8 as'8 b'8 c''8")
                >>> label(staff).color_note_heads()
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
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
        color_map = color_map or self._pc_number_to_color
        for leaf in iterate(self.client).by_class(scoretools.Leaf):
            if isinstance(leaf, scoretools.Chord):
                for note_head in leaf.note_heads:
                    pc = note_head.written_pitch.numbered_pitch_class
                    color = color_map.get(pc, None)
                    if color is not None:
                        note_head.tweak.color = color
            elif isinstance(leaf, scoretools.Note):
                note_head = leaf.note_head
                pc = note_head.written_pitch.numbered_pitch_class
                color = color_map[pc.pitch_class_number]
                if color is not None:
                    override(leaf).note_head.color = color

    def remove_markup(self):
        r'''Removes markup from leaves.

        ..  container:: example

            **Example.**

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> label(staff).with_pitches()
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
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

                >>> label(staff).remove_markup()
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8
                    d'8
                    e'8
                    f'8
                }

        Returns none.
        '''
        leaves = iterate(self.client).by_class(scoretools.Leaf)
        for leaf in leaves:
            detach(markuptools.Markup, leaf)

    def vertical_moments(self, direction=Up, prototype=None):
        r'''Labels vertical moments.

        ..  container:: example

            **Example 1.** Labels indices:

            ::

                >>> staff_group = StaffGroup([])
                >>> staff = Staff("c'8 d'4 e'16 f'16")
                >>> staff_group.append(staff)
                >>> staff = Staff(r"""\clef "alto" g4 f4""")
                >>> staff_group.append(staff)
                >>> staff = Staff(r"""\clef "bass" c,2""")
                >>> staff_group.append(staff)

            ::

                >>> label(staff_group).vertical_moments()
                >>> show(staff_group) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff_group))
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

            **Example 2.** Labels pitch numbers:

            ::

                >>> staff_group = StaffGroup([])
                >>> staff = Staff("c'8 d'4 e'16 f'16")
                >>> staff_group.append(staff)
                >>> staff = Staff(r"""\clef "alto" g4 f4""")
                >>> staff_group.append(staff)
                >>> staff = Staff(r"""\clef "bass" c,2""")
                >>> staff_group.append(staff)

            ::

                >>> prototype = pitchtools.NumberedPitch
                >>> label(staff_group).vertical_moments(prototype=prototype)
                >>> show(staff_group) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff_group))
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

            **Example 3.** Labels pitch-class numbers:

            ::

                >>> staff_group = StaffGroup([])
                >>> staff = Staff("c'8 d'4 e'16 f'16")
                >>> staff_group.append(staff)
                >>> staff = Staff(r"""\clef "alto" g4 f4""")
                >>> staff_group.append(staff)
                >>> staff = Staff(r"""\clef "bass" c,2""")
                >>> staff_group.append(staff)

            ::

                >>> prototype = pitchtools.NumberedPitchClass
                >>> label(staff_group).vertical_moments(prototype=prototype)
                >>> show(staff_group) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff_group))
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

            **Example 4.** Labels interval numbers:

            ::

                >>> staff_group = StaffGroup([])
                >>> staff = Staff("c'8 d'4 e'16 f'16")
                >>> staff_group.append(staff)
                >>> staff = Staff(r"""\clef "alto" g4 f4""")
                >>> staff_group.append(staff)
                >>> staff = Staff(r"""\clef "bass" c,2""")
                >>> staff_group.append(staff)

            ::

                >>> prototype = pitchtools.NumberedInterval
                >>> label(staff_group).vertical_moments(prototype=prototype)
                >>> show(staff_group) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff_group))
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

            **Example 5.** Labels interval-class numbers:

            ::

                >>> staff_group = StaffGroup([])
                >>> staff = Staff("c'8 d'4 e'16 f'16")
                >>> staff_group.append(staff)
                >>> staff = Staff(r"""\clef "alto" g4 f4""")
                >>> staff_group.append(staff)
                >>> staff = Staff(r"""\clef "bass" c,2""")
                >>> staff_group.append(staff)

            ::

                >>> prototype = pitchtools.NumberedIntervalClass
                >>> label(staff_group).vertical_moments(prototype=prototype)
                >>> show(staff_group) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff_group))
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

            **Example 6.** Labels interval-class vectors:

            ::

                >>> staff_group = StaffGroup([])
                >>> staff = Staff("c'8 d'4 e'16 f'16")
                >>> staff_group.append(staff)
                >>> staff = Staff(r"""\clef "alto" g4 f4""")
                >>> staff_group.append(staff)
                >>> staff = Staff(r"""\clef "bass" c,2""")
                >>> staff_group.append(staff)

            ::

                >>> prototype = pitchtools.IntervalClassVector
                >>> label(staff_group).vertical_moments(prototype=prototype)
                >>> show(staff_group) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff_group))
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

        Set `prototype` to one of the classes shown above.

        Returns none.
        '''
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
                pitch_numbers = [
                    pitch.numbered_pitch.pitch_number
                    for pitch in pitches
                    ]
                pitch_numbers = [markuptools.Markup(_) for _ in pitch_numbers]
                label = markuptools.Markup.column(pitch_numbers, direction)
            elif prototype is pitchtools.NumberedPitchClass:
                leaves = vertical_moment.leaves
                pitches = pitchtools.PitchSegment.from_selection(leaves)
                if not pitches:
                    continue
                pitch_classes = [
                    pitch.numbered_pitch_class.pitch_class_number
                    for pitch in pitches
                    ]
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
                notes.sort(key=lambda x: x.written_pitch.numbered_pitch)
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
                notes.sort(key=lambda x: x.written_pitch.numbered_pitch)
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
                formatted = self._format_interval_class_vector(
                    interval_class_vector)
                label = markuptools.Markup(formatted, direction=direction)
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

            **Example 1.** Labels logical tie durations:

            ::

                >>> staff = Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")
                >>> label(staff).with_durations()
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
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

            **Example 2.** Labels logical ties with preferred denominator:

            ::

                >>> staff = Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")
                >>> label(staff).with_durations(preferred_denominator=16)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
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

            **Example 1.** Labels logical tie indices:

            ::

                >>> staff = Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                >>> label(staff).with_indices()
                >>> override(staff).text_script.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 2.** Labels note indices:

            ::

                >>> staff = Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                >>> label(staff).with_indices(prototype=Note)
                >>> override(staff).text_script.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 3.** Labels chord indices:

            ::

                >>> staff = Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                >>> label(staff).with_indices(prototype=Chord)
                >>> override(staff).text_script.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 4.** Labels leaf indices:

            ::

                >>> staff = Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                >>> label(staff).with_indices(prototype=scoretools.Leaf)
                >>> override(staff).text_script.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 5.** Labels tuplet indices:

            ::

                >>> staff = Staff(4 * Tuplet((2, 3), "c'8 [ d'8 e'8 ]"))
                >>> label(staff).with_indices(prototype=Tuplet)
                >>> override(staff).text_script.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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
        if prototype is None:
            items = iterate(self.client).by_logical_tie()
        else:
            items = iterate(self.client).by_class(prototype=prototype)
        items = list(items)
        #raise Exception((self.client, items))
        for index, item in enumerate(items):
            string = str(index)
            label = markuptools.Markup(string, direction=direction)
            label = label.small()
            leaves = iterate(item).by_class(scoretools.Leaf)
            first_leaf = list(leaves)[0]
            attach(label, first_leaf)

    def with_intervals(self, direction=Up, prototype=None):
        r"""Labels consecutive notes with intervals.

        ..  container:: example

            **Example 1.** Labels consecutive notes with interval names:

            ::

                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = scoretools.make_notes(pitch_numbers, [(1, 4)])
                >>> staff = Staff(notes)
                >>> label(staff).with_intervals(prototype=None)
                >>> override(staff).text_script.staff_padding = 4
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 2.** Labels consecutive notes with interval-class names:

            ::

                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = scoretools.make_notes(pitch_numbers, [(1, 4)])
                >>> staff = Staff(notes)
                >>> prototype = pitchtools.NamedIntervalClass
                >>> label(staff).with_intervals(prototype=prototype)
                >>> override(staff).text_script.staff_padding = 4
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 3.** Labels consecutive notes with interval numbers:

            ::

                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = scoretools.make_notes(pitch_numbers, [(1, 4)])
                >>> staff = Staff(notes)
                >>> prototype = pitchtools.NumberedInterval
                >>> label(staff).with_intervals(prototype=prototype)
                >>> override(staff).text_script.staff_padding = 4
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 4.** Labels consecutive notes with interval-class
            numbers:

            ::

                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = scoretools.make_notes(pitch_numbers, [(1, 4)])
                >>> staff = Staff(notes)
                >>> prototype = pitchtools.NumberedIntervalClass
                >>> label(staff).with_intervals(prototype=prototype)
                >>> override(staff).text_script.staff_padding = 4
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 5.** Labels consecutive notes with inversion-equivalent
            interval-class numbers:

            ::

                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = scoretools.make_notes(pitch_numbers, [(1, 4)])
                >>> staff = Staff(notes)
                >>> prototype = pitchtools.NumberedInversionEquivalentIntervalClass
                >>> label(staff).with_intervals(prototype=prototype)
                >>> override(staff).text_script.staff_padding = 4
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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
        prototype = prototype or pitchtools.NamedInterval
        notes = iterate(self.client).by_class(scoretools.Note)
        for note in notes:
            label = None
            next_leaf = inspect_(note).get_leaf(1)
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

            **Example 1.** Labels logical ties with pitch names:

            ::

                >>> staff = Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                >>> label(staff).with_pitches(prototype=None)
                >>> override(staff).text_script.staff_padding = 4
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 2.** Labels logical ties with pitch numbers:

            ::

                >>> staff = Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                >>> prototype = pitchtools.NumberedPitch
                >>> label(staff).with_pitches(prototype=prototype)
                >>> override(staff).text_script.staff_padding = 4
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 3.** Labels logical ties with pitch-class numbers:

            ::

                >>> staff = Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                >>> prototype = pitchtools.NumberedPitchClass
                >>> label(staff).with_pitches(prototype=prototype)
                >>> override(staff).text_script.staff_padding = 4
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

        Returns none.
        '''
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
                    pitch = leaf.written_pitch.pitch_number
                    label = str(pitch)
                    label = markuptools.Markup(label, direction=direction)
                    label = label.small()
                elif isinstance(leaf, scoretools.Chord):
                    pitches = leaf.written_pitches
                    pitches = reversed(pitches)
                    pitches = [_.pitch_number for _ in pitches]
                    pitches = [markuptools.Markup(_) for _ in pitches]
                    label = markuptools.Markup.column(pitches)
                    label = label.small()
            elif prototype is pitchtools.NumberedPitchClass:
                if isinstance(leaf, scoretools.Note):
                    pitch = leaf.written_pitch.pitch_class_number
                    label = str(pitch)
                    label = markuptools.Markup(label, direction=direction)
                    label = label.small()
                elif isinstance(leaf, scoretools.Chord):
                    pitches = leaf.written_pitches
                    pitches = reversed(pitches)
                    pitches = [_.pitch_class_number for _ in pitches]
                    pitches = [markuptools.Markup(_) for _ in pitches]
                    label = markuptools.Markup.column(pitches)
                    label = label.small()
            if label is not None:
                label = new(label, direction=direction)
                attach(label, leaf)

    def with_start_offsets(
        self,
        clock_time=False,
        direction=Up,
        font_size=None,
        ):
        r'''Labels logical ties with start offsets.

        ..  container:: example

            **Example 1.** Labels logical tie start offsets:

            ::

                >>> staff = Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
                >>> label(staff).with_start_offsets(direction=Up)
                >>> override(staff).text_script.staff_padding = 4
                >>> override(staff).tuplet_bracket.staff_padding = 0
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
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

            **Example 2.** Labels logical tie start offsets with clock time:

            ::

                >>> staff = Staff(r"c'2 d' e' f'")
                >>> score = Score([staff])
                >>> attach(Tempo(Duration(1, 4), 60), staff[0])
                >>> label(staff).with_start_offsets(clock_time=True)
                >>> override(staff).text_script.staff_padding = 4
                >>> override(staff).tuplet_bracket.staff_padding = 0
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> print(format(score))
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

            **Example 3.** Labels logical tie start offsets with clock time and
            custom font size:

            ::

                >>> staff = Staff(r"c'2 d' e' f'")
                >>> score = Score([staff])
                >>> attach(Tempo(Duration(1, 4), 60), staff[0])
                >>> label(staff).with_start_offsets(
                ...     clock_time=True,
                ...     font_size=-3,
                ...     )
                >>> override(staff).text_script.staff_padding = 4
                >>> override(staff).tuplet_bracket.staff_padding = 0
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> print(format(score))
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
        logical_ties = iterate(self.client).by_logical_tie()
        for logical_tie in logical_ties:
            if clock_time:
                inspector = inspect_(logical_tie.head)
                timespan = inspector.get_timespan(in_seconds=True)
                start_offset = timespan.start_offset
                string = start_offset.to_clock_string()
                string = '"{}"'.format(string)
            else:
                timespan = inspect_(logical_tie.head).get_timespan()
                start_offset = timespan.start_offset
                string = str(start_offset)
            label = markuptools.Markup(string, direction=direction)
            if font_size is not None:
                label = label.fontsize(font_size)
            attach(label, logical_tie.head)

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Gets client of label agent.

        Returns component, selection, spanner or none.
        '''
        return self._client
