import collections
import enum
import typing

from . import _getlib, _iterlib, _updatelib
from . import duration as _duration
from . import indicators as _indicators
from . import iterate as _iterate
from . import parentage as _parentage
from . import pitch as _pitch
from . import score as _score
from . import select as _select
from . import tag as _tag
from . import timespan as _timespan
from . import typings as _typings


def after_grace_container(argument):
    r"""
    Gets after grace containers attached to component.

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
        ...     container = abjad.get.after_grace_container(component)
        ...     print(f"{repr(component):30} {repr(container)}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") None
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') None
        Note("c'4")                    None
        BeforeGraceContainer("cs'16")  None
        Note("cs'16")                  None
        Note("d'4")                    None
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") None
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") None
        Chord("<e' g'>16")             None
        Note("gs'16")                  None
        Note("a'16")                   None
        Note("as'16")                  None
        Voice("e'4", name='MusicVoice') None
        Note("e'4")                    None
        Note("f'4")                    AfterGraceContainer("fs'16")
        AfterGraceContainer("fs'16")   None
        Note("fs'16")                  None

    """
    return getattr(argument, "_after_grace_container", None)


def annotation(
    argument,
    annotation: typing.Any,
    default: typing.Any | None = None,
    unwrap: bool = True,
) -> typing.Any:
    r"""
    Gets annotation.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 e' e' f'")
        >>> abjad.annotate(staff[0], 'default_instrument', abjad.Cello())
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                e'4
                e'4
                f'4
            }

        >>> string = 'default_instrument'
        >>> abjad.get.annotation(staff[0], string)
        Cello(clefs=('bass', 'tenor', 'treble'), context='Staff', middle_c_sounding_pitch=NamedPitch("c'"), pitch_range=PitchRange(range_string='[C2, G5]'), tuning=Tuning(pitches=(NamedPitch('c,'), NamedPitch('g,'), NamedPitch('d'), NamedPitch('a'))))

        >>> abjad.get.annotation(staff[1], string) is None
        True

        >>> abjad.get.annotation(staff[2], string) is None
        True

        >>> abjad.get.annotation(staff[3], string) is None
        True

        Returns default when no annotation is found:

        >>> abjad.get.annotation(staff[3], string, abjad.Violin())
        Violin(clefs=('treble',), context='Staff', middle_c_sounding_pitch=NamedPitch("c'"), pitch_range=PitchRange(range_string='[G3, G7]'), tuning=Tuning(pitches=(NamedPitch('g'), NamedPitch("d'"), NamedPitch("a'"), NamedPitch("e''"))))

    ..  container:: example

        REGRESSION: annotation is not picked up as effective indicator:

        >>> prototype = abjad.Instrument
        >>> abjad.get.effective(staff[0], prototype) is None
        True

        >>> abjad.get.effective(staff[1], prototype) is None
        True

        >>> abjad.get.effective(staff[2], prototype) is None
        True

        >>> abjad.get.effective(staff[3], prototype) is None
        True

    """
    return _getlib._get_annotation(argument, annotation, default=default, unwrap=unwrap)


def annotation_wrappers(argument):
    r"""
    Gets annotation wrappers.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 e' e' f'")
        >>> abjad.annotate(staff[0], 'default_instrument', abjad.Cello())
        >>> abjad.annotate(staff[0], 'default_clef', abjad.Clef('tenor'))
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                e'4
                e'4
                f'4
            }

        >>> for wrapper in abjad.get.annotation_wrappers(staff[0]): wrapper
        Wrapper(annotation='default_instrument', context=None, deactivate=False, direction=None, indicator=Cello(clefs=('bass', 'tenor', 'treble'), context='Staff', middle_c_sounding_pitch=NamedPitch("c'"), pitch_range=PitchRange(range_string='[C2, G5]'), tuning=Tuning(pitches=(NamedPitch('c,'), NamedPitch('g,'), NamedPitch('d'), NamedPitch('a')))), synthetic_offset=None, tag=Tag(string=''))
        Wrapper(annotation='default_clef', context=None, deactivate=False, direction=None, indicator=Clef(name='tenor', hide=False), synthetic_offset=None, tag=Tag(string=''))

    """
    return _getlib._get_annotation_wrappers(argument)


def bar_line_crossing(argument) -> bool:
    r"""
    Is true when ``argument`` crosses bar line.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4")
        >>> score = abjad.Score([staff], name="Score")
        >>> time_signature = abjad.TimeSignature((3, 8))
        >>> abjad.attach(time_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 3/8
                c'4
                d'4
                e'4
            }

        >>> for note in staff:
        ...     result = abjad.get.bar_line_crossing(note)
        ...     print(note, result)
        ...
        Note("c'4") False
        Note("d'4") True
        Note("e'4") False

    """
    if not isinstance(argument, _score.Component):
        raise Exception("can only get indicator on component.")
    time_signature = _getlib._get_effective(argument, _indicators.TimeSignature)
    if time_signature is None:
        time_signature_duration = _duration.Duration(4, 4)
    else:
        time_signature_duration = time_signature.duration
    partial = getattr(time_signature, "partial", 0)
    partial = partial or 0
    start_offset = timespan(argument).start_offset
    shifted_start = start_offset - partial
    shifted_start %= time_signature_duration
    stop_offset = argument._get_duration() + shifted_start
    if time_signature_duration < stop_offset:
        return True
    return False


def before_grace_container(argument):
    r"""
    Gets before-grace container attached to leaf.

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
        ...     container = abjad.get.before_grace_container(component)
        ...     print(f"{repr(component):30} {repr(container)}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") None
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') None
        Note("c'4")                    None
        BeforeGraceContainer("cs'16")  None
        Note("cs'16")                  None
        Note("d'4")                    BeforeGraceContainer("cs'16")
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") None
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") None
        Chord("<e' g'>16")             None
        Note("gs'16")                  None
        Note("a'16")                   None
        Note("as'16")                  None
        Voice("e'4", name='MusicVoice') None
        Note("e'4")                    None
        Note("f'4")                    None
        AfterGraceContainer("fs'16")   None
        Note("fs'16")                  None

    """
    return getattr(argument, "_before_grace_container", None)


def contents(argument) -> list[_score.Component]:
    r"""
    Gets contents.

    REGRESSION. Works with grace notes (and containers):

    ..  container:: example

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
        ...     contents = abjad.get.contents(component)
        ...     print(f"{repr(component)}:")
        ...     for component_ in contents:
        ...         print(f"    {repr(component_)}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice'):
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Note("c'4")
            Note("d'4")
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            Note("f'4")
        Note("c'4"):
            Note("c'4")
        BeforeGraceContainer("cs'16"):
            BeforeGraceContainer("cs'16")
            Note("cs'16")
        Note("cs'16"):
            Note("cs'16")
        Note("d'4"):
            Note("d'4")
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }"):
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Voice("e'4", name='MusicVoice')
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Chord("<e' g'>16")
            Note("gs'16")
            Note("a'16")
            Note("as'16")
        Chord("<e' g'>16"):
            Chord("<e' g'>16")
        Note("gs'16"):
            Note("gs'16")
        Note("a'16"):
            Note("a'16")
        Note("as'16"):
            Note("as'16")
        Voice("e'4", name='MusicVoice'):
            Voice("e'4", name='MusicVoice')
            Note("e'4")
        Note("e'4"):
            Note("e'4")
        Note("f'4"):
            Note("f'4")
        AfterGraceContainer("fs'16"):
            AfterGraceContainer("fs'16")
            Note("fs'16")
        Note("fs'16"):
            Note("fs'16")

    ..  container:: example

        REGRESSSION. Works with tremolo containers:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
        >>> staff.append("cs'4")
        >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
        >>> staff.append("ds'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \repeat tremolo 2
                {
                    c'16
                    e'16
                }
                cs'4
                \repeat tremolo 2
                {
                    d'16
                    f'16
                }
                ds'4
            }

        >>> for component in abjad.select.components(staff):
        ...     contents = abjad.get.contents(component)
        ...     print(f"{repr(component)}:")
        ...     for component_ in contents:
        ...         print(f"    {repr(component_)}")
        Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4"):
            Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4")
            TremoloContainer("c'16 e'16")
            Note("cs'4")
            TremoloContainer("d'16 f'16")
            Note("ds'4")
        TremoloContainer("c'16 e'16"):
            TremoloContainer("c'16 e'16")
            Note("c'16")
            Note("e'16")
        Note("c'16"):
            Note("c'16")
        Note("e'16"):
            Note("e'16")
        Note("cs'4"):
            Note("cs'4")
        TremoloContainer("d'16 f'16"):
            TremoloContainer("d'16 f'16")
            Note("d'16")
            Note("f'16")
        Note("d'16"):
            Note("d'16")
        Note("f'16"):
            Note("f'16")
        Note("ds'4"):
            Note("ds'4")

    """
    if not isinstance(argument, _score.Component):
        raise Exception("can only get contents of component.")
    result = []
    result.append(argument)
    result.extend(getattr(argument, "components", []))
    return result


def descendants(argument) -> list[_score.Component]:
    r"""
    Gets descendants.

    REGRESSION. Works with grace notes (and containers):

    ..  container:: example

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
        ...     descendants = abjad.get.descendants(component)
        ...     print(f"{repr(component)}:")
        ...     for component_ in descendants:
        ...         print(f"    {repr(component_)}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }"):
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
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice'):
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
        Note("c'4"):
            Note("c'4")
        BeforeGraceContainer("cs'16"):
            BeforeGraceContainer("cs'16")
            Note("cs'16")
        Note("cs'16"):
            Note("cs'16")
        Note("d'4"):
            Note("d'4")
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }"):
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Chord("<e' g'>16")
            Note("gs'16")
            Note("a'16")
            Note("as'16")
            Voice("e'4", name='MusicVoice')
            Note("e'4")
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Chord("<e' g'>16")
            Note("gs'16")
            Note("a'16")
            Note("as'16")
        Chord("<e' g'>16"):
            Chord("<e' g'>16")
        Note("gs'16"):
            Note("gs'16")
        Note("a'16"):
            Note("a'16")
        Note("as'16"):
            Note("as'16")
        Voice("e'4", name='MusicVoice'):
            Voice("e'4", name='MusicVoice')
            Note("e'4")
        Note("e'4"):
            Note("e'4")
        Note("f'4"):
            Note("f'4")
        AfterGraceContainer("fs'16"):
            AfterGraceContainer("fs'16")
            Note("fs'16")
        Note("fs'16"):
            Note("fs'16")

    """
    if isinstance(argument, _score.Component):
        argument = [argument]
    components = []
    for item in argument:
        generator = _iterlib._iterate_descendants(item)
        for component in generator:
            if component not in components:
                components.append(component)
    return components


