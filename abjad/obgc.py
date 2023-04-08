import typing

from . import _indentlib, _iterlib
from . import bind as _bind
from . import duration as _duration
from . import get as _get
from . import indicators as _indicators
from . import iterate as _iterate
from . import mutate as _mutate
from . import parentage as _parentage
from . import score as _score
from . import select as _select
from . import spanners as _spanners
from . import tag as _tag
from . import tweaks as _tweaks
from . import typings as _typings


class OnBeatGraceContainer(_score.Container):
    r"""
    On-beat grace container.

    ..  note:: On-beat grace containers must be included in a named voice.

    ..  container:: example

        On-beat grace containers implement custom formatting not available in LilyPond:

        >>> music_voice = abjad.Voice("c'4 d'4 e'4 f'4", name="MusicVoice")
        >>> string = "<d' g'>8 a' b' c'' d'' c'' b' a' b' c'' d''"
        >>> container = abjad.on_beat_grace_container(
        ...     string, music_voice[1:3], grace_leaf_duration=(1, 24)
        ... )
        >>> abjad.attach(abjad.Articulation(">"), container[0])
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
                                g'
                            >8 * 1/3
                            - \accent
                            [
                            (
                            a'8 * 1/3
                            b'8 * 1/3
                            c''8 * 1/3
                            d''8 * 1/3
                            c''8 * 1/3
                            b'8 * 1/3
                            a'8 * 1/3
                            b'8 * 1/3
                            c''8 * 1/3
                            d''8 * 1/3
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

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_grace_leaf_duration",)

    ### INITIALIZER ###

    def __init__(
        self,
        components: str | typing.Sequence[_score.Leaf] = (),
        *,
        grace_leaf_duration: _typings.Duration | None = None,
        identifier: str | None = None,
        name: str | None = None,
        tag: _tag.Tag | None = None,
    ) -> None:
        super().__init__(components, identifier=identifier, name=name, tag=tag)
        if grace_leaf_duration is not None:
            grace_leaf_duration = _duration.Duration(grace_leaf_duration)
        self._grace_leaf_duration = grace_leaf_duration

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        """
        Gets new after grace container arguments.

        Returns tuple of single empty list.
        """
        return ([],)

    ### PRIVATE METHODS ###

    def _attach_lilypond_one_voice(self):
        anchor_leaf = self.get_anchor_leaf()
        anchor_voice = _parentage.Parentage(anchor_leaf).get(_score.Voice)
        final_anchor_leaf = _iterlib._get_leaf(anchor_voice, -1)
        next_leaf = _iterlib._get_leaf(final_anchor_leaf, 1)
        if next_leaf is None:
            return
        command = _indicators.VoiceNumber()
        if _get.has_indicator(next_leaf, command):
            return
        next_leaf_parent = _get.parentage(next_leaf).parent
        if isinstance(next_leaf_parent, OnBeatGraceContainer):
            return
        if self._is_on_beat_anchor_voice(next_leaf_parent):
            return
        tag = self.tag
        tag = tag.append(
            _tag.Tag("abjad.OnBeatGraceContainer._attach_lilypond_one_voice()")
        )
        tag = tag.append(_tag.Tag("ONE_VOICE_COMMAND"))
        _bind.attach(command, next_leaf, tag=tag)

    def _format_invocation(self):
        return r'\context Voice = "On_Beat_Grace_Container"'

    def _format_open_brackets_site(self, contributions):
        result = []
        if self.identifier:
            open_bracket = f"{{   {self.identifier}"
        else:
            open_bracket = "{"
        brackets_open = [open_bracket]
        overrides = contributions.grob_overrides
        settings = contributions.context_settings
        if overrides or settings:
            contributions = [self._format_invocation(), r"\with", "{"]
            contributions = self._tag_strings(contributions)
            result.extend(contributions)
            contributions = [_indentlib.INDENT + _ for _ in overrides]
            contributions = self._tag_strings(contributions)
            result.extend(contributions)
            contributions = [_indentlib.INDENT + _ for _ in settings]
            contributions = self._tag_strings(contributions)
            result.extend(contributions)
            contributions = [f"}} {brackets_open[0]}"]
            contributions = ["}", open_bracket]
            contributions = self._tag_strings(contributions)
            result.extend(contributions)
        else:
            contribution = self._format_invocation()
            contribution += f" {brackets_open[0]}"
            contributions = [contribution]
            contributions = [self._format_invocation(), open_bracket]
            contributions = self._tag_strings(contributions)
            result.extend(contributions)
        return result

    @staticmethod
    def _is_on_beat_anchor_voice(container):
        wrapper = _get.parentage(container).parent
        if wrapper is None:
            return False
        if not isinstance(container, _score.Voice):
            return False
        return OnBeatGraceContainer._is_on_beat_wrapper(wrapper)

    @staticmethod
    def _is_on_beat_wrapper(container):
        if not container.simultaneous:
            return False
        if len(container) != 2:
            return False
        if isinstance(container[0], OnBeatGraceContainer) and isinstance(
            container[1], _score.Voice
        ):
            return True
        if isinstance(container[0], _score.Voice) and isinstance(
            container[1], OnBeatGraceContainer
        ):
            return True
        return False

    def _match_anchor_leaf(self):
        string = "abjad.OnBeatGraceContainer._match_anchor_leaf()"
        tag = self.tag.append(_tag.Tag(string))
        first_grace = _iterlib._get_leaf(self, 0)
        if not isinstance(first_grace, _score.Note | _score.Chord):
            message = "must start with note or chord:\n"
            message += f"    {repr(self)}"
            raise Exception(message)
        anchor_leaf = self.get_anchor_leaf()
        if not isinstance(anchor_leaf, _score.Note | _score.Chord):
            return
        if not isinstance(first_grace, _score.Note | _score.Chord):
            return
        if isinstance(first_grace, _score.Note):
            chord = _score.Chord(first_grace, tag=tag)
            _mutate.replace(first_grace, chord)
            first_grace = chord
        generator = _iterate.pitches(anchor_leaf)
        anchor_pitches = list(generator)
        highest_pitch = list(sorted(anchor_pitches))[-1]
        if highest_pitch not in first_grace.note_heads:
            first_grace.note_heads.append(highest_pitch)
        grace_mate_head = first_grace.note_heads.get(highest_pitch)
        _tweaks.tweak(grace_mate_head, r"\tweak font-size 0", tag=tag)
        _tweaks.tweak(grace_mate_head, r"\tweak transparent ##t", tag=tag)

    def _set_leaf_durations(self):
        if self.grace_leaf_duration is None:
            return
        for leaf in _select.leaves(self):
            duration = _get.duration(leaf)
            if duration != self.grace_leaf_duration:
                multiplier = self.grace_leaf_duration / duration
                leaf.multiplier = _duration.pair(multiplier)

    ### PUBLIC PROPERTIES ###

    @property
    def grace_leaf_duration(self) -> _duration.Duration | None:
        """
        Gets grace leaf duration.
        """
        return self._grace_leaf_duration

    ### PUBLIC METHODS ###

    def get_anchor_leaf(self):
        """
        Gets anchor leaf.
        """
        container = _get.parentage(self).parent
        if container is None:
            return None
        if len(container) != 2:
            raise Exception("Combine on-beat grace container with one other voice.")
        if container.index(self) == 0:
            anchor_voice = container[-1]
        else:
            assert container.index(self) == 1
            anchor_voice = container[0]
        anchor_leaf = _select.leaf(anchor_voice, 0, grace=False)
        return anchor_leaf


def on_beat_grace_container(
    grace_leaves: str | typing.Sequence[_score.Leaf],
    nongrace_leaves: typing.Sequence[_score.Leaf],
    *,
    do_not_attach_one_voice_command: bool = False,
    do_not_beam: bool = False,
    do_not_slash: bool = False,
    do_not_slur: bool = False,
    grace_font_size: int = -3,
    grace_leaf_duration: _typings.Duration | None = None,
    grace_polyphony_command: _indicators.VoiceNumber = _indicators.VoiceNumber(1),
    nongrace_polyphony_command: _indicators.VoiceNumber = _indicators.VoiceNumber(2),
    tag: _tag.Tag = _tag.Tag(),
) -> "OnBeatGraceContainer":
    r"""
    Makes on-beat grace container (with ``grace_leaves``) and attaches to
    ``nongrace_leaves``.

    ..  container:: example

        >>> def make_lilypond_file(anchor_voice_string, obgc_string, *, below=False):
        ...     music_voice = abjad.Voice(anchor_voice_string, name="MusicVoice")
        ...     if below is False:
        ...         nongrace_polyphony_command = abjad.VoiceNumber(2)
        ...         grace_polyphony_command = abjad.VoiceNumber(1)
        ...     else:
        ...         nongrace_polyphony_command = abjad.VoiceNumber(1)
        ...         grace_polyphony_command = abjad.VoiceNumber(2)
        ...     result = abjad.on_beat_grace_container(
        ...         obgc_string,
        ...         music_voice[1:3],
        ...         grace_leaf_duration=abjad.Duration(1, 30),
        ...         grace_polyphony_command=grace_polyphony_command,
        ...         nongrace_polyphony_command=nongrace_polyphony_command,
        ...     )
        ...     staff = abjad.Staff([music_voice])
        ...     lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        ...     return lilypond_file

    ..  container:: example

        GRACE NOTES ABOVE.

        Note-to-note anchor:

        >>> lilypond_file = make_lilypond_file(
        ...     "c'4 d' e' f'",
        ...     "g'8 a' b' c'' d'' c'' b' a' b' c'' d''",
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff = lilypond_file.items[-1]
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
                                g'
                            >8 * 4/15
                            [
                            (
                            a'8 * 4/15
                            b'8 * 4/15
                            c''8 * 4/15
                            d''8 * 4/15
                            c''8 * 4/15
                            b'8 * 4/15
                            a'8 * 4/15
                            b'8 * 4/15
                            c''8 * 4/15
                            d''8 * 4/15
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

        Note-to-chord anchor:

        >>> lilypond_file = make_lilypond_file(
        ...     "<a c'>4 <b d'> <c' e'> <d' f'>",
        ...     "g'8 a' b' c'' d'' c'' b' a' b' c'' d''",
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff = lilypond_file.items[-1]
            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    <a c'>4
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
                                g'
                            >8 * 4/15
                            [
                            (
                            a'8 * 4/15
                            b'8 * 4/15
                            c''8 * 4/15
                            d''8 * 4/15
                            c''8 * 4/15
                            b'8 * 4/15
                            a'8 * 4/15
                            b'8 * 4/15
                            c''8 * 4/15
                            d''8 * 4/15
                            )
                            ]
                        }
                        \context Voice = "MusicVoice"
                        {
                            \voiceTwo
                            <b d'>4
                            <c' e'>4
                        }
                    >>
                    \oneVoice
                    <d' f'>4
                }
            }

        Chord-to-note anchor:

        >>> lilypond_file = make_lilypond_file(
        ...     "c'4 d' e' f'",
        ...     "<g' b'>8 a' b' c'' d'' c'' b' a' b' c'' d''",
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff = lilypond_file.items[-1]
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
                                g'
                                b'
                            >8 * 4/15
                            [
                            (
                            a'8 * 4/15
                            b'8 * 4/15
                            c''8 * 4/15
                            d''8 * 4/15
                            c''8 * 4/15
                            b'8 * 4/15
                            a'8 * 4/15
                            b'8 * 4/15
                            c''8 * 4/15
                            d''8 * 4/15
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

        Chord-to-chord anchor:

        >>> lilypond_file = make_lilypond_file(
        ...     "<a c'>4 <b d'> <c' e'> <d' f'>",
        ...     "<g' b'>8 a' b' c'' d'' c'' b' a' b' c'' d''",
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff = lilypond_file.items[-1]
            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    <a c'>4
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
                                g'
                                b'
                            >8 * 4/15
                            [
                            (
                            a'8 * 4/15
                            b'8 * 4/15
                            c''8 * 4/15
                            d''8 * 4/15
                            c''8 * 4/15
                            b'8 * 4/15
                            a'8 * 4/15
                            b'8 * 4/15
                            c''8 * 4/15
                            d''8 * 4/15
                            )
                            ]
                        }
                        \context Voice = "MusicVoice"
                        {
                            \voiceTwo
                            <b d'>4
                            <c' e'>4
                        }
                    >>
                    \oneVoice
                    <d' f'>4
                }
            }

    ..  container:: example

        GRACE NOTES BELOW.

        Note-to-note anchor:

        >>> lilypond_file = make_lilypond_file(
        ...     "c'4 d' e' f'",
        ...     "g8 a b c' d' c' b a b c' d'",
        ...     below=True,
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff = lilypond_file.items[-1]
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
                            \voiceTwo
                            <
                                g
                                \tweak font-size 0
                                \tweak transparent ##t
                                d'
                            >8 * 4/15
                            [
                            (
                            a8 * 4/15
                            b8 * 4/15
                            c'8 * 4/15
                            d'8 * 4/15
                            c'8 * 4/15
                            b8 * 4/15
                            a8 * 4/15
                            b8 * 4/15
                            c'8 * 4/15
                            d'8 * 4/15
                            )
                            ]
                        }
                        \context Voice = "MusicVoice"
                        {
                            \voiceOne
                            d'4
                            e'4
                        }
                    >>
                    \oneVoice
                    f'4
                }
            }

        Note-to-chord anchor:

        >>> lilypond_file = make_lilypond_file(
        ...     "<c' e'>4 <d' f'> <e' g'> <f' a'>",
        ...     "g8 a b c' d' c' b a b c' d'",
        ...     below=True,
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff = lilypond_file.items[-1]
            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    <c' e'>4
                    <<
                        \context Voice = "On_Beat_Grace_Container"
                        {
                            \set fontSize = #-3
                            \slash
                            \voiceTwo
                            <
                                g
                                \tweak font-size 0
                                \tweak transparent ##t
                                f'
                            >8 * 4/15
                            [
                            (
                            a8 * 4/15
                            b8 * 4/15
                            c'8 * 4/15
                            d'8 * 4/15
                            c'8 * 4/15
                            b8 * 4/15
                            a8 * 4/15
                            b8 * 4/15
                            c'8 * 4/15
                            d'8 * 4/15
                            )
                            ]
                        }
                        \context Voice = "MusicVoice"
                        {
                            \voiceOne
                            <d' f'>4
                            <e' g'>4
                        }
                    >>
                    \oneVoice
                    <f' a'>4
                }
            }

        Chord-to-note anchor:

        >>> lilypond_file = make_lilypond_file(
        ...     "c'4 d' e' f'",
        ...     "<e g>8 a b c' d' c' b a b c' d'",
        ...     below=True,
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff = lilypond_file.items[-1]
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
                            \voiceTwo
                            <
                                e
                                g
                                \tweak font-size 0
                                \tweak transparent ##t
                                d'
                            >8 * 4/15
                            [
                            (
                            a8 * 4/15
                            b8 * 4/15
                            c'8 * 4/15
                            d'8 * 4/15
                            c'8 * 4/15
                            b8 * 4/15
                            a8 * 4/15
                            b8 * 4/15
                            c'8 * 4/15
                            d'8 * 4/15
                            )
                            ]
                        }
                        \context Voice = "MusicVoice"
                        {
                            \voiceOne
                            d'4
                            e'4
                        }
                    >>
                    \oneVoice
                    f'4
                }
            }

        Chord-to-chord anchor:

        >>> lilypond_file = make_lilypond_file(
        ...     "<c' e'>4 <d' f'> <e' g'> <f' a'>",
        ...     "<e g>8 a b c' d' c' b a b c' d'",
        ...     below=True,
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff = lilypond_file.items[-1]
            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    <c' e'>4
                    <<
                        \context Voice = "On_Beat_Grace_Container"
                        {
                            \set fontSize = #-3
                            \slash
                            \voiceTwo
                            <
                                e
                                g
                                \tweak font-size 0
                                \tweak transparent ##t
                                f'
                            >8 * 4/15
                            [
                            (
                            a8 * 4/15
                            b8 * 4/15
                            c'8 * 4/15
                            d'8 * 4/15
                            c'8 * 4/15
                            b8 * 4/15
                            a8 * 4/15
                            b8 * 4/15
                            c'8 * 4/15
                            d'8 * 4/15
                            )
                            ]
                        }
                        \context Voice = "MusicVoice"
                        {
                            \voiceOne
                            <d' f'>4
                            <e' g'>4
                        }
                    >>
                    \oneVoice
                    <f' a'>4
                }
            }

        ..  TODO:: Fix stem-alignment in final example.

    """
    if not isinstance(grace_leaves, str):
        assert all(isinstance(_, _score.Leaf) for _ in grace_leaves), repr(grace_leaves)
    assert all(isinstance(_, _score.Leaf) for _ in nongrace_leaves), repr(
        nongrace_leaves
    )
    assert isinstance(grace_font_size, int), repr(grace_font_size)
    assert isinstance(grace_polyphony_command, _indicators.VoiceNumber), repr(
        grace_polyphony_command
    )
    assert isinstance(nongrace_polyphony_command, _indicators.VoiceNumber), repr(
        nongrace_polyphony_command
    )
    assert isinstance(tag, _tag.Tag), repr(tag)
    tag = tag.append(_tag.Tag("abjad.on_beat_grace_container()"))
    if not _mutate._are_contiguous_same_parent(
        nongrace_leaves, ignore_before_after_grace=True
    ):
        message = "nongrace leaves must be contiguous in same parent:\n"
        message += f"   {repr(nongrace_leaves)}"
        raise Exception(message)
    on_beat_grace_container = OnBeatGraceContainer(
        grace_leaves, grace_leaf_duration=grace_leaf_duration, tag=tag
    )
    anchor_leaf = _iterlib._get_leaf(nongrace_leaves, 0)
    anchor_voice = _parentage.Parentage(anchor_leaf).get(_score.Voice)
    assert isinstance(anchor_voice, _score.Voice), repr(anchor_voice)
    if anchor_voice.name is None:
        raise Exception(f"anchor voice must be named:\n   {repr(anchor_voice)}")
    anchor_voice_insert = _score.Voice(name=anchor_voice.name, tag=tag)
    _mutate.wrap(nongrace_leaves, anchor_voice_insert)
    container = _score.Container(simultaneous=True, tag=tag)
    _mutate.wrap(anchor_voice_insert, container)
    container.insert(0, on_beat_grace_container)
    on_beat_grace_container._match_anchor_leaf()
    on_beat_grace_container._set_leaf_durations()
    insert_duration = _get.duration(anchor_voice_insert)
    grace_container_duration = _get.duration(on_beat_grace_container)
    if insert_duration < grace_container_duration:
        message = f"grace {repr(grace_container_duration)}"
        message += f" exceeds anchor {repr(insert_duration)}."
        raise Exception(message)
    literal = _indicators.LilyPondLiteral(
        rf"\set fontSize = #{grace_font_size}",
        site="before",
    )
    _bind.attach(literal, on_beat_grace_container[0], tag=tag)
    if not do_not_beam:
        _spanners.beam(on_beat_grace_container[:], tag=tag)
    if not do_not_slash:
        literal = _indicators.LilyPondLiteral(r"\slash", site="before")
        _bind.attach(literal, on_beat_grace_container[0], tag=tag)
    if not do_not_slur:
        _spanners.slur(on_beat_grace_container[:], tag=tag)
    first_grace = _iterlib._get_leaf(on_beat_grace_container, 0)
    _bind.detach(_indicators.VoiceNumber(), anchor_leaf)
    _bind.attach(
        grace_polyphony_command,
        first_grace,
        tag=tag,
    )
    _bind.detach(_indicators.VoiceNumber(), anchor_leaf)
    _bind.attach(
        nongrace_polyphony_command,
        anchor_leaf,
        tag=tag,
    )
    if not do_not_attach_one_voice_command:
        last_anchor_leaf = _iterlib._get_leaf(nongrace_leaves, -1)
        next_leaf = _iterlib._get_leaf(last_anchor_leaf, 1)
        if next_leaf is not None:
            command = _indicators.VoiceNumber()
            _bind.attach(command, next_leaf, tag=tag)
    return on_beat_grace_container
