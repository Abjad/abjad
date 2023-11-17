r"""
..  container:: example

    **CORNER CASE 1.**

    Before-grace-to-on-beat-grace works correctly when before-grace container
    is attached first:

    >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
    >>> container = abjad.BeforeGraceContainer("gs'16")
    >>> abjad.attach(container, music_voice[1])
    >>> obgc = abjad.on_beat_grace_container(
    ...     "a'8 b' c'' b'", music_voice[1:3], grace_leaf_duration=(1, 24)
    ... )
    >>> abjad.attach(abjad.Articulation(">"), obgc[0])
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
                <<
                    \context Voice = "On_Beat_Grace_Container"
                    {
                        \set fontSize = #-3
                        \slash
                        \voiceOne
                        <
                            \tweak font-size 0
                            \tweak transparent ##t
                            d'
                            a'
                        >8 * 1/3
                        - \accent
                        [
                        (
                        b'8 * 1/3
                        c''8 * 1/3
                        b'8 * 1/3
                        )
                        ]
                    }
                    \context Voice = "MusicVoice"
                    {
                        \grace {
                            gs'16
                        }
                        \voiceTwo
                        d'4
                        e'4
                    }
                >>
                \oneVoice
                f'4
            }
        }

    Before-grace-to-on-beat-grace works correctly when on-beat grace container
    is attached first:

    >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
    >>> obgc = abjad.on_beat_grace_container(
    ...     "a'8 b' c'' b'", music_voice[1:3], grace_leaf_duration=(1, 24)
    ... )
    >>> abjad.attach(abjad.Articulation(">"), obgc[0])
    >>> container = abjad.BeforeGraceContainer("gs'16")
    >>> abjad.attach(container, music_voice[1][1][0])
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
                <<
                    \context Voice = "On_Beat_Grace_Container"
                    {
                        \set fontSize = #-3
                        \slash
                        \voiceOne
                        <
                            \tweak font-size 0
                            \tweak transparent ##t
                            d'
                            a'
                        >8 * 1/3
                        - \accent
                        [
                        (
                        b'8 * 1/3
                        c''8 * 1/3
                        b'8 * 1/3
                        )
                        ]
                    }
                    \context Voice = "MusicVoice"
                    {
                        \grace {
                            gs'16
                        }
                        \voiceTwo
                        d'4
                        e'4
                    }
                >>
                \oneVoice
                f'4
            }
        }

..  container:: example

    **CORNER CASE 2.** After-grace-within-on-beat-grace works correctly:

    >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
    >>> container = abjad.AfterGraceContainer("cs'16")
    >>> abjad.attach(container, music_voice[1])
    >>> obgc = abjad.on_beat_grace_container(
    ...     "a'8 b' c'' b'", music_voice[1:3], grace_leaf_duration=(1, 24)
    ... )
    >>> abjad.attach(abjad.Articulation(">"), obgc[0])
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
                <<
                    \context Voice = "On_Beat_Grace_Container"
                    {
                        \set fontSize = #-3
                        \slash
                        \voiceOne
                        <
                            \tweak font-size 0
                            \tweak transparent ##t
                            d'
                            a'
                        >8 * 1/3
                        - \accent
                        [
                        (
                        b'8 * 1/3
                        c''8 * 1/3
                        b'8 * 1/3
                        )
                        ]
                    }
                    \context Voice = "MusicVoice"
                    {
                        \voiceTwo
                        \afterGrace
                        d'4
                        {
                            cs'16
                        }
                        e'4
                    }
                >>
                \oneVoice
                f'4
            }
        }

..  container:: example

    **CORNER CASE 3.** After-grace-to-before-grace works correctly:

    >>> music_voice = abjad.Voice("b4 d' e' f'", name="MusicVoice")
    >>> container = abjad.AfterGraceContainer("c'16")
    >>> abjad.attach(container, music_voice[0])
    >>> container = abjad.BeforeGraceContainer("cs'16")
    >>> abjad.attach(container, music_voice[1])
    >>> staff = abjad.Staff([music_voice])
    >>> abjad.show(staff) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            \context Voice = "MusicVoice"
            {
                \afterGrace
                b4
                {
                    c'16
                }
                \grace {
                    cs'16
                }
                d'4
                e'4
                f'4
            }
        }

    >>> for component in abjad.iterate.components(staff):
    ...     timespan = abjad.get.timespan(component)
    ...     print(f"{repr(component):30} {repr(timespan)}")
    Staff("{ b4 d'4 e'4 f'4 }")    Timespan(Offset((0, 1)), Offset((1, 1)))
    Voice("b4 d'4 e'4 f'4", name='MusicVoice') Timespan(Offset((0, 1)), Offset((1, 1)))
    Note('b4')                     Timespan(Offset((0, 1)), Offset((1, 4)))
    AfterGraceContainer("c'16")    Timespan(Offset((1, 4), displacement=Duration(-1, 8)), Offset((1, 4), displacement=Duration(-1, 16)))
    Note("c'16")                   Timespan(Offset((1, 4), displacement=Duration(-1, 8)), Offset((1, 4), displacement=Duration(-1, 16)))
    BeforeGraceContainer("cs'16")  Timespan(Offset((1, 4), displacement=Duration(-1, 16)), Offset((1, 4)))
    Note("cs'16")                  Timespan(Offset((1, 4), displacement=Duration(-1, 16)), Offset((1, 4)))
    Note("d'4")                    Timespan(Offset((1, 4)), Offset((1, 2)))
    Note("e'4")                    Timespan(Offset((1, 2)), Offset((3, 4)))
    Note("f'4")                    Timespan(Offset((3, 4)), Offset((1, 1)))

..  container:: example

    **CORNER CASE 4.** After-grace-to-on-beat-grace works correctly:

    >>> music_voice = abjad.Voice("b4 d' e' f'", name="MusicVoice")
    >>> container = abjad.AfterGraceContainer("c'16")
    >>> abjad.attach(container, music_voice[0])
    >>> obgc = abjad.on_beat_grace_container(
    ...     "a'8 b' c'' b'", music_voice[1:3], grace_leaf_duration=(1, 24)
    ... )
    >>> abjad.attach(abjad.Articulation(">"), obgc[0])
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
                \afterGrace
                b4
                {
                    c'16
                }
                <<
                    \context Voice = "On_Beat_Grace_Container"
                    {
                        \set fontSize = #-3
                        \slash
                        \voiceOne
                        <
                            \tweak font-size 0
                            \tweak transparent ##t
                            d'
                            a'
                        >8 * 1/3
                        - \accent
                        [
                        (
                        b'8 * 1/3
                        c''8 * 1/3
                        b'8 * 1/3
                        )
                        ]
                    }
                    \context Voice = "MusicVoice"
                    {
                        \voiceTwo
                        d'4
                        e'4
                    }
                >>
                \oneVoice
                f'4
            }
        }

    >>> for component in abjad.iterate.components(staff):
    ...     timespan = abjad.get.timespan(component)
    ...     print(f"{repr(component):30} {repr(timespan)}")
    Staff("{ b4 { { <d' a'>8 * 1/3 b'8 * 1/3 c''8 * 1/3 b'8 * 1/3 } { d'4 e'4 } } f'4 }") Timespan(Offset((0, 1)), Offset((1, 1)))
    Voice("b4 { { <d' a'>8 * 1/3 b'8 * 1/3 c''8 * 1/3 b'8 * 1/3 } { d'4 e'4 } } f'4", name='MusicVoice') Timespan(Offset((0, 1)), Offset((1, 1)))
    Note('b4')                     Timespan(Offset((0, 1)), Offset((1, 4)))
    AfterGraceContainer("c'16")    Timespan(Offset((1, 4), displacement=Duration(-1, 16)), Offset((1, 4)))
    Note("c'16")                   Timespan(Offset((1, 4), displacement=Duration(-1, 16)), Offset((1, 4)))
    Container("{ <d' a'>8 * 1/3 b'8 * 1/3 c''8 * 1/3 b'8 * 1/3 } { d'4 e'4 }") Timespan(Offset((1, 4)), Offset((3, 4)))
    OnBeatGraceContainer("<d' a'>8 * 1/3 b'8 * 1/3 c''8 * 1/3 b'8 * 1/3") Timespan(Offset((1, 4)), Offset((1, 4), displacement=Duration(1, 6)))
    Chord("<d' a'>8 * 1/3")        Timespan(Offset((1, 4)), Offset((1, 4), displacement=Duration(1, 24)))
    Note("b'8 * 1/3")              Timespan(Offset((1, 4), displacement=Duration(1, 24)), Offset((1, 4), displacement=Duration(1, 12)))
    Note("c''8 * 1/3")             Timespan(Offset((1, 4), displacement=Duration(1, 12)), Offset((1, 4), displacement=Duration(1, 8)))
    Note("b'8 * 1/3")              Timespan(Offset((1, 4), displacement=Duration(1, 8)), Offset((1, 4), displacement=Duration(1, 6)))
    Voice("d'4 e'4", name='MusicVoice') Timespan(Offset((1, 4)), Offset((3, 4)))
    Note("d'4")                    Timespan(Offset((1, 4), displacement=Duration(1, 6)), Offset((1, 2)))
    Note("e'4")                    Timespan(Offset((1, 2)), Offset((3, 4)))
    Note("f'4")                    Timespan(Offset((3, 4)), Offset((1, 1)))

"""


def grace_corner_cases():
    """
    Read these module-level examples.
    """
    pass