def duration(
    argument, in_seconds: bool = False, preprolated: bool = False
) -> _duration.Duration:
    r"""
    Gets duration.

    REGRESSION. Works with grace notes (and containers):

    ..  container:: example

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
        ...     duration = abjad.get.duration(component)
        ...     print(f"{repr(component):30} {repr(duration)}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") Duration(1, 1)
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') Duration(1, 1)
        Note("c'4")                    Duration(1, 4)
        BeforeGraceContainer("cs'16")  Duration(1, 16)
        Note("cs'16")                  Duration(1, 16)
        Note("d'4")                    Duration(1, 4)
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") Duration(1, 4)
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") Duration(1, 4)
        Chord("<e' g'>16")             Duration(1, 16)
        Note("gs'16")                  Duration(1, 16)
        Note("a'16")                   Duration(1, 16)
        Note("as'16")                  Duration(1, 16)
        Voice("e'4", name='MusicVoice') Duration(1, 4)
        Note("e'4")                    Duration(1, 4)
        Note("f'4")                    Duration(1, 4)
        AfterGraceContainer("fs'16")   Duration(1, 16)
        Note("fs'16")                  Duration(1, 16)

    ..  container:: example

        REGRESSION. Duration of independent after-grace containers defined equal to 0:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> lilypond_file = abjad.LilyPondFile([staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        gf'16
                    }
                    f'4
                }
            }

        >>> for component in abjad.select.components(staff):
        ...     duration = abjad.get.duration(component)
        ...     print(f"{repr(component):30} {repr(duration)}")
        Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }") Duration(1, 1)
        Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice') Duration(1, 1)
        Note("c'4")                    Duration(1, 4)
        Note("d'4")                    Duration(1, 4)
        Note("e'4")                    Duration(1, 4)
        IndependentAfterGraceContainer("gf'16") Duration(0, 1)
        Note("gf'16")                  Duration(1, 16)
        Note("f'4")                    Duration(1, 4)

    ..  container:: example

        REGRESSSION. Works with tremolo containers:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
        >>> staff.append("cs'4")
        >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
        >>> staff.append("ds'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \repeat tremolo 2
                {
                    c'16
                    e'16
                }
                cs'4
                \repeat tremolo 2
                {
                    d'16
                    f'16
                }
                ds'4
            }

        >>> for component in abjad.select.components(staff):
        ...     duration = abjad.get.duration(component)
        ...     print(f"{repr(component):30} {repr(duration)}")
        Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4") Duration(1, 1)
        TremoloContainer("c'16 e'16")  Duration(1, 4)
        Note("c'16")                   Duration(1, 8)
        Note("e'16")                   Duration(1, 8)
        Note("cs'4")                   Duration(1, 4)
        TremoloContainer("d'16 f'16")  Duration(1, 4)
        Note("d'16")                   Duration(1, 8)
        Note("f'16")                   Duration(1, 8)
        Note("ds'4")                   Duration(1, 4)

    ..  container:: example

        REGRESSION. Works with selections:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
            }

        >>> selection = staff[:3]
        >>> abjad.get.duration(selection)
        Duration(3, 4)

    ..  container:: example

        Gets preprolated duration:

        >>> staff = abjad.Staff(r"\times 2/3 { c'4 ~ c' } \times 2/3 { d' ~ d' }")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak edge-height #'(0.7 . 0)
                \tuplet 3/2
                {
                    c'4
                    ~
                    c'4
                }
                \tweak edge-height #'(0.7 . 0)
                \tuplet 3/2
                {
                    d'4
                    ~
                    d'4
                }
            }

        >>> for lt in abjad.select.logical_ties(staff):
        ...     duration = abjad.get.duration(lt)
        ...     preprolated = abjad.get.duration(lt, preprolated=True)
        ...     lt, duration, preprolated
        (LogicalTie(items=[Note("c'4"), Note("c'4")]), Duration(1, 3), Duration(1, 2))
        (LogicalTie(items=[Note("d'4"), Note("d'4")]), Duration(1, 3), Duration(1, 2))

    """
    return _getlib._get_duration(
        argument, in_seconds=in_seconds, preprolated=preprolated
    )


