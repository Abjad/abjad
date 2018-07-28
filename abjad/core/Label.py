import collections
import inspect
from abjad import enums
from abjad.indicators.LilyPondComment import LilyPondComment
from abjad.indicators.LilyPondLiteral import LilyPondLiteral
from abjad.markups import Markup
from abjad.markups import MarkupCommand
from abjad.mathtools.NonreducedFraction import NonreducedFraction
from abjad.pitch.IntervalClassVector import IntervalClassVector
from abjad.pitch.NamedInterval import NamedInterval
from abjad.pitch.NamedIntervalClass import NamedIntervalClass
from abjad.pitch.NamedPitch import NamedPitch
from abjad.pitch.NumberedInversionEquivalentIntervalClass import \
    NumberedInversionEquivalentIntervalClass
from abjad.pitch.NumberedInterval import NumberedInterval
from abjad.pitch.NumberedIntervalClass import NumberedIntervalClass
from abjad.pitch.NumberedPitch import NumberedPitch
from abjad.pitch.NumberedPitchClass import NumberedPitchClass
from abjad.pitch.PitchClassSet import PitchClassSet
from abjad.pitch.PitchSegment import PitchSegment
from abjad.pitch.SetClass import SetClass
from abjad.scheme import SchemeColor
from abjad.system.AbjadObject import AbjadObject
from abjad.top.attach import attach
from abjad.top.detach import detach
from abjad.top.inspect import inspect as abjad_inspect
from abjad.top.iterate import iterate
from abjad.top.new import new
from abjad.top.override import override
from abjad.top.select import select
from abjad.utilities.Duration import Duration
from abjad.utilities.Expression import Expression
from .Component import Component
from .Chord import Chord
from .Note import Note
from .Skip import Skip


