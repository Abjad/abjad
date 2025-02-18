import typing

from . import _iterlib
from . import duration as _duration
from . import pcollections as _pcollections
from . import pitch as _pitch
from . import score as _score
from . import select as _select


@typing.overload
def components(
    argument,
    *,
    exclude=None,
    grace=None,
    reverse=None,
) -> typing.Iterator[_score.Component]:
    pass


@typing.overload
def components(
    argument,
    prototype: typing.Type[_score.Tuplet],
    *,
    exclude=None,
    grace=None,
    reverse=None,
) -> typing.Iterator[_score.Tuplet]:
    pass


@typing.overload
def components(
    argument,
    prototype: typing.Type[_score.Container],
    *,
    exclude=None,
    grace=None,
    reverse=None,
) -> typing.Iterator[_score.Container]:
    pass


@typing.overload
def components(
    argument,
    prototype: typing.Type[_score.Leaf],
    *,
    exclude=None,
    grace=None,
    reverse=None,
) -> typing.Iterator[_score.Leaf]:
    pass


def components(
    argument,
    prototype=None,
    *,
    exclude=None,
    grace=None,
    reverse=None,
):
    r"""
    Iterates components in ``argument``.

    ..  container:: example

        Grace iteration is controlled by a ternary flag.

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

        Leave ``grace`` unset to iterate grace and nongrace components
        together:

        >>> for component in abjad.iterate.components(staff):
        ...     component
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
        Note("c'4")
        BeforeGraceContainer("cs'16")
        Note("cs'16")
        Note("d'4")
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
        Chord("<e' g'>16")
        Note("gs'16")
        Note("a'16")
        Note("as'16")
        Voice("e'4", name='MusicVoice')
        Note("e'4")
        Note("f'4")
        AfterGraceContainer("fs'16")
        Note("fs'16")

        >>> for component in abjad.iterate.components(staff, reverse=True):
        ...     component
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
        AfterGraceContainer("fs'16")
        Note("fs'16")
        Note("f'4")
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
        Voice("e'4", name='MusicVoice')
        Note("e'4")
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
        Note("as'16")
        Note("a'16")
        Note("gs'16")
        Chord("<e' g'>16")
        Note("d'4")
        BeforeGraceContainer("cs'16")
        Note("cs'16")
        Note("c'4")

        Set ``grace=True`` to iterate only grace components:

        >>> for component in abjad.iterate.components(staff, grace=True):
        ...     component
        BeforeGraceContainer("cs'16")
        Note("cs'16")
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
        Chord("<e' g'>16")
        Note("gs'16")
        Note("a'16")
        Note("as'16")
        AfterGraceContainer("fs'16")
        Note("fs'16")

        >>> for component in abjad.iterate.components(staff, grace=True, reverse=True):
        ...     component
        AfterGraceContainer("fs'16")
        Note("fs'16")
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
        Note("as'16")
        Note("a'16")
        Note("gs'16")
        Chord("<e' g'>16")
        BeforeGraceContainer("cs'16")
        Note("cs'16")

        Set ``grace=False`` to iterate only nongrace components:

        >>> for component in abjad.iterate.components(staff, grace=False):
        ...     component
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
        Note("c'4")
        Note("d'4")
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
        Voice("e'4", name='MusicVoice')
        Note("e'4")
        Note("f'4")

        >>> for component in abjad.iterate.components(staff, grace=False, reverse=True):
        ...     component
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
        Note("f'4")
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
        Voice("e'4", name='MusicVoice')
        Note("e'4")
        Note("d'4")
        Note("c'4")

    """
    return _iterlib._public_iterate_components(
        argument,
        prototype,
        exclude=exclude,
        grace=grace,
        reverse=reverse,
    )