def effective(
    argument,
    prototype: _typings.Prototype,
    *,
    attributes: dict | None = None,
    default: typing.Any | None = None,
    n: int = 0,
    unwrap: bool = True,
) -> typing.Any:
    r"""
    Gets effective indicator.

    REGRESSION. Works with grace notes (and containers):

    ..  container:: example

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> staff = abjad.Staff([music_voice])
        >>> container = abjad.BeforeGraceContainer("cs'16")
        >>> abjad.attach(container, music_voice[1])
        >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
        >>> abjad.attach(abjad.Clef("alto"), obgc[0])
        >>> abjad.attach(abjad.Articulation(">"), obgc[0])
        >>> container = abjad.AfterGraceContainer("fs'16")
        >>> abjad.attach(container, music_voice[3])
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
                            \clef "alto"
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
        ...     clef = abjad.get.effective(component, abjad.Clef)
        ...     print(f"{repr(component):30} {repr(clef)}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") None
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') None
        Note("c'4")                    None
        BeforeGraceContainer("cs'16")  None
        Note("cs'16")                  None
        Note("d'4")                    None
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") Clef(name='alto', hide=False)
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") Clef(name='alto', hide=False)
        Chord("<e' g'>16")             Clef(name='alto', hide=False)
        Note("gs'16")                  Clef(name='alto', hide=False)
        Note("a'16")                   Clef(name='alto', hide=False)
        Note("as'16")                  Clef(name='alto', hide=False)
        Voice("e'4", name='MusicVoice') Clef(name='alto', hide=False)
        Note("e'4")                    Clef(name='alto', hide=False)
        Note("f'4")                    Clef(name='alto', hide=False)
        AfterGraceContainer("fs'16")   Clef(name='alto', hide=False)
        Note("fs'16")                  Clef(name='alto', hide=False)

    ..  container:: example

        REGRESSION. Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.attach(abjad.Clef("alto"), container[0])
        >>> lilypond_file = abjad.LilyPondFile([staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        \clef "alto"
                        gf'16
                    }
                    f'4
                }
            }

        >>> for component in abjad.select.components(staff):
        ...     clef = abjad.get.effective(component, abjad.Clef)
        ...     print(f"{repr(component):30} {repr(clef)}")
        Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }") None
        Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice') None
        Note("c'4")                    None
        Note("d'4")                    None
        Note("e'4")                    None
        IndependentAfterGraceContainer("gf'16") Clef(name='alto', hide=False)
        Note("gf'16")                  Clef(name='alto', hide=False)
        Note("f'4")                    Clef(name='alto', hide=False)

    ..  container:: example

        REGRESSSION. Works with tremolo containers:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
        >>> staff.append("cs'4")
        >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
        >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
        >>> staff.append("ds'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \repeat tremolo 2
                {
                    c'16
                    e'16
                }
                cs'4
                \repeat tremolo 2
                {
                    \clef "alto"
                    d'16
                    f'16
                }
                ds'4
            }

        >>> for component in abjad.select.components(staff):
        ...     clef = abjad.get.effective(component, abjad.Clef)
        ...     print(f"{repr(component):30} {repr(clef)}")
        Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4") None
        TremoloContainer("c'16 e'16")  None
        Note("c'16")                   None
        Note("e'16")                   None
        Note("cs'4")                   None
        TremoloContainer("d'16 f'16")  Clef(name='alto', hide=False)
        Note("d'16")                   Clef(name='alto', hide=False)
        Note("f'16")                   Clef(name='alto', hide=False)
        Note("ds'4")                   Clef(name='alto', hide=False)

    ..  container:: example

        Arbitrary objects (like strings) can be contexted:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.attach("color", staff[1], context="Staff")
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

        >>> for component in abjad.iterate.components(staff):
        ...     string = abjad.get.effective(component, str)
        ...     print(component, repr(string))
        ...
        Staff("c'8 d'8 e'8 f'8") None
        Note("c'8") None
        Note("d'8") 'color'
        Note("e'8") 'color'
        Note("f'8") 'color'

    ..  container:: example

        Scans forwards or backwards when ``n`` is set:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8")
        >>> abjad.attach("red", staff[0], context="Staff")
        >>> abjad.attach("blue", staff[2], context="Staff")
        >>> abjad.attach("yellow", staff[4], context="Staff")
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
                g'8
            }

        >>> for n in (-1, 0, 1):
        ...     color = abjad.get.effective(staff[0], str, n=n)
        ...     print(n, repr(color))
        ...
        -1 None
        0 'red'
        1 'blue'

        >>> for n in (-1, 0, 1):
        ...     color = abjad.get.effective(staff[1], str, n=n)
        ...     print(n, repr(color))
        ...
        -1 None
        0 'red'
        1 'blue'

        >>> for n in (-1, 0, 1):
        ...     color = abjad.get.effective(staff[2], str, n=n)
        ...     print(n, repr(color))
        ...
        -1 'red'
        0 'blue'
        1 'yellow'

        >>> for n in (-1, 0, 1):
        ...     color = abjad.get.effective(staff[3], str, n=n)
        ...     print(n, repr(color))
        ...
        -1 'red'
        0 'blue'
        1 'yellow'

        >>> for n in (-1, 0, 1):
        ...     color = abjad.get.effective(staff[4], str, n=n)
        ...     print(n, repr(color))
        ...
        -1 'blue'
        0 'yellow'
        1 None

    ..  container:: example

        Use synthetic offsets to hide a clef before the start of a staff
        like this:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> abjad.attach(
        ...     abjad.Clef("treble", hide=True),
        ...     staff[0],
        ...     synthetic_offset=abjad.Offset(-1),
        ... )
        >>> abjad.attach(abjad.Clef("alto"), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "alto"
                c'4
                d'4
                e'4
                f'4
            }

        >>> for leaf in staff:
        ...     clef = abjad.get.effective(leaf, abjad.Clef)
        ...     (leaf, clef)
        ...
        (Note("c'4"), Clef(name='alto', hide=False))
        (Note("d'4"), Clef(name='alto', hide=False))
        (Note("e'4"), Clef(name='alto', hide=False))
        (Note("f'4"), Clef(name='alto', hide=False))

        >>> abjad.get.effective(staff[0], abjad.Clef)
        Clef(name='alto', hide=False)

        >>> abjad.get.effective(staff[0], abjad.Clef, n=-1)
        Clef(name='treble', hide=True)

        >>> abjad.get.effective(staff[0], abjad.Clef, n=-2) is None
        True

        Note that ``hide=True`` is set on the offset clef to prevent
        duplicate clef commands in LilyPond output.

        Note also that the order of attachment (offset versus non-offset)
        makes no difference.

    ..  container:: example

        Here's how to hide a clef after the end of a staff:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> abjad.attach(abjad.Clef("treble"), staff[0])
        >>> abjad.attach(
        ...     abjad.Clef("alto", hide=True),
        ...     staff[-1],
        ...     synthetic_offset=abjad.Offset(1),
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "treble"
                c'4
                d'4
                e'4
                f'4
            }

        >>> for leaf in staff:
        ...     clef = abjad.get.effective(leaf, abjad.Clef)
        ...     (leaf, clef)
        ...
        (Note("c'4"), Clef(name='treble', hide=False))
        (Note("d'4"), Clef(name='treble', hide=False))
        (Note("e'4"), Clef(name='treble', hide=False))
        (Note("f'4"), Clef(name='treble', hide=False))

        >>> abjad.get.effective(staff[-1], abjad.Clef)
        Clef(name='treble', hide=False)

        >>> abjad.get.effective(staff[-1], abjad.Clef, n=1)
        Clef(name='alto', hide=True)

        >>> abjad.get.effective(staff[-1], abjad.Clef, n=2) is None
        True

    ..  container:: example

        Gets effective time signature:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff], name="Score")
        >>> leaves = abjad.select.leaves(staff)
        >>> abjad.attach(abjad.TimeSignature((3, 8)), leaves[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 3/8
                c'4
                d'4
                e'4
                f'4
            }

        >>> prototype = abjad.TimeSignature
        >>> for component in abjad.iterate.components(staff):
        ...     time_signature = abjad.get.effective(component, prototype)
        ...     print(component, time_signature)
        ...
        Staff("c'4 d'4 e'4 f'4") TimeSignature(pair=(3, 8), hide=False, partial=None)
        Note("c'4") TimeSignature(pair=(3, 8), hide=False, partial=None)
        Note("d'4") TimeSignature(pair=(3, 8), hide=False, partial=None)
        Note("e'4") TimeSignature(pair=(3, 8), hide=False, partial=None)
        Note("f'4") TimeSignature(pair=(3, 8), hide=False, partial=None)

    ..  container:: example

        Test attributes like this:

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> staff = abjad.Staff([voice])
        >>> start_text_span = abjad.StartTextSpan()
        >>> abjad.attach(start_text_span, voice[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, voice[2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \new Voice
                {
                    c'4
                    \startTextSpan
                    d'4
                    e'4
                    \stopTextSpan
                    f'4
                }
            }

        >>> for note in abjad.select.notes(staff):
        ...     note, abjad.get.effective(note, abjad.StartTextSpan)
        ...
        (Note("c'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, concat_hspace_right=None, left_broken_text=None, left_text=None, right_padding=None, right_text=None, style=None))
        (Note("d'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, concat_hspace_right=None, left_broken_text=None, left_text=None, right_padding=None, right_text=None, style=None))
        (Note("e'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, concat_hspace_right=None, left_broken_text=None, left_text=None, right_padding=None, right_text=None, style=None))
        (Note("f'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, concat_hspace_right=None, left_broken_text=None, left_text=None, right_padding=None, right_text=None, style=None))

        >>> for note in abjad.select.notes(staff):
        ...     note, abjad.get.effective(note, abjad.StopTextSpan)
        ...
        (Note("c'4"), None)
        (Note("d'4"), None)
        (Note("e'4"), StopTextSpan(command='\\stopTextSpan', leak=False))
        (Note("f'4"), StopTextSpan(command='\\stopTextSpan', leak=False))

        >>> attributes = {'parameter': 'TEXT_SPANNER'}
        >>> for note in abjad.select.notes(staff):
        ...     indicator = abjad.get.effective(
        ...         note,
        ...         object,
        ...         attributes=attributes,
        ...         )
        ...     print(f"{note!r}:")
        ...     print(f"    {indicator!r}")
        Note("c'4"):
            StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, concat_hspace_right=None, left_broken_text=None, left_text=None, right_padding=None, right_text=None, style=None)
        Note("d'4"):
            StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, concat_hspace_right=None, left_broken_text=None, left_text=None, right_padding=None, right_text=None, style=None)
        Note("e'4"):
            StopTextSpan(command='\\stopTextSpan', leak=False)
        Note("f'4"):
            StopTextSpan(command='\\stopTextSpan', leak=False)

    ..  container:: example

        REGRESSION. Matching start-beam and stop-beam indicators work correctly:

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8 g'4 a'4")
        >>> abjad.attach(abjad.StartBeam(), voice[0])
        >>> abjad.attach(abjad.StopBeam(), voice[3])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'8
                [
                d'8
                e'8
                f'8
                ]
                g'4
                a'4
            }

        >>> for leaf in abjad.select.leaves(voice):
        ...     start_beam = abjad.get.effective(leaf, abjad.StartBeam)
        ...     stop_beam = abjad.get.effective(leaf, abjad.StopBeam)
        ...     leaf, start_beam, stop_beam
        (Note("c'8"), StartBeam(), None)
        (Note("d'8"), StartBeam(), None)
        (Note("e'8"), StartBeam(), None)
        (Note("f'8"), StartBeam(), StopBeam(leak=False))
        (Note("g'4"), StartBeam(), StopBeam(leak=False))
        (Note("a'4"), StartBeam(), StopBeam(leak=False))

    ..  container:: example

        REGRESSION. Bar lines work like this:

        >>> voice = abjad.Voice("c'2 d'2 e'2 f'2")
        >>> score = abjad.Score([voice])
        >>> abjad.attach(abjad.BarLine("||"), voice[1])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Voice
                {
                    c'2
                    d'2
                    \bar "||"
                    e'2
                    f'2
                }
            >>

        >>> for leaf in abjad.select.leaves(score):
        ...     bar_line = abjad.get.effective(leaf, abjad.BarLine)
        ...     leaf, bar_line
        (Note("c'2"), None)
        (Note("d'2"), BarLine(abbreviation='||', site='after'))
        (Note("e'2"), BarLine(abbreviation='||', site='after'))
        (Note("f'2"), BarLine(abbreviation='||', site='after'))

    """
    if not isinstance(argument, _score.Component):
        raise Exception("can only get effective on components.")
    if attributes is not None:
        assert isinstance(attributes, dict), repr(attributes)
    result = _getlib._get_effective(
        argument, prototype, attributes=attributes, n=n, unwrap=unwrap
    )
    if result is None:
        result = default
    return result


def effective_staff(argument) -> typing.Optional["_score.Staff"]:
    r"""
    Gets effective staff.

    REGRESSION. Works with grace notes (and containers):

    ..  container:: example

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
        ...     staff = abjad.get.effective_staff(component)
        ...     print(f"{component!r}:")
        ...     print(f"    {staff!r}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice'):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Note("c'4"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        BeforeGraceContainer("cs'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Note("cs'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Note("d'4"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Chord("<e' g'>16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Note("gs'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Note("a'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Note("as'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Voice("e'4", name='MusicVoice'):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Note("e'4"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Note("f'4"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        AfterGraceContainer("fs'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
        Note("fs'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")

    """
    if not isinstance(argument, _score.Component):
        raise Exception("can only get effective staff on components.")
    staff_change = _getlib._get_effective(argument, _indicators.StaffChange)
    if staff_change is not None:
        for component in argument._get_parentage():
            root = component
        effective_staff = root[staff_change.staff_name]
        return effective_staff
    for component in argument._get_parentage():
        if isinstance(component, _score.Staff):
            effective_staff = component
            break
    return effective_staff


def effective_wrapper(
    argument,
    prototype: _typings.Prototype,
    *,
    attributes: dict | None = None,
    n: int = 0,
):
    r"""
    Gets effective wrapper.

    ..  container:: example

        REGRESSION. Works with grace notes (and containers):

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> staff = abjad.Staff([music_voice])
        >>> container = abjad.BeforeGraceContainer("cs'16")
        >>> abjad.attach(container, music_voice[1])
        >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
        >>> abjad.attach(abjad.Clef("alto"), obgc[0])
        >>> abjad.attach(abjad.Articulation(">"), obgc[0])
        >>> container = abjad.AfterGraceContainer("fs'16")
        >>> abjad.attach(container, music_voice[3])
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
                            \clef "alto"
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
        ...     wrapper = abjad.get.effective_wrapper(component, abjad.Clef)
        ...     print(f"{repr(component):}")
        ...     print(f"    {repr(wrapper)}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            None
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            None
        Note("c'4")
            None
        BeforeGraceContainer("cs'16")
            None
        Note("cs'16")
            None
        Note("d'4")
            None
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string=''))
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string=''))
        Chord("<e' g'>16")
            Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string=''))
        Note("gs'16")
            Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string=''))
        Note("a'16")
            Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string=''))
        Note("as'16")
            Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string=''))
        Voice("e'4", name='MusicVoice')
            Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string=''))
        Note("e'4")
            Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string=''))
        Note("f'4")
            Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string=''))
        AfterGraceContainer("fs'16")
            Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string=''))
        Note("fs'16")
            Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string=''))

    """
    if attributes is not None:
        assert isinstance(attributes, dict), repr(attributes)
    return effective(argument, prototype, attributes=attributes, n=n, unwrap=False)


