import collections
import typing

from . import math
from .duration import Multiplier
from .ordereddict import OrderedDict
from .score import (
    AfterGraceContainer,
    BeforeGraceContainer,
    Component,
    Score,
    Staff,
    StaffGroup,
    Voice,
)
from .storage import StorageFormatManager


class Parentage(collections.abc.Sequence):
    r'''
    Parentage of a component.

    ..  container:: example

        >>> score = abjad.Score()
        >>> string = r"""\new Voice = "Treble_Voice" { e'4 }"""
        >>> treble_staff = abjad.Staff(string, name="Treble_Staff")
        >>> score.append(treble_staff)
        >>> string = r"""\new Voice = "Bass_Voice" { c4 }"""
        >>> bass_staff = abjad.Staff(string, name="Bass_Staff")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, bass_staff[0][0])
        >>> score.append(bass_staff)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        e'4
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        c4
                    }
                }
            >>

        >>> bass_voice = score["Bass_Voice"]
        >>> note = bass_voice[0]
        >>> for component in abjad.get.parentage(note):
        ...     component
        ...
        Note('c4')
        Voice('c4', name='Bass_Voice')
        <Staff-"Bass_Staff"{1}>
        <Score<<2>>>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = "Selections"

    __slots__ = ("_component", "_components")

    ### INITIALIZER ###

    def __init__(self, component=None):
        components = []
        if component is not None:
            assert isinstance(component, Component), repr(component)
            components.extend(component._get_parentage())
        self._component = component
        self._components = tuple(components)

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        """
        Gets ``argument``.

        Returns component or tuple of components.
        """
        return self.components.__getitem__(argument)

    def __len__(self) -> int:
        """
        Gets number of components in parentage.
        """
        return len(self.components)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
    def _id_string(component):
        lhs = component.__class__.__name__
        rhs = getattr(component, "name", None) or id(component)
        return f"{lhs}-{rhs!r}"

    def _prolations(self):
        prolations = []
        default = Multiplier(1)
        for parent in self:
            prolation = getattr(parent, "implied_prolation", default)
            prolations.append(prolation)
        return prolations

    ### PUBLIC PROPERTIES ###

    @property
    def component(self) -> Component:
        r"""
        Gets component.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3
                                \slash
                                \voiceOne
                                <
                                    \tweak font-size 0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo
                                e'4
                            }
                        >>
                        \oneVoice
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.get.parentage(component)
            ...     print(f"{repr(component):30} {repr(parentage.component)}")
            <Staff{1}>                     <Staff{1}>
            <Voice-"Music_Voice"{4}>       <Voice-"Music_Voice"{4}>
            Note("c'4")                    Note("c'4")
            BeforeGraceContainer("cs'16")        BeforeGraceContainer("cs'16")
            Note("cs'16")                  Note("cs'16")
            Note("d'4")                    Note("d'4")
            <<<2>>>                        <<<2>>>
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Chord("<e' g'>16")             Chord("<e' g'>16")
            Note("gs'16")                  Note("gs'16")
            Note("a'16")                   Note("a'16")
            Note("as'16")                  Note("as'16")
            Voice("e'4", name='Music_Voice') Voice("e'4", name='Music_Voice')
            Note("e'4")                    Note("e'4")
            Note("f'4")                    Note("f'4")
            AfterGraceContainer("fs'16")   AfterGraceContainer("fs'16")
            Note("fs'16")                  Note("fs'16")

        """
        return self._component

    @property
    def components(self) -> typing.Tuple[Component]:
        r"""
        Gets components.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3
                                \slash
                                \voiceOne
                                <
                                    \tweak font-size 0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo
                                e'4
                            }
                        >>
                        \oneVoice
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.get.parentage(component)
            ...     components = parentage.components
            ...     print(f"{repr(component)}:")
            ...     for component_ in components:
            ...         print(f"    {repr(component_)}")
            <Staff{1}>:
                <Staff{1}>
            <Voice-"Music_Voice"{4}>:
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("c'4"):
                Note("c'4")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            BeforeGraceContainer("cs'16"):
                BeforeGraceContainer("cs'16")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("cs'16"):
                Note("cs'16")
                BeforeGraceContainer("cs'16")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("d'4"):
                Note("d'4")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            <<<2>>>:
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Chord("<e' g'>16"):
                Chord("<e' g'>16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("gs'16"):
                Note("gs'16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("a'16"):
                Note("a'16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("as'16"):
                Note("as'16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Voice("e'4", name='Music_Voice'):
                Voice("e'4", name='Music_Voice')
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("e'4"):
                Note("e'4")
                Voice("e'4", name='Music_Voice')
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("f'4"):
                Note("f'4")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            AfterGraceContainer("fs'16"):
                AfterGraceContainer("fs'16")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("fs'16"):
                Note("fs'16")
                AfterGraceContainer("fs'16")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>

        """
        return self._components

    @property
    def orphan(self) -> bool:
        r"""
        Is true when component has no parent.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3
                                \slash
                                \voiceOne
                                <
                                    \tweak font-size 0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo
                                e'4
                            }
                        >>
                        \oneVoice
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.get.parentage(component)
            ...     print(f"{repr(component):30} {repr(parentage.orphan)}")
            <Staff{1}>                     True
            <Voice-"Music_Voice"{4}>       False
            Note("c'4")                    False
            BeforeGraceContainer("cs'16")        False
            Note("cs'16")                  False
            Note("d'4")                    False
            <<<2>>>                        False
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") False
            Chord("<e' g'>16")             False
            Note("gs'16")                  False
            Note("a'16")                   False
            Note("as'16")                  False
            Voice("e'4", name='Music_Voice') False
            Note("e'4")                    False
            Note("f'4")                    False
            AfterGraceContainer("fs'16")   False
            Note("fs'16")                  False

        """
        return self.parent is None

    @property
    def parent(self) -> typing.Optional[Component]:
        r"""
        Gets parent.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3
                                \slash
                                \voiceOne
                                <
                                    \tweak font-size 0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo
                                e'4
                            }
                        >>
                        \oneVoice
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.get.parentage(component)
            ...     print(f"{repr(component):30} {repr(parentage.parent)}")
            <Staff{1}>                     None
            <Voice-"Music_Voice"{4}>       <Staff{1}>
            Note("c'4")                    <Voice-"Music_Voice"{4}>
            BeforeGraceContainer("cs'16")        <Voice-"Music_Voice"{4}>
            Note("cs'16")                  BeforeGraceContainer("cs'16")
            Note("d'4")                    <Voice-"Music_Voice"{4}>
            <<<2>>>                        <Voice-"Music_Voice"{4}>
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") <<<2>>>
            Chord("<e' g'>16")             OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Note("gs'16")                  OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Note("a'16")                   OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Note("as'16")                  OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Voice("e'4", name='Music_Voice') <<<2>>>
            Note("e'4")                    Voice("e'4", name='Music_Voice')
            Note("f'4")                    <Voice-"Music_Voice"{4}>
            AfterGraceContainer("fs'16")   <Voice-"Music_Voice"{4}>
            Note("fs'16")                  AfterGraceContainer("fs'16")

        """
        return self.get(n=1)

    @property
    def prolation(self) -> Multiplier:
        r"""
        Gets prolation.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice(
            ...     r"\times 2/3 { c'4 d' e' } \times 2/3 { f' g' a' }",
            ...     name="Music_Voice"
            ... )
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[0][1])

            >>> container = abjad.on_beat_grace_container(
            ...     "a'8 b'", music_voice[1][:1]
            ... )

            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[1][2])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        \times 2/3 {
                            c'4
                            \grace {
                                cs'16
                            }
                            d'4
                            e'4
                        }
                        \times 2/3 {
                            <<
                                \context Voice = "On_Beat_Grace_Container"
                                {
                                    \set fontSize = #-3
                                    \slash
                                    \voiceOne
                                    <
                                        \tweak font-size 0
                                        \tweak transparent ##t
                                        f'
                                        a'
                                    >8
                                    [
                                    (
                                    b'8
                                    )
                                    ]
                                }
                                \context Voice = "Music_Voice"
                                {
                                    \voiceTwo
                                    f'4
                                }
                            >>
                            \oneVoice
                            g'4
                            \afterGrace
                            a'4
                            {
                                fs'16
                            }
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.get.parentage(component)
            ...     print(f"{repr(component):30} {repr(parentage.prolation)}")
            <Staff{1}>                     Multiplier(1, 1)
            <Voice-"Music_Voice"{2}>       Multiplier(1, 1)
            Tuplet('3:2', "c'4 d'4 e'4") Multiplier(2, 3)
            Note("c'4")                    Multiplier(2, 3)
            BeforeGraceContainer("cs'16")        Multiplier(2, 3)
            Note("cs'16")                  Multiplier(2, 3)
            Note("d'4")                    Multiplier(2, 3)
            Note("e'4")                    Multiplier(2, 3)
            Tuplet('3:2', "{ { <f' a'>8 b'8 } { f'4 } } g'4 a'4") Multiplier(2, 3)
            <<<2>>>                        Multiplier(2, 3)
            OnBeatGraceContainer("<f' a'>8 b'8") Multiplier(2, 3)
            Chord("<f' a'>8")              Multiplier(2, 3)
            Note("b'8")                    Multiplier(2, 3)
            Voice("f'4", name='Music_Voice') Multiplier(2, 3)
            Note("f'4")                    Multiplier(2, 3)
            Note("g'4")                    Multiplier(2, 3)
            Note("a'4")                    Multiplier(2, 3)
            AfterGraceContainer("fs'16")   Multiplier(2, 3)
            Note("fs'16")                  Multiplier(2, 3)

        """
        prolations = [Multiplier(1)] + self._prolations()
        products = math.cumulative_products(prolations)
        return products[-1]

    @property
    def root(self) -> Component:
        r"""
        Gets root.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3
                                \slash
                                \voiceOne
                                <
                                    \tweak font-size 0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo
                                e'4
                            }
                        >>
                        \oneVoice
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.get.parentage(component)
            ...     print(f"{repr(component):30} {repr(parentage.root)}")
            <Staff{1}>                     <Staff{1}>
            <Voice-"Music_Voice"{4}>       <Staff{1}>
            Note("c'4")                    <Staff{1}>
            BeforeGraceContainer("cs'16")        <Staff{1}>
            Note("cs'16")                  <Staff{1}>
            Note("d'4")                    <Staff{1}>
            <<<2>>>                        <Staff{1}>
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") <Staff{1}>
            Chord("<e' g'>16")             <Staff{1}>
            Note("gs'16")                  <Staff{1}>
            Note("a'16")                   <Staff{1}>
            Note("as'16")                  <Staff{1}>
            Voice("e'4", name='Music_Voice') <Staff{1}>
            Note("e'4")                    <Staff{1}>
            Note("f'4")                    <Staff{1}>
            AfterGraceContainer("fs'16")   <Staff{1}>
            Note("fs'16")                  <Staff{1}>

        """
        root = self.get(n=-1)
        assert isinstance(root, Component), repr(root)
        return root

    ### PUBLIC METHODS ###

    def count(self, prototype=None) -> int:
        r"""
        Gets number of ``prototype`` in parentage.

        ..  container:: example

            Gets tuplet count:

            >>> staff = abjad.Staff(
            ...     r"\times 2/3 { c'2 \times 2/3 { d'8 e' f' } } \times 2/3 { c'4 d' e' }"
            ... )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \times 2/3 {
                        c'2
                        \times 2/3 {
                            d'8
                            e'8
                            f'8
                        }
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.get.parentage(component)
            ...     count = parentage.count(abjad.Tuplet)
            ...     print(f"{repr(component):55} {repr(count)}")
            <Staff{2}>                                              0
            Tuplet('3:2', "c'2 { 2/3 d'8 e'8 f'8 }")                1
            Note("c'2")                                             1
            Tuplet('3:2', "d'8 e'8 f'8")                            2
            Note("d'8")                                             2
            Note("e'8")                                             2
            Note("f'8")                                             2
            Tuplet('3:2', "c'4 d'4 e'4")                            1
            Note("c'4")                                             1
            Note("d'4")                                             1
            Note("e'4")                                             1

        ..  container:: example

            Gets voice count:

            >>> outer_red_voice = abjad.Voice("e''8 d''", name="Red_Voice")
            >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name="Red_Voice")
            >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name="Blue_Voice")
            >>> container = abjad.Container(
            ...     [inner_red_voice, inner_blue_voice],
            ...     simultaneous=True,
            ... )
            >>> outer_red_voice.append(container)
            >>> outer_red_voice.extend("d''8")
            >>> abjad.override(outer_red_voice).NoteHead.color = "#red"
            >>> literal = abjad.LilyPondLiteral(r"\voiceOne")
            >>> abjad.attach(literal, outer_red_voice[0])
            >>> abjad.override(inner_blue_voice).NoteHead.color = "#blue"
            >>> literal = abjad.LilyPondLiteral(r"\voiceTwo")
            >>> abjad.attach(literal, inner_blue_voice[0])
            >>> dynamic = abjad.Dynamic("f")
            >>> abjad.attach(dynamic, outer_red_voice[0])
            >>> abjad.show(outer_red_voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(outer_red_voice)
                >>> print(string)
                \context Voice = "Red_Voice"
                \with
                {
                    \override NoteHead.color = #red
                }
                {
                    \voiceOne
                    e''8
                    \f
                    d''8
                    <<
                        \context Voice = "Red_Voice"
                        {
                            c''4
                            b'4
                            c''8
                        }
                        \context Voice = "Blue_Voice"
                        \with
                        {
                            \override NoteHead.color = #blue
                        }
                        {
                            \voiceTwo
                            e'4
                            f'4
                            e'8
                        }
                    >>
                    d''8
                }

            >>> for leaf in abjad.iterate(outer_red_voice).leaves():
            ...     depth = abjad.get.parentage(leaf).count(abjad.Voice)
            ...     print(leaf, depth)
            ...
            e''8 1
            d''8 1
            c''4 2
            b'4 2
            c''8 2
            e'4 2
            f'4 2
            e'8 2
            d''8 1

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3
                                \slash
                                \voiceOne
                                <
                                    \tweak font-size 0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo
                                e'4
                            }
                        >>
                        \oneVoice
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.get.parentage(component)
            ...     count = parentage.count(abjad.Staff)
            ...     print(f"{repr(component):30} {repr(count)}")
            <Staff{1}>                     1
            <Voice-"Music_Voice"{4}>       1
            Note("c'4")                    1
            BeforeGraceContainer("cs'16")        1
            Note("cs'16")                  1
            Note("d'4")                    1
            <<<2>>>                        1
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") 1
            Chord("<e' g'>16")             1
            Note("gs'16")                  1
            Note("a'16")                   1
            Note("as'16")                  1
            Voice("e'4", name='Music_Voice') 1
            Note("e'4")                    1
            Note("f'4")                    1
            AfterGraceContainer("fs'16")   1
            Note("fs'16")                  1

        """
        n = 0
        if prototype is None:
            prototype = Component
        for component in self:
            if isinstance(component, prototype):
                n += 1
        return n

    def get(self, prototype=None, n=0) -> typing.Optional[Component]:
        r"""
        Gets instance ``n`` of ``prototype`` in parentage.

        ..  container:: example

            >>> outer_red_voice = abjad.Voice("e''8 d''", name="Red_Voice")
            >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name="Red_Voice")
            >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name="Blue_Voice")
            >>> container = abjad.Container(
            ...     [inner_red_voice, inner_blue_voice],
            ...     simultaneous=True,
            ... )
            >>> outer_red_voice.append(container)
            >>> outer_red_voice.extend("d''8")
            >>> abjad.override(outer_red_voice).NoteHead.color = "#red"
            >>> literal = abjad.LilyPondLiteral(r"\voiceOne")
            >>> abjad.attach(literal, outer_red_voice[0])
            >>> abjad.override(inner_blue_voice).NoteHead.color = "#blue"
            >>> literal = abjad.LilyPondLiteral(r"\voiceTwo")
            >>> abjad.attach(literal, inner_blue_voice[0])
            >>> dynamic = abjad.Dynamic("f")
            >>> abjad.attach(dynamic, outer_red_voice[0])
            >>> abjad.show(outer_red_voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(outer_red_voice)
                >>> print(string)
                \context Voice = "Red_Voice"
                \with
                {
                    \override NoteHead.color = #red
                }
                {
                    \voiceOne
                    e''8
                    \f
                    d''8
                    <<
                        \context Voice = "Red_Voice"
                        {
                            c''4
                            b'4
                            c''8
                        }
                        \context Voice = "Blue_Voice"
                        \with
                        {
                            \override NoteHead.color = #blue
                        }
                        {
                            \voiceTwo
                            e'4
                            f'4
                            e'8
                        }
                    >>
                    d''8
                }

            ..  container:: example

                >>> leaf = abjad.get.leaf(inner_red_voice, 0)
                >>> leaf
                Note("c''4")

                >>> parentage = abjad.get.parentage(leaf)

                Returns self when ``n=0``:

                >>> parentage.get(abjad.Component, 0)
                Note("c''4")

                Returns parents with positive ``n``:

                >>> parentage.get(abjad.Component, 1)
                Voice("c''4 b'4 c''8", name='Red_Voice')

                >>> parentage.get(abjad.Component, 2)
                <<<2>>>

                >>> parentage.get(abjad.Component, 3)
                <Voice-"Red_Voice"{4}>

                Returns none with ``n`` greater than score depth:

                >>> parentage.get(abjad.Component, 4) is None
                True

                >>> parentage.get(abjad.Component, 5) is None
                True

                >>> parentage.get(abjad.Component, 99) is None
                True

                Returns score root with ``n=-1``:

                >>> parentage.get(abjad.Component, -1)
                <Voice-"Red_Voice"{4}>

                With other negative ``n``:

                >>> parentage.get(abjad.Component, -2)
                <<<2>>>

                >>> parentage.get(abjad.Component, -3)
                Voice("c''4 b'4 c''8", name='Red_Voice')

                >>> parentage.get(abjad.Component, -4)
                Note("c''4")

                Returns none for sufficiently negative ``n``:

                >>> parentage.get(abjad.Component, -5) is None
                True

                >>> parentage.get(abjad.Component, -7) is None
                True

                >>> parentage.get(abjad.Component, -99) is None
                True

            ..  container:: example

                Works with nested voices and tuplets:

                >>> leaf = abjad.get.leaf(inner_red_voice, 0)
                >>> parentage = abjad.get.parentage(leaf)
                >>> leaf
                Note("c''4")

                Nonnegative ``n``:

                >>> parentage.get(abjad.Voice, 0)
                Voice("c''4 b'4 c''8", name='Red_Voice')

                >>> parentage.get(abjad.Voice, 1)
                <Voice-"Red_Voice"{4}>

                >>> parentage.get(abjad.Voice, 2) is None
                True

                >>> parentage.get(abjad.Voice, 9) is None
                True

                Negative ``n``:

                >>> parentage.get(abjad.Voice, -1)
                <Voice-"Red_Voice"{4}>

                >>> parentage.get(abjad.Voice, -2)
                Voice("c''4 b'4 c''8", name='Red_Voice')

                >>> parentage.get(abjad.Voice, -3) is None
                True

                >>> parentage.get(abjad.Voice, -99) is None
                True

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3
                                \slash
                                \voiceOne
                                <
                                    \tweak font-size 0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo
                                e'4
                            }
                        >>
                        \oneVoice
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.get.parentage(component)
            ...     result = parentage.get(abjad.Staff)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{1}>                     <Staff{1}>
            <Voice-"Music_Voice"{4}>       <Staff{1}>
            Note("c'4")                    <Staff{1}>
            BeforeGraceContainer("cs'16")        <Staff{1}>
            Note("cs'16")                  <Staff{1}>
            Note("d'4")                    <Staff{1}>
            <<<2>>>                        <Staff{1}>
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") <Staff{1}>
            Chord("<e' g'>16")             <Staff{1}>
            Note("gs'16")                  <Staff{1}>
            Note("a'16")                   <Staff{1}>
            Note("as'16")                  <Staff{1}>
            Voice("e'4", name='Music_Voice') <Staff{1}>
            Note("e'4")                    <Staff{1}>
            Note("f'4")                    <Staff{1}>
            AfterGraceContainer("fs'16")   <Staff{1}>
            Note("fs'16")                  <Staff{1}>

        """
        if prototype is None:
            prototype = (Component,)
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        if 0 <= n:
            i = 0
            for component in self:
                if isinstance(component, prototype):
                    if i == n:
                        return component
                    i += 1
        else:
            i = -1
            for component in reversed(self):
                if isinstance(component, prototype):
                    if i == n:
                        return component
                    i -= 1
        return None

    def logical_voice(self) -> OrderedDict:
        r"""
        Gets logical voice.

        ..  container:: example

            Gets logical voice of note:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4", name="Music_Voice")
            >>> staff = abjad.Staff([voice], name="Music_Staff")
            >>> score = abjad.Score([staff], name="Score")
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Music_Staff"
                    {
                        \context Voice = "Music_Voice"
                        {
                            c'4
                            d'4
                            e'4
                            f'4
                        }
                    }
                >>

            >>> note = voice[0]
            >>> parentage = abjad.get.parentage(note)
            >>> logical_voice = parentage.logical_voice()
            >>> string = abjad.storage(logical_voice)
            >>> print(string)
            abjad.OrderedDict(
                [
                    ('score', "Score-'Score'"),
                    ('staff', "Staff-'Music_Staff'"),
                    ('staff group', ''),
                    ('voice', "Voice-'Music_Voice'"),
                    ]
                )

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container_1 = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container_1, voice[1])
            >>> container_2 = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container_2, voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Music_Voice"
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    e'4
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> lv = abjad.get.parentage(voice).logical_voice()
            >>> string = abjad.storage(lv)
            >>> print(string)
            abjad.OrderedDict(
                [
                    ('score', ''),
                    ('staff', ''),
                    ('staff group', ''),
                    ('voice', "Voice-'Music_Voice'"),
                    ]
                )

            >>> lv = abjad.get.parentage(container_1).logical_voice()
            >>> string = abjad.storage(lv)
            >>> print(string)
            abjad.OrderedDict(
                [
                    ('score', ''),
                    ('staff', ''),
                    ('staff group', ''),
                    ('voice', "Voice-'Music_Voice'"),
                    ]
                )

            >>> lv = abjad.get.parentage(container_1[0]).logical_voice()
            >>> string = abjad.storage(lv)
            >>> print(string)
            abjad.OrderedDict(
                [
                    ('score', ''),
                    ('staff', ''),
                    ('staff group', ''),
                    ('voice', "Voice-'Music_Voice'"),
                    ]
                )

            >>> lv = abjad.get.parentage(container_2).logical_voice()
            >>> string = abjad.storage(lv)
            >>> print(string)
            abjad.OrderedDict(
                [
                    ('score', ''),
                    ('staff', ''),
                    ('staff group', ''),
                    ('voice', "Voice-'Music_Voice'"),
                    ]
                )

            >>> lv = abjad.get.parentage(container_2[0]).logical_voice()
            >>> string = abjad.storage(lv)
            >>> print(string)
            abjad.OrderedDict(
                [
                    ('score', ''),
                    ('staff', ''),
                    ('staff group', ''),
                    ('voice', "Voice-'Music_Voice'"),
                    ]
                )

        """
        keys = ("score", "staff group", "staff", "voice")
        logical_voice = collections.OrderedDict.fromkeys(keys, "")
        for component in self:
            if isinstance(component, Voice):
                if not logical_voice["voice"]:
                    logical_voice["voice"] = self._id_string(component)
            elif isinstance(component, Staff):
                if not logical_voice["staff"]:
                    logical_voice["staff"] = self._id_string(component)
                    # explicit staff demands a nested voice:
                    # if no explicit voice has been found,
                    # create implicit voice here with random integer
                    if not logical_voice["voice"]:
                        logical_voice["voice"] = str(id(component))
            elif isinstance(component, StaffGroup):
                if not logical_voice["staff group"]:
                    logical_voice["staff group"] = self._id_string(component)
            elif isinstance(component, Score):
                if not logical_voice["score"]:
                    logical_voice["score"] = self._id_string(component)
        logical_voice_ = OrderedDict(logical_voice)
        return logical_voice_

    def score_index(self) -> typing.Tuple[typing.Union[int, str], ...]:
        r"""
        Gets score index.

        ..  container:: example

            >>> staff_1 = abjad.Staff(r"\times 2/3 { c''2 b'2 a'2 }")
            >>> staff_2 = abjad.Staff("c'2 d'2")
            >>> score = abjad.Score([staff_1, staff_2])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                <<
                    \new Staff
                    {
                        \times 2/3 {
                            c''2
                            b'2
                            a'2
                        }
                    }
                    \new Staff
                    {
                        c'2
                        d'2
                    }
                >>

            >>> for component in abjad.select(score).components():
            ...     parentage = abjad.get.parentage(component)
            ...     component, parentage.score_index()
            ...
            (<Score<<2>>>, ())
            (<Staff{1}>, (0,))
            (Tuplet('3:2', "c''2 b'2 a'2"), (0, 0))
            (Note("c''2"), (0, 0, 0))
            (Note("b'2"), (0, 0, 1))
            (Note("a'2"), (0, 0, 2))
            (Staff("c'2 d'2"), (1,))
            (Note("c'2"), (1, 0))
            (Note("d'2"), (1, 1))

            Score root sets score index to ``()``.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3
                                \slash
                                \voiceOne
                                <
                                    \tweak font-size 0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo
                                e'4
                            }
                        >>
                        \oneVoice
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.get.parentage(component)
            ...     score_index = parentage.score_index()
            ...     print(f"{repr(component):30} {repr(score_index)}")
            <Staff{1}>                     ()
            <Voice-"Music_Voice"{4}>       (0,)
            Note("c'4")                    (0, 0)
            BeforeGraceContainer("cs'16")        (0, 0, 1, '-G')
            Note("cs'16")                  (0, 0, 1, '-G', 0)
            Note("d'4")                    (0, 1)
            <<<2>>>                        (0, 2)
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") (0, 2, 0)
            Chord("<e' g'>16")             (0, 2, 0, 0)
            Note("gs'16")                  (0, 2, 0, 1)
            Note("a'16")                   (0, 2, 0, 2)
            Note("as'16")                  (0, 2, 0, 3)
            Voice("e'4", name='Music_Voice') (0, 2, 1)
            Note("e'4")                    (0, 2, 1, 0)
            Note("f'4")                    (0, 3)
            AfterGraceContainer("fs'16")   (0, 0, 3, '+G')
            Note("fs'16")                  (0, 0, 3, '+G', 0)

        """
        result: typing.List[typing.Union[int, str]] = []
        current = self[0]
        for parent in self[1:]:
            if isinstance(current, BeforeGraceContainer):
                tuple_ = type(self)(current._main_leaf).score_index()
                list_ = list(tuple_) + ["-G"]
                result[0:0] = list_
            elif isinstance(current, AfterGraceContainer):
                tuple_ = type(self)(current._main_leaf).score_index()
                list_ = list(tuple_) + ["+G"]
                result[0:0] = list_
            else:
                index = parent.index(current)
                result.insert(0, index)
            current = parent
        return tuple(result)