def leaves(
    argument,
    prototype=None,
    *,
    exclude=None,
    grace=None,
    pitched=None,
    reverse=None,
) -> typing.Iterator:
    r"""
    Iterates leaves in ``argument``.

    ..  container:: example

        Set ``exclude=<annotation>`` to exclude leaves with annotation:

        >>> staff = abjad.Staff()
        >>> score = abjad.Score([staff], name="Score")
        >>> staff.extend("<c' bf'>8 <g' a'>8")
        >>> staff.extend("af'8 r8")
        >>> staff.extend("r8 gf'8")
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.attach("RED", staff[0])
        >>> abjad.attach("BLUE", staff[1])
        >>> abjad.attach("GREEN", staff[2])
        >>> abjad.attach("RED", staff[3])
        >>> abjad.attach("BLUE", staff[4])
        >>> abjad.attach("GREEN", staff[5])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 2/8
                <c' bf'>8
                <g' a'>8
                af'8
                r8
                r8
                gf'8
            }

        >>> for leaf in abjad.iterate.leaves(staff, exclude=['RED', 'BLUE']):
        ...     leaf
        ...
        Note("af'8")
        Note("gf'8")

        Excludes leaves to which ``'RED'`` or ``'BLUE'`` attaches.

    ..  container:: example

        Grace iteration is controlled by a ternary flag.

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

        Leave ``grace`` unset to iterate grace and nongrace leaves together:

        >>> for leaf in abjad.iterate.leaves(staff):
        ...     leaf
        Note("c'4")
        Note("cs'16")
        Note("d'4")
        Chord("<e' g'>16")
        Note("gs'16")
        Note("a'16")
        Note("as'16")
        Note("e'4")
        Note("f'4")
        Note("fs'16")

        Set ``grace=True`` to iterate only grace leaves:

        >>> for leaf in abjad.iterate.leaves(staff, grace=True):
        ...     leaf
        Note("cs'16")
        Chord("<e' g'>16")
        Note("gs'16")
        Note("a'16")
        Note("as'16")
        Note("fs'16")

        Set ``grace=False`` to iterate only nongrace leaves:

        >>> for leaf in abjad.iterate.leaves(staff, grace=False):
        ...     leaf
        Note("c'4")
        Note("d'4")
        Note("e'4")
        Note("f'4")

    ..  container:: example

        Pitched iteration is controlled by a ternary flag.

        >>> staff = abjad.Staff()
        >>> score = abjad.Score([staff], name="Score")
        >>> staff.extend("<c' bf'>8 <g' a'>8")
        >>> staff.extend("af'8 r8")
        >>> staff.extend("r8 gf'8")
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 2/8
                <c' bf'>8
                <g' a'>8
                af'8
                r8
                r8
                gf'8
            }

        Leaves ``pitched`` unset to iterate pitched and unpitched leaves
        together:

        >>> for leaf in abjad.iterate.leaves(staff):
        ...     leaf
        ...
        Chord("<c' bf'>8")
        Chord("<g' a'>8")
        Note("af'8")
        Rest('r8')
        Rest('r8')
        Note("gf'8")

        >>> for leaf in abjad.iterate.leaves(staff, reverse=True):
        ...     leaf
        Note("gf'8")
        Rest('r8')
        Rest('r8')
        Note("af'8")
        Chord("<g' a'>8")
        Chord("<c' bf'>8")

        Set ``pitched=True`` to iterate pitched leaves only:

        >>> for leaf in abjad.iterate.leaves(staff, pitched=True):
        ...     leaf
        ...
        Chord("<c' bf'>8")
        Chord("<g' a'>8")
        Note("af'8")
        Note("gf'8")

        >>> for leaf in abjad.iterate.leaves(staff, pitched=True, reverse=True):
        ...     leaf
        Note("gf'8")
        Note("af'8")
        Chord("<g' a'>8")
        Chord("<c' bf'>8")

        Set ``pitched=False`` to iterate unpitched leaves only:

        >>> for leaf in abjad.iterate.leaves(staff, pitched=False):
        ...     leaf
        ...
        Rest('r8')
        Rest('r8')

        >>> for leaf in abjad.iterate.leaves(staff, pitched=False):
        ...     leaf
        ...
        Rest('r8')
        Rest('r8')

    """
    return _iterlib._public_iterate_leaves(
        argument,
        prototype=prototype,
        exclude=exclude,
        grace=grace,
        pitched=pitched,
        reverse=reverse,
    )