def grace(argument) -> bool:
    r"""
    Is true when ``argument`` is grace music.

    Grace music defined equal to grace container, after-grace container and
    contents of those containers.

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
        ...     result = abjad.get.grace(component)
        ...     print(f"{repr(component):30} {repr(result)}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") False
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') False
        Note("c'4")                    False
        BeforeGraceContainer("cs'16")  True
        Note("cs'16")                  True
        Note("d'4")                    False
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") False
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") True
        Chord("<e' g'>16")             True
        Note("gs'16")                  True
        Note("a'16")                   True
        Note("as'16")                  True
        Voice("e'4", name='MusicVoice') False
        Note("e'4")                    False
        Note("f'4")                    False
        AfterGraceContainer("fs'16")   True
        Note("fs'16")                  True

    ..  container:: example

        REGRESSION. Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> lilypond_file = abjad.LilyPondFile([staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        gf'16
                    }
                    f'4
                }
            }

        >>> for component in abjad.select.components(staff):
        ...     result = abjad.get.grace(component)
        ...     print(f"{repr(component):30} {repr(result)}")
        Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }") False
        Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice') False
        Note("c'4")                    False
        Note("d'4")                    False
        Note("e'4")                    False
        IndependentAfterGraceContainer("gf'16") True
        Note("gf'16")                  True
        Note("f'4")                    False

    """
    if _getlib._get_grace_container(argument) is True:
        return True
    for component in argument._get_parentage():
        if isinstance(component, _score.IndependentAfterGraceContainer):
            return True
    return False


def has_effective_indicator(
    argument,
    prototype: _typings.Prototype | None = None,
    *,
    attributes: dict | None = None,
) -> bool:
    r"""
    Is true when ``argument`` has effective indicator.

    ..  container:: example

        REGRESSION. Works with grace notes (and containers):

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> staff = abjad.Staff([music_voice])
        >>> container = abjad.BeforeGraceContainer("cs'16")
        >>> abjad.attach(container, music_voice[1])
        >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
        >>> abjad.attach(abjad.Clef("alto"), obgc[0])
        >>> abjad.attach(abjad.Articulation(">"), obgc[0])
        >>> container = abjad.AfterGraceContainer("fs'16")
        >>> abjad.attach(container, music_voice[3])
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
                            \clef "alto"
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
        ...     function = abjad.get.has_effective_indicator
        ...     result = function(component, abjad.Clef)
        ...     print(f"{repr(component):30} {repr(result)}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") False
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') False
        Note("c'4")                    False
        BeforeGraceContainer("cs'16")  False
        Note("cs'16")                  False
        Note("d'4")                    False
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") True
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") True
        Chord("<e' g'>16")             True
        Note("gs'16")                  True
        Note("a'16")                   True
        Note("as'16")                  True
        Voice("e'4", name='MusicVoice') True
        Note("e'4")                    True
        Note("f'4")                    True
        AfterGraceContainer("fs'16")   True
        Note("fs'16")                  True

    ..  container:: example

        REGRESSION. Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.attach(abjad.Clef("alto"), container[0])
        >>> lilypond_file = abjad.LilyPondFile([staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        \clef "alto"
                        gf'16
                    }
                    f'4
                }
            }

        >>> for component in abjad.select.components(staff):
        ...     function = abjad.get.has_effective_indicator
        ...     result = function(component, abjad.Clef)
        ...     print(f"{repr(component):30} {repr(result)}")
        Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }") False
        Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice') False
        Note("c'4")                    False
        Note("d'4")                    False
        Note("e'4")                    False
        IndependentAfterGraceContainer("gf'16") True
        Note("gf'16")                  True
        Note("f'4")                    True

    ..  container:: example

        REGRESSSION. Works with tremolo containers:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
        >>> staff.append("cs'4")
        >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
        >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
        >>> staff.append("ds'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \repeat tremolo 2
                {
                    c'16
                    e'16
                }
                cs'4
                \repeat tremolo 2
                {
                    \clef "alto"
                    d'16
                    f'16
                }
                ds'4
            }

        >>> for component in abjad.select.components(staff):
        ...     function = abjad.get.has_effective_indicator
        ...     result = function(component, abjad.Clef)
        ...     print(f"{repr(component):30} {repr(result)}")
        Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4") False
        TremoloContainer("c'16 e'16")  False
        Note("c'16")                   False
        Note("e'16")                   False
        Note("cs'4")                   False
        TremoloContainer("d'16 f'16")  True
        Note("d'16")                   True
        Note("f'16")                   True
        Note("ds'4")                   True

    """
    if not isinstance(argument, _score.Component):
        raise Exception("can only get effective indicator on component.")
    if attributes is not None:
        assert isinstance(attributes, dict), repr(attributes)
    indicator = _getlib._get_effective(argument, prototype, attributes=attributes)
    return indicator is not None


def has_indicator(
    argument,
    prototype: str | _typings.Prototype | enum.Enum | None = None,
    *,
    attributes: dict | None = None,
) -> bool:
    r"""
    Is true when ``argument`` has one or more indicators.

    ..  container:: example

        REGRESSION. Works with grace notes (and containers):

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> staff = abjad.Staff([music_voice])
        >>> container = abjad.BeforeGraceContainer("cs'16")
        >>> abjad.attach(container, music_voice[1])
        >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
        >>> abjad.attach(abjad.Clef("alto"), obgc[0])
        >>> abjad.attach(abjad.Articulation(">"), obgc[0])
        >>> container = abjad.AfterGraceContainer("fs'16")
        >>> abjad.attach(container, music_voice[3])
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
                            \clef "alto"
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
        ...     result = abjad.get.has_indicator(component, abjad.Clef)
        ...     print(f"{repr(component):30} {repr(result)}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") False
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') False
        Note("c'4")                    False
        BeforeGraceContainer("cs'16")  False
        Note("cs'16")                  False
        Note("d'4")                    False
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") False
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") False
        Chord("<e' g'>16")             True
        Note("gs'16")                  False
        Note("a'16")                   False
        Note("as'16")                  False
        Voice("e'4", name='MusicVoice') False
        Note("e'4")                    False
        Note("f'4")                    False
        AfterGraceContainer("fs'16")   False
        Note("fs'16")                  False

    ..  container:: example

        REGRESSION. Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.attach(abjad.Clef("alto"), container[0])
        >>> lilypond_file = abjad.LilyPondFile([staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        \clef "alto"
                        gf'16
                    }
                    f'4
                }
            }

        >>> for component in abjad.select.components(staff):
        ...     result = abjad.get.has_indicator(component, abjad.Clef)
        ...     print(f"{repr(component):30} {repr(result)}")
        Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }") False
        Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice') False
        Note("c'4")                    False
        Note("d'4")                    False
        Note("e'4")                    False
        IndependentAfterGraceContainer("gf'16") False
        Note("gf'16")                  True
        Note("f'4")                    False

    ..  container:: example

        REGRESSSION. Works with tremolo containers:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
        >>> staff.append("cs'4")
        >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
        >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
        >>> staff.append("ds'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \repeat tremolo 2
                {
                    c'16
                    e'16
                }
                cs'4
                \repeat tremolo 2
                {
                    \clef "alto"
                    d'16
                    f'16
                }
                ds'4
            }

        >>> for component in abjad.select.components(staff):
        ...     result = abjad.get.has_indicator(component, abjad.Clef)
        ...     print(f"{repr(component):30} {repr(result)}")
        Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4") False
        TremoloContainer("c'16 e'16")  False
        Note("c'16")                   False
        Note("e'16")                   False
        Note("cs'4")                   False
        TremoloContainer("d'16 f'16")  False
        Note("d'16")                   True
        Note("f'16")                   False
        Note("ds'4")                   False

    ..  container:: example

        Set ``attributes`` dictionary to test indicator attributes:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> staff = abjad.Staff([voice], name="Staff")
        >>> abjad.attach(abjad.Clef('treble'), voice[0])
        >>> abjad.attach(abjad.Clef('alto'), voice[2])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \clef "treble"
                c'4
                c'4
                \clef "alto"
                c'4
                c'4
            }

        >>> attributes = {'name': 'alto'}
        >>> abjad.get.has_indicator(voice[0], abjad.Clef)
        True

        >>> abjad.get.has_indicator(
        ...     voice[0],
        ...     abjad.Clef,
        ...     attributes=attributes,
        ...     )
        False

        >>> abjad.get.has_indicator(voice[2], abjad.Clef)
        True

        >>> abjad.get.has_indicator(
        ...     voice[2],
        ...     abjad.Clef,
        ...     attributes=attributes,
        ...     )
        True


    """
    if isinstance(prototype, _tag.Tag):
        raise Exception("do not attach tags; use tag=None keyword.")
    if not isinstance(argument, _score.Component):
        raise Exception("can only get indicator on component.")
    if attributes is not None:
        assert isinstance(attributes, dict), repr(attributes)
    return argument._has_indicator(prototype=prototype, attributes=attributes)


