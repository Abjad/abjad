import collections
import inspect
import typing

from . import _inspect, _iterate, enums
from .attach import attach, detach
from .cyclictuple import CyclicTuple
from .duration import Duration, NonreducedFraction
from .expression import Expression
from .indicators.LilyPondComment import LilyPondComment
from .iterate import Iteration
from .markups import Markup
from .new import new
from .overrides import LilyPondLiteral, override, tweak
from .pitch.SetClass import SetClass
from .pitch.intervalclasses import (
    NamedIntervalClass,
    NumberedIntervalClass,
    NumberedInversionEquivalentIntervalClass,
)
from .pitch.intervals import NamedInterval, NumberedInterval
from .pitch.pitchclasses import NumberedPitchClass
from .pitch.pitches import NamedPitch, NumberedPitch
from .pitch.segments import PitchSegment
from .pitch.sets import PitchClassSet
from .pitch.vectors import IntervalClassVector
from .score import Chord, Component, Note, Skip
from .select import Selection
from .storage import StorageFormatManager
from .tag import Tag
from .verticalmoment import iterate_vertical_moments


class Label:
    r"""
    Label.

    ..  container:: example

        Labels pitch names:

        ..  container:: example

            >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
            >>> abjad.label(staff).with_pitches(locale='us')

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
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
            >>> string = abjad.storage(expression)
            >>> print(string)
            abjad.Expression(
                callbacks=[
                    abjad.Expression(
                        evaluation_template='abjad.Label',
                        is_initializer=True,
                        keywords={
                            'tag': None,
                            },
                        ),
                    abjad.Expression(
                        evaluation_template="{}.with_pitches(locale='us')",
                        qualified_method_name='abjad.Label.with_pitches',
                        ),
                    ],
                proxy_class=abjad.Label,
                )

            >>> expression(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
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

                >>> string = abjad.lilypond(staff)
                >>> print(string)
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
            >>> string = abjad.storage(expression)
            >>> print(string)
            abjad.Expression(
                callbacks=[
                    abjad.Expression(
                        evaluation_template='abjad.Label',
                        is_initializer=True,
                        keywords={
                            'tag': None,
                            },
                        ),
                    abjad.Expression(
                        evaluation_template='{}.with_durations()',
                        qualified_method_name='abjad.Label.with_durations',
                        ),
                    ],
                proxy_class=abjad.Label,
                )

            >>> expression(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
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

    __documentation_section__ = "Collaborators"

    __slots__ = ("_client", "_deactivate", "_expression", "_tag")

    _pc_number_to_color = {
        0: "#(x11-color 'red)",
        1: "#(x11-color 'MediumBlue)",
        2: "#(x11-color 'orange)",
        3: "#(x11-color 'LightSlateBlue)",
        4: "#(x11-color 'ForestGreen)",
        5: "#(x11-color 'MediumOrchid)",
        6: "#(x11-color 'firebrick)",
        7: "#(x11-color 'DeepPink)",
        8: "#(x11-color 'DarkOrange)",
        9: "#(x11-color 'IndianRed)",
        10: "#(x11-color 'CadetBlue)",
        11: "#(x11-color 'SeaGreen)",
        12: "#(x11-color 'LimeGreen)",
    }

    ### INITIALIZER ###

    def __init__(self, client=None, deactivate=None, tag=None):
        prototype = (Component, collections.abc.Iterable, type(None))
        if not isinstance(client, prototype):
            raise TypeError(f"must be component, iterable or none: {client!r}.")
        self._client = client
        self._deactivate = deactivate
        self._expression = None
        self._tag = tag

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _attach(self, label, leaf):
        attach(label, leaf, deactivate=self.deactivate, tag=self.tag)

    def _color_leaf(self, leaf, color):
        if isinstance(leaf, Skip):
            color = color[1:]
            comment = LilyPondComment(color)
            self._attach(comment, leaf)
        else:
            assert color.startswith("#")
            string = fr"\abjad-color-music #'{color[1:]}"
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

        Returns component, selection or none.
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
    def tag(self) -> typing.Optional[Tag]:
        """
        Gets tag.
        """
        return self._tag

    ### PUBLIC METHODS ###

    def color_container(self, color="#red"):
        r"""
        Colors contents of ``container``.

        ..  container:: example

            Colors measure:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8")
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.label(staff).color_container("#red")
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override Accidental.color = #red
                        \override Beam.color = #red
                        \override Dots.color = #red
                        \override NoteHead.color = #red
                        \override Rest.color = #red
                        \override Stem.color = #red
                        \override TupletBracket.color = #red
                        \override TupletNumber.color = #red
                    }
                    {
                        \time 2/8
                        c'8
                        d'8
                    }

            ..  container:: example expression

                >>> staff = abjad.Staff("c'8 d'8")
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> expression = abjad.label().color_container("#red")
                >>> expression(staff)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override Accidental.color = #red
                        \override Beam.color = #red
                        \override Dots.color = #red
                        \override NoteHead.color = #red
                        \override Rest.color = #red
                        \override Stem.color = #red
                        \override TupletBracket.color = #red
                        \override TupletNumber.color = #red
                    }
                    {
                        \time 2/8
                        c'8
                        d'8
                    }

        Returns none.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        override(self.client).Accidental.color = color
        override(self.client).Beam.color = color
        override(self.client).Dots.color = color
        override(self.client).NoteHead.color = color
        override(self.client).Rest.color = color
        override(self.client).Stem.color = color
        override(self.client).TupletBracket.color = color
        override(self.client).TupletNumber.color = color

    def color_leaves(self, color="#red"):
        r"""
        Colors leaves.

        ..  container:: example

            Colors leaves red:

            ..  container:: example

                >>> staff = abjad.Staff("cs'8. r8. s8. <c' cs' a'>8.")
                >>> abjad.beam(staff[:])
                >>> abjad.label(staff).color_leaves("#red")
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    {
                        \abjad-color-music #'red
                        cs'8.
                        [
                        \abjad-color-music #'red
                        r8.
                        % red
                        s8.
                        \abjad-color-music #'red
                        <c' cs' a'>8.
                        ]
                    }

            ..  container:: example expression

                >>> staff = abjad.Staff("cs'8. r8. s8. <c' cs' a'>8.")
                >>> abjad.beam(staff[:])
                >>> expression = abjad.label().color_leaves("#red")
                >>> expression(staff)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    {
                        \abjad-color-music #'red
                        cs'8.
                        [
                        \abjad-color-music #'red
                        r8.
                        % red
                        s8.
                        \abjad-color-music #'red
                        <c' cs' a'>8.
                        ]
                    }

        Returns none.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        for leaf in Iteration(self.client).leaves():
            self._color_leaf(leaf, color)

    def color_note_heads(self, color_map=None):
        r"""
        Colors note note-heads.

        ..  container:: example

            Colors chord note-heads:

            ..  container:: example

                >>> chord = abjad.Chord([12, 14, 18, 21, 23], (1, 4))
                >>> pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
                >>> colors = ["#red", "#blue", "#green"]
                >>> color_map = abjad.ColorMap(colors=colors, pitch_iterables=pitches)
                >>> abjad.label(chord).color_note_heads(color_map)
                >>> abjad.show(chord) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(chord)
                    >>> print(string)
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
                >>> colors = ["#red", "#blue", "#green"]
                >>> color_map = abjad.ColorMap(colors=colors, pitch_iterables=pitches)
                >>> expression = abjad.label().color_note_heads(color_map)
                >>> expression(chord)
                >>> abjad.show(chord) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(chord)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(note)
                    >>> print(string)
                    \once \override NoteHead.color = #red
                    c'4

            ..  container:: example expression

                >>> note = abjad.Note("c'4")
                >>> expression = abjad.label().color_note_heads(color_map)
                >>> expression(note)
                >>> abjad.show(note) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(note)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
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
        for leaf in Iteration(self.client).leaves():
            if isinstance(leaf, Chord):
                for note_head in leaf.note_heads:
                    number = note_head.written_pitch.number
                    pc = NumberedPitchClass(number)
                    color = color_map.get(pc, None)
                    if color is not None:
                        tweak(note_head).color = color
            elif isinstance(leaf, Note):
                note_head = leaf.note_head
                number = note_head.written_pitch.number
                pc = NumberedPitchClass(number)
                color = color_map[pc.number]
                if color is not None:
                    override(leaf).NoteHead.color = color

    def by_selector(self, selector, colors=None) -> None:
        """
        Colors client by ``selector``.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if selector._is_singular_get_item():
            colors = colors or ["#green"]
            color = colors[0]
            self.color_leaves(color=color)
        else:
            colors = colors or ["#red", "#blue"]
            colors = CyclicTuple(colors)
            for i, item in enumerate(self.client):
                color = colors[i]
                Label(item).color_leaves(color=color)

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

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
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
        for leaf in Iteration(self.client).leaves():
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

                    >>> string = abjad.lilypond(staff_group)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff_group)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff_group)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff_group)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff_group)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff_group)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff_group)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff_group)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff_group)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff_group)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff_group)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff_group)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff_group)
                    >>> print(string)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
                            c'8
                            ^ \markup \tiny \line { "SC(2-5){0, 5}" }
                            d'4
                            ^ \markup \tiny \line { "SC(3-9){0, 2, 7}" }
                            e'16
                            ^ \markup \tiny \line { "SC(3-4){0, 1, 5}" }
                            f'16
                            ^ \markup \tiny \line { "SC(2-5){0, 5}" }
                        }
                        \new Staff
                        {
                            \clef "alto"
                            g4
                            f4
                            ^ \markup \tiny \line { "SC(3-7){0, 2, 5}" }
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

                    >>> string = abjad.lilypond(staff_group)
                    >>> print(string)
                    \new StaffGroup
                    <<
                        \new Staff
                        {
                            c'8
                            ^ \markup \tiny \line { "SC(2-5){0, 5}" }
                            d'4
                            ^ \markup \tiny \line { "SC(3-9){0, 2, 7}" }
                            e'16
                            ^ \markup \tiny \line { "SC(3-4){0, 1, 5}" }
                            f'16
                            ^ \markup \tiny \line { "SC(2-5){0, 5}" }
                        }
                        \new Staff
                        {
                            \clef "alto"
                            g4
                            f4
                            ^ \markup \tiny \line { "SC(3-7){0, 2, 5}" }
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
        vertical_moments = iterate_vertical_moments(self.client)
        for index, vertical_moment in enumerate(vertical_moments):
            label, string = None, None
            if prototype is int:
                label = Markup(index, direction=direction)
            elif prototype is NumberedPitch:
                leaves = vertical_moment.leaves
                pitches = PitchSegment.from_selection(leaves)
                if not pitches:
                    continue
                pitch_numbers = [str(pitch.number) for pitch in pitches]
                label = Markup(
                    rf'\column {{ {" ".join(pitch_numbers)} }}',
                    direction=direction,
                )
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
                label = Markup(
                    rf'\column {{ {" ".join(numbers)} }}',
                    direction=direction,
                )
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
                        bass_note.written_pitch, upper_note.written_pitch
                    )
                    named_intervals.append(named_interval)
                numbers = [str(x.number) for x in named_intervals]
                label = Markup(
                    rf'\column {{ {" ".join(numbers)} }}',
                    direction=direction,
                )
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
                        bass_note.written_pitch, upper_note.written_pitch
                    )
                    interval_class = NumberedIntervalClass(interval)
                    number = interval_class.number
                    numbers.append(number)
                string = " ".join([str(_) for _ in numbers])
                label = Markup(
                    rf"\column {{ {string} }}",
                    direction=direction,
                )
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
            elif prototype is SetClass or isinstance(prototype, SetClass):
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
                string = rf'\line {{ "{string}" }}'
            else:
                raise TypeError(f"unknown prototype {prototype!r}.")
            if label is not None:
                assert len(label.contents) == 1, repr(label)
                label = Markup(rf"\tiny {label.contents[0]}", direction=label.direction)
                if direction is enums.Up:
                    leaf = vertical_moment.start_leaves[0]
                else:
                    leaf = vertical_moment.start_leaves[-1]
                self._attach(label, leaf)
            elif string is not None:
                string = rf"\markup \tiny {string}"
                label = Markup(string, direction=direction, literal=True)
                if direction is enums.Up:
                    leaf = vertical_moment.start_leaves[0]
                else:
                    leaf = vertical_moment.start_leaves[-1]
                self._attach(label, leaf)

    def with_durations(
        self, *, denominator=None, direction=enums.Up, in_seconds: bool = None
    ):
        r"""
        Labels logical ties with durations.

        ..  container:: example

            Labels logical tie durations:

            ..  container:: example

                >>> staff = abjad.Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")
                >>> abjad.label(staff).with_durations()
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
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
                                4
                                8
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

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
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
                                4
                                8
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

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
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

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
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
        for logical_tie in Iteration(self.client).logical_ties():
            duration = _inspect._get_duration(logical_tie, in_seconds=in_seconds)
            if denominator is not None:
                duration = NonreducedFraction(duration)
                duration = duration.with_denominator(denominator)
            pair = duration.pair
            numerator, denominator = pair
            label = Markup(rf"\fraction {numerator} {denominator}", direction=direction)
            self._attach(label, logical_tie.head)

    def with_indices(self, direction=enums.Up, prototype=None):
        r"""Labels logical ties with indices.

        ..  container:: example

            Labels logical tie indices:

            ..  container:: example

                >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
                >>> abjad.label(staff).with_indices()
                >>> abjad.override(staff).TextScript.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 2
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
                >>> abjad.override(staff).TextScript.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 2
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
                >>> abjad.override(staff).TextScript.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 2
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
                >>> abjad.override(staff).TextScript.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 2
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
                >>> abjad.override(staff).TextScript.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 2
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
                >>> abjad.override(staff).TextScript.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 2
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
                >>> abjad.override(staff).TextScript.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 2
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
                >>> abjad.override(staff).TextScript.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 2
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
                >>> tuplets = abjad.mutate.copy(tuplet, 4)
                >>> staff = abjad.Staff(tuplets)
                >>> abjad.label(staff).with_indices(prototype=abjad.Tuplet)
                >>> abjad.override(staff).TextScript.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 2
                    }
                    {
                        \times 2/3 {
                            c'8
                            ^ \markup { 0 }
                            [
                            d'8
                            e'8
                            ]
                        }
                        \times 2/3 {
                            c'8
                            ^ \markup { 1 }
                            [
                            d'8
                            e'8
                            ]
                        }
                        \times 2/3 {
                            c'8
                            ^ \markup { 2 }
                            [
                            d'8
                            e'8
                            ]
                        }
                        \times 2/3 {
                            c'8
                            ^ \markup { 3 }
                            [
                            d'8
                            e'8
                            ]
                        }
                    }

            ..  container:: example expression

                >>> tuplet = abjad.Tuplet((2, 3), "c'8 [ d'8 e'8 ]")
                >>> tuplets = abjad.mutate.copy(tuplet, 4)
                >>> staff = abjad.Staff(tuplets)
                >>> expression = abjad.label().with_indices(
                ...     prototype=abjad.Tuplet,
                ...     )
                >>> expression(staff)
                >>> abjad.override(staff).TextScript.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 2
                    }
                    {
                        \times 2/3 {
                            c'8
                            ^ \markup { 0 }
                            [
                            d'8
                            e'8
                            ]
                        }
                        \times 2/3 {
                            c'8
                            ^ \markup { 1 }
                            [
                            d'8
                            e'8
                            ]
                        }
                        \times 2/3 {
                            c'8
                            ^ \markup { 2 }
                            [
                            d'8
                            e'8
                            ]
                        }
                        \times 2/3 {
                            c'8
                            ^ \markup { 3 }
                            [
                            d'8
                            e'8
                            ]
                        }
                    }

        Returns none.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if prototype is None:
            items = Iteration(self.client).logical_ties()
        else:
            items = Iteration(self.client).components(prototype=prototype)
        items = list(items)
        for index, item in enumerate(items):
            string = str(index)
            label = Markup(string, direction=direction)
            leaves = Selection(item).leaves()
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
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
        for note in Iteration(self.client).leaves(Note):
            label = None
            next_leaf = _iterate._get_leaf(note, 1)
            if isinstance(next_leaf, Note):
                interval = NamedInterval.from_pitch_carriers(note, next_leaf)
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
                    }
                    {
                        <a d' fs'>4
                        ^ \markup \column { "fs'" "d'" "a" }
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
                    }
                    {
                        <a d' fs'>4
                        ^ \markup \column { "fs'" "d'" "a" }
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
                    }
                    {
                        <a d' fs'>4
                        ^ \markup \column { "F#4" "D4" "A3" }
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
                    }
                    {
                        <a d' fs'>4
                        ^ \markup \column { "F#4" "D4" "A3" }
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
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
                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
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
                ...     abjad.horizontal_bracket(selection)
                ...
                >>> abjad.label(selections).with_pitches()
                >>> abjad.override(voice).HorizontalBracket.staff_padding = 3
                >>> abjad.override(voice).TextScript.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = 3
                        \override TextScript.staff-padding = 2
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
                ...     abjad.horizontal_bracket(selection)
                ...
                >>> expression = abjad.label().with_pitches()
                >>> expression(selections)
                >>> abjad.override(voice).HorizontalBracket.staff_padding = 3
                >>> abjad.override(voice).TextScript.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = 3
                        \override TextScript.staff-padding = 2
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
                ...     abjad.horizontal_bracket(selection)
                ...
                >>> prototype = abjad.NumberedPitch
                >>> abjad.label(selections).with_pitches(prototype=prototype)
                >>> abjad.override(voice).HorizontalBracket.staff_padding = 3
                >>> abjad.override(voice).TextScript.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = 3
                        \override TextScript.staff-padding = 2
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
                ...     abjad.horizontal_bracket(selection)
                ...
                >>> prototype = abjad.NumberedPitch
                >>> expression = abjad.label().with_pitches(prototype=prototype)
                >>> expression(selections)
                >>> abjad.override(voice).HorizontalBracket.staff_padding = 3
                >>> abjad.override(voice).TextScript.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = 3
                        \override TextScript.staff-padding = 2
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
                ...     abjad.horizontal_bracket(selection)
                ...
                >>> prototype = abjad.NumberedPitchClass
                >>> abjad.label(selections).with_pitches(prototype=prototype)
                >>> abjad.override(voice).HorizontalBracket.staff_padding = 3
                >>> abjad.override(voice).TextScript.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = 3
                        \override TextScript.staff-padding = 2
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
                ...     abjad.horizontal_bracket(selection)
                ...
                >>> prototype = abjad.NumberedPitchClass
                >>> expression = abjad.label().with_pitches(prototype=prototype)
                >>> expression(selections)
                >>> abjad.override(voice).HorizontalBracket.staff_padding = 3
                >>> abjad.override(voice).TextScript.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = 3
                        \override TextScript.staff-padding = 2
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
        logical_ties = Iteration(self.client).logical_ties()
        for logical_tie in logical_ties:
            leaf = logical_tie.head
            label = None
            if prototype is NamedPitch:
                if isinstance(leaf, Note):
                    string = leaf.written_pitch.get_name(locale=locale)
                    if "#" in string:
                        string = '"' + string + '"'
                    label = Markup(
                        rf"\markup {{ {string} }}",
                        direction=direction,
                        literal=True,
                    )
                elif isinstance(leaf, Chord):
                    pitches = leaf.written_pitches
                    pitches = reversed(pitches)
                    names = []
                    for pitch in pitches:
                        name = pitch.get_name(locale=locale)
                        name = '"' + name + '"'
                        names.append(name)
                    string = " ".join(names)
                    label = Markup(
                        rf"\markup \column {{ {string} }}",
                        direction=direction,
                        literal=True,
                    )
            elif prototype is NumberedPitch:
                if isinstance(leaf, Note):
                    pitch = leaf.written_pitch.number
                    label = str(pitch)
                    label = Markup(label, direction=direction)
                elif isinstance(leaf, Chord):
                    pitches = leaf.written_pitches
                    pitches = reversed(pitches)
                    pitches = [str(_.number) for _ in pitches]
                    string = " ".join(pitches)
                    label = Markup(
                        rf"\column {{ {string} }}",
                        direction=direction,
                    )
            elif prototype is NumberedPitchClass:
                if isinstance(leaf, Note):
                    pitch = leaf.written_pitch.pitch_class.number
                    label = str(pitch)
                    label = Markup(label, direction=direction)
                elif isinstance(leaf, Chord):
                    pitches = leaf.written_pitches
                    pitches = reversed(pitches)
                    pitches = [str(_.pitch_class.number) for _ in pitches]
                    string = " ".join(pitches)
                    label = Markup(
                        rf"\column {{ {string} }}",
                        direction=direction,
                    )
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
                ...     abjad.horizontal_bracket(selection)
                ...
                >>> abjad.label(selections).with_set_classes()
                >>> abjad.override(voice).HorizontalBracket.staff_padding = 3
                >>> abjad.override(voice).TextScript.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = 3
                        \override TextScript.staff-padding = 2
                    }
                    {
                        df''8
                        ^ \markup \tiny \line { "SC(4-3){0, 1, 3, 4}" }
                        \startGroup
                        c''8
                        bf'8
                        a'8
                        \stopGroup
                        f'4.
                        fs'8
                        ^ \markup \tiny \line { "SC(4-20){0, 1, 5, 8}" }
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
                ...     abjad.horizontal_bracket(selection)
                ...
                >>> expression = abjad.label().with_set_classes()
                >>> expression(selections)
                >>> abjad.override(voice).HorizontalBracket.staff_padding = 3
                >>> abjad.override(voice).TextScript.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = 3
                        \override TextScript.staff-padding = 2
                    }
                    {
                        df''8
                        ^ \markup \tiny \line { "SC(4-3){0, 1, 3, 4}" }
                        \startGroup
                        c''8
                        bf'8
                        a'8
                        \stopGroup
                        f'4.
                        fs'8
                        ^ \markup \tiny \line { "SC(4-20){0, 1, 5, 8}" }
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
                ...     abjad.horizontal_bracket(selection)
                ...
                >>> prototype = abjad.SetClass(lex_rank=True)
                >>> abjad.label(selections).with_set_classes(prototype=prototype)
                >>> abjad.override(voice).HorizontalBracket.staff_padding = 3
                >>> abjad.override(voice).TextScript.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = 3
                        \override TextScript.staff-padding = 2
                    }
                    {
                        df''8
                        ^ \markup \tiny \line { "SC(4-6){0, 1, 3, 4}" }
                        \startGroup
                        c''8
                        bf'8
                        a'8
                        \stopGroup
                        f'4.
                        fs'8
                        ^ \markup \tiny \line { "SC(4-16){0, 1, 5, 8}" }
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
                ...     abjad.horizontal_bracket(selection)
                ...
                >>> prototype = abjad.SetClass(lex_rank=True)
                >>> expression = abjad.label().with_set_classes(prototype=prototype)
                >>> expression(selections)
                >>> abjad.override(voice).HorizontalBracket.staff_padding = 3
                >>> abjad.override(voice).TextScript.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = 3
                        \override TextScript.staff-padding = 2
                    }
                    {
                        df''8
                        ^ \markup \tiny \line { "SC(4-6){0, 1, 3, 4}" }
                        \startGroup
                        c''8
                        bf'8
                        a'8
                        \stopGroup
                        f'4.
                        fs'8
                        ^ \markup \tiny \line { "SC(4-16){0, 1, 5, 8}" }
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
                ...     abjad.horizontal_bracket(selection)
                ...
                >>> prototype = abjad.SetClass(transposition_only=True)
                >>> abjad.label(selections).with_set_classes(prototype=prototype)
                >>> abjad.override(voice).HorizontalBracket.staff_padding = 3
                >>> abjad.override(voice).TextScript.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = 3
                        \override TextScript.staff-padding = 2
                    }
                    {
                        df''8
                        ^ \markup \tiny \line { "SC(4-6){0, 1, 3, 4}" }
                        \startGroup
                        c''8
                        bf'8
                        a'8
                        \stopGroup
                        f'4.
                        fs'8
                        ^ \markup \tiny \line { "SC(4-16){0, 1, 5, 8}" }
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
                ...     abjad.horizontal_bracket(selection)
                ...
                >>> prototype = abjad.SetClass(transposition_only=True)
                >>> expression = abjad.label().with_set_classes(prototype=prototype)
                >>> expression(selections)
                >>> abjad.override(voice).HorizontalBracket.staff_padding = 3
                >>> abjad.override(voice).TextScript.staff_padding = 2
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                        \override HorizontalBracket.staff-padding = 3
                        \override TextScript.staff-padding = 2
                    }
                    {
                        df''8
                        ^ \markup \tiny \line { "SC(4-6){0, 1, 3, 4}" }
                        \startGroup
                        c''8
                        bf'8
                        a'8
                        \stopGroup
                        f'4.
                        fs'8
                        ^ \markup \tiny \line { "SC(4-16){0, 1, 5, 8}" }
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
            string = rf'\markup \tiny \line {{ "{string}" }}'
            label = Markup(string, direction=direction, literal=True)
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

                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.override(staff).TupletBracket.staff_padding = 0
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
                        \override TupletBracket.staff-padding = 0
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

                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.override(staff).TupletBracket.staff_padding = 0
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
                        \override TupletBracket.staff-padding = 0
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

                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.override(staff).TupletBracket.staff_padding = 0
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(score)
                    >>> print(string)
                    \new Score
                    <<
                        \new Staff
                        \with
                        {
                            \override TextScript.staff-padding = 4
                            \override TupletBracket.staff-padding = 0
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

                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.override(staff).TupletBracket.staff_padding = 0
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(score)
                    >>> print(string)
                    \new Score
                    <<
                        \new Staff
                        \with
                        {
                            \override TextScript.staff-padding = 4
                            \override TupletBracket.staff-padding = 0
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
            command. No PDF shown here because command is custom:

            ..  container:: example

                >>> staff = abjad.Staff(r"c'2 d' e' f'")
                >>> score = abjad.Score([staff])
                >>> mark = abjad.MetronomeMark((1, 4), 60)
                >>> abjad.attach(mark, staff[0])
                >>> abjad.label(staff).with_start_offsets(
                ...     clock_time=True,
                ...     markup_command=r'\dark_cyan_markup',
                ...     )
                Duration(8, 1)

                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.override(staff).TupletBracket.staff_padding = 0

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                <<
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
                        \override TupletBracket.staff-padding = 0
                    }
                    {
                        \tempo 4=60
                        c'2
                        ^ \dark_cyan_markup "0'00''"
                        d'2
                        ^ \dark_cyan_markup "0'02''"
                        e'2
                        ^ \dark_cyan_markup "0'04''"
                        f'2
                        ^ \dark_cyan_markup "0'06''"
                    }
                >>

            ..  container:: example expression

                >>> staff = abjad.Staff(r"c'2 d' e' f'")
                >>> score = abjad.Score([staff])
                >>> mark = abjad.MetronomeMark((1, 4), 60)
                >>> abjad.attach(mark, staff[0])
                >>> expression = abjad.label().with_start_offsets(
                ...     clock_time=True,
                ...     markup_command=r'\dark_cyan_markup',
                ...     )
                >>> expression(staff)
                Duration(8, 1)

                >>> abjad.override(staff).TextScript.staff_padding = 4
                >>> abjad.override(staff).TupletBracket.staff_padding = 0

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                <<
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 4
                        \override TupletBracket.staff-padding = 0
                    }
                    {
                        \tempo 4=60
                        c'2
                        ^ \dark_cyan_markup "0'00''"
                        d'2
                        ^ \dark_cyan_markup "0'02''"
                        e'2
                        ^ \dark_cyan_markup "0'04''"
                        f'2
                        ^ \dark_cyan_markup "0'06''"
                    }
                >>

        Returns total duration.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        direction = direction or enums.Up
        if global_offset is not None:
            assert isinstance(global_offset, Duration)
        for logical_tie in Iteration(self.client).logical_ties():
            if clock_time:
                timespan = logical_tie.head._get_timespan(in_seconds=True)
                start_offset = timespan.start_offset
                if global_offset is not None:
                    start_offset += global_offset
                string = start_offset.to_clock_string()
                if brackets:
                    string = f'"[{string}]"'
                else:
                    string = f'"{string}"'
            else:
                timespan = logical_tie.head._get_timespan()
                start_offset = timespan.start_offset
                if global_offset is not None:
                    start_offset += global_offset
                string = str(start_offset)
                if brackets:
                    string = "[" + string + "]"
            if markup_command is not None:
                string = f"{markup_command} {string}"
                label = Markup(string, direction=direction, literal=True)
            else:
                label = Markup(string, direction=direction)
            self._attach(label, logical_tie.head)
        total_duration = Duration(timespan.stop_offset)
        if global_offset is not None:
            total_duration += global_offset
        return total_duration


class ColorMap:
    """
    Color map.

    ..  container:: example

        Maps pitch-classes to red, green and blue:

        >>> color_map = abjad.ColorMap(
        ...     colors=["#red", "#green", "#blue"],
        ...     pitch_iterables=[
        ...         [-8, 2, 10, 21],
        ...         [0, 11, 32, 41],
        ...         [15, 25, 42, 43],
        ...     ],
        ... )

        >>> string = abjad.storage(color_map)
        >>> print(string)
        abjad.ColorMap(
            colors=['#red', '#green', '#blue'],
            pitch_iterables=[
                [-8, 2, 10, 21],
                [0, 11, 32, 41],
                [15, 25, 42, 43],
                ],
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_color_dictionary", "_colors", "_pitch_iterables")

    ### INITIALIZER ###

    def __init__(self, *, colors=None, pitch_iterables=None):
        pitch_iterables = pitch_iterables or []
        colors = colors or []
        assert len(pitch_iterables) == len(colors)
        self._pitch_iterables = pitch_iterables
        self._colors = colors
        self._color_dictionary = {}
        self._initialize_color_dictionary()

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __getitem__(self, pitch_class) -> str:
        """
        Gets ``pitch_class`` color.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=["#red", "#green", "#blue"],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...     ],
            ... )

            >>> color_map[11]
            '#green'

        """
        pitch_class = NumberedPitchClass(pitch_class)
        return self._color_dictionary[pitch_class.number]

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _initialize_color_dictionary(self):
        for pitch_iterable, color in zip(self.pitch_iterables, self.colors):
            for pitch in pitch_iterable:
                pc = NumberedPitchClass(pitch)
                keys = self._color_dictionary.keys()
                if pc.number in list(keys):
                    print(pc, list(self._color_dictionary.keys()))
                    raise KeyError("duplicated pitch-class in color map: {pc!r}.")
                self._color_dictionary[pc.number] = color

    ### PUBLIC PROPERTIES ###

    @property
    def colors(self) -> typing.List[str]:
        """
        Gets colors.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=["#red", "#green", "#blue"],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...     ],
            ... )

            >>> color_map.colors
            ['#red', '#green', '#blue']

        """
        return self._colors

    @property
    def is_twelve_tone_complete(self) -> bool:
        """
        Is true when color map contains all 12-ET pitch-classes.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=["#red", "#green", "#blue"],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...     ],
            ... )

            >>> color_map.is_twelve_tone_complete
            True

        """
        pcs = range(12)
        return set(pcs).issubset(set(self._color_dictionary.keys()))

    @property
    def is_twenty_four_tone_complete(self) -> bool:
        """
        Is true when color map contains all 24-ET pitch-classes.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=["#red", "#green", "#blue"],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...     ],
            ... )

            >>> color_map.is_twenty_four_tone_complete
            False

        """
        pcs = [x / 2.0 for x in range(24)]
        pcs = [int(x) if int(x) == x else x for x in pcs]
        return set(pcs).issubset(set(self._color_dictionary.keys()))

    @property
    def pairs(self) -> typing.List[typing.Tuple[int, str]]:
        """
        Gets pairs.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=["#red", "#green", "#blue"],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...     ],
            ... )

            >>> for pair in color_map.pairs:
            ...     pair
            ...
            (0, '#green')
            (1, '#blue')
            (2, '#red')
            (3, '#blue')
            (4, '#red')
            (5, '#green')
            (6, '#blue')
            (7, '#blue')
            (8, '#green')
            (9, '#red')
            (10, '#red')
            (11, '#green')

        """
        items = list(self._color_dictionary.items())
        return list(sorted(items))

    @property
    def pitch_iterables(self) -> typing.List[typing.List[int]]:
        """
        Gets pitch iterables.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=["#red", "#green", "#blue"],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...     ],
            ... )

            >>> color_map.pitch_iterables
            [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]

        """
        return self._pitch_iterables

    ### PUBLIC METHODS ###

    def get(self, key, alternative=None) -> str:
        """
        Gets ``key`` from color map.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=["#red", "#green", "#blue"],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...     ],
            ... )

            >>> color_map.get(11)
            '#green'

        Returns ``alternative`` when ``key`` is not found.
        """
        try:
            return self[key]
        except (KeyError, TypeError, ValueError):
            return alternative


### FUNCTIONS ###


def label(client=None, deactivate=None, tag=None):
    r"""
    Makes label agent or label expression.

    ..  container:: example

        Labels logical ties with start offsets:

        >>> staff = abjad.Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
        >>> abjad.label(staff).with_start_offsets(direction=abjad.Up)
        Duration(1, 1)

        >>> abjad.override(staff).TextScript.staff_padding = 4
        >>> abjad.override(staff).TupletBracket.staff_padding = 0
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override TextScript.staff-padding = 4
                \override TupletBracket.staff-padding = 0
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

        See the ``Label`` API entry for many more examples.

    ..  container:: example expression

        Initializes positionally:

        >>> expression = abjad.label()
        >>> expression(staff)
        Label(client=<Staff{3}>)

        Initializes from keyword:

        >>> expression = abjad.label()
        >>> expression(client=staff)
        Label(client=<Staff{3}>)

        Makes label expression:

            >>> expression = abjad.label()
            >>> expression = expression.with_start_offsets()

        >>> staff = abjad.Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
        >>> expression(staff)
        Duration(1, 1)

        >>> abjad.override(staff).TextScript.staff_padding = 4
        >>> abjad.override(staff).TupletBracket.staff_padding = 0
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override TextScript.staff-padding = 4
                \override TupletBracket.staff-padding = 0
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

        See the ``Label`` API entry for many more examples.

    Returns label agent when ``client`` is not none.

    Returns label expression when ``client`` is none.
    """
    if client is not None:
        return Label(client=client, deactivate=deactivate, tag=tag)
    expression = Expression(proxy_class=Label)
    callback = Expression._make_initializer_callback(Label, tag=tag)
    expression = expression.append_callback(callback)
    return expression