def logical_ties(
    argument,
    *,
    exclude=None,
    grace=None,
    nontrivial=None,
    pitched=None,
    reverse=None,
) -> typing.Iterator[_select.LogicalTie]:
    r"""
    Iterates logical ties in ``argument``.

    ..  container:: example

        Iterates logical ties:

        >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
        >>> staff = abjad.Staff(string)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                ~
                \tuplet 3/2
                {
                    c'16
                    d'8
                }
                e'8
                f'4
                ~
                f'16
            }

        >>> for logical_tie in abjad.iterate.logical_ties(staff):
        ...     logical_tie
        ...
        LogicalTie(items=[Note("c'4"), Note("c'16")])
        LogicalTie(items=[Note("d'8")])
        LogicalTie(items=[Note("e'8")])
        LogicalTie(items=[Note("f'4"), Note("f'16")])

    ..  container:: example

        Grace iteration is controlled by a ternary flag.

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

        Leave ``grace`` unset to iterate grace and nongrace logical ties together:

        >>> for lt in abjad.iterate.logical_ties(staff):
        ...     lt
        LogicalTie(items=[Note("c'4")])
        LogicalTie(items=[Note("cs'16")])
        LogicalTie(items=[Note("d'4")])
        LogicalTie(items=[Chord("<e' g'>16")])
        LogicalTie(items=[Note("gs'16")])
        LogicalTie(items=[Note("a'16")])
        LogicalTie(items=[Note("as'16")])
        LogicalTie(items=[Note("e'4")])
        LogicalTie(items=[Note("f'4")])
        LogicalTie(items=[Note("fs'16")])

        >>> for lt in abjad.iterate.logical_ties(staff, reverse=True):
        ...     lt
        LogicalTie(items=[Note("fs'16")])
        LogicalTie(items=[Note("f'4")])
        LogicalTie(items=[Note("e'4")])
        LogicalTie(items=[Note("as'16")])
        LogicalTie(items=[Note("a'16")])
        LogicalTie(items=[Note("gs'16")])
        LogicalTie(items=[Chord("<e' g'>16")])
        LogicalTie(items=[Note("d'4")])
        LogicalTie(items=[Note("cs'16")])
        LogicalTie(items=[Note("c'4")])

        Set ``grace=True`` to iterate grace logical ties only:

        >>> for lt in abjad.iterate.logical_ties(staff, grace=True):
        ...     lt
        LogicalTie(items=[Note("cs'16")])
        LogicalTie(items=[Chord("<e' g'>16")])
        LogicalTie(items=[Note("gs'16")])
        LogicalTie(items=[Note("a'16")])
        LogicalTie(items=[Note("as'16")])
        LogicalTie(items=[Note("fs'16")])

        >>> for lt in abjad.iterate.logical_ties(staff, grace=True, reverse=True):
        ...     lt
        LogicalTie(items=[Note("fs'16")])
        LogicalTie(items=[Note("as'16")])
        LogicalTie(items=[Note("a'16")])
        LogicalTie(items=[Note("gs'16")])
        LogicalTie(items=[Chord("<e' g'>16")])
        LogicalTie(items=[Note("cs'16")])

        Set ``grace=False`` to iterate nongrace logical ties only:

        >>> for lt in abjad.iterate.logical_ties(staff, grace=False):
        ...     lt
        LogicalTie(items=[Note("c'4")])
        LogicalTie(items=[Note("d'4")])
        LogicalTie(items=[Note("e'4")])
        LogicalTie(items=[Note("f'4")])

        >>> for lt in abjad.iterate.logical_ties(staff, grace=False, reverse=True):
        ...     lt
        LogicalTie(items=[Note("f'4")])
        LogicalTie(items=[Note("e'4")])
        LogicalTie(items=[Note("d'4")])
        LogicalTie(items=[Note("c'4")])

    ..  container:: example

        Logical tie triviality is controlled by a ternary flag.

        >>> string = r"c'4 ~ \times 2/3 { c'8 d'4 }"
        >>> string += r" e'4 ~ \times 2/3 { e'8 f' }"
        >>> staff = abjad.Staff(string)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                ~
                \tuplet 3/2
                {
                    c'8
                    d'4
                }
                e'4
                ~
                \tweak edge-height #'(0.7 . 0)
                \tuplet 3/2
                {
                    e'8
                    f'8
                }
            }

        Leave ``nontrivial`` unset to iterate trivial and nontrivial
        logical ties together:

        >>> for lt in abjad.iterate.logical_ties(staff):
        ...     lt
        LogicalTie(items=[Note("c'4"), Note("c'8")])
        LogicalTie(items=[Note("d'4")])
        LogicalTie(items=[Note("e'4"), Note("e'8")])
        LogicalTie(items=[Note("f'8")])

        >>> for lt in abjad.iterate.logical_ties(staff, reverse=True):
        ...     lt
        LogicalTie(items=[Note("f'8")])
        LogicalTie(items=[Note("e'4"), Note("e'8")])
        LogicalTie(items=[Note("d'4")])
        LogicalTie(items=[Note("c'4"), Note("c'8")])

        Set ``nontrivial=True`` to iterate nontrivial logical ties only:

        >>> for lt in abjad.iterate.logical_ties(staff, nontrivial=True):
        ...     lt
        LogicalTie(items=[Note("c'4"), Note("c'8")])
        LogicalTie(items=[Note("e'4"), Note("e'8")])

        >>> for lt in abjad.iterate.logical_ties(staff, nontrivial=True, reverse=True):
        ...     lt
        LogicalTie(items=[Note("e'4"), Note("e'8")])
        LogicalTie(items=[Note("c'4"), Note("c'8")])

        Set ``nontrivial=False`` to iterate trivial logical ties only:

        >>> for lt in abjad.iterate.logical_ties(staff, nontrivial=False):
        ...     lt
        LogicalTie(items=[Note("d'4")])
        LogicalTie(items=[Note("f'8")])

        >>> for lt in abjad.iterate.logical_ties(staff, nontrivial=False, reverse=True):
        ...     lt
        LogicalTie(items=[Note("f'8")])
        LogicalTie(items=[Note("d'4")])

    ..  container:: example

        Logical tie pitchedness is controlled by a ternary flag.

        >>> string = r"c'4 ~ \times 2/3 { c'8 r4 }"
        >>> string += r"d'4 ~ \times 2/3 { d'8 r4 }"
        >>> staff = abjad.Staff(string)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                ~
                \tuplet 3/2
                {
                    c'8
                    r4
                }
                d'4
                ~
                \tuplet 3/2
                {
                    d'8
                    r4
                }
            }

        Leave ``pitched`` unset to iterate pitched and unpitched logical ties together:

        >>> for lt in abjad.iterate.logical_ties(staff):
        ...     lt
        LogicalTie(items=[Note("c'4"), Note("c'8")])
        LogicalTie(items=[Rest('r4')])
        LogicalTie(items=[Note("d'4"), Note("d'8")])
        LogicalTie(items=[Rest('r4')])

        >>> for lt in abjad.iterate.logical_ties(staff, reverse=True):
        ...     lt
        LogicalTie(items=[Rest('r4')])
        LogicalTie(items=[Note("d'4"), Note("d'8")])
        LogicalTie(items=[Rest('r4')])
        LogicalTie(items=[Note("c'4"), Note("c'8")])

        Set ``pitched=True`` to iterate pitched logical ties only:

        >>> for lt in abjad.iterate.logical_ties(staff, pitched=True):
        ...     lt
        LogicalTie(items=[Note("c'4"), Note("c'8")])
        LogicalTie(items=[Note("d'4"), Note("d'8")])

        >>> for lt in abjad.iterate.logical_ties(staff, pitched=True, reverse=True):
        ...     lt
        LogicalTie(items=[Note("d'4"), Note("d'8")])
        LogicalTie(items=[Note("c'4"), Note("c'8")])

        Set ``pitched=False`` to iterate unpitched logical ties only:

        >>> for lt in abjad.iterate.logical_ties(staff, pitched=False):
        ...     lt
        LogicalTie(items=[Rest('r4')])
        LogicalTie(items=[Rest('r4')])

        >>> for lt in abjad.iterate.logical_ties(staff, pitched=False, reverse=True):
        ...     lt
        LogicalTie(items=[Rest('r4')])
        LogicalTie(items=[Rest('r4')])

    ..  container:: example

        REGRESSION. Yields logical tie even when leaves are missing in
        input:

        >>> voice = abjad.Voice("c'8 [ ~ c' ~ c' d' ]")
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'8
                [
                ~
                c'8
                ~
                c'8
                d'8
                ]
            }

        >>> selection = voice[:2]
        >>> for logical_tie in abjad.iterate.logical_ties(selection):
        ...     logical_tie
        ...
        LogicalTie(items=[Note("c'8"), Note("c'8"), Note("c'8")])

    """
    return _iterlib._iterate_logical_ties(
        argument,
        exclude=exclude,
        grace=grace,
        nontrivial=nontrivial,
        pitched=pitched,
        reverse=reverse,
    )