def indicator(
    argument,
    prototype: _typings.Prototype | None = None,
    *,
    default: typing.Any | None = None,
    unwrap: bool = True,
) -> typing.Any:
    r"""
    Gets indicator.

    ..  container:: example

        REGRESSION. Works with grace notes (and containers):

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> staff = abjad.Staff([music_voice])
        >>> container = abjad.BeforeGraceContainer("cs'16")
        >>> abjad.attach(container, music_voice[1])
        >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
        >>> abjad.attach(abjad.Clef("alto"), obgc[0])
        >>> abjad.attach(abjad.Articulation(">"), obgc[0])
        >>> container = abjad.AfterGraceContainer("fs'16")
        >>> abjad.attach(container, music_voice[3])
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
                            \clef "alto"
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
        ...     result = abjad.get.indicator(component, abjad.Clef)
        ...     print(f"{repr(component):30} {repr(result)}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }") None
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice') None
        Note("c'4")                    None
        BeforeGraceContainer("cs'16")  None
        Note("cs'16")                  None
        Note("d'4")                    None
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }") None
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") None
        Chord("<e' g'>16")             Clef(name='alto', hide=False)
        Note("gs'16")                  None
        Note("a'16")                   None
        Note("as'16")                  None
        Voice("e'4", name='MusicVoice') None
        Note("e'4")                    None
        Note("f'4")                    None
        AfterGraceContainer("fs'16")   None
        Note("fs'16")                  None

    ..  container:: example

        REGRESSSION. Works with tremolo containers:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
        >>> staff.append("cs'4")
        >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
        >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
        >>> staff.append("ds'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \repeat tremolo 2
                {
                    c'16
                    e'16
                }
                cs'4
                \repeat tremolo 2
                {
                    \clef "alto"
                    d'16
                    f'16
                }
                ds'4
            }

        >>> for component in abjad.select.components(staff):
        ...     result = abjad.get.indicator(component, abjad.Clef)
        ...     print(f"{repr(component):30} {repr(result)}")
        Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4") None
        TremoloContainer("c'16 e'16")  None
        Note("c'16")                   None
        Note("e'16")                   None
        Note("cs'4")                   None
        TremoloContainer("d'16 f'16")  None
        Note("d'16")                   Clef(name='alto', hide=False)
        Note("f'16")                   None
        Note("ds'4")                   None

    Raises exception when more than one indicator of ``prototype`` attach to
    ``argument``.

    Returns default when no indicator of ``prototype`` attaches to ``argument``.
    """
    return _getlib._get_indicator(argument, prototype, default=default, unwrap=unwrap)


def indicators(
    argument: _score.Component,
    prototype: _typings.Prototype | None = None,
    *,
    attributes: dict | None = None,
    unwrap: bool = True,
) -> list:
    r"""
    Get indicators.

    ..  container:: example

        REGRESSION. Works with grace notes (and containers):

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> staff = abjad.Staff([music_voice])
        >>> container = abjad.BeforeGraceContainer("cs'16")
        >>> abjad.attach(container, music_voice[1])
        >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
        >>> abjad.attach(abjad.Clef("alto"), obgc[0])
        >>> abjad.attach(abjad.Articulation(">"), obgc[0])
        >>> container = abjad.AfterGraceContainer("fs'16")
        >>> abjad.attach(container, music_voice[3])
        >>> for note in abjad.select.notes(staff):
        ...     abjad.attach(abjad.Articulation("."), note)

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
                    - \staccato
                    \grace {
                        cs'16
                        - \staccato
                    }
                    d'4
                    - \staccato
                    <<
                        \context Voice = "On_Beat_Grace_Container"
                        {
                            \clef "alto"
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
                            - \staccato
                            a'16
                            - \staccato
                            as'16
                            - \staccato
                            )
                            ]
                        }
                        \context Voice = "MusicVoice"
                        {
                            \voiceTwo
                            e'4
                            - \staccato
                        }
                    >>
                    \oneVoice
                    \afterGrace
                    f'4
                    - \staccato
                    {
                        fs'16
                        - \staccato
                    }
                }
            }

        >>> for component in abjad.select.components(staff):
        ...     result = abjad.get.indicators(component)
        ...     print(f"{component!r}:")
        ...     print(f"    {result!r}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }"):
            []
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice'):
            []
        Note("c'4"):
            [Articulation(name='.')]
        BeforeGraceContainer("cs'16"):
            []
        Note("cs'16"):
            [Articulation(name='.')]
        Note("d'4"):
            [Articulation(name='.')]
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }"):
            []
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
            []
        Chord("<e' g'>16"):
            [LilyPondLiteral(argument='\\set fontSize = #-3', site='before', directed=False), StartBeam(), LilyPondLiteral(argument='\\slash', site='before', directed=False), StartSlur(), VoiceNumber(n=1, leak=False), Clef(name='alto', hide=False), Articulation(name='>')]
        Note("gs'16"):
            [Articulation(name='.')]
        Note("a'16"):
            [Articulation(name='.')]
        Note("as'16"):
            [StopBeam(leak=False), StopSlur(leak=False), Articulation(name='.')]
        Voice("e'4", name='MusicVoice'):
            []
        Note("e'4"):
            [VoiceNumber(n=2, leak=False), Articulation(name='.')]
        Note("f'4"):
            [VoiceNumber(n=None, leak=False), Articulation(name='.')]
        AfterGraceContainer("fs'16"):
            []
        Note("fs'16"):
            [Articulation(name='.')]

    ..  container:: example

        REGRESSSION. Works with tremolo containers:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
        >>> staff.append("cs'4")
        >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
        >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
        >>> staff.append("ds'4")
        >>> for note in abjad.select.notes(staff):
        ...     abjad.attach(abjad.Articulation("."), note)

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \repeat tremolo 2
                {
                    c'16
                    - \staccato
                    e'16
                    - \staccato
                }
                cs'4
                - \staccato
                \repeat tremolo 2
                {
                    \clef "alto"
                    d'16
                    - \staccato
                    f'16
                    - \staccato
                }
                ds'4
                - \staccato
            }

        >>> for component in abjad.select.components(staff):
        ...     result = abjad.get.indicators(component)
        ...     print(f"{repr(component):30} {repr(result)}")
        Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4") []
        TremoloContainer("c'16 e'16")  []
        Note("c'16")                   [Articulation(name='.')]
        Note("e'16")                   [Articulation(name='.')]
        Note("cs'4")                   [Articulation(name='.')]
        TremoloContainer("d'16 f'16")  []
        Note("d'16")                   [Clef(name='alto', hide=False), Articulation(name='.')]
        Note("f'16")                   [Articulation(name='.')]
        Note("ds'4")                   [Articulation(name='.')]

    """
    if not isinstance(argument, _score.Component):
        message = "can only get indicators on component"
        message += f" (not {argument!r})."
        raise Exception(message)
    if attributes is not None:
        assert isinstance(attributes, dict), repr(attributes)
    result = argument._get_indicators(
        prototype=prototype, attributes=attributes, unwrap=unwrap
    )
    return list(result)


def leaf(argument, n: int = 0) -> typing.Optional["_score.Leaf"]:
    r"""
    Gets leaf ``n``.

    ``n`` constrained to -1, 0, 1 for previous, current, next leaf.

    ..  container:: example

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.Voice("c'8 d'8 e'8 f'8"))
        >>> staff.append(abjad.Voice("g'8 a'8 b'8 c''8"))
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \new Voice
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }
                \new Voice
                {
                    g'8
                    a'8
                    b'8
                    c''8
                }
            }

    ..  container:: example

        Gets leaf **FROM** ``argument`` when ``argument`` is a leaf:

        >>> leaf = staff[0][1]

        >>> abjad.get.leaf(leaf, -1)
        Note("c'8")

        >>> abjad.get.leaf(leaf, 0)
        Note("d'8")

        >>> abjad.get.leaf(leaf, 1)
        Note("e'8")

    ..  container:: example

        Gets leaf **IN** ``argument`` when ``argument`` is a container:

        >>> voice = staff[0]

        >>> abjad.get.leaf(voice, -1)
        Note("f'8")

        >>> abjad.get.leaf(voice, 0)
        Note("c'8")

        >>> abjad.get.leaf(voice, 1)
        Note("d'8")

    ..  container:: example

        REGRESSION. Works with grace notes (and containers):

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> staff = abjad.Staff([music_voice])
        >>> container = abjad.BeforeGraceContainer("cs'16")
        >>> abjad.attach(container, music_voice[1])
        >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
        >>> abjad.attach(abjad.Clef("alto"), obgc[0])
        >>> abjad.attach(abjad.Articulation(">"), obgc[0])
        >>> container = abjad.AfterGraceContainer("fs'16")
        >>> abjad.attach(container, music_voice[3])
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
                            \clef "alto"
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

        >>> for current_leaf in abjad.select.leaves(staff):
        ...     previous_leaf = abjad.get.leaf(current_leaf, -1)
        ...     next_leaf = abjad.get.leaf(current_leaf, 1)
        ...     print(f"previous leaf: {repr(previous_leaf)}")
        ...     print(f"current leaf:  {repr(current_leaf)}")
        ...     print(f"next leaf:     {repr(next_leaf)}")
        ...     print("---")
        previous leaf: None
        current leaf:  Note("c'4")
        next leaf:     Note("cs'16")
        ---
        previous leaf: Note("c'4")
        current leaf:  Note("cs'16")
        next leaf:     Note("d'4")
        ---
        previous leaf: Note("cs'16")
        current leaf:  Note("d'4")
        next leaf:     Chord("<e' g'>16")
        ---
        previous leaf: Note("d'4")
        current leaf:  Chord("<e' g'>16")
        next leaf:     Note("gs'16")
        ---
        previous leaf: Chord("<e' g'>16")
        current leaf:  Note("gs'16")
        next leaf:     Note("a'16")
        ---
        previous leaf: Note("gs'16")
        current leaf:  Note("a'16")
        next leaf:     Note("as'16")
        ---
        previous leaf: Note("a'16")
        current leaf:  Note("as'16")
        next leaf:     Note("e'4")
        ---
        previous leaf: Note("as'16")
        current leaf:  Note("e'4")
        next leaf:     Note("f'4")
        ---
        previous leaf: Note("e'4")
        current leaf:  Note("f'4")
        next leaf:     Note("fs'16")
        ---
        previous leaf: Note("f'4")
        current leaf:  Note("fs'16")
        next leaf:     None
        ---

    ..  container:: example

        REGRESSION. Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> lilypond_file = abjad.LilyPondFile([staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        gf'16
                    }
                    f'4
                }
            }

        >>> for current_leaf in abjad.select.leaves(staff):
        ...     previous_leaf = abjad.get.leaf(current_leaf, -1)
        ...     next_leaf = abjad.get.leaf(current_leaf, 1)
        ...     print(f"previous leaf: {repr(previous_leaf)}")
        ...     print(f"current leaf:  {repr(current_leaf)}")
        ...     print(f"next leaf:     {repr(next_leaf)}")
        ...     print("---")
        previous leaf: None
        current leaf:  Note("c'4")
        next leaf:     Note("d'4")
        ---
        previous leaf: Note("c'4")
        current leaf:  Note("d'4")
        next leaf:     Note("e'4")
        ---
        previous leaf: Note("d'4")
        current leaf:  Note("e'4")
        next leaf:     Note("gf'16")
        ---
        previous leaf: Note("e'4")
        current leaf:  Note("gf'16")
        next leaf:     Note("f'4")
        ---
        previous leaf: Note("gf'16")
        current leaf:  Note("f'4")
        next leaf:     None
        ---

    ..  container:: example

        REGRESSSION. Works with tremolo containers:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
        >>> staff.append("cs'4")
        >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
        >>> staff.append("ds'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \repeat tremolo 2
                {
                    c'16
                    e'16
                }
                cs'4
                \repeat tremolo 2
                {
                    d'16
                    f'16
                }
                ds'4
            }

        >>> for current_leaf in abjad.select.leaves(staff):
        ...     previous_leaf = abjad.get.leaf(current_leaf, -1)
        ...     next_leaf = abjad.get.leaf(current_leaf, 1)
        ...     print(f"previous leaf: {repr(previous_leaf)}")
        ...     print(f"current leaf:  {repr(current_leaf)}")
        ...     print(f"next leaf:     {repr(next_leaf)}")
        ...     print("---")
        previous leaf: None
        current leaf:  Note("c'16")
        next leaf:     Note("e'16")
        ---
        previous leaf: Note("c'16")
        current leaf:  Note("e'16")
        next leaf:     Note("cs'4")
        ---
        previous leaf: Note("e'16")
        current leaf:  Note("cs'4")
        next leaf:     Note("d'16")
        ---
        previous leaf: Note("cs'4")
        current leaf:  Note("d'16")
        next leaf:     Note("f'16")
        ---
        previous leaf: Note("d'16")
        current leaf:  Note("f'16")
        next leaf:     Note("ds'4")
        ---
        previous leaf: Note("f'16")
        current leaf:  Note("ds'4")
        next leaf:     None
        ---

    """
    return _iterlib._get_leaf(argument, n=n)


