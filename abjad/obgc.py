import typing

from . import _iterate, mutate, typings
from .attach import attach, detach
from .bundle import LilyPondFormatBundle
from .duration import Duration
from .overrides import LilyPondLiteral, tweak
from .parentage import Parentage
from .pitch.sets import PitchSet
from .score import Chord, Container, Note, Voice
from .select import Selection
from .spanners import beam, slur
from .tag import Tag


class OnBeatGraceContainer(Container):
    r"""
    On-beat grace container.

    ..  note:: On-beat grace containers must be included in a named voice.

    ..  container:: example

        On-beat grace containers implement custom formatting not available in
        LilyPond:

        >>> music_voice = abjad.Voice("c'4 d'4 e'4 f'4", name="Music_Voice")
        >>> string = "<d' g'>8 a' b' c'' d'' c'' b' a' b' c'' d''"
        >>> container = abjad.on_beat_grace_container(
        ...     string, music_voice[1:3], leaf_duration=(1, 24)
        ... )
        >>> abjad.attach(abjad.Articulation(">"), container[0])
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
                        \context Voice = "Music_Voice"
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

    __slots__ = ("_leaf_duration",)

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        identifier: str = None,
        leaf_duration: typings.DurationTyping = None,
        name: str = None,
        tag: Tag = None,
    ) -> None:
        super().__init__(components, identifier=identifier, name=name, tag=tag)
        if leaf_duration is not None:
            leaf_duration = Duration(leaf_duration)
        self._leaf_duration = leaf_duration

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        """
        Gets new after grace container arguments.

        Returns tuple of single empty list.
        """
        return ([],)

    ### PRIVATE METHODS ###

    # NOTE: format="absolute_before" for \oneVoice so that this works:
    #
    #           \oneVoice
    #           \override Stem.direction = #down
    #
    # ... because this ...
    #
    #           \override Stem.direction = #down
    #           \oneVoice
    #
    # ... doesn't work.
    #
    # This is hackish, and some sort of longer term solution should
    # happen later.
    def _attach_lilypond_one_voice(self):
        anchor_leaf = self._get_on_beat_anchor_leaf()
        anchor_voice = Parentage(anchor_leaf).get(Voice)
        final_anchor_leaf = _iterate._get_leaf(anchor_voice, -1)
        next_leaf = _iterate._get_leaf(final_anchor_leaf, 1)
        literal = LilyPondLiteral(r"\oneVoice", format_slot="absolute_before")
        if next_leaf._has_indicator(literal):
            return
        if isinstance(next_leaf._parent, OnBeatGraceContainer):
            return
        if self._is_on_beat_anchor_voice(next_leaf._parent):
            return
        site = "abjad.OnBeatGraceContainer._attach_lilypond_one_voice()"
        tag = Tag(site)
        tag = tag.append(Tag("ONE_VOICE_COMMAND"))
        attach(literal, next_leaf, tag=tag)

    def _format_invocation(self):
        return r'\context Voice = "On_Beat_Grace_Container"'

    def _format_open_brackets_slot(self, bundle):
        indent = LilyPondFormatBundle.indent
        result = []
        if self.identifier:
            open_bracket = f"{{   {self.identifier}"
        else:
            open_bracket = "{"
        brackets_open = [open_bracket]
        overrides = bundle.grob_overrides
        settings = bundle.context_settings
        if overrides or settings:
            contributions = [self._format_invocation(), r"\with", "{"]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("context_brackets", "open")
            result.append((identifier_pair, contributions))
            contributions = [indent + _ for _ in overrides]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("overrides", "overrides")
            result.append((identifier_pair, contributions))
            contributions = [indent + _ for _ in settings]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("settings", "settings")
            result.append((identifier_pair, contributions))
            contributions = [f"}} {brackets_open[0]}"]
            contributions = ["}", open_bracket]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("context_brackets", "open")
            result.append((identifier_pair, contributions))
        else:
            contribution = self._format_invocation()
            contribution += f" {brackets_open[0]}"
            contributions = [contribution]
            contributions = [self._format_invocation(), open_bracket]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("context_brackets", "open")
            result.append((identifier_pair, contributions))
        return tuple(result)

    def _get_on_beat_anchor_leaf(self):
        container = self._parent
        if container is None:
            return None
        if len(container) != 2:
            raise Exception("Combine on-beat grace container with one other voice.")
        if container.index(self) == 0:
            anchor_voice = container[-1]
        else:
            assert container.index(self) == 1
            anchor_voice = container[0]
        anchor_leaf = Selection(anchor_voice).leaf(0, grace=False)
        return anchor_leaf

    @staticmethod
    def _is_on_beat_anchor_voice(CONTAINER):
        wrapper = CONTAINER._parent
        if wrapper is None:
            return False
        if not isinstance(CONTAINER, Voice):
            return False
        return OnBeatGraceContainer._is_on_beat_wrapper(wrapper)

    @staticmethod
    def _is_on_beat_wrapper(CONTAINER):
        if not CONTAINER.simultaneous:
            return False
        if len(CONTAINER) != 2:
            return False
        if isinstance(CONTAINER[0], OnBeatGraceContainer) and isinstance(
            CONTAINER[1], Voice
        ):
            return True
        if isinstance(CONTAINER[0], Voice) and isinstance(
            CONTAINER[1], OnBeatGraceContainer
        ):
            return True
        return False

    def _match_anchor_leaf(self):
        first_grace = _iterate._get_leaf(self, 0)
        if not isinstance(first_grace, (Note, Chord)):
            message = "must start with note or chord:\n"
            message += f"    {repr(self)}"
            raise Exception(message)
        anchor_leaf = self._get_on_beat_anchor_leaf()
        if isinstance(anchor_leaf, (Note, Chord)) and isinstance(
            first_grace, (Note, Chord)
        ):
            if isinstance(first_grace, Note):
                chord = Chord(first_grace)
                mutate.replace(first_grace, chord)
                first_grace = chord
            selection = Selection(anchor_leaf)
            anchor_pitches = PitchSet.from_selection(selection)
            highest_pitch = list(sorted(anchor_pitches))[-1]
            if highest_pitch not in first_grace.note_heads:
                first_grace.note_heads.append(highest_pitch)
            grace_mate_head = first_grace.note_heads.get(highest_pitch)
            tweak(grace_mate_head).font_size = 0
            tweak(grace_mate_head).transparent = True

    def _set_leaf_durations(self):
        if self.leaf_duration is None:
            return
        for leaf in Selection(self).leaves():
            duration = leaf._get_duration()
            if duration != self.leaf_duration:
                multiplier = self.leaf_duration / duration
                leaf.multiplier = multiplier

    ### PUBLIC PROPERTIES ###

    @property
    def leaf_duration(self) -> typing.Optional[Duration]:
        """
        Gets leaf duration.
        """
        return self._leaf_duration


### FACTORY FUNCTIONS ###


def on_beat_grace_container(
    contents,
    anchor_voice_selection,
    *,
    anchor_voice_number=2,
    do_not_beam=None,
    do_not_slash=None,
    do_not_slur=None,
    do_not_stop_polyphony=None,
    font_size=-3,
    grace_voice_number=1,
    leaf_duration=None,
):
    r"""
    Makes on-beat grace container and wraps around ``selection``.

    ..  container:: example

        GRACE NOTES ABOVE.

        Note-to-note anchor:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
        >>> string = "g'8 a' b' c'' d'' c'' b' a' b' c'' d''"
        >>> result = abjad.on_beat_grace_container(
        ...     string, music_voice[1:3], leaf_duration=(1, 30)
        ... )
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
                        \context Voice = "Music_Voice"
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

        >>> music_voice = abjad.Voice(
        ...     "<a c'>4 <b d'> <c' e'> <d' f'>", name="Music_Voice"
        ... )
        >>> string = "g'8 a' b' c'' d'' c'' b' a' b' c'' d''"
        >>> result = abjad.on_beat_grace_container(
        ...     string, music_voice[1:3], leaf_duration=(1, 30)
        ... )
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "Music_Voice"
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
                        \context Voice = "Music_Voice"
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

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
        >>> string = "<g' b'>8 a' b' c'' d'' c'' b' a' b' c'' d''"
        >>> result = abjad.on_beat_grace_container(
        ...     string, music_voice[1:3], leaf_duration=(1, 30)
        ... )
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
                        \context Voice = "Music_Voice"
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

        >>> music_voice = abjad.Voice(
        ...     "<a c'>4 <b d'> <c' e'> <d' f'>", name="Music_Voice"
        ... )
        >>> string = "<g' b'>8 a' b' c'' d'' c'' b' a' b' c'' d''"
        >>> result = abjad.on_beat_grace_container(
        ...     string, music_voice[1:3], leaf_duration=(1, 30)
        ... )
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "Music_Voice"
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
                        \context Voice = "Music_Voice"
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

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
        >>> string = "g8 a b c' d' c' b a b c' d'"
        >>> result = abjad.on_beat_grace_container(
        ...     string,
        ...     music_voice[1:3],
        ...     anchor_voice_number=1,
        ...     grace_voice_number=2,
        ...     leaf_duration=(1, 30),
        ... )
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
                        \context Voice = "Music_Voice"
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

        >>> music_voice = abjad.Voice(
        ...     "<c' e'>4 <d' f'> <e' g'> <f' a'>", name="Music_Voice"
        ... )
        >>> string = "g8 a b c' d' c' b a b c' d'"
        >>> result = abjad.on_beat_grace_container(
        ...     string,
        ...     music_voice[1:3],
        ...     anchor_voice_number=1,
        ...     grace_voice_number=2,
        ...     leaf_duration=(1, 30),
        ... )
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "Music_Voice"
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
                        \context Voice = "Music_Voice"
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

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
        >>> string = "<e g>8 a b c' d' c' b a b c' d'"
        >>> result = abjad.on_beat_grace_container(
        ...     string,
        ...     music_voice[1:3],
        ...     anchor_voice_number=1,
        ...     grace_voice_number=2,
        ...     leaf_duration=(1, 30),
        ... )
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
                        \context Voice = "Music_Voice"
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

        >>> music_voice = abjad.Voice(
        ...     "<c' e'>4 <d' f'> <e' g'> <f' a'>", name="Music_Voice"
        ... )
        >>> string = "<e g>8 a b c' d' c' b a b c' d'"
        >>> result = abjad.on_beat_grace_container(
        ...     string,
        ...     music_voice[1:3],
        ...     anchor_voice_number=1,
        ...     grace_voice_number=2,
        ...     leaf_duration=(1, 30),
        ... )
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "Music_Voice"
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
                        \context Voice = "Music_Voice"
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

    ..  container:: example

        Raises exception when duration of on-beat grace container exceeds
        duration of anchor container:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
        >>> string = "g'8 a' b' c'' d'' c'' b' a' b' c'' d''"
        >>> result = abjad.on_beat_grace_container(
        ...     string, music_voice[1:2], leaf_duration=(1, 8)
        ... )
        Traceback (most recent call last):
            ...
        Exception: grace Duration(11, 8) exceeds anchor Duration(1, 4).

    """

    def _site(n):
        return Tag(f"abjad.on_beat_grace_container({n})")

    assert isinstance(anchor_voice_selection, Selection)
    if not anchor_voice_selection.are_contiguous_same_parent(
        ignore_before_after_grace=True
    ):
        message = "selection must be contiguous in same parent:\n"
        message += f"   {repr(anchor_voice_selection)}"
        raise Exception(message)
    on_beat_grace_container = OnBeatGraceContainer(
        contents, leaf_duration=leaf_duration
    )
    if not isinstance(anchor_voice_selection, Selection):
        raise Exception(f"must be selection:\n {repr(anchor_voice_selection)}")
    anchor_leaf = _iterate._get_leaf(anchor_voice_selection, 0)
    anchor_voice = Parentage(anchor_leaf).get(Voice)
    if anchor_voice.name is None:
        raise Exception(f"anchor voice must be named:\n   {repr(anchor_voice)}")
    anchor_voice_insert = Voice(name=anchor_voice.name)
    mutate.wrap(anchor_voice_selection, anchor_voice_insert)
    container = Container(simultaneous=True)
    mutate.wrap(anchor_voice_insert, container)
    container.insert(0, on_beat_grace_container)
    on_beat_grace_container._match_anchor_leaf()
    on_beat_grace_container._set_leaf_durations()
    insert_duration = anchor_voice_insert._get_duration()
    grace_container_duration = on_beat_grace_container._get_duration()
    if insert_duration < grace_container_duration:
        message = f"grace {repr(grace_container_duration)}"
        message += f" exceeds anchor {repr(insert_duration)}."
        raise Exception(message)
    if font_size is not None:
        string = rf"\set fontSize = #{font_size}"
        literal = LilyPondLiteral(string)
        attach(literal, on_beat_grace_container, tag=_site(1))
    if not do_not_beam:
        beam(on_beat_grace_container[:])
    if not do_not_slash:
        literal = LilyPondLiteral(r"\slash")
        attach(literal, on_beat_grace_container[0], tag=_site(2))
    if not do_not_slur:
        slur(on_beat_grace_container[:])
    voice_number_to_string = {
        1: r"\voiceOne",
        2: r"\voiceTwo",
        3: r"\voiceThree",
        4: r"\voiceFour",
    }
    first_grace = _iterate._get_leaf(on_beat_grace_container, 0)
    one_voice_literal = LilyPondLiteral(r"\oneVoice", format_slot="absolute_before")
    string = voice_number_to_string.get(grace_voice_number, None)
    if string is not None:
        literal
        detach(one_voice_literal, anchor_leaf)
        attach(LilyPondLiteral(string), first_grace, tag=_site(3))
    string = voice_number_to_string.get(anchor_voice_number, None)
    if string is not None:
        detach(one_voice_literal, anchor_leaf)
        attach(LilyPondLiteral(string), anchor_leaf, tag=_site(4))
    if not do_not_stop_polyphony:
        last_anchor_leaf = _iterate._get_leaf(anchor_voice_selection, -1)
        next_leaf = _iterate._get_leaf(last_anchor_leaf, 1)
        if next_leaf is not None:
            literal = LilyPondLiteral(r"\oneVoice", format_slot="absolute_before")
            attach(literal, next_leaf, tag=_site(5))
    return on_beat_grace_container