def pitches(argument) -> typing.Iterator[_pitch.NamedPitch]:
    r"""
    Iterates pitches in ``argument``.

    ..  container:: example

        Iterates pitches in container:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
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

        >>> for pitch in abjad.iterate.pitches(staff):
        ...     pitch
        ...
        NamedPitch("c'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("f'")

    ..  container:: example

        Iterates pitches in pitch set:

        >>> pitch_set = abjad.PitchSet([0, 2, 4, 5])

        >>> for pitch in abjad.iterate.pitches(pitch_set):
        ...     pitch
        ...
        NumberedPitch(0)
        NumberedPitch(2)
        NumberedPitch(4)
        NumberedPitch(5)

    ..  container:: example

        Iterates different types of object in tuple:

        >>> argument = (
        ...     abjad.NamedPitch("c'"),
        ...     abjad.Note("d'4"),
        ...     abjad.Chord("<e' fs' g>4"),
        ...     )

        >>> for pitch in abjad.iterate.pitches(argument):
        ...     pitch
        ...
        NamedPitch("c'")
        NamedPitch("d'")
        NamedPitch('g')
        NamedPitch("e'")
        NamedPitch("fs'")

    """
    if isinstance(argument, _pitch.Pitch):
        pitch = _pitch.NamedPitch(argument)
        yield pitch
    result = []
    try:
        result.extend(argument.pitches)
    except AttributeError:
        pass
    if isinstance(argument, _score.Chord):
        result.extend(argument.written_pitches)
    elif isinstance(argument, _pcollections.PitchSet):
        result.extend(sorted(list(argument)))
    elif isinstance(argument, list | tuple | set):
        for item in argument:
            for pitch_ in pitches(item):
                result.append(pitch_)
    else:
        for leaf in leaves(argument):
            try:
                result.append(leaf.written_pitch)
            except AttributeError:
                pass
            try:
                result.extend(leaf.written_pitches)
            except AttributeError:
                pass
    for pitch in result:
        yield pitch