def lineage(argument) -> "Lineage":
    r"""
    Gets lineage.

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
        ...     lineage = abjad.get.lineage(component)
        ...     print(f"{repr(component)}:")
        ...     for component_ in lineage:
        ...         print(f"    {repr(component_)}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }"):
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
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice'):
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
        Note("c'4"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Note("c'4")
        BeforeGraceContainer("cs'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            BeforeGraceContainer("cs'16")
            Note("cs'16")
        Note("cs'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            BeforeGraceContainer("cs'16")
            Note("cs'16")
        Note("d'4"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Note("d'4")
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Chord("<e' g'>16")
            Note("gs'16")
            Note("a'16")
            Note("as'16")
            Voice("e'4", name='MusicVoice')
            Note("e'4")
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Chord("<e' g'>16")
            Note("gs'16")
            Note("a'16")
            Note("as'16")
        Chord("<e' g'>16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Chord("<e' g'>16")
        Note("gs'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Note("gs'16")
        Note("a'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Note("a'16")
        Note("as'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            Note("as'16")
        Voice("e'4", name='MusicVoice'):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            Voice("e'4", name='MusicVoice')
            Note("e'4")
        Note("e'4"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            Voice("e'4", name='MusicVoice')
            Note("e'4")
        Note("f'4"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            Note("f'4")
        AfterGraceContainer("fs'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            AfterGraceContainer("fs'16")
            Note("fs'16")
        Note("fs'16"):
            Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            AfterGraceContainer("fs'16")
            Note("fs'16")

    """
    if not isinstance(argument, _score.Component):
        raise Exception("can only get lineage on component.")
    return Lineage(argument)


def logical_tie(argument) -> "_select.LogicalTie":
    r"""
    Gets logical tie.

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

        >>> for leaf in abjad.select.leaves(staff):
        ...     lt = abjad.get.logical_tie(leaf)
        ...     print(f"{repr(leaf):30} {repr(lt)}")
        Note("c'4")                    LogicalTie(items=[Note("c'4")])
        Note("cs'16")                  LogicalTie(items=[Note("cs'16")])
        Note("d'4")                    LogicalTie(items=[Note("d'4")])
        Chord("<e' g'>16")             LogicalTie(items=[Chord("<e' g'>16")])
        Note("gs'16")                  LogicalTie(items=[Note("gs'16")])
        Note("a'16")                   LogicalTie(items=[Note("a'16")])
        Note("as'16")                  LogicalTie(items=[Note("as'16")])
        Note("e'4")                    LogicalTie(items=[Note("e'4")])
        Note("f'4")                    LogicalTie(items=[Note("f'4")])
        Note("fs'16")                  LogicalTie(items=[Note("fs'16")])

    ..  container:: example

        REGRESSSION. Works with tremolo containers:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
        >>> staff.append("cs'4")
        >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
        >>> staff.append("ds'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \repeat tremolo 2
                {
                    c'16
                    e'16
                }
                cs'4
                \repeat tremolo 2
                {
                    d'16
                    f'16
                }
                ds'4
            }

        >>> for leaf in abjad.select.leaves(staff):
        ...     lt = abjad.get.logical_tie(leaf)
        ...     print(f"{repr(leaf):30} {repr(lt)}")
        Note("c'16")                   LogicalTie(items=[Note("c'16")])
        Note("e'16")                   LogicalTie(items=[Note("e'16")])
        Note("cs'4")                   LogicalTie(items=[Note("cs'4")])
        Note("d'16")                   LogicalTie(items=[Note("d'16")])
        Note("f'16")                   LogicalTie(items=[Note("f'16")])
        Note("ds'4")                   LogicalTie(items=[Note("ds'4")])

    ..  container:: example

        REGRESSSION. Omits spurious rest when user ties from note to rest:

        >>> staff = abjad.Staff("c'4 r4")
        >>> # user error; shouldn't tie note to rest:
        >>> abjad.attach(abjad.Tie(), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                ~
                r4
            }

        >>> abjad.get.logical_tie(staff[0])
        LogicalTie(items=[Note("c'4")])

        >>> abjad.get.logical_tie(staff[1])
        LogicalTie(items=[Rest('r4')])

        Omits spurious rest when user repeat-ties into rest from note:

        >>> voice = abjad.Voice("r4 c'4", name="Voice")
        >>> # user error; shouldn't tie note to rest:
        >>> abjad.attach(abjad.RepeatTie(), voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                r4
                c'4
                \repeatTie
            }

        >>> abjad.get.logical_tie(voice[0])
        LogicalTie(items=[Rest('r4')])

        >>> abjad.get.logical_tie(voice[1])
        LogicalTie(items=[Note("c'4")])

    """
    if not isinstance(argument, _score.Leaf):
        raise Exception("can only get logical tie on leaf.")
    leaves = _iterlib._get_logical_tie_leaves(argument)
    return _select.LogicalTie(leaves)


def markup(
    argument: _score.Component, *, direction: int | None = None
) -> list[_indicators.Markup]:
    """
    Gets markup.
    """
    if not isinstance(argument, _score.Component):
        raise Exception("can only get markup on component.")
    result = argument._get_markup(direction=direction)
    return list(result)


def measure_number(argument) -> int:
    r"""
    Gets measure number.

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
        ...     measure_number = abjad.get.measure_number(component)
        ...     print(f"{repr(component):30} {measure_number}")
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

    ..  container:: example

        REGRESSION. Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> lilypond_file = abjad.LilyPondFile([staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        gf'16
                    }
                    f'4
                }
            }

        >>> for component in abjad.select.components(staff):
        ...     measure_number = abjad.get.measure_number(component)
        ...     print(f"{repr(component):30} {measure_number}")
        Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }") 1
        Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice') 1
        Note("c'4")                    1
        Note("d'4")                    1
        Note("e'4")                    1
        IndependentAfterGraceContainer("gf'16") 1
        Note("gf'16")                  1
        Note("f'4")                    1

    ..  container:: example

        REGRESSION. Measure number of score-initial grace notes is set equal to 0:

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> container = abjad.BeforeGraceContainer("b16")
        >>> abjad.attach(container, voice[0])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \grace {
                    b16
                }
                c'4
                d'4
                e'4
                f'4
            }

        >>> for component in abjad.select.components(voice):
        ...     measure_number = abjad.get.measure_number(component)
        ...     print(f"{repr(component):30} {measure_number}")
        Voice("c'4 d'4 e'4 f'4")       1
        BeforeGraceContainer('b16')          0
        Note('b16')                    0
        Note("c'4")                    1
        Note("d'4")                    1
        Note("e'4")                    1
        Note("f'4")                    1

    ..  container:: example

        REGRESSSION. Works with tremolo containers:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
        >>> staff.append("cs'4")
        >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
        >>> staff.append("ds'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \repeat tremolo 2
                {
                    c'16
                    e'16
                }
                cs'4
                \repeat tremolo 2
                {
                    d'16
                    f'16
                }
                ds'4
            }

        >>> for component in abjad.select.components(staff):
        ...     measure_number = abjad.get.measure_number(component)
        ...     print(f"{repr(component):30} {measure_number}")
        Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4") 1
        TremoloContainer("c'16 e'16")  1
        Note("c'16")                   1
        Note("e'16")                   1
        Note("cs'4")                   1
        TremoloContainer("d'16 f'16")  1
        Note("d'16")                   1
        Note("f'16")                   1
        Note("ds'4")                   1

    """
    if not isinstance(argument, _score.Component):
        raise Exception("can only get measure number on component.")
    _updatelib._update_measure_numbers(argument)
    assert isinstance(argument._measure_number, int)
    return argument._measure_number


