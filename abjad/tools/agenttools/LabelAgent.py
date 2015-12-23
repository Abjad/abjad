# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import durationtools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import iterate


class LabelAgent(abctools.AbjadObject):
    r'''A wrapper around the Abjad label methods.

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

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Gets client of inspection agent.

        Returns component, selection, spanner or none.
        '''
        return self._client

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

    ### PUBLIC METHODS ###

    def color_container(self, color):
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
                    \override Accidental #'color = #red
                    \override Beam #'color = #red
                    \override Dots #'color = #red
                    \override NoteHead #'color = #red
                    \override Rest #'color = #red
                    \override Stem #'color = #red
                    \override TupletBracket #'color = #red
                    \override TupletNumber #'color = #red
                    \time 2/8
                    c'8
                    d'8
                    \revert Accidental #'color
                    \revert Beam #'color
                    \revert Dots #'color
                    \revert NoteHead #'color
                    \revert Rest #'color
                    \revert Stem #'color
                    \revert TupletBracket #'color
                    \revert TupletNumber #'color
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

    def color_note_heads(self, color_map=None):
        r'''Colors note heads by `color_map`.

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
                    \tweak #'color #red
                    c''
                    \tweak #'color #red
                    d''
                    \tweak #'color #green
                    fs''
                    \tweak #'color #green
                    a''
                    \tweak #'color #blue
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
                \once \override NoteHead #'color = #red
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
                    \once \override NoteHead #'color = #(x11-color 'red)
                    c'8
                    \once \override NoteHead #'color = #(x11-color 'MediumBlue)
                    cs'8
                    \once \override NoteHead #'color = #(x11-color 'orange)
                    d'8
                    \once \override NoteHead #'color = #(x11-color 'LightSlateBlue)
                    ds'8
                    \once \override NoteHead #'color = #(x11-color 'ForestGreen)
                    e'8
                    \once \override NoteHead #'color = #(x11-color 'MediumOrchid)
                    f'8
                    \once \override NoteHead #'color = #(x11-color 'firebrick)
                    fs'8
                    \once \override NoteHead #'color = #(x11-color 'DeepPink)
                    g'8
                    \once \override NoteHead #'color = #(x11-color 'DarkOrange)
                    gs'8
                    \once \override NoteHead #'color = #(x11-color 'IndianRed)
                    a'8
                    \once \override NoteHead #'color = #(x11-color 'CadetBlue)
                    as'8
                    \once \override NoteHead #'color = #(x11-color 'SeaGreen)
                    b'8
                    \once \override NoteHead #'color = #(x11-color 'red)
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

    def color_leaves(self, color):
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
                    \once \override Accidental #'color = #red
                    \once \override Beam #'color = #red
                    \once \override Dots #'color = #red
                    \once \override NoteHead #'color = #red
                    \once \override Stem #'color = #red
                    cs'8. [
                    \once \override Dots #'color = #red
                    \once \override Rest #'color = #red
                    r8.
                    s8.
                    \once \override Accidental #'color = #red
                    \once \override Beam #'color = #red
                    \once \override Dots #'color = #red
                    \once \override NoteHead #'color = #red
                    \once \override Stem #'color = #red
                    <c' cs' a'>8. ]
                }

        Returns none.
        """
        for leaf in iterate(self.client).by_class(scoretools.Leaf):
            self._color_leaf(leaf, color)

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

    def with_durations(self, direction=Up):
        r'''Labels durations.


        ..  container:: example

            **Example 1.** Above staff:

            ::

                >>> staff = Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
                >>> label(staff).with_durations(direction=Up)
                >>> override(staff).text_script.staff_padding = 4
                >>> override(staff).tuplet_bracket.staff_padding = 0
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override TextScript #'staff-padding = #4
                    \override TupletBracket #'staff-padding = #0
                } {
                    \times 2/3 {
                        c'4
                            ^ \markup {
                                \small
                                    1/6
                                }
                        d'4
                            ^ \markup {
                                \small
                                    1/6
                                }
                        e'4 ~
                            ^ \markup {
                                \small
                                    5/12
                                }
                    }
                    e'4
                    ef'4
                        ^ \markup {
                            \small
                                1/4
                            }
                }

        ..  container:: example

            **Example 2.** Below staff:

            ::

                >>> staff = Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
                >>> label(staff).with_durations(direction=Down)
                >>> override(staff).text_script.staff_padding = 6
                >>> override(staff).tuplet_bracket.staff_padding = 0
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override TextScript #'staff-padding = #6
                    \override TupletBracket #'staff-padding = #0
                } {
                    \times 2/3 {
                        c'4
                            _ \markup {
                                \small
                                    1/6
                                }
                        d'4
                            _ \markup {
                                \small
                                    1/6
                                }
                        e'4 ~
                            _ \markup {
                                \small
                                    5/12
                                }
                    }
                    e'4
                    ef'4
                        _ \markup {
                            \small
                                1/4
                            }
                }

        Returns none.
        '''
        logical_ties = iterate(self.client).by_logical_tie()
        for logical_tie in logical_ties:
            duration = logical_tie.get_duration()
            label = markuptools.Markup(str(duration), direction=direction)
            label = label.small()
            attach(label, logical_tie.head)

    def with_intervals(self, direction=Up, prototype=None):
        r"""Labels intervals.

        ..  container:: example

            **Example 1.** Labels interval names:

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
                    \override TextScript #'staff-padding = #4
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

            **Example 2.** Labels interval class names:

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
                    \override TextScript #'staff-padding = #4
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

            **Example 3.** Labels interval numbers:

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
                    \override TextScript #'staff-padding = #4
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

            **Example 4.** Labels interval-class numbers:

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
                    \override TextScript #'staff-padding = #4
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

            **Example 5.** Labels inversion-equivalent interval-class numbers:

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
                    \override TextScript #'staff-padding = #4
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

    def with_leaf_indices(self, direction=Up):
        r'''Labels leaf indices.

        ..  container:: example

            **Example 1.** Labels leaf indices above staff:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> label(staff).with_leaf_indices(direction=Up)
                >>> override(staff).text_script.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript #'staff-padding = #2
                } {
                    c'8
                        ^ \markup {
                            \small
                                0
                            }
                    d'8
                        ^ \markup {
                            \small
                                1
                            }
                    e'8
                        ^ \markup {
                            \small
                                2
                            }
                    f'8
                        ^ \markup {
                            \small
                                3
                            }
                }

        ..  container:: example

            **Example 2.** Labels leaf indices below staff:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> label(staff).with_leaf_indices(direction=Down)
                >>> override(staff).text_script.staff_padding = 4
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript #'staff-padding = #4
                } {
                    c'8
                        _ \markup {
                            \small
                                0
                            }
                    d'8
                        _ \markup {
                            \small
                                1
                            }
                    e'8
                        _ \markup {
                            \small
                                2
                            }
                    f'8
                        _ \markup {
                            \small
                                3
                            }
                }

        Returns none.
        '''
        leaves = iterate(self.client).by_class(scoretools.Leaf)
        for index, leaf in enumerate(leaves):
            string = str(index)
            label = markuptools.Markup(string, direction=direction)
            label = label.small()
            attach(label, leaf)

    def with_pitches(self, direction=Up, prototype=None):
        r'''Labels pitches.

        ..  container:: example

            **Example 1.** Labels pitch names:

            ::

                >>> staff = Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                >>> label(staff).with_pitches(prototype=None)
                >>> override(staff).text_script.staff_padding = 4
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript #'staff-padding = #4
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

            **Example 2.** Labels pitch numbers:

            ::

                >>> staff = Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                >>> prototype = pitchtools.NumberedPitch
                >>> label(staff).with_pitches(prototype=prototype)
                >>> override(staff).text_script.staff_padding = 4
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript #'staff-padding = #4
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

            **Example 3.** Labels pitch-class numbers:

            ::

                >>> staff = Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                >>> prototype = pitchtools.NumberedPitchClass
                >>> label(staff).with_pitches(prototype=prototype)
                >>> override(staff).text_script.staff_padding = 4
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript #'staff-padding = #4
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
                attach(label, leaf)