import collections
import fractions

from . import math as _math
from . import score as _score


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
        Staff('{ c4 }', name='Bass_Staff')
        Score("{ { e'4 } } { { c4 } }", simultaneous=True)

    '''

    ### CLASS VARIABLES ###

    __slots__ = ("_component", "_components")

    ### INITIALIZER ###

    def __init__(self, component=None):
        components = []
        if component is not None:
            assert isinstance(component, _score.Component), repr(component)
            components.extend(component._get_parentage())
        self._component = component
        self._components = tuple(components)

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a parent with the same components as this parentage.
        """
        if isinstance(argument, type(self)):
            if len(self) == len(argument):
                for c, d in zip(self, argument):
                    if c is not d:
                        return False
                else:
                    return True
        return False

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

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}(component={self.component!r})"

    ### PRIVATE METHODS ###

    @staticmethod
    def _id_string(component):
        lhs = component.__class__.__name__
        rhs = getattr(component, "name", None) or id(component)
        return f"{lhs}-{rhs!r}"

    def _prolations(self):
        prolations = []
        default = fractions.Fraction(1)
        for parent in self:
            prolation = getattr(parent, "implied_prolation", default)
            prolations.append(prolation)
        return prolations

    ### PUBLIC PROPERTIES ###

    @property
    def component(self) -> _score.Component:
        r"""
        Gets component.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
            >>> abjad.attach(abjad.Articulation(">"), obgc[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "MusicVoice"
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
                            \context Voice = "MusicVoice"
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

            >>> for component in abjad.select.components(staff):
            ...     parentage = abjad.get.parentage(component)
            ...     print(f"{repr(component):30} {repr(parentage.component)}")
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Note("c'4")                    Note("c'4")
            BeforeGraceContainer("cs'16")  BeforeGraceContainer("cs'16")
            Note("cs'16")                  Note("cs'16")
            Note("d'4")                    Note("d'4")
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Chord("<e' g'>16")             Chord("<e' g'>16")
            Note("gs'16")                  Note("gs'16")
            Note("a'16")                   Note("a'16")
            Note("as'16")                  Note("as'16")
            Voice("e'4", name='MusicVoice') Voice("e'4", name='MusicVoice')
            Note("e'4")                    Note("e'4")
            Note("f'4")                    Note("f'4")
            AfterGraceContainer("fs'16")   AfterGraceContainer("fs'16")
            Note("fs'16")                  Note("fs'16")

        """
        return self._component

    @property
    def components(self) -> tuple[_score.Component]:
        r"""
        Gets components.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
            >>> abjad.attach(abjad.Articulation(">"), obgc[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "MusicVoice"
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
                            \context Voice = "MusicVoice"
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

            >>> for component in abjad.select.components(staff):
            ...     parentage = abjad.get.parentage(component)
            ...     components = parentage.components
            ...     print(f"{repr(component)}:")
            ...     for component_ in components:
            ...         print(f"    {repr(component_)}")
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }"):
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice'):
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("c'4"):
                Note("c'4")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            BeforeGraceContainer("cs'16"):
                BeforeGraceContainer("cs'16")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("cs'16"):
                Note("cs'16")
                BeforeGraceContainer("cs'16")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("d'4"):
                Note("d'4")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }"):
                Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Chord("<e' g'>16"):
                Chord("<e' g'>16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("gs'16"):
                Note("gs'16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("a'16"):
                Note("a'16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("as'16"):
                Note("as'16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("e'4", name='MusicVoice'):
                Voice("e'4", name='MusicVoice')
                Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("e'4"):
                Note("e'4")
                Voice("e'4", name='MusicVoice')
                Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("f'4"):
                Note("f'4")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            AfterGraceContainer("fs'16"):
                AfterGraceContainer("fs'16")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("fs'16"):
                Note("fs'16")
                AfterGraceContainer("fs'16")
                Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
                Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")

        """
        return self._components

    @property
    def orphan(self) -> bool:
        r"""
        Is true when component has no parent.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
            >>> abjad.attach(abjad.Articulation(">"), obgc[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "MusicVoice"
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
                            \context Voice = "MusicVoice"
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

            >>> for component in abjad.select.components(staff):
            ...     parentage = abjad.get.parentage(component)
            ...     print(f"{repr(component):30} {repr(parentage.orphan)}")
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") True
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') False
            Note("c'4")                    False
            BeforeGraceContainer("cs'16")  False
            Note("cs'16")                  False
            Note("d'4")                    False
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") False
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") False
            Chord("<e' g'>16")             False
            Note("gs'16")                  False
            Note("a'16")                   False
            Note("as'16")                  False
            Voice("e'4", name='MusicVoice') False
            Note("e'4")                    False
            Note("f'4")                    False
            AfterGraceContainer("fs'16")   False
            Note("fs'16")                  False

        """
        return self.parent is None

    @property
    def parent(self) -> _score.Component | None:
        r"""
        Gets parent.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
            >>> abjad.attach(abjad.Articulation(">"), obgc[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "MusicVoice"
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
                            \context Voice = "MusicVoice"
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

            >>> for component in abjad.select.components(staff):
            ...     parentage = abjad.get.parentage(component)
            ...     print(f"{repr(component):30} {repr(parentage.parent)}")
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") None
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("c'4")                    Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            BeforeGraceContainer("cs'16")  Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Note("cs'16")                  BeforeGraceContainer("cs'16")
            Note("d'4")                    Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            Chord("<e' g'>16")             OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Note("gs'16")                  OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Note("a'16")                   OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Note("as'16")                  OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Voice("e'4", name='MusicVoice') Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            Note("e'4")                    Voice("e'4", name='MusicVoice')
            Note("f'4")                    Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            AfterGraceContainer("fs'16")   Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Note("fs'16")                  AfterGraceContainer("fs'16")

        """
        return self.get(n=1)

    @property
    def prolation(self) -> fractions.Fraction:
        r"""
        Gets prolation.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice(
            ...     r"\times 2/3 { c'4 d' e' } \times 2/3 { f' g' a' }",
            ...     name="MusicVoice"
            ... )
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[0][1])
            >>> obgc = abjad.on_beat_grace_container("a'8 b'", music_voice[1][:1])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[1][2])
            >>> staff = abjad.Staff([music_voice])
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "MusicVoice"
                    {
                        \tuplet 3/2
                        {
                            c'4
                            \grace {
                                cs'16
                            }
                            d'4
                            e'4
                        }
                        \tuplet 3/2
                        {
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
                                \context Voice = "MusicVoice"
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

            >>> for component in abjad.select.components(staff):
            ...     parentage = abjad.get.parentage(component)
            ...     print(f"{repr(component):30} {repr(parentage.prolation)}")
            Staff("{ { 3:2 c'4 d'4 e'4 } { 3:2 { { <f' a'>8 b'8 } { f'4 } } g'4 a'4 } }") Fraction(1, 1)
            Voice("{ 3:2 c'4 d'4 e'4 } { 3:2 { { <f' a'>8 b'8 } { f'4 } } g'4 a'4 }", name='MusicVoice') Fraction(1, 1)
            Tuplet('3:2', "c'4 d'4 e'4")   Fraction(2, 3)
            Note("c'4")                    Fraction(2, 3)
            BeforeGraceContainer("cs'16")  Fraction(2, 3)
            Note("cs'16")                  Fraction(2, 3)
            Note("d'4")                    Fraction(2, 3)
            Note("e'4")                    Fraction(2, 3)
            Tuplet('3:2', "{ { <f' a'>8 b'8 } { f'4 } } g'4 a'4") Fraction(2, 3)
            Container("{ <f' a'>8 b'8 } { f'4 }") Fraction(2, 3)
            OnBeatGraceContainer("<f' a'>8 b'8") Fraction(2, 3)
            Chord("<f' a'>8")              Fraction(2, 3)
            Note("b'8")                    Fraction(2, 3)
            Voice("f'4", name='MusicVoice') Fraction(2, 3)
            Note("f'4")                    Fraction(2, 3)
            Note("g'4")                    Fraction(2, 3)
            Note("a'4")                    Fraction(2, 3)
            AfterGraceContainer("fs'16")   Fraction(2, 3)
            Note("fs'16")                  Fraction(2, 3)

        """
        prolations = [fractions.Fraction(1)] + self._prolations()
        products = _math.cumulative_products(prolations)
        return products[-1]

    @property
    def root(self) -> _score.Component:
        r"""
        Gets root.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
            >>> abjad.attach(abjad.Articulation(">"), obgc[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "MusicVoice"
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
                            \context Voice = "MusicVoice"
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

            >>> for component in abjad.select.components(staff):
            ...     parentage = abjad.get.parentage(component)
            ...     print(f"{repr(component):30} {repr(parentage.root)}")
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("c'4")                    Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            BeforeGraceContainer("cs'16")  Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("cs'16")                  Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("d'4")                    Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Chord("<e' g'>16")             Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("gs'16")                  Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("a'16")                   Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("as'16")                  Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("e'4", name='MusicVoice') Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("e'4")                    Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("f'4")                    Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            AfterGraceContainer("fs'16")   Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("fs'16")                  Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")

        """
        root = self.get(n=-1)
        assert isinstance(root, _score.Component), repr(root)
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
                    \tuplet 3/2
                    {
                        c'2
                        \tuplet 3/2
                        {
                            d'8
                            e'8
                            f'8
                        }
                    }
                    \tuplet 3/2
                    {
                        c'4
                        d'4
                        e'4
                    }
                }

            >>> for component in abjad.select.components(staff):
            ...     parentage = abjad.get.parentage(component)
            ...     count = parentage.count(abjad.Tuplet)
            ...     print(f"{repr(component):55} {repr(count)}")
            Staff("{ 3:2 c'2 { 3:2 d'8 e'8 f'8 } } { 3:2 c'4 d'4 e'4 }") 0
            Tuplet('3:2', "c'2 { 3:2 d'8 e'8 f'8 }")                1
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
            >>> command = abjad.VoiceNumber(1)
            >>> abjad.attach(command, outer_red_voice[0])
            >>> abjad.override(inner_blue_voice).NoteHead.color = "#blue"
            >>> command = abjad.VoiceNumber(2)
            >>> abjad.attach(command, inner_blue_voice[0])
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

            >>> for leaf in abjad.iterate.leaves(outer_red_voice):
            ...     depth = abjad.get.parentage(leaf).count(abjad.Voice)
            ...     print(leaf, depth)
            ...
            Note("e''8") 1
            Note("d''8") 1
            Note("c''4") 2
            Note("b'4") 2
            Note("c''8") 2
            Note("e'4") 2
            Note("f'4") 2
            Note("e'8") 2
            Note("d''8") 1

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
            >>> abjad.attach(abjad.Articulation(">"), obgc[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "MusicVoice"
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
                            \context Voice = "MusicVoice"
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

            >>> for component in abjad.select.components(staff):
            ...     parentage = abjad.get.parentage(component)
            ...     count = parentage.count(abjad.Staff)
            ...     print(f"{repr(component):30} {repr(count)}")
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") 1
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') 1
            Note("c'4")                    1
            BeforeGraceContainer("cs'16")  1
            Note("cs'16")                  1
            Note("d'4")                    1
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") 1
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") 1
            Chord("<e' g'>16")             1
            Note("gs'16")                  1
            Note("a'16")                   1
            Note("as'16")                  1
            Voice("e'4", name='MusicVoice') 1
            Note("e'4")                    1
            Note("f'4")                    1
            AfterGraceContainer("fs'16")   1
            Note("fs'16")                  1

        """
        n = 0
        if prototype is None:
            prototype = _score.Component
        for component in self:
            if isinstance(component, prototype):
                n += 1
        return n

    def get(self, prototype=None, n=0) -> _score.Component | None:
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
            >>> command = abjad.VoiceNumber(1)
            >>> abjad.attach(command, outer_red_voice[0])
            >>> abjad.override(inner_blue_voice).NoteHead.color = "#blue"
            >>> command = abjad.VoiceNumber(2)
            >>> abjad.attach(command, inner_blue_voice[0])
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
                Container("{ c''4 b'4 c''8 } { e'4 f'4 e'8 }")

                >>> parentage.get(abjad.Component, 3)
                Voice("e''8 d''8 { { c''4 b'4 c''8 } { e'4 f'4 e'8 } } d''8", name='Red_Voice')

                Returns none with ``n`` greater than score depth:

                >>> parentage.get(abjad.Component, 4) is None
                True

                >>> parentage.get(abjad.Component, 5) is None
                True

                >>> parentage.get(abjad.Component, 99) is None
                True

                Returns score root with ``n=-1``:

                >>> parentage.get(abjad.Component, -1)
                Voice("e''8 d''8 { { c''4 b'4 c''8 } { e'4 f'4 e'8 } } d''8", name='Red_Voice')

                With other negative ``n``:

                >>> parentage.get(abjad.Component, -2)
                Container("{ c''4 b'4 c''8 } { e'4 f'4 e'8 }")

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
                Voice("e''8 d''8 { { c''4 b'4 c''8 } { e'4 f'4 e'8 } } d''8", name='Red_Voice')

                >>> parentage.get(abjad.Voice, 2) is None
                True

                >>> parentage.get(abjad.Voice, 9) is None
                True

                Negative ``n``:

                >>> parentage.get(abjad.Voice, -1)
                Voice("e''8 d''8 { { c''4 b'4 c''8 } { e'4 f'4 e'8 } } d''8", name='Red_Voice')

                >>> parentage.get(abjad.Voice, -2)
                Voice("c''4 b'4 c''8", name='Red_Voice')

                >>> parentage.get(abjad.Voice, -3) is None
                True

                >>> parentage.get(abjad.Voice, -99) is None
                True

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
            >>> abjad.attach(abjad.Articulation(">"), obgc[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "MusicVoice"
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
                            \context Voice = "MusicVoice"
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

            >>> for component in abjad.select.components(staff):
            ...     parentage = abjad.get.parentage(component)
            ...     result = parentage.get(abjad.Staff)
            ...     print(f"{repr(component):30} {repr(result)}")
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("c'4")                    Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            BeforeGraceContainer("cs'16")  Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("cs'16")                  Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("d'4")                    Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Chord("<e' g'>16")             Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("gs'16")                  Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("a'16")                   Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("as'16")                  Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("e'4", name='MusicVoice') Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("e'4")                    Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("f'4")                    Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            AfterGraceContainer("fs'16")   Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Note("fs'16")                  Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")

        """
        if prototype is None:
            prototype = (_score.Component,)
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

    def logical_voice(self) -> dict:
        r"""
        Gets logical voice.

        ..  container:: example

            Gets logical voice of note:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4", name="MusicVoice")
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
                        \context Voice = "MusicVoice"
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
            >>> parentage.logical_voice()
            {'score': "Score-'Score'", 'staff group': '', 'staff': "Staff-'Music_Staff'", 'voice': "Voice-'MusicVoice'"}

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
            >>> container_1 = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container_1, voice[1])
            >>> container_2 = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container_2, voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "MusicVoice"
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

            >>> abjad.get.parentage(voice).logical_voice()
            {'score': '', 'staff group': '', 'staff': '', 'voice': "Voice-'MusicVoice'"}

            >>> abjad.get.parentage(container_1).logical_voice()
            {'score': '', 'staff group': '', 'staff': '', 'voice': "Voice-'MusicVoice'"}

            >>> abjad.get.parentage(container_1[0]).logical_voice()
            {'score': '', 'staff group': '', 'staff': '', 'voice': "Voice-'MusicVoice'"}

            >>> abjad.get.parentage(container_2).logical_voice()
            {'score': '', 'staff group': '', 'staff': '', 'voice': "Voice-'MusicVoice'"}

            >>> abjad.get.parentage(container_2[0]).logical_voice()
            {'score': '', 'staff group': '', 'staff': '', 'voice': "Voice-'MusicVoice'"}

        """
        keys = ("score", "staff group", "staff", "voice")
        logical_voice = dict.fromkeys(keys, "")
        for component in self:
            if isinstance(component, _score.Voice):
                if not logical_voice["voice"]:
                    logical_voice["voice"] = self._id_string(component)
            elif isinstance(component, _score.Staff):
                if not logical_voice["staff"]:
                    logical_voice["staff"] = self._id_string(component)
                    # explicit staff demands a nested voice:
                    # if no explicit voice has been found,
                    # create implicit voice here with random integer
                    if not logical_voice["voice"]:
                        logical_voice["voice"] = str(id(component))
            elif isinstance(component, _score.StaffGroup):
                if not logical_voice["staff group"]:
                    logical_voice["staff group"] = self._id_string(component)
            elif isinstance(component, _score.Score):
                if not logical_voice["score"]:
                    logical_voice["score"] = self._id_string(component)
        logical_voice_ = dict(logical_voice)
        return logical_voice_

    def score_index(self) -> tuple[int | str, ...]:
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
                        \tuplet 3/2
                        {
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

            >>> for component in abjad.select.components(score):
            ...     parentage = abjad.get.parentage(component)
            ...     component, parentage.score_index()
            ...
            (Score("{ { 3:2 c''2 b'2 a'2 } } { c'2 d'2 }", simultaneous=True), ())
            (Staff("{ 3:2 c''2 b'2 a'2 }"), (0,))
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

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
            >>> abjad.attach(abjad.Articulation(">"), obgc[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "MusicVoice"
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
                            \context Voice = "MusicVoice"
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

            >>> for component in abjad.select.components(staff):
            ...     parentage = abjad.get.parentage(component)
            ...     score_index = parentage.score_index()
            ...     print(f"{repr(component):30} {repr(score_index)}")
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") ()
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') (0,)
            Note("c'4")                    (0, 0)
            BeforeGraceContainer("cs'16")  (0, 0, 1, '-G')
            Note("cs'16")                  (0, 0, 1, '-G', 0)
            Note("d'4")                    (0, 1)
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") (0, 2)
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") (0, 2, 0)
            Chord("<e' g'>16")             (0, 2, 0, 0)
            Note("gs'16")                  (0, 2, 0, 1)
            Note("a'16")                   (0, 2, 0, 2)
            Note("as'16")                  (0, 2, 0, 3)
            Voice("e'4", name='MusicVoice') (0, 2, 1)
            Note("e'4")                    (0, 2, 1, 0)
            Note("f'4")                    (0, 3)
            AfterGraceContainer("fs'16")   (0, 0, 3, '+G')
            Note("fs'16")                  (0, 0, 3, '+G', 0)

        """
        result: list[int | str] = []
        current = self[0]
        for parent in self[1:]:
            if isinstance(current, _score.BeforeGraceContainer):
                tuple_ = type(self)(current._main_leaf).score_index()
                list_ = list(tuple_) + ["-G"]
                result[0:0] = list_
            elif isinstance(current, _score.AfterGraceContainer):
                tuple_ = type(self)(current._main_leaf).score_index()
                list_ = list(tuple_) + ["+G"]
                result[0:0] = list_
            else:
                index = parent.index(current)
                result.insert(0, index)
            current = parent
        return tuple(result)