def parentage(argument) -> "_parentage.Parentage":
    r"""
    Gets parentage.

    ..  container:: example

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
        ...     print(f"{repr(component)}:")
        ...     for component_ in parentage[:]:
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

    ..  container:: example

        REGRESSION. Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> lilypond_file = abjad.LilyPondFile([staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        gf'16
                    }
                    f'4
                }
            }

        >>> for component in abjad.select.components(staff):
        ...     parentage = abjad.get.parentage(component)
        ...     print(f"{repr(component)}:")
        ...     for component_ in parentage[:]:
        ...         print(f"    {repr(component_)}")
        Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }"):
            Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }")
        Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice'):
            Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice')
            Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }")
        Note("c'4"):
            Note("c'4")
            Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice')
            Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }")
        Note("d'4"):
            Note("d'4")
            Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice')
            Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }")
        Note("e'4"):
            Note("e'4")
            Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice')
            Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }")
        IndependentAfterGraceContainer("gf'16"):
            IndependentAfterGraceContainer("gf'16")
            Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice')
            Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }")
        Note("gf'16"):
            Note("gf'16")
            IndependentAfterGraceContainer("gf'16")
            Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice')
            Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }")
        Note("f'4"):
            Note("f'4")
            Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice')
            Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }")

    ..  container:: example

        REGRESSSION. Works with tremolo containers:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
        >>> staff.append("cs'4")
        >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
        >>> staff.append("ds'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \repeat tremolo 2
                {
                    c'16
                    e'16
                }
                cs'4
                \repeat tremolo 2
                {
                    d'16
                    f'16
                }
                ds'4
            }

        >>> for component in abjad.select.components(staff):
        ...     parentage = abjad.get.parentage(component)
        ...     print(f"{repr(component)}:")
        ...     print(f"    {repr(parentage[:])}")
        Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4"):
            (Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4"),)
        TremoloContainer("c'16 e'16"):
            (TremoloContainer("c'16 e'16"), Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4"))
        Note("c'16"):
            (Note("c'16"), TremoloContainer("c'16 e'16"), Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4"))
        Note("e'16"):
            (Note("e'16"), TremoloContainer("c'16 e'16"), Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4"))
        Note("cs'4"):
            (Note("cs'4"), Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4"))
        TremoloContainer("d'16 f'16"):
            (TremoloContainer("d'16 f'16"), Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4"))
        Note("d'16"):
            (Note("d'16"), TremoloContainer("d'16 f'16"), Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4"))
        Note("f'16"):
            (Note("f'16"), TremoloContainer("d'16 f'16"), Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4"))
        Note("ds'4"):
            (Note("ds'4"), Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4"))

    """
    if not isinstance(argument, _score.Component):
        message = "can only get parentage on component"
        message += f" (not {argument})."
        raise Exception(message)
    return _parentage.Parentage(argument)


def pitches(argument) -> set[_pitch.NamedPitch]:
    r"""
    Gets pitches.

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
        ...     pitches = abjad.get.pitches(component)
        ...     component
        ...     for _ in sorted(pitches): print(f"    {_!r}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }")
            NamedPitch("c'")
            NamedPitch("cs'")
            NamedPitch("d'")
            NamedPitch("e'")
            NamedPitch("f'")
            NamedPitch("fs'")
            NamedPitch("g'")
            NamedPitch("gs'")
            NamedPitch("a'")
            NamedPitch("as'")
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice')
            NamedPitch("c'")
            NamedPitch("cs'")
            NamedPitch("d'")
            NamedPitch("e'")
            NamedPitch("f'")
            NamedPitch("fs'")
            NamedPitch("g'")
            NamedPitch("gs'")
            NamedPitch("a'")
            NamedPitch("as'")
        Note("c'4")
            NamedPitch("c'")
        BeforeGraceContainer("cs'16")
            NamedPitch("cs'")
        Note("cs'16")
            NamedPitch("cs'")
        Note("d'4")
            NamedPitch("d'")
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }")
            NamedPitch("e'")
            NamedPitch("g'")
            NamedPitch("gs'")
            NamedPitch("a'")
            NamedPitch("as'")
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
            NamedPitch("e'")
            NamedPitch("g'")
            NamedPitch("gs'")
            NamedPitch("a'")
            NamedPitch("as'")
        Chord("<e' g'>16")
            NamedPitch("e'")
            NamedPitch("g'")
        Note("gs'16")
            NamedPitch("gs'")
        Note("a'16")
            NamedPitch("a'")
        Note("as'16")
            NamedPitch("as'")
        Voice("e'4", name='MusicVoice')
            NamedPitch("e'")
        Note("e'4")
            NamedPitch("e'")
        Note("f'4")
            NamedPitch("f'")
        AfterGraceContainer("fs'16")
            NamedPitch("fs'")
        Note("fs'16")
            NamedPitch("fs'")

    """
    generator = _iterate.pitches(argument)
    return set(generator)


def sounding_pitch(argument: _score.Note) -> _pitch.NamedPitch:
    r"""
    Gets sounding pitch of note.

    ..  container:: example

        >>> staff = abjad.Staff("d''8 e''8 f''8 g''8")
        >>> piccolo = abjad.Piccolo()
        >>> abjad.attach(piccolo, staff[0])
        >>> abjad.iterpitches.transpose_from_sounding_pitch(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                d'8
                e'8
                f'8
                g'8
            }

        >>> for note in abjad.select.notes(staff):
        ...     pitch = abjad.get.sounding_pitch(note)
        ...     print(f"{repr(note):10} {repr(pitch)}")
        Note("d'8") NamedPitch("d''")
        Note("e'8") NamedPitch("e''")
        Note("f'8") NamedPitch("f''")
        Note("g'8") NamedPitch("g''")

    """
    if not isinstance(argument, _score.Note):
        raise Exception("can only get sounding pitch of note.")
    return _getlib._get_sounding_pitch(argument)


def sounding_pitches(argument: _score.Chord) -> set[_pitch.NamedPitch]:
    r"""
    Gets sounding pitches.

    ..  container:: example

        >>> staff = abjad.Staff("<c''' e'''>4 <d''' fs'''>4")
        >>> glockenspiel = abjad.Glockenspiel()
        >>> abjad.attach(glockenspiel, staff[0])
        >>> abjad.iterpitches.transpose_from_sounding_pitch(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c' e'>4
                <d' fs'>4
            }

        >>> for chord in abjad.select.chords(staff):
        ...     pitches = abjad.get.sounding_pitches(chord)
        ...     chord
        ...     for _ in sorted(pitches): print(f"    {_!r}")
        Chord("<c' e'>4")
            NamedPitch("c'''")
            NamedPitch("e'''")
        Chord("<d' fs'>4")
            NamedPitch("d'''")
            NamedPitch("fs'''")

    """
    if not isinstance(argument, _score.Chord):
        raise Exception("can only get sounding pitches of chord.")
    pitches = _getlib._get_sounding_pitches(argument)
    return set(pitches)


def sustained(argument) -> bool:
    r"""
    Is true when ``argument`` is sustained.

    ..  container:: example

        >>> tuplet = abjad.Tuplet((3, 2), "c'4 ~ c' ~ c'")
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  container:: example

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 2/3
            {
                c'4
                ~
                c'4
                ~
                c'4
            }

        >>> abjad.get.sustained(tuplet)
        True

    """
    lt_head_count = 0
    leaves = _select.leaves(argument)
    for leaf in leaves:
        lt = logical_tie(leaf)
        if lt.head is leaf:
            lt_head_count += 1
    if lt_head_count == 0:
        return True
    lt = logical_tie(leaves[0])
    if lt.head is leaves[0] and lt_head_count == 1:
        return True
    return False


def timespan(argument, in_seconds: bool = False) -> _timespan.Timespan:
    r"""
    Gets timespan.

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
        ...     timespan = abjad.get.timespan(component)
        ...     print(f"{component!r}:")
        ...     print(f"    {timespan!r}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }"):
            Timespan(Offset((0, 1)), Offset((1, 1)))
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice'):
            Timespan(Offset((0, 1)), Offset((1, 1)))
        Note("c'4"):
            Timespan(Offset((0, 1)), Offset((1, 4)))
        BeforeGraceContainer("cs'16"):
            Timespan(Offset((1, 4), displacement=Duration(-1, 16)), Offset((1, 4)))
        Note("cs'16"):
            Timespan(Offset((1, 4), displacement=Duration(-1, 16)), Offset((1, 4)))
        Note("d'4"):
            Timespan(Offset((1, 4)), Offset((1, 2)))
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }"):
            Timespan(Offset((1, 2)), Offset((3, 4)))
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
            Timespan(Offset((1, 2)), Offset((1, 2), displacement=Duration(1, 4)))
        Chord("<e' g'>16"):
            Timespan(Offset((1, 2)), Offset((1, 2), displacement=Duration(1, 16)))
        Note("gs'16"):
            Timespan(Offset((1, 2), displacement=Duration(1, 16)), Offset((1, 2), displacement=Duration(1, 8)))
        Note("a'16"):
            Timespan(Offset((1, 2), displacement=Duration(1, 8)), Offset((1, 2), displacement=Duration(3, 16)))
        Note("as'16"):
            Timespan(Offset((1, 2), displacement=Duration(3, 16)), Offset((1, 2), displacement=Duration(1, 4)))
        Voice("e'4", name='MusicVoice'):
            Timespan(Offset((1, 2)), Offset((3, 4)))
        Note("e'4"):
            Timespan(Offset((1, 2), displacement=Duration(1, 4)), Offset((3, 4)))
        Note("f'4"):
            Timespan(Offset((3, 4)), Offset((1, 1)))
        AfterGraceContainer("fs'16"):
            Timespan(Offset((1, 1), displacement=Duration(-1, 16)), Offset((1, 1)))
        Note("fs'16"):
            Timespan(Offset((1, 1), displacement=Duration(-1, 16)), Offset((1, 1)))

    ..  container:: example

        REGRESSION. Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> lilypond_file = abjad.LilyPondFile([staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        gf'16
                    }
                    f'4
                }
            }

        >>> for component in abjad.select.components(staff):
        ...     timespan = abjad.get.timespan(component)
        ...     print(f"{component!r}:")
        ...     print(f"    {timespan!r}")
        Staff("{ c'4 d'4 e'4 { gf'16 } f'4 }"):
            Timespan(Offset((0, 1)), Offset((1, 1)))
        Voice("c'4 d'4 e'4 { gf'16 } f'4", name='MusicVoice'):
            Timespan(Offset((0, 1)), Offset((1, 1)))
        Note("c'4"):
            Timespan(Offset((0, 1)), Offset((1, 4)))
        Note("d'4"):
            Timespan(Offset((1, 4)), Offset((1, 2)))
        Note("e'4"):
            Timespan(Offset((1, 2)), Offset((3, 4)))
        IndependentAfterGraceContainer("gf'16"):
            Timespan(Offset((3, 4), displacement=Duration(-1, 16)), Offset((3, 4)))
        Note("gf'16"):
            Timespan(Offset((3, 4), displacement=Duration(-1, 16)), Offset((3, 4)))
        Note("f'4"):
            Timespan(Offset((3, 4)), Offset((1, 1)))

    ..  container:: example

        REGRESSSION. Works with tremolo containers:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
        >>> staff.append("cs'4")
        >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
        >>> staff.append("ds'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \repeat tremolo 2
                {
                    c'16
                    e'16
                }
                cs'4
                \repeat tremolo 2
                {
                    d'16
                    f'16
                }
                ds'4
            }

        >>> for component in abjad.select.components(staff):
        ...     timespan = abjad.get.timespan(component)
        ...     print(f"{repr(component):30} {repr(timespan)}")
        Staff("{ c'16 e'16 } cs'4 { d'16 f'16 } ds'4") Timespan(Offset((0, 1)), Offset((1, 1)))
        TremoloContainer("c'16 e'16")  Timespan(Offset((0, 1)), Offset((1, 4)))
        Note("c'16")                   Timespan(Offset((0, 1)), Offset((1, 8)))
        Note("e'16")                   Timespan(Offset((1, 8)), Offset((1, 4)))
        Note("cs'4")                   Timespan(Offset((1, 4)), Offset((1, 2)))
        TremoloContainer("d'16 f'16")  Timespan(Offset((1, 2)), Offset((3, 4)))
        Note("d'16")                   Timespan(Offset((1, 2)), Offset((5, 8)))
        Note("f'16")                   Timespan(Offset((5, 8)), Offset((3, 4)))
        Note("ds'4")                   Timespan(Offset((3, 4)), Offset((1, 1)))

    ..  container:: example

        REGRESION. Works with selection:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
            }

        >>> abjad.get.timespan(staff[:3])
        Timespan(Offset((0, 1)), Offset((3, 4)))

    """
    return _getlib._get_timespan(argument, in_seconds=in_seconds)