def timeline(
    argument, prototype=None, *, exclude=None, reverse=None
) -> tuple[_score.Component, ...]:
    r"""
    Iterates leaves in ``argument`` in timeline order.

    ..  container:: example

        Timeline-iterates leaves:

        >>> score = abjad.Score()
        >>> score.append(abjad.Staff("c'4 d'4 e'4 f'4"))
        >>> score.append(abjad.Staff("g'8 a'8 b'8 c''8"))
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }
                \new Staff
                {
                    g'8
                    a'8
                    b'8
                    c''8
                }
            >>

        >>> for leaf in abjad.iterate.timeline(score):
        ...     leaf
        ...
        Note("c'4")
        Note("g'8")
        Note("a'8")
        Note("d'4")
        Note("b'8")
        Note("c''8")
        Note("e'4")
        Note("f'4")

        >>> for component in abjad.iterate.timeline(score, reverse=True):
        ...     component
        ...
        Note("f'4")
        Note("e'4")
        Note("c''8")
        Note("b'8")
        Note("d'4")
        Note("a'8")
        Note("g'8")
        Note("c'4")

    ..  container:: example

        REGRESSION. Works with grace note (and containers):

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

        >>> for leaf in abjad.iterate.timeline(staff):
        ...     leaf
        Note("c'4")
        Note("cs'16")
        Note("d'4")
        Chord("<e' g'>16")
        Note("gs'16")
        Note("a'16")
        Note("as'16")
        Note("e'4")
        Note("f'4")
        Note("fs'16")

        >>> for leaf in abjad.iterate.timeline(staff, reverse=True):
        ...     leaf
        Note("fs'16")
        Note("f'4")
        Note("e'4")
        Note("as'16")
        Note("a'16")
        Note("gs'16")
        Chord("<e' g'>16")
        Note("d'4")
        Note("cs'16")
        Note("c'4")

    Iterates leaves when ``prototype`` is none.
    """
    generator = leaves(argument, prototype=prototype, exclude=exclude)
    components = list(generator)
    components.sort(key=lambda _: _._get_timespan().start_offset)
    offset_to_components: dict[_duration.Offset, list[_score.Component]] = dict()
    for component in components:
        start_offset = component._get_timespan().start_offset
        if start_offset not in offset_to_components:
            offset_to_components[start_offset] = []
    for component in components:
        start_offset = component._get_timespan().start_offset
        offset_to_components[start_offset].append(component)
    result: list[_score.Component] = []
    for start_offset, list_ in offset_to_components.items():
        result.extend(list_)
    if reverse:
        result.reverse()
    return tuple(result)