class Label(AbjadObject):
    r"""
    Label.

    ..  container:: example

        Labels pitch names:

        ..  container:: example

            >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
            >>> abjad.label(staff).with_pitches(locale='us')

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    ^ \markup { C4 }
                    e'4
                    ^ \markup { E4 }
                    d'4
                    ^ \markup { D4 }
                    f'4
                    ^ \markup { F4 }
                }

        ..  container:: example expression

            >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
            >>> expression = abjad.label().with_pitches(locale='us')
            >>> abjad.f(expression)
            abjad.Expression(
                callbacks=[
                    abjad.Expression(
                        evaluation_template='abjad.core.Label',
                        is_initializer=True,
                        keywords={
                            'tag': None,
                            },
                        ),
                    abjad.Expression(
                        evaluation_template="{}.with_pitches(locale='us')",
                        qualified_method_name='abjad.core.Label.with_pitches',
                        ),
                    ],
                proxy_class=abjad.Label,
                )

            >>> expression(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    ^ \markup { C4 }
                    e'4
                    ^ \markup { E4 }
                    d'4
                    ^ \markup { D4 }
                    f'4
                    ^ \markup { F4 }
                }

    ..  container:: example

        Labels durations:

        ..  container:: example

            >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
            >>> abjad.label(staff).with_durations()

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    ^ \markup {
                        \fraction
                            1
                            4
                        }
                    e'4
                    ^ \markup {
                        \fraction
                            1
                            4
                        }
                    d'4
                    ^ \markup {
                        \fraction
                            1
                            4
                        }
                    f'4
                    ^ \markup {
                        \fraction
                            1
                            4
                        }
                }

        ..  container:: example expression

            >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
            >>> expression = abjad.label().with_durations()
            >>> abjad.f(expression)
            abjad.Expression(
                callbacks=[
                    abjad.Expression(
                        evaluation_template='abjad.core.Label',
                        is_initializer=True,
                        keywords={
                            'tag': None,
                            },
                        ),
                    abjad.Expression(
                        evaluation_template='{}.with_durations()',
                        qualified_method_name='abjad.core.Label.with_durations',
                        ),
                    ],
                proxy_class=abjad.Label,
                )

            >>> expression(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    ^ \markup {
                        \fraction
                            1
                            4
                        }
                    e'4
                    ^ \markup {
                        \fraction
                            1
                            4
                        }
                    d'4
                    ^ \markup {
                        \fraction
                            1
                            4
                        }
                    f'4
                    ^ \markup {
                        \fraction
                            1
                            4
                        }
                }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Collaborators'

    __slots__ = (
        '_client',
        '_deactivate',
        '_expression',
        '_tag',
        )

    _pc_number_to_color = {
        0: SchemeColor('red'),
        1: SchemeColor('MediumBlue'),
        2: SchemeColor('orange'),
        3: SchemeColor('LightSlateBlue'),
        4: SchemeColor('ForestGreen'),
        5: SchemeColor('MediumOrchid'),
        6: SchemeColor('firebrick'),
        7: SchemeColor('DeepPink'),
        8: SchemeColor('DarkOrange'),
        9: SchemeColor('IndianRed'),
        10: SchemeColor('CadetBlue'),
        11: SchemeColor('SeaGreen'),
        12: SchemeColor('LimeGreen'),
        }

    ### INITIALIZER ###

    def __init__(self, client=None, deactivate=None, tag=None):
        prototype = (
            Component,
            collections.Iterable,
            type(None),
            )
        if not isinstance(client, prototype):
            message = 'must be component, iterable or none: {!r}.'
            message = message.format(client)
            raise TypeError(message)
        self._client = client
        self._deactivate = deactivate
        self._expression = None
        self._tag = tag

    ### PRIVATE METHODS ###

    def _attach(self, label, leaf):
        attach(
            label,
            leaf,
            deactivate=self.deactivate,
            tag=self.tag,
            )

    def _color_leaf(self, leaf, color):
        if isinstance(leaf, Skip):
            comment = LilyPondComment(color)
            self._attach(comment, leaf)
        else:
            string = fr'\abjad_color_music "{color}"'
            literal = LilyPondLiteral(string)
            self._attach(literal, leaf)
        return leaf

    def _update_expression(self, frame):
        callback = Expression._frame_to_callback(frame)
        return self._expression.append_callback(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        """
        Gets client of label.

        Returns component, selection, spanner or none.
        """
        return self._client

    @property
    def deactivate(self):
        """
        Is true when deactivated label attaches to leaf.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._deactivate

    @property
    def tag(self):
        """
        Gets tag.

        Returns string or none.
        """
        return self._tag

    ### PUBLIC METHODS ###

    def color_container(self, color='red'):
        r"""
        Colors contents of ``container``.

        ..  container:: example

            Colors measure:

            ..  container:: example

                >>> measure = abjad.Measure((2, 8), "c'8 d'8")
                >>> abjad.label(measure).color_container('red')
                >>> abjad.show(measure) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(measure)
                    {   % measure
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
                    }   % measure

            ..  container:: example expression

                >>> measure = abjad.Measure((2, 8), "c'8 d'8")
                >>> expression = abjad.label().color_container('red')
                >>> expression(measure)
                >>> abjad.show(measure) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(measure)
                    {   % measure
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
                    }   % measure

        Returns none.
        """
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
        r"""
        Colors leaves.

        ..  container:: example

            Colors leaves red:

            ..  container:: example

                >>> staff = abjad.Staff("cs'8. r8. s8. <c' cs' a'>8.")
                >>> beam = abjad.Beam(beam_rests=True)
                >>> abjad.attach(beam, staff[:])
                >>> abjad.label(staff).color_leaves('red')
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        \abjad_color_music "red"
                        cs'8.
                        [
                        \abjad_color_music "red"
                        r8.
                        % red
                        s8.
                        \abjad_color_music "red"
                        <c' cs' a'>8.
                        ]
                    }

            ..  container:: example expression

                >>> staff = abjad.Staff("cs'8. r8. s8. <c' cs' a'>8.")
                >>> beam = abjad.Beam(beam_rests=True)
                >>> abjad.attach(beam, staff[:])
                >>> expression = abjad.label().color_leaves('red')
                >>> expression(staff)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        \abjad_color_music "red"
                        cs'8.
                        [
                        \abjad_color_music "red"
                        r8.
                        % red
                        s8.
                        \abjad_color_music "red"
                        <c' cs' a'>8.
                        ]
                    }

        Returns none.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        for leaf in iterate(self.client).leaves():
            self._color_leaf(leaf, color)

    def color_note_heads(self, color_map=None):
        r"""
        Colors note note-heads.

        ..  container:: example

            Colors chord note-heads:

            ..  container:: example

                >>> chord = abjad.Chord([12, 14, 18, 21, 23], (1, 4))
                >>> pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
                >>> colors = ['red', 'blue', 'green']
                >>> color_map = abjad.ColorMap(colors=colors, pitch_iterables=pitches)
                >>> abjad.label(chord).color_note_heads(color_map)
                >>> abjad.show(chord) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(chord)
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

                >>> chord = abjad.Chord([12, 14, 18, 21, 23], (1, 4))
                >>> pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
                >>> colors = ['red', 'blue', 'green']
                >>> color_map = abjad.ColorMap(colors=colors, pitch_iterables=pitches)
                >>> expression = abjad.label().color_note_heads(color_map)
                >>> expression(chord)
                >>> abjad.show(chord) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(chord)
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

                >>> note = abjad.Note("c'4")
                >>> abjad.label(note).color_note_heads(color_map)
                >>> abjad.show(note) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(note)
                    \once \override NoteHead.color = #red
                    c'4

            ..  container:: example expression

                >>> note = abjad.Note("c'4")
                >>> expression = abjad.label().color_note_heads(color_map)
                >>> expression(note)
                >>> abjad.show(note) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(note)
                    \once \override NoteHead.color = #red
                    c'4

        ..  container:: example

            Colors nothing:

            ..  container:: example

                >>> staff = abjad.Staff()
                >>> abjad.label(staff).color_note_heads(color_map)

            ..  container:: example expression

                >>> staff = abjad.Staff()
                >>> expression = abjad.label().color_note_heads(color_map)
                >>> expression(staff)

        ..  container:: example

            Colors note-heads:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 cs'8 d'8 ds'8 e'8 f'8 fs'8 g'8 gs'8 a'8 as'8 b'8 c''8")
                >>> abjad.label(staff).color_note_heads()
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
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

                >>> staff = abjad.Staff("c'8 cs'8 d'8 ds'8 e'8 f'8 fs'8 g'8 gs'8 a'8 as'8 b'8 c''8")
                >>> expression = abjad.label().color_note_heads()
                >>> expression(staff)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
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
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        color_map = color_map or self._pc_number_to_color
        for leaf in iterate(self.client).leaves():
            if isinstance(leaf, Chord):
                for note_head in leaf.note_heads:
                    number = note_head.written_pitch.number
                    pc = NumberedPitchClass(number)
                    color = color_map.get(pc, None)
                    if color is not None:
                        note_head.tweaks.color = color
            elif isinstance(leaf, Note):
                note_head = leaf.note_head
                number = note_head.written_pitch.number
                pc = NumberedPitchClass(number)
                color = color_map[pc.number]
                if color is not None:
                    override(leaf).note_head.color = color

    def remove_markup(self):
        r"""
        Removes markup from leaves.

        ..  container:: example

            Removes markup:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> abjad.label(staff).with_pitches()
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'8
                        ^ \markup { c' }
                        d'8
                        ^ \markup { d' }
                        e'8
                        ^ \markup { e' }
                        f'8
                        ^ \markup { f' }
                    }

                >>> abjad.label(staff).remove_markup()
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'8
                        d'8
                        e'8
                        f'8
                    }

            ..  container:: example expression

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> expression = abjad.label().with_pitches()
                >>> expression(staff)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'8
                        ^ \markup { c' }
                        d'8
                        ^ \markup { d' }
                        e'8
                        ^ \markup { e' }
                        f'8
                        ^ \markup { f' }
                    }

                >>> expression = abjad.label().remove_markup()
                >>> expression(staff)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'8
                        d'8
                        e'8
                        f'8
                    }

        Returns none.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        for leaf in iterate(self.client).leaves():
            detach(Markup, leaf)

    def vertical_moments(self, direction=enums.Up, prototype=None):
        r'''
        Labels vertical moments.

        ..  container:: example

            Labels indices:

            ..  container:: example

                >>> staff_group = abjad.StaffGroup([])
                >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                >>> staff_group.append(staff)
                >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                >>> staff_group.append(staff)
                >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                >>> staff_group.append(staff)
                >>> abjad.label(staff_group).vertical_moments()
                >>> abjad.show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff_group)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
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
                        \new Staff
                        {
                            \clef "alto"
                            g4
                            f4
                            ^ \markup {
                                \tiny
                                    2
                                }
                        }
                        \new Staff
                        {
                            \clef "bass"
                            c,2
                        }
                    >>

            ..  container:: example expression

                >>> staff_group = abjad.StaffGroup([])
                >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                >>> staff_group.append(staff)
                >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                >>> staff_group.append(staff)
                >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                >>> staff_group.append(staff)
                >>> expression = abjad.label().vertical_moments()
                >>> expression(staff_group)
                >>> abjad.show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff_group)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
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
                        \new Staff
                        {
                            \clef "alto"
                            g4
                            f4
                            ^ \markup {
                                \tiny
                                    2
                                }
                        }
                        \new Staff
                        {
                            \clef "bass"
                            c,2
                        }
                    >>

        ..  container:: example

            Labels pitch numbers:

            ..  container:: example

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
                >>> abjad.show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff_group)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
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
                        \new Staff
                        {
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
                        \new Staff
                        {
                            \clef "bass"
                            c,2
                        }
                    >>

            ..  container:: example expression

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
                >>> abjad.show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff_group)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
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
                        \new Staff
                        {
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
                        \new Staff
                        {
                            \clef "bass"
                            c,2
                        }
                    >>

        ..  container:: example

            Labels pitch-class numbers:

            ..  container:: example

                >>> staff_group = abjad.StaffGroup([])
                >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                >>> staff_group.append(staff)
                >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                >>> staff_group.append(staff)
                >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                >>> staff_group.append(staff)
                >>> prototype = abjad.NumberedPitchClass
                >>> abjad.label(staff_group).vertical_moments(prototype=prototype)
                >>> abjad.show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff_group)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
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
                        \new Staff
                        {
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
                        \new Staff
                        {
                            \clef "bass"
                            c,2
                        }
                    >>

            ..  container:: example expression

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
                >>> abjad.show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff_group)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
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
                        \new Staff
                        {
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
                        \new Staff
                        {
                            \clef "bass"
                            c,2
                        }
                    >>

        ..  container:: example

            Labels interval numbers:

            ..  container:: example

                >>> staff_group = abjad.StaffGroup([])
                >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                >>> staff_group.append(staff)
                >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                >>> staff_group.append(staff)
                >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                >>> staff_group.append(staff)
                >>> prototype = abjad.NumberedInterval
                >>> abjad.label(staff_group).vertical_moments(prototype=prototype)
                >>> abjad.show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff_group)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
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
                        \new Staff
                        {
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
                        \new Staff
                        {
                            \clef "bass"
                            c,2
                        }
                    >>

            ..  container:: example expression

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
                >>> abjad.show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff_group)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
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
                        \new Staff
                        {
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
                        \new Staff
                        {
                            \clef "bass"
                            c,2
                        }
                    >>

        ..  container:: example

            Labels interval-class numbers:

            ..  container:: example

                >>> staff_group = abjad.StaffGroup([])
                >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                >>> staff_group.append(staff)
                >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                >>> staff_group.append(staff)
                >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                >>> staff_group.append(staff)
                >>> prototype = abjad.NumberedIntervalClass
                >>> abjad.label(staff_group).vertical_moments(prototype=prototype)
                >>> abjad.show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff_group)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
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
                        \new Staff
                        {
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
                        \new Staff
                        {
                            \clef "bass"
                            c,2
                        }
                    >>

            ..  container:: example expression

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
                >>> abjad.show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff_group)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
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
                        \new Staff
                        {
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
                        \new Staff
                        {
                            \clef "bass"
                            c,2
                        }
                    >>

        ..  container:: example

            Labels interval-class vectors:

            ..  container:: example

                >>> staff_group = abjad.StaffGroup([])
                >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                >>> staff_group.append(staff)
                >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                >>> staff_group.append(staff)
                >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                >>> staff_group.append(staff)
                >>> prototype = abjad.IntervalClassVector
                >>> abjad.label(staff_group).vertical_moments(prototype=prototype)
                >>> abjad.show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff_group)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
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
                        \new Staff
                        {
                            \clef "alto"
                            g4
                            f4
                            ^ \markup {
                                \tiny
                                    \tiny
                                        0011010
                                }
                        }
                        \new Staff
                        {
                            \clef "bass"
                            c,2
                        }
                    >>

            ..  container:: example expression

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
                >>> abjad.show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff_group)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
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
                        \new Staff
                        {
                            \clef "alto"
                            g4
                            f4
                            ^ \markup {
                                \tiny
                                    \tiny
                                        0011010
                                }
                        }
                        \new Staff
                        {
                            \clef "bass"
                            c,2
                        }
                    >>

        ..  container:: example

            Labels set-classes:

            ..  container:: example

                >>> staff_group = abjad.StaffGroup([])
                >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
                >>> staff_group.append(staff)
                >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
                >>> staff_group.append(staff)
                >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
                >>> staff_group.append(staff)
                >>> prototype = abjad.SetClass()
                >>> abjad.label(staff_group).vertical_moments(prototype=prototype)
                >>> abjad.show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff_group)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
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
                        \new Staff
                        {
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
                        \new Staff
                        {
                            \clef "bass"
                            c,2
                        }
                    >>

            ..  container:: example expression

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
                >>> abjad.show(staff_group) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff_group)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
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
                        \new Staff
                        {
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
                        \new Staff
                        {
                            \clef "bass"
                            c,2
                        }
                    >>

        Set ``prototype`` to one of the classes shown above.

        Returns none.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        prototype = prototype or int
        vertical_moments = iterate(self.client).vertical_moments()
        for index, vertical_moment in enumerate(vertical_moments):
            label = None
            if prototype is int:
                label = Markup(index, direction=direction)
            elif prototype is NumberedPitch:
                leaves = vertical_moment.leaves
                pitches = PitchSegment.from_selection(leaves)
                if not pitches:
                    continue
                pitch_numbers = [pitch.number for pitch in pitches]
                pitch_numbers = [Markup(_) for _ in pitch_numbers]
                label = Markup.column(pitch_numbers, direction=direction)
            elif prototype is NumberedPitchClass:
                leaves = vertical_moment.leaves
                pitches = PitchSegment.from_selection(leaves)
                if not pitches:
                    continue
                pitch_classes = [pitch.pitch_class.number for pitch in pitches]
                pitch_classes = list(set(pitch_classes))
                pitch_classes.sort()
                pitch_classes.reverse()
                numbers = [str(_) for _ in pitch_classes]
                markup = [Markup(_) for _ in numbers]
                label = Markup.column(markup, direction=direction)
            elif prototype is NumberedInterval:
                leaves = vertical_moment.leaves
                notes = [_ for _ in leaves if isinstance(_, Note)]
                if not notes:
                    continue
                notes.sort(key=lambda x: x.written_pitch.number)
                notes.reverse()
                bass_note = notes[-1]
                upper_notes = notes[:-1]
                named_intervals = []
                for upper_note in upper_notes:
                    named_interval = NamedInterval.from_pitch_carriers(
                        bass_note.written_pitch,
                        upper_note.written_pitch,
                        )
                    named_intervals.append(named_interval)
                numbers = [x.number for x in named_intervals]
                markup = [Markup(_) for _ in numbers]
                label = Markup.column(markup, direction=direction)
            elif prototype is NumberedIntervalClass:
                leaves = vertical_moment.leaves
                notes = [_ for _ in leaves if isinstance(_, Note)]
                if not notes:
                    continue
                notes.sort(key=lambda x: x.written_pitch.number)
                notes.reverse()
                bass_note = notes[-1]
                upper_notes = notes[:-1]
                numbers = []
                for upper_note in upper_notes:
                    interval = NamedInterval.from_pitch_carriers(
                        bass_note.written_pitch,
                        upper_note.written_pitch,
                        )
                    interval_class = NumberedIntervalClass(interval)
                    number = interval_class.number
                    numbers.append(number)
                markup = [Markup(_) for _ in numbers]
                label = Markup.column(markup, direction=direction)
            elif prototype is IntervalClassVector:
                leaves = vertical_moment.leaves
                pitches = PitchSegment.from_selection(leaves)
                if not pitches:
                    continue
                interval_class_vector = IntervalClassVector(
                    pitches,
                    item_class=NumberedInversionEquivalentIntervalClass,
                    )
                markup = interval_class_vector._label
                label = Markup(markup, direction=direction)
            elif (prototype is SetClass or
                isinstance(prototype, SetClass)):
                if prototype is SetClass:
                    prototype = prototype()
                assert isinstance(prototype, SetClass)
                leaves = vertical_moment.leaves
                pitch_class_set = PitchClassSet.from_selection(leaves)
                if not pitch_class_set:
                    continue
                set_class = SetClass.from_pitch_class_set(
                    pitch_class_set,
                    lex_rank=prototype.lex_rank,
                    transposition_only=prototype.transposition_only,
                    )
                string = str(set_class)
                command = MarkupCommand('line', [string])
                label = Markup(command, direction=direction)
            else:
                message = 'unknown prototype: {!r}.'
                message = message.format(prototype)
                raise TypeError(message)
            if label is not None:
                label = label.tiny()
                if direction is enums.Up:
                    leaf = vertical_moment.start_leaves[0]
                else:
                    leaf = vertical_moment.start_leaves[-1]
                self._attach(label, leaf)

    def with_durations(self, direction=enums.Up, denominator=None):
        r"""Labels logical ties with durations.

        ..  container:: example

            Labels logical tie durations:

            ..  container:: example

                >>> staff = abjad.Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")
                >>> abjad.label(staff).with_durations()
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4.
                        ^ \markup {
                            \fraction
                                3
                                8
                            }
                        d'8
                        ^ \markup {
                            \fraction
                                1
                                2
                            }
                        ~
                        d'4.
                        e'16
                        ^ \markup {
                            \fraction
                                1
                                16
                            }
                        [
                        ef'16
                        ^ \markup {
                            \fraction
                                1
                                16
                            }
                        ]
                    }

            ..  container:: example expression

                >>> staff = abjad.Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")
                >>> expression = abjad.label().with_durations()
                >>> expression(staff)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4.
                        ^ \markup {
                            \fraction
                                3
                                8
                            }
                        d'8
                        ^ \markup {
                            \fraction
                                1
                                2
                            }
                        ~
                        d'4.
                        e'16
                        ^ \markup {
                            \fraction
                                1
                                16
                            }
                        [
                        ef'16
                        ^ \markup {
                            \fraction
                                1
                                16
                            }
                        ]
                    }

        ..  container:: example

            Labels logical ties with preferred denominator:

            ..  container:: example

                >>> staff = abjad.Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")
                >>> abjad.label(staff).with_durations(denominator=16)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4.
                        ^ \markup {
                            \fraction
                                6
                                16
                            }
                        d'8
                        ^ \markup {
                            \fraction
                                8
                                16
                            }
                        ~
                        d'4.
                        e'16
                        ^ \markup {
                            \fraction
                                1
                                16
                            }
                        [
                        ef'16
                        ^ \markup {
                            \fraction
                                1
                                16
                            }
                        ]
                    }

            ..  container:: example expression

                >>> staff = abjad.Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")
                >>> expression = abjad.label().with_durations(denominator=16)
                >>> expression(staff)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4.
                        ^ \markup {
                            \fraction
                                6
                                16
                            }
                        d'8
                        ^ \markup {
                            \fraction
                                8
                                16
                            }
                        ~
                        d'4.
                        e'16
                        ^ \markup {
                            \fraction
                                1
                                16
                            }
                        [
                        ef'16
                        ^ \markup {
                            \fraction
                                1
                                16
                            }
                        ]
                    }

        Returns none.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        for logical_tie in iterate(self.client).logical_ties():
            duration = abjad_inspect(logical_tie).duration()
            if denominator is not None:
                duration = NonreducedFraction(duration)
                duration = duration.with_denominator(denominator)
            pair = duration.pair
            label = Markup.fraction(*pair, direction=direction)
            self._attach(label, logical_tie.head)

    def with_indices(self, direction=enums.Up, prototype=None):
        r"""Labels logical ties with indices.

        ..  container:: example

            Labels logical tie indices:

            ..  container:: example

                >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                >>> abjad.label(staff).with_indices()
                >>> abjad.override(staff).text_script.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #2
                    }
                    {
                        <c' bf'>8
                        ^ \markup { 0 }
                        <g' a'>4
                        ^ \markup { 1 }
                        af'8
                        ^ \markup { 2 }
                        ~
                        af'8
                        gf'8
                        ^ \markup { 3 }
                        ~
                        gf'4
                    }

            ..  container:: example expression

                >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                >>> expression = abjad.label().with_indices()
                >>> expression(staff)
                >>> abjad.override(staff).text_script.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #2
                    }
                    {
                        <c' bf'>8
                        ^ \markup { 0 }
                        <g' a'>4
                        ^ \markup { 1 }
                        af'8
                        ^ \markup { 2 }
                        ~
                        af'8
                        gf'8
                        ^ \markup { 3 }
                        ~
                        gf'4
                    }

        ..  container:: example

            Labels note indices:

            ..  container:: example

                >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                >>> abjad.label(staff).with_indices(prototype=abjad.Note)
                >>> abjad.override(staff).text_script.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #2
                    }
                    {
                        <c' bf'>8
                        <g' a'>4
                        af'8
                        ^ \markup { 0 }
                        ~
                        af'8
                        ^ \markup { 1 }
                        gf'8
                        ^ \markup { 2 }
                        ~
                        gf'4
                        ^ \markup { 3 }
                    }

            ..  container:: example expression

                >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                >>> expression = abjad.label().with_indices(
                ...     prototype=abjad.Note,
                ...     )
                >>> expression(staff)
                >>> abjad.override(staff).text_script.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #2
                    }
                    {
                        <c' bf'>8
                        <g' a'>4
                        af'8
                        ^ \markup { 0 }
                        ~
                        af'8
                        ^ \markup { 1 }
                        gf'8
                        ^ \markup { 2 }
                        ~
                        gf'4
                        ^ \markup { 3 }
                    }

        ..  container:: example

            Labels chord indices:

            ..  container:: example

                >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                >>> abjad.label(staff).with_indices(prototype=abjad.Chord)
                >>> abjad.override(staff).text_script.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #2
                    }
                    {
                        <c' bf'>8
                        ^ \markup { 0 }
                        <g' a'>4
                        ^ \markup { 1 }
                        af'8
                        ~
                        af'8
                        gf'8
                        ~
                        gf'4
                    }

            ..  container:: example expression

                >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                >>> expression = abjad.label().with_indices(
                ...     prototype=abjad.Chord,
                ...     )
                >>> expression(staff)
                >>> abjad.override(staff).text_script.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #2
                    }
                    {
                        <c' bf'>8
                        ^ \markup { 0 }
                        <g' a'>4
                        ^ \markup { 1 }
                        af'8
                        ~
                        af'8
                        gf'8
                        ~
                        gf'4
                    }

        ..  container:: example

            Labels leaf indices:

            ..  container:: example

                >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                >>> abjad.label(staff).with_indices(prototype=abjad.Leaf)
                >>> abjad.override(staff).text_script.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #2
                    }
                    {
                        <c' bf'>8
                        ^ \markup { 0 }
                        <g' a'>4
                        ^ \markup { 1 }
                        af'8
                        ^ \markup { 2 }
                        ~
                        af'8
                        ^ \markup { 3 }
                        gf'8
                        ^ \markup { 4 }
                        ~
                        gf'4
                        ^ \markup { 5 }
                    }

            ..  container:: example expression

                >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                >>> expression = abjad.label().with_indices(
                ...     prototype=abjad.Leaf,
                ...     )
                >>> expression(staff)
                >>> abjad.override(staff).text_script.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #2
                    }
                    {
                        <c' bf'>8
                        ^ \markup { 0 }
                        <g' a'>4
                        ^ \markup { 1 }
                        af'8
                        ^ \markup { 2 }
                        ~
                        af'8
                        ^ \markup { 3 }
                        gf'8
                        ^ \markup { 4 }
                        ~
                        gf'4
                        ^ \markup { 5 }
                    }

        ..  container:: example

            Labels tuplet indices:

            ..  container:: example

                >>> tuplet = abjad.Tuplet((2, 3), "c'8 [ d'8 e'8 ]")
                >>> staff = abjad.Staff(4 * tuplet)
                >>> abjad.label(staff).with_indices(prototype=abjad.Tuplet)
                >>> abjad.override(staff).text_script.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #2
                    }
                    {
                        \times 2/3 {
                            c'8
                            ^ \markup { 0 }
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                            ^ \markup { 1 }
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                            ^ \markup { 2 }
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                            ^ \markup { 3 }
                            d'8
                            e'8
                        }
                    }

            ..  container:: example expression

                >>> tuplet = abjad.Tuplet((2, 3), "c'8 [ d'8 e'8 ]")
                >>> staff = abjad.Staff(4 * tuplet)
                >>> expression = abjad.label().with_indices(
                ...     prototype=abjad.Tuplet,
                ...     )
                >>> expression(staff)
                >>> abjad.override(staff).text_script.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #2
                    }
                    {
                        \times 2/3 {
                            c'8
                            ^ \markup { 0 }
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                            ^ \markup { 1 }
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                            ^ \markup { 2 }
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                            ^ \markup { 3 }
                            d'8
                            e'8
                        }
                    }

        Returns none.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if prototype is None:
            items = iterate(self.client).logical_ties()
        else:
            items = iterate(self.client).components(prototype=prototype)
        items = list(items)
        for index, item in enumerate(items):
            string = str(index)
            label = Markup(string, direction=direction)
            leaves = select(item).leaves()
            first_leaf = leaves[0]
            self._attach(label, first_leaf)

    def with_intervals(self, direction=enums.Up, prototype=None):
        r"""
        Labels consecutive notes with intervals.

        ..  container:: example

            Labels consecutive notes with interval names:

            ..  container:: example

                >>> maker = abjad.NoteMaker()
                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = maker(pitch_numbers, [(1, 4)])
                >>> staff = abjad.Staff(notes)
                >>> abjad.label(staff).with_intervals(prototype=None)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        c'4
                        ^ \markup { +A15 }
                        cs'''4
                        ^ \markup { -M9 }
                        b'4
                        ^ \markup { -A9 }
                        af4
                        ^ \markup { -m7 }
                        bf,4
                        ^ \markup { +A1 }
                        b,4
                        ^ \markup { +m14 }
                        a'4
                        ^ \markup { +m2 }
                        bf'4
                    }

            ..  container:: example expression

                >>> maker = abjad.NoteMaker()
                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = maker(pitch_numbers, [(1, 4)])
                >>> staff = abjad.Staff(notes)
                >>> expression = abjad.label().with_intervals(prototype=None)
                >>> expression(staff)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        c'4
                        ^ \markup { +A15 }
                        cs'''4
                        ^ \markup { -M9 }
                        b'4
                        ^ \markup { -A9 }
                        af4
                        ^ \markup { -m7 }
                        bf,4
                        ^ \markup { +A1 }
                        b,4
                        ^ \markup { +m14 }
                        a'4
                        ^ \markup { +m2 }
                        bf'4
                    }

        ..  container:: example

            Labels consecutive notes with interval-class names:

            ..  container:: example

                >>> maker = abjad.NoteMaker()
                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = maker(pitch_numbers, [(1, 4)])
                >>> staff = abjad.Staff(notes)
                >>> prototype = abjad.NamedIntervalClass
                >>> abjad.label(staff).with_intervals(prototype=prototype)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        c'4
                        ^ \markup { +A1 }
                        cs'''4
                        ^ \markup { -M2 }
                        b'4
                        ^ \markup { -A2 }
                        af4
                        ^ \markup { -m7 }
                        bf,4
                        ^ \markup { +A1 }
                        b,4
                        ^ \markup { +m7 }
                        a'4
                        ^ \markup { +m2 }
                        bf'4
                    }

            ..  container:: example expression

                >>> maker = abjad.NoteMaker()
                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = maker(pitch_numbers, [(1, 4)])
                >>> staff = abjad.Staff(notes)
                >>> prototype = abjad.NamedIntervalClass
                >>> expression = abjad.label().with_intervals(prototype=prototype)
                >>> expression(staff)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        c'4
                        ^ \markup { +A1 }
                        cs'''4
                        ^ \markup { -M2 }
                        b'4
                        ^ \markup { -A2 }
                        af4
                        ^ \markup { -m7 }
                        bf,4
                        ^ \markup { +A1 }
                        b,4
                        ^ \markup { +m7 }
                        a'4
                        ^ \markup { +m2 }
                        bf'4
                    }

        ..  container:: example

            Labels consecutive notes with interval numbers:

            ..  container:: example

                >>> maker = abjad.NoteMaker()
                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = maker(pitch_numbers, [(1, 4)])
                >>> staff = abjad.Staff(notes)
                >>> prototype = abjad.NumberedInterval
                >>> abjad.label(staff).with_intervals(prototype=prototype)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        c'4
                        ^ \markup { +25 }
                        cs'''4
                        ^ \markup { -14 }
                        b'4
                        ^ \markup { -15 }
                        af4
                        ^ \markup { -10 }
                        bf,4
                        ^ \markup { +1 }
                        b,4
                        ^ \markup { +22 }
                        a'4
                        ^ \markup { +1 }
                        bf'4
                    }

            ..  container:: example expression

                >>> maker = abjad.NoteMaker()
                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = maker(pitch_numbers, [(1, 4)])
                >>> staff = abjad.Staff(notes)
                >>> prototype = abjad.NumberedInterval
                >>> expression = abjad.label().with_intervals(prototype=prototype)
                >>> expression(staff)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        c'4
                        ^ \markup { +25 }
                        cs'''4
                        ^ \markup { -14 }
                        b'4
                        ^ \markup { -15 }
                        af4
                        ^ \markup { -10 }
                        bf,4
                        ^ \markup { +1 }
                        b,4
                        ^ \markup { +22 }
                        a'4
                        ^ \markup { +1 }
                        bf'4
                    }


        ..  container:: example

            Labels consecutive notes with interval-class numbers:

            ..  container:: example

                >>> maker = abjad.NoteMaker()
                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = maker(pitch_numbers, [(1, 4)])
                >>> staff = abjad.Staff(notes)
                >>> prototype = abjad.NumberedIntervalClass
                >>> abjad.label(staff).with_intervals(prototype=prototype)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        c'4
                        ^ \markup { +1 }
                        cs'''4
                        ^ \markup { -2 }
                        b'4
                        ^ \markup { -3 }
                        af4
                        ^ \markup { -10 }
                        bf,4
                        ^ \markup { +1 }
                        b,4
                        ^ \markup { +10 }
                        a'4
                        ^ \markup { +1 }
                        bf'4
                    }

            ..  container:: example expression

                >>> maker = abjad.NoteMaker()
                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = maker(pitch_numbers, [(1, 4)])
                >>> staff = abjad.Staff(notes)
                >>> prototype = abjad.NumberedIntervalClass
                >>> expression = abjad.label().with_intervals(prototype=prototype)
                >>> expression(staff)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        c'4
                        ^ \markup { +1 }
                        cs'''4
                        ^ \markup { -2 }
                        b'4
                        ^ \markup { -3 }
                        af4
                        ^ \markup { -10 }
                        bf,4
                        ^ \markup { +1 }
                        b,4
                        ^ \markup { +10 }
                        a'4
                        ^ \markup { +1 }
                        bf'4
                    }

        ..  container:: example

            Labels consecutive notes with inversion-equivalent interval-class
            numbers:

            ..  container:: example

                >>> maker = abjad.NoteMaker()
                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = maker(pitch_numbers, [(1, 4)])
                >>> staff = abjad.Staff(notes)
                >>> prototype = abjad.NumberedInversionEquivalentIntervalClass
                >>> abjad.label(staff).with_intervals(prototype=prototype)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        c'4
                        ^ \markup { 1 }
                        cs'''4
                        ^ \markup { 2 }
                        b'4
                        ^ \markup { 3 }
                        af4
                        ^ \markup { 2 }
                        bf,4
                        ^ \markup { 1 }
                        b,4
                        ^ \markup { 2 }
                        a'4
                        ^ \markup { 1 }
                        bf'4
                    }

            ..  container:: example expression

                >>> maker = abjad.NoteMaker()
                >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
                >>> notes = maker(pitch_numbers, [(1, 4)])
                >>> staff = abjad.Staff(notes)
                >>> prototype = abjad.NumberedInversionEquivalentIntervalClass
                >>> expression = abjad.label().with_intervals(prototype=prototype)
                >>> expression(staff)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        c'4
                        ^ \markup { 1 }
                        cs'''4
                        ^ \markup { 2 }
                        b'4
                        ^ \markup { 3 }
                        af4
                        ^ \markup { 2 }
                        bf,4
                        ^ \markup { 1 }
                        b,4
                        ^ \markup { 2 }
                        a'4
                        ^ \markup { 1 }
                        bf'4
                    }

        Returns none.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        prototype = prototype or NamedInterval
        for note in  iterate(self.client).leaves(Note):
            label = None
            next_leaf = abjad_inspect(note).leaf(1)
            if isinstance(next_leaf, Note):
                interval = NamedInterval.from_pitch_carriers(
                    note,
                    next_leaf,
                    )
                if prototype is NamedInterval:
                    label = Markup(interval, direction=direction)
                elif prototype is NamedIntervalClass:
                    label = NamedIntervalClass(interval)
                    label = Markup(label, direction=direction)
                elif prototype is NumberedInterval:
                    label = NumberedInterval(interval)
                    label = Markup(label, direction=direction)
                elif prototype is NumberedIntervalClass:
                    label = NumberedIntervalClass(interval)
                    label = Markup(label, direction=direction)
                elif prototype is NumberedInversionEquivalentIntervalClass:
                    label = NumberedInversionEquivalentIntervalClass(interval)
                    label = Markup(label, direction=direction)
                if label is not None:
                    self._attach(label, note)

    def with_pitches(self, direction=enums.Up, locale=None, prototype=None):
        r"""
        Labels logical ties with pitches.

        ..  container:: example

            Labels logical ties with pitch names:

            ..  container:: example

                >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                >>> abjad.label(staff).with_pitches(prototype=None)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        <a d' fs'>4
                        ^ \markup {
                            \column
                                {
                                    fs'
                                    d'
                                    a
                                }
                            }
                        g'4
                        ^ \markup { g' }
                        ~
                        g'8
                        r8
                        fs''4
                        ^ \markup { fs'' }
                    }

            ..  container:: example expression

                >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                >>> expression = abjad.label().with_pitches(prototype=None)
                >>> expression(staff)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        <a d' fs'>4
                        ^ \markup {
                            \column
                                {
                                    fs'
                                    d'
                                    a
                                }
                            }
                        g'4
                        ^ \markup { g' }
                        ~
                        g'8
                        r8
                        fs''4
                        ^ \markup { fs'' }
                    }

        ..  container:: example

            Labels logical ties with American pitch names:

            ..  container:: example

                >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                >>> abjad.label(staff).with_pitches(locale='us', prototype=None)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        <a d' fs'>4
                        ^ \markup {
                            \column
                                {
                                    "F#4"
                                    D4
                                    A3
                                }
                            }
                        g'4
                        ^ \markup { G4 }
                        ~
                        g'8
                        r8
                        fs''4
                        ^ \markup { "F#5" }
                    }

            ..  container:: example expression

                >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                >>> expression = abjad.label().with_pitches(locale='us', prototype=None)
                >>> expression(staff)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        <a d' fs'>4
                        ^ \markup {
                            \column
                                {
                                    "F#4"
                                    D4
                                    A3
                                }
                            }
                        g'4
                        ^ \markup { G4 }
                        ~
                        g'8
                        r8
                        fs''4
                        ^ \markup { "F#5" }
                    }

        ..  container:: example

            Labels logical ties with pitch numbers:

            ..  container:: example

                >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                >>> prototype = abjad.NumberedPitch
                >>> abjad.label(staff).with_pitches(prototype=prototype)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        <a d' fs'>4
                        ^ \markup {
                            \column
                                {
                                    6
                                    2
                                    -3
                                }
                            }
                        g'4
                        ^ \markup { 7 }
                        ~
                        g'8
                        r8
                        fs''4
                        ^ \markup { 18 }
                    }

            ..  container:: example expression

                >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                >>> prototype = abjad.NumberedPitch
                >>> expression = abjad.label().with_pitches(prototype=prototype)
                >>> expression(staff)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        <a d' fs'>4
                        ^ \markup {
                            \column
                                {
                                    6
                                    2
                                    -3
                                }
                            }
                        g'4
                        ^ \markup { 7 }
                        ~
                        g'8
                        r8
                        fs''4
                        ^ \markup { 18 }
                    }

        ..  container:: example

            Labels logical ties with pitch-class numbers:

            ..  container:: example

                >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                >>> prototype = abjad.NumberedPitchClass
                >>> abjad.label(staff).with_pitches(prototype=prototype)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        <a d' fs'>4
                        ^ \markup {
                            \column
                                {
                                    6
                                    2
                                    9
                                }
                            }
                        g'4
                        ^ \markup { 7 }
                        ~
                        g'8
                        r8
                        fs''4
                        ^ \markup { 6 }
                    }

            ..  container:: example expression

                >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
                >>> prototype = abjad.NumberedPitchClass
                >>> expression = abjad.label().with_pitches(prototype=prototype)
                >>> expression(staff)
                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                    }
                    {
                        <a d' fs'>4
                        ^ \markup {
                            \column
                                {
                                    6
                                    2
                                    9
                                }
                            }
                        g'4
                        ^ \markup { 7 }
                        ~
                        g'8
                        r8
                        fs''4
                        ^ \markup { 6 }
                    }

        ..  container:: example

            Labels logical ties with pitch names (filtered by selection):

            ..  container:: example

                >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
                >>> string = 'Horizontal_bracket_engraver'
                >>> voice.consists_commands.append(string)
                >>> selections = [voice[:2], voice[-2:]]
                >>> for selection in selections:
                ...     spanner = abjad.HorizontalBracket()
                ...     abjad.attach(spanner, selection)
                ...
                >>> abjad.label(selections).with_pitches()
                >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                >>> abjad.override(voice).text_script.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    }
                    {
                        df''4
                        ^ \markup { df'' }
                        \startGroup
                        c''4
                        ^ \markup { c'' }
                        \stopGroup
                        f'4
                        fs'4
                        d''4
                        ^ \markup { d'' }
                        \startGroup
                        ds''4
                        ^ \markup { ds'' }
                        \stopGroup
                    }

            ..  container:: example expression

                >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
                >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                >>> selections = [voice[:2], voice[-2:]]
                >>> for selection in selections:
                ...     spanner = abjad.HorizontalBracket()
                ...     abjad.attach(spanner, selection)
                ...
                >>> expression = abjad.label().with_pitches()
                >>> expression(selections)
                >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                >>> abjad.override(voice).text_script.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    }
                    {
                        df''4
                        ^ \markup { df'' }
                        \startGroup
                        c''4
                        ^ \markup { c'' }
                        \stopGroup
                        f'4
                        fs'4
                        d''4
                        ^ \markup { d'' }
                        \startGroup
                        ds''4
                        ^ \markup { ds'' }
                        \stopGroup
                    }

        ..  container:: example

            Labels logical ties with pitch numbers (filtered by selection):

            ..  container:: example

                >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
                >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                >>> selections = [voice[:2], voice[-2:]]
                >>> for selection in selections:
                ...     spanner = abjad.HorizontalBracket()
                ...     abjad.attach(spanner, selection)
                ...
                >>> prototype = abjad.NumberedPitch
                >>> abjad.label(selections).with_pitches(prototype=prototype)
                >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                >>> abjad.override(voice).text_script.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    }
                    {
                        df''4
                        ^ \markup { 13 }
                        \startGroup
                        c''4
                        ^ \markup { 12 }
                        \stopGroup
                        f'4
                        fs'4
                        d''4
                        ^ \markup { 14 }
                        \startGroup
                        ds''4
                        ^ \markup { 15 }
                        \stopGroup
                    }

            ..  container:: example expression

                >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
                >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                >>> selections = [voice[:2], voice[-2:]]
                >>> for selection in selections:
                ...     spanner = abjad.HorizontalBracket()
                ...     abjad.attach(spanner, selection)
                ...
                >>> prototype = abjad.NumberedPitch
                >>> expression = abjad.label().with_pitches(prototype=prototype)
                >>> expression(selections)
                >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                >>> abjad.override(voice).text_script.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    }
                    {
                        df''4
                        ^ \markup { 13 }
                        \startGroup
                        c''4
                        ^ \markup { 12 }
                        \stopGroup
                        f'4
                        fs'4
                        d''4
                        ^ \markup { 14 }
                        \startGroup
                        ds''4
                        ^ \markup { 15 }
                        \stopGroup
                    }

        ..  container:: example

            Labels logical ties with pitch-class numbers (filtered by
            selection):

            ..  container:: example

                >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
                >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                >>> selections = [voice[:2], voice[-2:]]
                >>> for selection in selections:
                ...     spanner = abjad.HorizontalBracket()
                ...     abjad.attach(spanner, selection)
                ...
                >>> prototype = abjad.NumberedPitchClass
                >>> abjad.label(selections).with_pitches(prototype=prototype)
                >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                >>> abjad.override(voice).text_script.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    }
                    {
                        df''4
                        ^ \markup { 1 }
                        \startGroup
                        c''4
                        ^ \markup { 0 }
                        \stopGroup
                        f'4
                        fs'4
                        d''4
                        ^ \markup { 2 }
                        \startGroup
                        ds''4
                        ^ \markup { 3 }
                        \stopGroup
                    }

            ..  container:: example expression

                >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
                >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                >>> selections = [voice[:2], voice[-2:]]
                >>> for selection in selections:
                ...     spanner = abjad.HorizontalBracket()
                ...     abjad.attach(spanner, selection)
                ...
                >>> prototype = abjad.NumberedPitchClass
                >>> expression = abjad.label().with_pitches(prototype=prototype)
                >>> expression(selections)
                >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                >>> abjad.override(voice).text_script.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    }
                    {
                        df''4
                        ^ \markup { 1 }
                        \startGroup
                        c''4
                        ^ \markup { 0 }
                        \stopGroup
                        f'4
                        fs'4
                        d''4
                        ^ \markup { 2 }
                        \startGroup
                        ds''4
                        ^ \markup { 3 }
                        \stopGroup
                    }

        Returns none.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        prototype = prototype or NamedPitch
        logical_ties = iterate(self.client).logical_ties()
        for logical_tie in logical_ties:
            leaf = logical_tie.head
            label = None
            if prototype is NamedPitch:
                if isinstance(leaf, Note):
                    label = leaf.written_pitch.get_name(locale=locale)
                    label = Markup.from_literal(
                        label,
                        direction=direction,
                        )
                elif isinstance(leaf, Chord):
                    pitches = leaf.written_pitches
                    pitches = reversed(pitches)
                    pitches = [
                        Markup.from_literal(_.get_name(locale=locale))
                        for _ in pitches
                        ]
                    label = Markup.column(pitches, direction=direction)
            elif prototype is NumberedPitch:
                if isinstance(leaf, Note):
                    pitch = leaf.written_pitch.number
                    label = str(pitch)
                    label = Markup(label, direction=direction)
                elif isinstance(leaf, Chord):
                    pitches = leaf.written_pitches
                    pitches = reversed(pitches)
                    pitches = [_.number for _ in pitches]
                    pitches = [Markup(_) for _ in pitches]
                    label = Markup.column(pitches)
            elif prototype is NumberedPitchClass:
                if isinstance(leaf, Note):
                    pitch = leaf.written_pitch.pitch_class.number
                    label = str(pitch)
                    label = Markup(label, direction=direction)
                elif isinstance(leaf, Chord):
                    pitches = leaf.written_pitches
                    pitches = reversed(pitches)
                    pitches = [_.pitch_class.number for _ in pitches]
                    pitches = [Markup(_) for _ in pitches]
                    label = Markup.column(pitches)
            if label is not None:
                label = new(label, direction=direction)
                self._attach(label, leaf)

    def with_set_classes(self, direction=enums.Up, prototype=None):
        r"""
        Labels items in client with set-classes.

        ..  container:: example

            Labels selections with Forte-ranked transposition-inversion
            set-classes:

            ..  container:: example

                >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
                >>> voice = abjad.Voice(string)
                >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                >>> selections = [voice[:4], voice[-4:]]
                >>> for selection in selections:
                ...     spanner = abjad.HorizontalBracket()
                ...     abjad.attach(spanner, selection)
                ...
                >>> abjad.label(selections).with_set_classes()
                >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                >>> abjad.override(voice).text_script.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    }
                    {
                        df''8
                        ^ \markup {
                            \tiny
                                \line
                                    {
                                        "SC(4-3){0, 1, 3, 4}"
                                    }
                            }
                        \startGroup
                        c''8
                        bf'8
                        a'8
                        \stopGroup
                        f'4.
                        fs'8
                        ^ \markup {
                            \tiny
                                \line
                                    {
                                        "SC(4-20){0, 1, 5, 8}"
                                    }
                            }
                        \startGroup
                        g'8
                        b'8
                        d''2.
                        \stopGroup
                    }

            ..  container:: example expression

                >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
                >>> voice = abjad.Voice(string)
                >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                >>> selections = [voice[:4], voice[-4:]]
                >>> for selection in selections:
                ...     spanner = abjad.HorizontalBracket()
                ...     abjad.attach(spanner, selection)
                ...
                >>> expression = abjad.label().with_set_classes()
                >>> expression(selections)
                >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                >>> abjad.override(voice).text_script.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    }
                    {
                        df''8
                        ^ \markup {
                            \tiny
                                \line
                                    {
                                        "SC(4-3){0, 1, 3, 4}"
                                    }
                            }
                        \startGroup
                        c''8
                        bf'8
                        a'8
                        \stopGroup
                        f'4.
                        fs'8
                        ^ \markup {
                            \tiny
                                \line
                                    {
                                        "SC(4-20){0, 1, 5, 8}"
                                    }
                            }
                        \startGroup
                        g'8
                        b'8
                        d''2.
                        \stopGroup
                    }

        ..  container:: example

            Labels selections with lex-ranked transposition-inversion
            set-classes:

            ..  container:: example

                >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
                >>> voice = abjad.Voice(string)
                >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                >>> selections = [voice[:4], voice[-4:]]
                >>> for selection in selections:
                ...     spanner = abjad.HorizontalBracket()
                ...     abjad.attach(spanner, selection)
                ...
                >>> prototype = abjad.SetClass(lex_rank=True)
                >>> abjad.label(selections).with_set_classes(prototype=prototype)
                >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                >>> abjad.override(voice).text_script.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    }
                    {
                        df''8
                        ^ \markup {
                            \tiny
                                \line
                                    {
                                        "SC(4-6){0, 1, 3, 4}"
                                    }
                            }
                        \startGroup
                        c''8
                        bf'8
                        a'8
                        \stopGroup
                        f'4.
                        fs'8
                        ^ \markup {
                            \tiny
                                \line
                                    {
                                        "SC(4-16){0, 1, 5, 8}"
                                    }
                            }
                        \startGroup
                        g'8
                        b'8
                        d''2.
                        \stopGroup
                    }

            ..  container:: example expression

                >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
                >>> voice = abjad.Voice(string)
                >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                >>> selections = [voice[:4], voice[-4:]]
                >>> for selection in selections:
                ...     spanner = abjad.HorizontalBracket()
                ...     abjad.attach(spanner, selection)
                ...
                >>> prototype = abjad.SetClass(lex_rank=True)
                >>> expression = abjad.label().with_set_classes(prototype=prototype)
                >>> expression(selections)
                >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                >>> abjad.override(voice).text_script.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    }
                    {
                        df''8
                        ^ \markup {
                            \tiny
                                \line
                                    {
                                        "SC(4-6){0, 1, 3, 4}"
                                    }
                            }
                        \startGroup
                        c''8
                        bf'8
                        a'8
                        \stopGroup
                        f'4.
                        fs'8
                        ^ \markup {
                            \tiny
                                \line
                                    {
                                        "SC(4-16){0, 1, 5, 8}"
                                    }
                            }
                        \startGroup
                        g'8
                        b'8
                        d''2.
                        \stopGroup
                    }

        ..  container:: example

            Labels selections with transposition-only set-classes:

            ..  container:: example

                >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
                >>> voice = abjad.Voice(string)
                >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                >>> selections = [voice[:4], voice[-4:]]
                >>> for selection in selections:
                ...     spanner = abjad.HorizontalBracket()
                ...     abjad.attach(spanner, selection)
                ...
                >>> prototype = abjad.SetClass(transposition_only=True)
                >>> abjad.label(selections).with_set_classes(prototype=prototype)
                >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                >>> abjad.override(voice).text_script.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    }
                    {
                        df''8
                        ^ \markup {
                            \tiny
                                \line
                                    {
                                        "SC(4-6){0, 1, 3, 4}"
                                    }
                            }
                        \startGroup
                        c''8
                        bf'8
                        a'8
                        \stopGroup
                        f'4.
                        fs'8
                        ^ \markup {
                            \tiny
                                \line
                                    {
                                        "SC(4-16){0, 1, 5, 8}"
                                    }
                            }
                        \startGroup
                        g'8
                        b'8
                        d''2.
                        \stopGroup
                    }

            ..  container:: example expression

                >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
                >>> voice = abjad.Voice(string)
                >>> voice.consists_commands.append('Horizontal_bracket_engraver')
                >>> selections = [voice[:4], voice[-4:]]
                >>> for selection in selections:
                ...     spanner = abjad.HorizontalBracket()
                ...     abjad.attach(spanner, selection)
                ...
                >>> prototype = abjad.SetClass(transposition_only=True)
                >>> expression = abjad.label().with_set_classes(prototype=prototype)
                >>> expression(selections)
                >>> abjad.override(voice).horizontal_bracket.staff_padding = 3
                >>> abjad.override(voice).text_script.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = #3
                        \override TextScript.staff-padding = #2
                    }
                    {
                        df''8
                        ^ \markup {
                            \tiny
                                \line
                                    {
                                        "SC(4-6){0, 1, 3, 4}"
                                    }
                            }
                        \startGroup
                        c''8
                        bf'8
                        a'8
                        \stopGroup
                        f'4.
                        fs'8
                        ^ \markup {
                            \tiny
                                \line
                                    {
                                        "SC(4-16){0, 1, 5, 8}"
                                    }
                            }
                        \startGroup
                        g'8
                        b'8
                        d''2.
                        \stopGroup
                    }

        Returns none.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        prototype = prototype or SetClass()
        if prototype is SetClass:
            prototype = prototype()
        assert isinstance(prototype, SetClass), repr(prototype)
        for selection in self._client:
            pitch_class_set = PitchClassSet.from_selection(selection)
            if not pitch_class_set:
                continue
            set_class = SetClass.from_pitch_class_set(
                pitch_class_set,
                lex_rank=prototype.lex_rank,
                transposition_only=prototype.transposition_only,
                )
            string = str(set_class)
            command = MarkupCommand('line', [string])
            label = Markup(command, direction=direction)
            if label is not None:
                label = label.tiny()
                leaf = selection[0]
                self._attach(label, leaf)

    def with_start_offsets(
        self,
        brackets=None,
        clock_time=None,
        direction=None,
        global_offset=None,
        markup_command=None,
        ):
        r"""
        Labels logical ties with start offsets.

        ..  container:: example

            Labels logical tie start offsets:

            ..  container:: example

                >>> string = r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4"
                >>> staff = abjad.Staff(string)
                >>> abjad.label(staff).with_start_offsets(direction=abjad.Up)
                Duration(1, 1)

                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                        \override TupletBracket.staff-padding = #0
                    }
                    {
                        \times 2/3 {
                            c'4
                            ^ \markup { 0 }
                            d'4
                            ^ \markup { 1/6 }
                            e'4
                            ^ \markup { 1/3 }
                            ~
                        }
                        e'4
                        ef'4
                        ^ \markup { 3/4 }
                    }

            ..  container:: example expression

                >>> string = r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4"
                >>> staff = abjad.Staff(string)
                >>> expression = abjad.label().with_start_offsets()
                >>> expression(staff)
                Duration(1, 1)

                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                        \override TupletBracket.staff-padding = #0
                    }
                    {
                        \times 2/3 {
                            c'4
                            ^ \markup { 0 }
                            d'4
                            ^ \markup { 1/6 }
                            e'4
                            ^ \markup { 1/3 }
                            ~
                        }
                        e'4
                        ef'4
                        ^ \markup { 3/4 }
                    }

        ..  container:: example

            Labels logical tie start offsets with clock time:

            ..  container:: example

                >>> staff = abjad.Staff(r"c'2 d' e' f'")
                >>> score = abjad.Score([staff])
                >>> mark = abjad.MetronomeMark((1, 4), 60)
                >>> abjad.attach(mark, staff[0])
                >>> abjad.label(staff).with_start_offsets(clock_time=True)
                Duration(8, 1)

                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        \with
                        {
                            \override TextScript.staff-padding = #4
                            \override TupletBracket.staff-padding = #0
                        }
                        {
                            \tempo 4=60
                            c'2
                            ^ \markup { 0'00'' }
                            d'2
                            ^ \markup { 0'02'' }
                            e'2
                            ^ \markup { 0'04'' }
                            f'2
                            ^ \markup { 0'06'' }
                        }
                    >>

            ..  container:: example

                >>> staff = abjad.Staff(r"c'2 d' e' f'")
                >>> score = abjad.Score([staff])
                >>> mark = abjad.MetronomeMark((1, 4), 60)
                >>> abjad.attach(mark, staff[0])
                >>> expression = abjad.label().with_start_offsets(clock_time=True)
                >>> expression(staff)
                Duration(8, 1)

                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        \with
                        {
                            \override TextScript.staff-padding = #4
                            \override TupletBracket.staff-padding = #0
                        }
                        {
                            \tempo 4=60
                            c'2
                            ^ \markup { 0'00'' }
                            d'2
                            ^ \markup { 0'02'' }
                            e'2
                            ^ \markup { 0'04'' }
                            f'2
                            ^ \markup { 0'06'' }
                        }
                    >>

        ..  container:: example

            Labels logical tie start offsets with clock time and custom markup
            command:

            ..  container:: example

                >>> staff = abjad.Staff(r"c'2 d' e' f'")
                >>> score = abjad.Score([staff])
                >>> mark = abjad.MetronomeMark((1, 4), 60)
                >>> abjad.attach(mark, staff[0])
                >>> abjad.label(staff).with_start_offsets(
                ...     clock_time=True,
                ...     markup_command=r'\make-dark-cyan',
                ...     )
                Duration(8, 1)

                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
                >>> abjad.show(score) # doctest: +SKIP

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                        \override TupletBracket.staff-padding = #0
                    }
                    {
                        \tempo 4=60
                        c'2
                        ^ \markup \make-dark-cyan "0'00''"
                        d'2
                        ^ \markup \make-dark-cyan "0'02''"
                        e'2
                        ^ \markup \make-dark-cyan "0'04''"
                        f'2
                        ^ \markup \make-dark-cyan "0'06''"
                    }
                >>

            ..  container:: example expression

                >>> staff = abjad.Staff(r"c'2 d' e' f'")
                >>> score = abjad.Score([staff])
                >>> mark = abjad.MetronomeMark((1, 4), 60)
                >>> abjad.attach(mark, staff[0])
                >>> expression = abjad.label().with_start_offsets(
                ...     clock_time=True,
                ...     markup_command='make-dark-cyan',
                ...     )
                >>> expression(staff)
                Duration(8, 1)

                >>> abjad.override(staff).text_script.staff_padding = 4
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
                >>> abjad.show(score) # doctest: +SKIP

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #4
                        \override TupletBracket.staff-padding = #0
                    }
                    {
                        \tempo 4=60
                        c'2
                        ^ \markup make-dark-cyan "0'00''"
                        d'2
                        ^ \markup make-dark-cyan "0'02''"
                        e'2
                        ^ \markup make-dark-cyan "0'04''"
                        f'2
                        ^ \markup make-dark-cyan "0'06''"
                    }
                >>

        Returns total duration.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        direction = direction or enums.Up
        if global_offset is not None:
            assert isinstance(global_offset, Duration)
        for logical_tie in iterate(self.client).logical_ties():
            if clock_time:
                inspector = abjad_inspect(logical_tie.head)
                timespan = inspector.timespan(in_seconds=True)
                start_offset = timespan.start_offset
                if global_offset is not None:
                    start_offset += global_offset
                string = start_offset.to_clock_string()
                if brackets:
                    string = '"[{}]"'.format(string)
                else:
                    string = '"{}"'.format(string)
            else:
                timespan = abjad_inspect(logical_tie.head).timespan()
                start_offset = timespan.start_offset
                if global_offset is not None:
                    start_offset += global_offset
                string = str(start_offset)
                if brackets:
                    string = '[' + string + ']'
            if markup_command is not None:
                string = f'{markup_command} {string}'
                label = Markup.from_literal(
                    string,
                    direction=direction,
                    literal=True
                    )
            else:
                label = Markup(string, direction=direction)
            self._attach(label, logical_tie.head)
        total_duration = Duration(timespan.stop_offset)
        if global_offset is not None:
            total_duration += global_offset
        return total_duration