def wrapper(
    argument,
    prototype: _typings.Prototype | None = None,
    *,
    attributes: dict | None = None,
):
    r"""
    Gets wrapper.

    ..  container:: example

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> staff = abjad.Staff([music_voice])
        >>> container = abjad.BeforeGraceContainer("cs'16")
        >>> abjad.attach(container, music_voice[1])
        >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
        >>> abjad.attach(abjad.Clef("alto"), obgc[0])
        >>> abjad.attach(abjad.Articulation(">"), obgc[0])
        >>> container = abjad.AfterGraceContainer("fs'16")
        >>> abjad.attach(container, music_voice[3])
        >>> for note in abjad.select.notes(staff):
        ...     abjad.attach(abjad.Articulation("."), note)

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
                    - \staccato
                    \grace {
                        cs'16
                        - \staccato
                    }
                    d'4
                    - \staccato
                    <<
                        \context Voice = "On_Beat_Grace_Container"
                        {
                            \clef "alto"
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
                            - \staccato
                            a'16
                            - \staccato
                            as'16
                            - \staccato
                            )
                            ]
                        }
                        \context Voice = "MusicVoice"
                        {
                            \voiceTwo
                            e'4
                            - \staccato
                        }
                    >>
                    \oneVoice
                    \afterGrace
                    f'4
                    - \staccato
                    {
                        fs'16
                        - \staccato
                    }
                }
            }

        REGRESSION. Works with grace notes (and containers):

        >>> for component in abjad.select.components(staff):
        ...     wrapper = abjad.get.wrapper(component, abjad.Articulation)
        ...     print(f"{component!r}:")
        ...     print(f"    {wrapper!r}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }"):
            None
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice'):
            None
        Note("c'4"):
            Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))
        BeforeGraceContainer("cs'16"):
            None
        Note("cs'16"):
            Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))
        Note("d'4"):
            Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }"):
            None
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
            None
        Chord("<e' g'>16"):
            Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='>'), synthetic_offset=None, tag=Tag(string=''))
        Note("gs'16"):
            Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))
        Note("a'16"):
            Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))
        Note("as'16"):
            Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))
        Voice("e'4", name='MusicVoice'):
            None
        Note("e'4"):
            Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))
        Note("f'4"):
            Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))
        AfterGraceContainer("fs'16"):
            None
        Note("fs'16"):
            Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))

    Raises exception when more than one indicator of ``prototype`` attach to
    ``argument``.
    """
    if attributes is not None:
        assert isinstance(attributes, dict), repr(attributes)
    return indicator(argument, prototype=prototype, unwrap=False)


def wrappers(
    argument,
    prototype: _typings.Prototype | None = None,
    *,
    attributes: dict | None = None,
):
    r"""
    Gets wrappers.

    ..  container:: example

        REGRESSION. Works with grace notes (and containers):

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> staff = abjad.Staff([music_voice])
        >>> container = abjad.BeforeGraceContainer("cs'16")
        >>> abjad.attach(container, music_voice[1])
        >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
        >>> abjad.attach(abjad.Clef("alto"), obgc[0])
        >>> abjad.attach(abjad.Articulation(">"), obgc[0])
        >>> container = abjad.AfterGraceContainer("fs'16")
        >>> abjad.attach(container, music_voice[3])
        >>> for note in abjad.select.notes(staff):
        ...     abjad.attach(abjad.Articulation("."), note)

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
                    - \staccato
                    \grace {
                        cs'16
                        - \staccato
                    }
                    d'4
                    - \staccato
                    <<
                        \context Voice = "On_Beat_Grace_Container"
                        {
                            \clef "alto"
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
                            - \staccato
                            a'16
                            - \staccato
                            as'16
                            - \staccato
                            )
                            ]
                        }
                        \context Voice = "MusicVoice"
                        {
                            \voiceTwo
                            e'4
                            - \staccato
                        }
                    >>
                    \oneVoice
                    \afterGrace
                    f'4
                    - \staccato
                    {
                        fs'16
                        - \staccato
                    }
                }
            }

        >>> for component in abjad.select.components(staff):
        ...     result = abjad.get.wrappers(component, abjad.Articulation)
        ...     print(f"{component!r}:")
        ...     print(f"    {result!r}")
        Staff("{ c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4 }"):
            []
        Voice("c'4 d'4 { { <e' g'>16 gs'16 a'16 as'16 } { e'4 } } f'4", name='MusicVoice'):
            []
        Note("c'4"):
            [Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))]
        BeforeGraceContainer("cs'16"):
            []
        Note("cs'16"):
            [Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))]
        Note("d'4"):
            [Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))]
        Container("{ <e' g'>16 gs'16 a'16 as'16 } { e'4 }"):
            []
        OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
            []
        Chord("<e' g'>16"):
            [Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='>'), synthetic_offset=None, tag=Tag(string=''))]
        Note("gs'16"):
            [Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))]
        Note("a'16"):
            [Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))]
        Note("as'16"):
            [Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))]
        Voice("e'4", name='MusicVoice'):
            []
        Note("e'4"):
            [Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))]
        Note("f'4"):
            [Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))]
        AfterGraceContainer("fs'16"):
            []
        Note("fs'16"):
            [Wrapper(annotation=None, context=None, deactivate=False, direction=None, indicator=Articulation(name='.'), synthetic_offset=None, tag=Tag(string=''))]

    """
    if attributes is not None:
        assert isinstance(attributes, dict), repr(attributes)
    return indicators(argument, prototype=prototype, unwrap=False)


class Lineage(collections.abc.Sequence):
    r'''
    Lineage of a component.

    ..  container:: example

        >>> score = abjad.Score()
        >>> staff = abjad.Staff(
        ...     r"""\new Voice = "Treble_Voice" { c'4 }""",
        ...     name='Treble_Staff',
        ...     )
        >>> score.append(staff)
        >>> bass = abjad.Staff(
        ...     r"""\new Voice = "Bass_Voice" { b,4 }""",
        ...     name='Bass_Staff',
        ...     )
        >>> score.append(bass)

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        c'4
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        b,4
                    }
                }
            >>

        >>> for component in abjad.get.lineage(score):
        ...     component
        ...
        Score("{ { c'4 } } { { b,4 } }", simultaneous=True)
        Staff("{ c'4 }", name='Treble_Staff')
        Voice("c'4", name='Treble_Voice')
        Note("c'4")
        Staff('{ b,4 }', name='Bass_Staff')
        Voice('b,4', name='Bass_Voice')
        Note('b,4')

        >>> bass_voice = score['Bass_Voice']
        >>> for component in abjad.get.lineage(bass_voice):
        ...     component
        ...
        Score("{ { c'4 } } { { b,4 } }", simultaneous=True)
        Staff('{ b,4 }', name='Bass_Staff')
        Voice('b,4', name='Bass_Voice')
        Note('b,4')

    '''

    __slots__ = ("_component", "_components")

    def __init__(self, component=None):
        if component is not None:
            assert hasattr(component, "_timespan"), repr(component)
        self._component = component
        components = []
        if component is not None:
            components.extend(reversed(parentage(component)[1:]))
            components.append(component)
            components.extend(descendants(component)[1:])
        self._components = components

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` lineage with components of same id.
        """
        if isinstance(argument, type(self)):
            if len(self) == len(argument):
                for c, d in zip(self.components, argument.components):
                    if c is not d:
                        return False
                else:
                    return True
        return False

    def __getitem__(self, argument):
        """
        Gets ``argument``.

        Returns component or tuple.
        """
        return self.components.__getitem__(argument)

    def __len__(self):
        """
        Gets length of lineage.

        Returns int.
        """
        return len(self._components)

    @property
    def component(self):
        """
        The component from which the lineage was derived.
        """
        return self._component

    @property
    def components(self):
        """
        Gets components.

        Returns tuple.
        """
        return self._components
