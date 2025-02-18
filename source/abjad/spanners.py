"""
Classes and functions for modeling spanners: beams, hairpins, slurs, etc.
"""

import typing

from . import _iterlib
from . import bind as _bind
from . import duration as _duration
from . import enums as _enums
from . import indicators as _indicators
from . import iterate as _iterate
from . import parentage as _parentage
from . import score as _score
from . import select as _select
from . import sequence as _sequence
from . import tag as _tag
from . import tweaks as _tweaks


def _apply_tweaks(argument, tweaks, i=None, total=None):
    if not tweaks:
        return argument
    if i is not None:
        assert isinstance(i, int), repr(i)
    if total is not None:
        assert isinstance(total, int), repr(total)
    tweak_objects = []
    for item in tweaks:
        if isinstance(item, _tweaks.Tweak) and item.i is not None:
            item, index = item, item.i
            if 0 <= index and index != i:
                continue
            if index < 0 and index != -(total - i):
                continue
        elif isinstance(item, tuple):
            raise Exception(f"use abjad.Tweak.i instead of tuple: {item}")
        assert isinstance(item, _tweaks.Tweak), repr(item)
        tweak_objects.append(item)
    bundle = _tweaks.bundle(argument, *tweak_objects)
    return bundle


def beam(
    argument: _score.Component | typing.Sequence[_score.Component],
    *,
    beam_lone_notes: bool = False,
    beam_rests: bool | None = True,
    direction: _enums.Vertical | None = None,
    durations: typing.Sequence[_duration.Duration] | None = None,
    span_beam_count: int | None = None,
    start_beam: _indicators.StartBeam | _tweaks.Bundle | None = None,
    stemlet_length: int | float | None = None,
    stop_beam: _indicators.StopBeam | None = None,
    tag: _tag.Tag | None = None,
) -> None:
    r"""
    Attaches beam indicators.

    ..  container:: example

        >>> voice = abjad.Voice("c'8 d' e' f'")
        >>> abjad.beam(voice[:], direction=abjad.UP)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'8
                ^ [
                d'8
                e'8
                f'8
                ]
            }

        Does not beam rests:

        >>> voice = abjad.Voice("c'8 r e' f'")
        >>> abjad.beam(voice[:], beam_rests=False)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'8
                r8
                e'8
                [
                f'8
                ]
            }

        Does beam rests:

        >>> voice = abjad.Voice("c'8 r e' f'")
        >>> abjad.beam(voice[:], beam_rests=True)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'8
                [
                r8
                e'8
                f'8
                ]
            }

        Beams rests and sets stemlet length:

        >>> voice = abjad.Voice("c'8 r e' f'")
        >>> abjad.beam(voice[:], beam_rests=True, stemlet_length=1)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \override Staff.Stem.stemlet-length = 1
                c'8
                [
                r8
                e'8
                f'8
                ]
                \revert Staff.Stem.stemlet-length
            }

    """
    original_leaves = list(_iterate.leaves(argument))
    silent_prototype = (_score.MultimeasureRest, _score.Rest, _score.Skip)

    def _is_beamable(argument, beam_rests=False):
        if isinstance(argument, _score.Chord | _score.Note):
            if 0 < argument.written_duration.flag_count:
                return True
        if beam_rests and isinstance(argument, silent_prototype):
            return True
        return False

    leaves = []
    for leaf in original_leaves:
        if not _is_beamable(leaf, beam_rests=beam_rests):
            continue
        leaves.append(leaf)
    runs = []
    run = []
    run.extend(leaves[:1])
    for leaf in leaves[1:]:
        this_index = original_leaves.index(run[-1])
        that_index = original_leaves.index(leaf)
        if this_index + 1 == that_index:
            run.append(leaf)
        else:
            runs.append(run)
            run = [leaf]
    if run:
        runs.append(run)
    runs_ = runs
    if not beam_lone_notes:
        result = _select.nontrivial(runs)
        runs_ = result
    for run in runs_:
        if all(isinstance(_, silent_prototype) for _ in run):
            continue
        start_leaf = run[0]
        stop_leaf = run[-1]
        start_beam_ = start_beam or _indicators.StartBeam()
        stop_beam_ = stop_beam or _indicators.StopBeam()
        _bind.detach(_indicators.StartBeam, start_leaf)
        _bind.attach(start_beam_, start_leaf, direction=direction, tag=tag)
        _bind.detach(_indicators.StopBeam, stop_leaf)
        _bind.attach(stop_beam_, stop_leaf, tag=tag)
        if stemlet_length is None:
            continue
        staff = _parentage.Parentage(start_leaf).get(_score.Staff)
        lilypond_type = getattr(staff, "lilypond_type", "Staff")
        string = rf"\override {lilypond_type}.Stem.stemlet-length = {stemlet_length}"
        literal = _indicators.LilyPondLiteral(string, site="before")
        for indicator in start_leaf._get_indicators():
            if indicator == literal:
                break
        else:
            _bind.attach(literal, start_leaf, tag=tag)
        staff = _parentage.Parentage(stop_leaf).get(_score.Staff)
        lilypond_type = getattr(staff, "lilypond_type", "Staff")
        string = rf"\revert {lilypond_type}.Stem.stemlet-length"
        literal = _indicators.LilyPondLiteral(string, site="after")
        for indicator in stop_leaf._get_indicators():
            if indicator == literal:
                break
        else:
            _bind.attach(literal, stop_leaf, tag=tag)
    if not durations:
        return
    if len(original_leaves) == 1:
        return

    def _leaf_neighbors(leaf, original_leaves):
        assert leaf is not original_leaves[0]
        assert leaf is not original_leaves[-1]
        this_index = original_leaves.index(leaf)
        previous_leaf = original_leaves[this_index - 1]
        previous = 0
        if _is_beamable(previous_leaf, beam_rests=beam_rests):
            previous = previous_leaf.written_duration.flag_count
        next_leaf = original_leaves[this_index + 1]
        next_ = 0
        if _is_beamable(next_leaf, beam_rests=beam_rests):
            next_ = next_leaf.written_duration.flag_count
        return previous, next_

    span_beam_count = span_beam_count or 1
    durations = [_duration.Duration(_) for _ in durations]
    leaf_durations = [_._get_duration() for _ in original_leaves]
    parts = _sequence.partition_by_weights(leaf_durations, durations, overhang=True)
    part_counts = [len(_) for _ in parts]
    parts = _sequence.partition_by_counts(original_leaves, part_counts)
    total_parts = len(parts)
    for i, part in enumerate(parts):
        is_first_part = False
        if i == 0:
            is_first_part = True
        is_last_part = False
        if i == total_parts - 1:
            is_last_part = True
        first_leaf = part[0]
        flag_count = first_leaf.written_duration.flag_count
        if len(part) == 1:
            if not _is_beamable(first_leaf, beam_rests=False):
                continue
            left = flag_count
            right = flag_count
            beam_count = _indicators.BeamCount(left, right)
            _bind.attach(beam_count, first_leaf, tag=tag)
            continue
        if _is_beamable(first_leaf, beam_rests=False):
            if is_first_part:
                left = 0
            else:
                left = span_beam_count
            beam_count = _indicators.BeamCount(left, flag_count)
            _bind.attach(beam_count, first_leaf, tag=tag)
        last_leaf = part[-1]
        if _is_beamable(last_leaf, beam_rests=False):
            flag_count = last_leaf.written_duration.flag_count
            if is_last_part:
                left = flag_count
                right = 0
            else:
                previous, next_ = _leaf_neighbors(last_leaf, original_leaves)
                if previous == next_ == 0:
                    left = right = flag_count
                elif previous == 0:
                    left = 0
                    right = flag_count
                elif next_ == 0:
                    left = flag_count
                    right = 0
                elif previous == flag_count:
                    left = flag_count
                    right = min(span_beam_count, next_)
                elif flag_count == next_:
                    left = min(previous, flag_count)
                    right = flag_count
                else:
                    left = flag_count
                    right = min(previous, flag_count)
            beam_count = _indicators.BeamCount(left, right)
            _bind.attach(beam_count, last_leaf, tag=tag)
        # TODO: eventually remove middle leaf beam counts?
        for middle_leaf in part[1:-1]:
            if not _is_beamable(middle_leaf, beam_rests=beam_rests):
                continue
            if isinstance(middle_leaf, silent_prototype):
                continue
            flag_count = middle_leaf.written_duration.flag_count
            previous, next_ = _leaf_neighbors(middle_leaf, original_leaves)
            if previous == next_ == 0:
                left = right = flag_count
            elif previous == 0:
                left = 0
                right = flag_count
            elif next_ == 0:
                left = flag_count
                right = 0
            elif previous == flag_count:
                left = flag_count
                right = min(flag_count, next_)
            elif flag_count == next_:
                left = min(previous, flag_count)
                right = flag_count
            else:
                left = min(previous, flag_count)
                right = flag_count
            beam_count = _indicators.BeamCount(left, right)
            _bind.attach(beam_count, middle_leaf, tag=tag)


def glissando(
    argument,
    *tweaks,
    allow_repeats: bool = False,
    allow_ties: bool = False,
    hide_middle_note_heads: bool = False,
    hide_middle_stems: bool = False,
    left_broken: bool = False,
    parenthesize_repeats: bool = False,
    right_broken: bool = False,
    right_broken_show_next: bool = False,
    tag: _tag.Tag | None = None,
    zero_padding: bool = False,
):
    r"""
    Attaches glissando indicators.

    ..  container:: example

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8", name="Voice")
        >>> staff = abjad.Staff([voice], name="Staff")
        >>> abjad.glissando(voice[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    c'8
                    \glissando
                    d'8
                    \glissando
                    e'8
                    \glissando
                    f'8
                }
            }

    ..  container:: example

        Glissando avoids bend-after indicators:

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8", name="Voice")
        >>> staff = abjad.Staff([voice], name="Staff")
        >>> bend_after = abjad.BendAfter()
        >>> abjad.attach(bend_after, voice[1])
        >>> abjad.glissando(voice[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    c'8
                    \glissando
                    d'8
                    - \bendAfter #'-4
                    e'8
                    \glissando
                    f'8
                }
            }

    ..  container:: example

        Does not allow repeated pitches:

        >>> voice = abjad.Voice("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8", name="Voice")
        >>> staff = abjad.Staff([voice], name="Staff")
        >>> abjad.glissando(voice[:], allow_repeats=True)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    a8
                    \glissando
                    a8
                    \glissando
                    b8
                    ~
                    b8
                    \glissando
                    c'8
                    \glissando
                    c'8
                    \glissando
                    d'8
                    ~
                    d'8
                }
            }

    ..  container:: example

        Allows repeated pitches (but not ties):

        >>> voice = abjad.Voice("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8", name="Voice")
        >>> staff = abjad.Staff([voice], name="Staff")
        >>> abjad.glissando(voice[:], allow_repeats=True)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    a8
                    \glissando
                    a8
                    \glissando
                    b8
                    ~
                    b8
                    \glissando
                    c'8
                    \glissando
                    c'8
                    \glissando
                    d'8
                    ~
                    d'8
                }
            }

    ..  container:: example

        Allows both repeated pitches and ties:

        >>> voice = abjad.Voice("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8", name="Voice")
        >>> staff = abjad.Staff([voice], name="Staff")
        >>> abjad.glissando(
        ...     voice[:],
        ...     allow_repeats=True,
        ...     allow_ties=True,
        ... )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    a8
                    \glissando
                    a8
                    \glissando
                    b8
                    \glissando
                    ~
                    b8
                    \glissando
                    c'8
                    \glissando
                    c'8
                    \glissando
                    d'8
                    \glissando
                    ~
                    d'8
                }
            }

        Ties are excluded when repeated pitches are not allowed because all ties
        comprise repeated pitches.

    ..  container:: example

        Spans and parenthesizes repeated pitches:

        >>> voice = abjad.Voice("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8", name="Voice")
        >>> staff = abjad.Staff([voice], name="Staff")
        >>> abjad.glissando(
        ...     voice[:],
        ...     allow_repeats=True,
        ...     parenthesize_repeats=True,
        ... )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    a8
                    \glissando
                    \parenthesize
                    a8
                    \glissando
                    b8
                    ~
                    \parenthesize
                    b8
                    \glissando
                    c'8
                    \glissando
                    \parenthesize
                    c'8
                    \glissando
                    d'8
                    ~
                    \parenthesize
                    d'8
                }
            }

    ..  container:: example

        Parenthesizes (but does not span) repeated pitches:

        >>> voice = abjad.Voice("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8", name="Voice")
        >>> staff = abjad.Staff([voice], name="Staff")
        >>> abjad.glissando(
        ...     voice[:],
        ...     parenthesize_repeats=True,
        ... )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    a8
                    \parenthesize
                    a8
                    \glissando
                    b8
                    ~
                    \parenthesize
                    b8
                    \glissando
                    c'8
                    \parenthesize
                    c'8
                    \glissando
                    d'8
                    ~
                    \parenthesize
                    d'8
                }
            }

    ..  container:: example

        With ``hide_middle_note_heads=True``:

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8", name="Voice")
        >>> staff = abjad.Staff([voice], name="Staff")
        >>> abjad.glissando(voice[:], hide_middle_note_heads=True)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    c'8
                    \glissando
                    \hide NoteHead
                    \override Accidental.stencil = ##f
                    \override NoteColumn.glissando-skip = ##t
                    \override NoteHead.no-ledgers = ##t
                    d'8
                    e'8
                    \revert Accidental.stencil
                    \revert NoteColumn.glissando-skip
                    \revert NoteHead.no-ledgers
                    \undo \hide NoteHead
                    f'8
                }
            }

    ..  container:: example

        With ``hide_middle_note_heads=True`` and ``hide_middle_stems=True``:

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8", name="Voice")
        >>> abjad.glissando(
        ...     voice[:],
        ...     hide_middle_note_heads=True,
        ...     hide_middle_stems=True,
        ... )
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                c'8
                \glissando
                \hide NoteHead
                \override Accidental.stencil = ##f
                \override NoteColumn.glissando-skip = ##t
                \override NoteHead.no-ledgers = ##t
                \override Dots.transparent = ##t
                \override Stem.transparent = ##t
                d'8
                e'8
                \revert Accidental.stencil
                \revert NoteColumn.glissando-skip
                \revert NoteHead.no-ledgers
                \undo \hide NoteHead
                \revert Dots.transparent
                \revert Stem.transparent
                f'8
            }

        ..  note:: Respects ``hide_middle_stems`` only when
            ``hide_middle_note_heads=True``.

    ..  container:: example

        With ``right_broken=True``:

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8", name="Voice")
        >>> abjad.glissando(voice[:], right_broken=True)
        >>> abjad.show(voice) # doctest: +SKIP

        LilyPond output looks like this:

        >>> string = abjad.lilypond(voice, tags=True)
        >>> print(string)
        \context Voice = "Voice"
        {
            c'8
            %! abjad.glissando(7)
            \glissando
            d'8
            %! abjad.glissando(7)
            \glissando
            e'8
            %! abjad.glissando(7)
            \glissando
            f'8
            %! SHOW_TO_JOIN_BROKEN_SPANNERS
            %! abjad.glissando(7)
            %@% \glissando
        }

    ..  container:: example

        With ``right_broken=True`` and ``hide_middle_note_heads=True``:

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8", name="Voice")
        >>> abjad.glissando(
        ...     voice[:],
        ...     right_broken=True,
        ...     hide_middle_note_heads=True,
        ... )
        >>> abjad.show(voice) # doctest: +SKIP

        LilyPond output looks like this:

        >>> string = abjad.lilypond(voice, tags=True)
        >>> print(string)
        \context Voice = "Voice"
        {
            c'8
            %! abjad.glissando(7)
            \glissando
            %! RIGHT_BROKEN
            %! SHOW_TO_JOIN_BROKEN_SPANNERS
            %! abjad.glissando(0)
            \hide NoteHead
            %! RIGHT_BROKEN
            %! SHOW_TO_JOIN_BROKEN_SPANNERS
            %! abjad.glissando(0)
            \override Accidental.stencil = ##f
            %! RIGHT_BROKEN
            %! SHOW_TO_JOIN_BROKEN_SPANNERS
            %! abjad.glissando(0)
            \override NoteColumn.glissando-skip = ##t
            %! RIGHT_BROKEN
            %! SHOW_TO_JOIN_BROKEN_SPANNERS
            %! abjad.glissando(0)
            \override NoteHead.no-ledgers = ##t
            d'8
            e'8
            %! HIDE_TO_JOIN_BROKEN_SPANNERS
            %! RIGHT_BROKEN
            %! abjad.glissando(4)
            \revert Accidental.stencil
            %! HIDE_TO_JOIN_BROKEN_SPANNERS
            %! RIGHT_BROKEN
            %! abjad.glissando(4)
            \revert NoteColumn.glissando-skip
            %! HIDE_TO_JOIN_BROKEN_SPANNERS
            %! RIGHT_BROKEN
            %! abjad.glissando(4)
            \revert NoteHead.no-ledgers
            %! HIDE_TO_JOIN_BROKEN_SPANNERS
            %! RIGHT_BROKEN
            %! abjad.glissando(4)
            \undo \hide NoteHead
            f'8
        }

    ..  container:: example

        With ``right_broken=True``, ``hide_middle_note_heads=True`` and
        ``right_broken_show_next=True``:

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8", name="Voice")
        >>> abjad.glissando(
        ...     voice[:],
        ...     hide_middle_note_heads=True,
        ...     right_broken=True,
        ...     right_broken_show_next=True,
        ... )
        >>> abjad.show(voice) # doctest: +SKIP

        LilyPond output looks like this:

        >>> string = abjad.lilypond(voice, tags=True)
        >>> print(string)
        \context Voice = "Voice"
        {
            c'8
            %! abjad.glissando(7)
            \glissando
            %! RIGHT_BROKEN
            %! SHOW_TO_JOIN_BROKEN_SPANNERS
            %! abjad.glissando(0)
            \hide NoteHead
            %! RIGHT_BROKEN
            %! SHOW_TO_JOIN_BROKEN_SPANNERS
            %! abjad.glissando(0)
            \override Accidental.stencil = ##f
            %! RIGHT_BROKEN
            %! SHOW_TO_JOIN_BROKEN_SPANNERS
            %! abjad.glissando(0)
            \override NoteColumn.glissando-skip = ##t
            %! RIGHT_BROKEN
            %! SHOW_TO_JOIN_BROKEN_SPANNERS
            %! abjad.glissando(0)
            \override NoteHead.no-ledgers = ##t
            d'8
            e'8
            %! HIDE_TO_JOIN_BROKEN_SPANNERS
            %! RIGHT_BROKEN
            %! abjad.glissando(4)
            \revert Accidental.stencil
            %! HIDE_TO_JOIN_BROKEN_SPANNERS
            %! RIGHT_BROKEN
            %! abjad.glissando(4)
            \revert NoteColumn.glissando-skip
            %! HIDE_TO_JOIN_BROKEN_SPANNERS
            %! RIGHT_BROKEN
            %! abjad.glissando(4)
            \revert NoteHead.no-ledgers
            %! HIDE_TO_JOIN_BROKEN_SPANNERS
            %! RIGHT_BROKEN
            %! abjad.glissando(4)
            \undo \hide NoteHead
            f'8
            %! RIGHT_BROKEN_SHOW_NEXT
            %! SHOW_TO_JOIN_BROKEN_SPANNERS
            %! abjad.glissando(5)
            %@% \revert Accidental.stencil
            %! RIGHT_BROKEN_SHOW_NEXT
            %! SHOW_TO_JOIN_BROKEN_SPANNERS
            %! abjad.glissando(5)
            %@% \revert NoteColumn.glissando-skip
            %! RIGHT_BROKEN_SHOW_NEXT
            %! SHOW_TO_JOIN_BROKEN_SPANNERS
            %! abjad.glissando(5)
            %@% \revert NoteHead.no-ledgers
            %! RIGHT_BROKEN_SHOW_NEXT
            %! SHOW_TO_JOIN_BROKEN_SPANNERS
            %! abjad.glissando(5)
            %@% \undo \hide NoteHead
        }

    ..  container:: example

        With ``left_broken=True`` (and ``hide_middle_note_heads=True``):

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8", name="Voice")
        >>> abjad.glissando(
        ...     voice[:],
        ...     left_broken=True,
        ...     hide_middle_note_heads=True,
        ... )
        >>> abjad.show(voice) # doctest: +SKIP

        LilyPond output looks like this:

        >>> string = abjad.lilypond(voice, tags=True)
        >>> print(string)
        \context Voice = "Voice"
        {
            %! HIDE_TO_JOIN_BROKEN_SPANNERS
            %! LEFT_BROKEN
            %! abjad.glissando(2)
            \hide NoteHead
            %! HIDE_TO_JOIN_BROKEN_SPANNERS
            %! LEFT_BROKEN
            %! abjad.glissando(2)
            \override Accidental.stencil = ##f
            %! HIDE_TO_JOIN_BROKEN_SPANNERS
            %! LEFT_BROKEN
            %! abjad.glissando(2)
            \override NoteHead.no-ledgers = ##t
            c'8
            %! abjad.glissando(7)
            \glissando
            %! HIDE_TO_JOIN_BROKEN_SPANNERS
            %! LEFT_BROKEN
            %! abjad.glissando(3)
            \override NoteColumn.glissando-skip = ##t
            d'8
            e'8
            %! abjad.glissando(6)
            \revert Accidental.stencil
            %! abjad.glissando(6)
            \revert NoteColumn.glissando-skip
            %! abjad.glissando(6)
            \revert NoteHead.no-ledgers
            %! abjad.glissando(6)
            \undo \hide NoteHead
            f'8
        }

        ..  note:: Respects left-broken only with ``hide_middle_note_heads=True``.

    ..  container:: example

        Tweaks apply to every glissando:

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8", name="Voice")
        >>> abjad.glissando(
        ...     voice[:],
        ...     abjad.Tweak(r"- \tweak style #'trill"),
        ... )
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                c'8
                - \tweak style #'trill
                \glissando
                d'8
                - \tweak style #'trill
                \glissando
                e'8
                - \tweak style #'trill
                \glissando
                f'8
            }

    ..  container:: example

        With ``zero_padding=True`` on fixed pitch:

        >>> voice = abjad.Voice("d'8 d'4. d'4. d'8", name="Voice")

        >>> abjad.glissando(
        ...     voice[:],
        ...     allow_repeats=True,
        ...     zero_padding=True,
        ... )
        >>> for note in voice[1:]:
        ...     abjad.override(note).NoteHead.transparent = True
        ...     abjad.override(note).NoteHead.X_extent = "#'(0 . 0)"
        ...
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', voice])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                d'8
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'4.
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'4.
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'8
            }

    ..  container:: example

        With ``zero_padding=True`` on changing pitches:

        >>> voice = abjad.Voice("c'8. d'8. e'8. f'8.", name="Voice")
        >>> abjad.glissando(voice[:], zero_padding=True)
        >>> for note in voice[1:-1]:
        ...     abjad.override(note).NoteHead.transparent = True
        ...     abjad.override(note).NoteHead.X_extent = "#'(0 . 0)"
        ...
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', voice])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                c'8.
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'8.
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                e'8.
                - \abjad-zero-padding-glissando
                \glissando
                f'8.
            }

    ..  container:: example

        With indexed tweaks:

        >>> voice = abjad.Voice("d'4 d' d' d'", name="Voice")
        >>> abjad.glissando(
        ...     voice[:],
        ...     abjad.Tweak(r"- \tweak color #red", i=0),
        ...     abjad.Tweak(r"- \tweak color #red", i=-1),
        ...     allow_repeats=True,
        ...     zero_padding=True,
        ... )
        >>> for note in voice[1:-1]:
        ...     abjad.override(note).NoteHead.transparent = True
        ...     abjad.override(note).NoteHead.X_extent = "#'(0 . 0)"
        ...
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', voice])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                d'4
                - \abjad-zero-padding-glissando
                - \tweak color #red
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'4
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'4
                - \abjad-zero-padding-glissando
                - \tweak color #red
                \glissando
                d'4
            }

    """
    tag = tag or _tag.Tag()

    if right_broken_show_next and not right_broken:
        raise Exception("set right_broken_show_next only when right_broken is true.")

    if hide_middle_stems and not hide_middle_note_heads:
        message = "set hide_middle_stems only when"
        message += " hide_middle_note_heads is true."
        raise Exception(message)

    def _is_last_in_tie_chain(leaf):
        logical_tie = _iterlib._get_logical_tie_leaves(leaf)
        return leaf is logical_tie[-1]

    def _next_leaf_changes_current_pitch(leaf):
        next_leaf = _iterlib._get_leaf(leaf, 1)
        if (
            isinstance(leaf, _score.Note)
            and isinstance(next_leaf, _score.Note)
            and leaf.written_pitch == next_leaf.written_pitch
        ):
            return False
        elif (
            isinstance(leaf, _score.Chord)
            and isinstance(next_leaf, _score.Chord)
            and leaf.written_pitches == next_leaf.written_pitches
        ):
            return False
        return True

    def _parenthesize_leaf(leaf):
        if isinstance(leaf, _score.Note):
            leaf.note_head.is_parenthesized = True
        elif isinstance(leaf, _score.Chord):
            for note_head in leaf.note_heads:
                note_head.is_parenthesized = True

    def _previous_leaf_changes_current_pitch(leaf):
        previous_leaf = _iterlib._get_leaf(leaf, -1)
        if (
            isinstance(leaf, _score.Note)
            and isinstance(previous_leaf, _score.Note)
            and leaf.written_pitch == previous_leaf.written_pitch
        ):
            return False
        elif (
            isinstance(leaf, _score.Chord)
            and isinstance(previous_leaf, _score.Chord)
            and leaf.written_pitches == previous_leaf.written_pitches
        ):
            return False
        return True

    leaves = _select.leaves(argument)
    total = len(leaves) - 1
    for i, leaf in enumerate(leaves):
        if leaf is not leaves[0]:
            if parenthesize_repeats:
                if not _previous_leaf_changes_current_pitch(leaf):
                    _parenthesize_leaf(leaf)
        should_attach_glissando = False
        deactivate_glissando = False
        if leaf._has_indicator(_indicators.BendAfter):
            pass
        elif leaf is leaves[-1]:
            if right_broken is True:
                should_attach_glissando = True
                deactivate_glissando = True
        elif not isinstance(leaf, _score.Chord | _score.Note):
            pass
        elif allow_repeats and allow_ties:
            should_attach_glissando = True
        elif allow_repeats and not allow_ties:
            should_attach_glissando = _is_last_in_tie_chain(leaf)
        elif not allow_repeats and allow_ties:
            if _next_leaf_changes_current_pitch(leaf):
                should_attach_glissando = True
        elif not allow_repeats and not allow_ties:
            if _next_leaf_changes_current_pitch(leaf):
                if _is_last_in_tie_chain(leaf):
                    should_attach_glissando = True
        if hide_middle_note_heads and 3 <= len(leaves):
            if leaf is not leaves[0]:
                should_attach_glissando = False
            if not left_broken and leaf is leaves[1]:
                strings = [
                    r"\hide NoteHead",
                    r"\override Accidental.stencil = ##f",
                    r"\override NoteColumn.glissando-skip = ##t",
                    r"\override NoteHead.no-ledgers = ##t",
                ]
                if hide_middle_stems:
                    strings.extend(
                        [
                            r"\override Dots.transparent = ##t",
                            r"\override Stem.transparent = ##t",
                        ]
                    )
                literal = _indicators.LilyPondLiteral(strings, site="before")
                if right_broken is True:
                    _bind.attach(
                        literal,
                        leaf,
                        tag=tag.append(_tag.Tag("abjad.glissando(0)"))
                        .append(_tag.Tag("SHOW_TO_JOIN_BROKEN_SPANNERS"))
                        .append(_tag.Tag("RIGHT_BROKEN")),
                    )
                else:
                    _bind.attach(
                        literal,
                        leaf,
                        tag=tag.append(_tag.Tag("abjad.glissando(1)")),
                    )
            elif left_broken and leaf is leaves[0]:
                strings = [
                    r"\hide NoteHead",
                    r"\override Accidental.stencil = ##f",
                    r"\override NoteHead.no-ledgers = ##t",
                ]
                if hide_middle_stems:
                    strings.extend(
                        [
                            r"\override Dots.transparent = ##t",
                            r"\override Stem.transparent = ##t",
                        ]
                    )
                literal = _indicators.LilyPondLiteral(strings, site="before")
                _bind.attach(
                    literal,
                    leaf,
                    tag=tag.append(_tag.Tag("abjad.glissando(2)"))
                    .append(_tag.Tag("HIDE_TO_JOIN_BROKEN_SPANNERS"))
                    .append(_tag.Tag("LEFT_BROKEN")),
                )
            elif left_broken and leaf is leaves[1]:
                string = r"\override NoteColumn.glissando-skip = ##t"
                literal = _indicators.LilyPondLiteral(string, site="before")
                _bind.attach(
                    literal,
                    leaf,
                    tag=tag.append(_tag.Tag("abjad.glissando(3)"))
                    .append(_tag.Tag("HIDE_TO_JOIN_BROKEN_SPANNERS"))
                    .append(_tag.Tag("LEFT_BROKEN")),
                )
            if leaf is leaves[-1]:
                strings = [
                    r"\revert Accidental.stencil",
                    r"\revert NoteColumn.glissando-skip",
                    r"\revert NoteHead.no-ledgers",
                    r"\undo \hide NoteHead",
                ]
                if hide_middle_stems:
                    strings.extend(
                        [r"\revert Dots.transparent", r"\revert Stem.transparent"]
                    )
                if right_broken:
                    deactivate_glissando = True
                    literal = _indicators.LilyPondLiteral(strings, site="before")
                    _bind.attach(
                        literal,
                        leaf,
                        deactivate=False,
                        tag=tag.append(_tag.Tag("abjad.glissando(4)"))
                        .append(_tag.Tag("HIDE_TO_JOIN_BROKEN_SPANNERS"))
                        .append(_tag.Tag("RIGHT_BROKEN")),
                    )
                    if right_broken_show_next:
                        literal = _indicators.LilyPondLiteral(strings, site="after")
                        _bind.attach(
                            literal,
                            leaf,
                            deactivate=True,
                            tag=tag.append(_tag.Tag("abjad.glissando(5)"))
                            .append(_tag.Tag("SHOW_TO_JOIN_BROKEN_SPANNERS"))
                            .append(_tag.Tag("RIGHT_BROKEN_SHOW_NEXT")),
                        )
                else:
                    literal = _indicators.LilyPondLiteral(strings, site="before")
                    _bind.attach(
                        literal,
                        leaf,
                        tag=tag.append(_tag.Tag("abjad.glissando(6)")),
                    )
        if should_attach_glissando:
            glissando = _indicators.Glissando(zero_padding=zero_padding)
            glissando = _apply_tweaks(glissando, tweaks, i=i, total=total)
            tag_ = tag.append(_tag.Tag("abjad.glissando(7)"))
            if deactivate_glissando:
                tag_ = tag_.append(_tag.Tag("SHOW_TO_JOIN_BROKEN_SPANNERS"))
            _bind.attach(glissando, leaf, deactivate=deactivate_glissando, tag=tag_)


def hairpin(
    descriptor: str,
    argument: _score.Component | typing.Sequence[_score.Component],
    *,
    direction: _enums.Vertical | None = None,
    tag: _tag.Tag | None = None,
) -> None:
    r"""
    Attaches hairpin indicators.

    ..  container:: example

        With three-part string descriptor:

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> abjad.hairpin("p < f", voice[:], direction=abjad.UP)
        >>> abjad.override(voice[0]).DynamicLineSpanner.staff_padding = 4
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \once \override DynamicLineSpanner.staff-padding = 4
                c'4
                ^ \p
                ^ \<
                d'4
                e'4
                f'4
                \f
            }

    ..  container:: example

        With two-part string descriptor:

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> abjad.hairpin("< !", voice[:])
        >>> abjad.override(voice[0]).DynamicLineSpanner.staff_padding = 4
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \once \override DynamicLineSpanner.staff-padding = 4
                c'4
                \<
                d'4
                e'4
                f'4
                \!
            }

    ..  container:: example

        With dynamic objects:

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> start_hairpin = abjad.StartHairpin("o<|")
        >>> bundle = abjad.bundle(start_hairpin, r"- \tweak color #blue")
        >>> stop_dynamic = abjad.Dynamic('"f"')
        >>> abjad.hairpin([bundle, stop_dynamic], voice[:])
        >>> abjad.override(voice[0]).DynamicLineSpanner.staff_padding = 4
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', voice])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \once \override DynamicLineSpanner.staff-padding = 4
                c'4
                - \tweak circled-tip ##t
                - \tweak stencil #abjad-flared-hairpin
                - \tweak color #blue
                \<
                d'4
                e'4
                f'4
                _ #(make-dynamic-script
                    (markup
                        #:whiteout
                        #:line (
                            #:general-align Y -2 #:normal-text #:larger "“"
                            #:hspace -0.4
                            #:dynamic "f"
                            #:hspace -0.2
                            #:general-align Y -2 #:normal-text #:larger "”"
                            )
                        )
                    )
            }

    """
    indicators: list = []
    start_dynamic: _indicators.Dynamic | None
    hairpin: _indicators.StartHairpin | None
    stop_dynamic: _indicators.Dynamic | None
    known_shapes = _indicators.StartHairpin("<").known_shapes
    if isinstance(descriptor, str):
        for string in descriptor.split():
            if string in known_shapes:
                hairpin = _indicators.StartHairpin(string)
                indicators.append(hairpin)
            elif string == "!":
                stop_hairpin = _indicators.StopHairpin()
                indicators.append(stop_hairpin)
            else:
                dynamic = _indicators.Dynamic(string)
                indicators.append(dynamic)
    else:
        assert isinstance(descriptor, list), repr(descriptor)
        indicators = descriptor

    start_dynamic, hairpin, stop_dynamic = None, None, None
    if len(indicators) == 1:
        if isinstance(indicators[0], _indicators.Dynamic):
            start_dynamic = indicators[0]
        else:
            hairpin = indicators[0]
    elif len(indicators) == 2:
        if isinstance(indicators[0], _indicators.Dynamic):
            start_dynamic = indicators[0]
            hairpin = indicators[1]
        else:
            hairpin = indicators[0]
            stop_dynamic = indicators[1]
    elif len(indicators) == 3:
        start_dynamic, hairpin, stop_dynamic = indicators
    else:
        raise Exception(indicators)

    if start_dynamic is not None:
        assert isinstance(start_dynamic, _indicators.Dynamic), repr(start_dynamic)

    leaves = _select.leaves(argument)
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]

    if start_dynamic is not None:
        _bind.attach(start_dynamic, start_leaf, direction=direction, tag=tag)
    if hairpin is not None:
        _bind.attach(hairpin, start_leaf, direction=direction, tag=tag)
    if stop_dynamic is not None:
        _bind.attach(stop_dynamic, stop_leaf, tag=tag)


def horizontal_bracket(
    argument: _score.Component | typing.Sequence[_score.Component],
    *,
    start_group: _indicators.StartGroup | _tweaks.Bundle | None = None,
    stop_group: _indicators.StopGroup | None = None,
    tag: _tag.Tag | None = None,
) -> None:
    r"""
    Attaches group indicators.

    ..  container:: example

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> voice.consists_commands.append("Horizontal_bracket_engraver")
        >>> abjad.horizontal_bracket(voice[:])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            \with
            {
                \consists Horizontal_bracket_engraver
            }
            {
                c'4
                \startGroup
                d'4
                e'4
                f'4
                \stopGroup
            }

    ..  container:: example

        Bundle start-group indicators to tweak the padding and outside-staff priority
        of nested analysis brackets:

        >>> voice = abjad.Voice("c'4 d' e' f' c' d' e' f'")
        >>> voice.consists_commands.append("Horizontal_bracket_engraver")
        >>> bundle = abjad.bundle(
        ...     abjad.StartGroup(),
        ...     r"- \tweak color #red",
        ...     r"- \tweak padding 1.5",
        ...     comment="% lexical order 1"
        ... )
        >>> abjad.horizontal_bracket(voice[:4], start_group=bundle)
        >>> bundle = abjad.bundle(
        ...     abjad.StartGroup(),
        ...     r"- \tweak color #red",
        ...     r"- \tweak padding 1.5",
        ...     comment="% lexical order 1"
        ... )
        >>> abjad.horizontal_bracket(voice[4:], start_group=bundle)
        >>> bundle = abjad.bundle(
        ...     abjad.StartGroup(),
        ...     r"- \tweak color #blue",
        ...     r"- \tweak outside-staff-priority 801",
        ...     r"- \tweak padding 1.5",
        ...     comment="% lexical order 0"
        ... )
        >>> abjad.horizontal_bracket(voice[:], start_group=bundle)

        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            \with
            {
                \consists Horizontal_bracket_engraver
            }
            {
                c'4
                % lexical order 0
                - \tweak color #blue
                - \tweak outside-staff-priority 801
                - \tweak padding 1.5
                \startGroup
                % lexical order 1
                - \tweak color #red
                - \tweak padding 1.5
                \startGroup
                d'4
                e'4
                f'4
                \stopGroup
                c'4
                % lexical order 1
                - \tweak color #red
                - \tweak padding 1.5
                \startGroup
                d'4
                e'4
                f'4
                \stopGroup
                \stopGroup
            }

    """
    start_group = start_group or _indicators.StartGroup()
    stop_group = stop_group or _indicators.StopGroup()
    leaves = _select.leaves(argument)
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    _bind.attach(start_group, start_leaf, tag=tag)
    _bind.attach(stop_group, stop_leaf, tag=tag)


def ottava(
    argument: _score.Component | typing.Sequence[_score.Component],
    *,
    start_ottava: _indicators.Ottava = _indicators.Ottava(n=1),
    stop_ottava: _indicators.Ottava = _indicators.Ottava(n=0, site="after"),
    tag: _tag.Tag | None = None,
) -> None:
    r"""
    Attaches ottava indicators.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.ottava(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \ottava 1
                c'4
                d'4
                e'4
                f'4
                \ottava 0
            }

    """
    assert isinstance(start_ottava, _indicators.Ottava), repr(start_ottava)
    assert isinstance(stop_ottava, _indicators.Ottava), repr(stop_ottava)
    leaves = _select.leaves(argument)
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    _bind.attach(start_ottava, start_leaf, tag=tag)
    _bind.attach(stop_ottava, stop_leaf, tag=tag)


def phrasing_slur(
    argument: _score.Component | typing.Sequence[_score.Component],
    *,
    direction: _enums.Vertical | None = None,
    start_phrasing_slur: _indicators.StartPhrasingSlur | _tweaks.Bundle | None = None,
    stop_phrasing_slur: _indicators.StopPhrasingSlur | None = None,
    tag: _tag.Tag | None = None,
) -> None:
    r"""
    Attaches phrasing slur indicators.

    ..  container:: example

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> abjad.phrasing_slur(voice[:], direction=abjad.UP)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                ^ \(
                d'4
                e'4
                f'4
                \)
            }


    """
    start_phrasing_slur = _indicators.StartPhrasingSlur()
    stop_phrasing_slur = _indicators.StopPhrasingSlur()
    leaves = _select.leaves(argument)
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    start_phrasing_slur = start_phrasing_slur or _indicators.StartPhrasingSlur()
    stop_phrasing_slur = stop_phrasing_slur or _indicators.StopPhrasingSlur()
    _bind.attach(start_phrasing_slur, start_leaf, direction=direction, tag=tag)
    _bind.attach(stop_phrasing_slur, stop_leaf, tag=tag)


def piano_pedal(
    argument: _score.Component | typing.Sequence[_score.Component],
    *,
    context: str | None = None,
    start_piano_pedal: _indicators.StartPianoPedal | _tweaks.Bundle | None = None,
    stop_piano_pedal: _indicators.StopPianoPedal | None = None,
    tag: _tag.Tag | None = None,
) -> None:
    r"""
    Attaches piano pedal indicators.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.piano_pedal(staff[:], context="Staff")
        >>> abjad.setting(staff).pedalSustainStyle = "#'mixed"
        >>> abjad.override(staff).SustainPedalLineSpanner.staff_padding = 5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override SustainPedalLineSpanner.staff-padding = 5
                pedalSustainStyle = #'mixed
            }
            {
                c'4
                \sustainOn
                d'4
                e'4
                f'4
                \sustainOff
            }

    """
    start_piano_pedal = start_piano_pedal or _indicators.StartPianoPedal()
    stop_piano_pedal = stop_piano_pedal or _indicators.StopPianoPedal()
    leaves = _select.leaves(argument)
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    _bind.attach(start_piano_pedal, start_leaf, context=context, tag=tag)
    _bind.attach(stop_piano_pedal, stop_leaf, context=context, tag=tag)


def slur(
    argument: _score.Component | typing.Sequence[_score.Component],
    *,
    direction: _enums.Vertical | None = None,
    start_slur: _indicators.StartSlur | _tweaks.Bundle | None = None,
    stop_slur: _indicators.StopSlur | None = None,
    tag: _tag.Tag | None = None,
) -> None:
    r"""
    Attaches slur indicators.

    ..  container:: example

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> abjad.slur(voice[:], direction=abjad.UP)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                ^ (
                d'4
                e'4
                f'4
                )
            }


    """
    start_slur = start_slur or _indicators.StartSlur()
    stop_slur = stop_slur or _indicators.StopSlur()
    leaves = _select.leaves(argument)
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    _bind.attach(start_slur, start_leaf, direction=direction, tag=tag)
    _bind.attach(stop_slur, stop_leaf, tag=tag)


def text_spanner(
    argument: _score.Component | typing.Sequence[_score.Component],
    *,
    direction: _enums.Vertical | None = None,
    start_text_span: _indicators.StartTextSpan | _tweaks.Bundle | None = None,
    stop_text_span: _indicators.StopTextSpan | None = None,
    tag: _tag.Tag | None = None,
) -> None:
    r"""
    Attaches text span indicators.

    ..  container:: example

        Single spanner:

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     right_text=abjad.Markup(r"\markup \upright tasto"),
        ...     style=r"\abjad-solid-line-with-arrow",
        ... )
        >>> abjad.text_spanner(
        ...     voice[:], direction=abjad.UP, start_text_span=start_text_span
        ... )
        >>> abjad.override(voice[0]).TextSpanner.staff_padding = 4
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', voice])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \once \override TextSpanner.staff-padding = 4
                c'4
                - \abjad-solid-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
                ^ \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    ..  container:: example

        Enchained spanners:

        >>> voice = abjad.Voice("c'4 d' e' f' r")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     style=r"\abjad-dashed-line-with-arrow",
        ... )
        >>> abjad.text_spanner(voice[:3], start_text_span=start_text_span)
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright tasto"),
        ...     right_text=abjad.Markup(r"\markup \upright pont."),
        ...     style=r"\abjad-dashed-line-with-arrow",
        ... )
        >>> abjad.text_spanner(voice[-3:], start_text_span=start_text_span)
        >>> abjad.override(voice).TextSpanner.staff_padding = 4
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', voice])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            \with
            {
                \override TextSpanner.staff-padding = 4
            }
            {
                c'4
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                \startTextSpan
                d'4
                e'4
                \stopTextSpan
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright tasto \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright pont.
                \startTextSpan
                f'4
                r4
                \stopTextSpan
            }

        >>> voice = abjad.Voice("c'4 d' e' f' r")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     style=r"\abjad-dashed-line-with-arrow",
        ... )
        >>> abjad.text_spanner(voice[:3], start_text_span=start_text_span)
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright tasto"),
        ...     style=r"\abjad-solid-line-with-hook",
        ... )
        >>> abjad.text_spanner(voice[-3:], start_text_span=start_text_span)
        >>> abjad.override(voice).TextSpanner.staff_padding = 4
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', voice])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            \with
            {
                \override TextSpanner.staff-padding = 4
            }
            {
                c'4
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                \startTextSpan
                d'4
                e'4
                \stopTextSpan
                - \abjad-solid-line-with-hook
                - \tweak bound-details.left.text \markup \concat { \upright tasto \hspace #0.5 }
                \startTextSpan
                f'4
                r4
                \stopTextSpan
            }

    """
    start_text_span = start_text_span or _indicators.StartTextSpan()
    stop_text_span = stop_text_span or _indicators.StopTextSpan()
    leaves = _select.leaves(argument)
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    _bind.attach(start_text_span, start_leaf, direction=direction, tag=tag)
    _bind.attach(stop_text_span, stop_leaf, tag=tag)


def tie(
    argument: _score.Component | typing.Sequence[_score.Component],
    *,
    direction: _enums.Vertical | None = None,
    repeat: bool | tuple[int, int] | typing.Callable = False,
    tag: _tag.Tag | None = None,
) -> None:
    r"""
    Attaches tie indicators.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 c' c' c'")
        >>> abjad.tie(staff[:], direction=abjad.UP)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                ^ ~
                c'4
                ^ ~
                c'4
                ^ ~
                c'4
            }

    ..  container:: example

        With repeat ties:

        >>> voice = abjad.Voice("c'4 c' c' c'", name="Voice")
        >>> abjad.tie(voice[:], repeat=True)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                c'4
                c'4
                \repeatTie
                c'4
                \repeatTie
                c'4
                \repeatTie
            }

    ..  container:: example

        Removes any existing ties before attaching new tie:

        >>> voice = abjad.Voice("c'4 ~ c' ~ c' ~ c'", name="Voice")
        >>> abjad.tie(voice[:])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                c'4
                ~
                c'4
                ~
                c'4
                ~
                c'4
            }

    ..  container:: example

        Ties consecutive chords if all adjacent pairs have at least one pitch
        in common:

        >>> voice = abjad.Voice("<c'>4 <c' d'>4 <d'>4", name="Voice")
        >>> abjad.tie(voice[:])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                <c'>4
                ~
                <c' d'>4
                ~
                <d'>4
            }

    ..  container:: example

        Enharmonics are allowed:

        >>> voice = abjad.Voice("c'4 bs c' dff'", name="Voice")
        >>> abjad.tie(voice[:])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                c'4
                ~
                bs4
                ~
                c'4
                ~
                dff'4
            }

    ..  container:: example

        Repeat tie threshold works like this:

        >>> voice = abjad.Voice("d'4. d'2 d'4. d'2", name="Voice")
        >>> abjad.tie(voice[:], repeat=(4, 8))
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                d'4.
                ~
                d'2
                d'4.
                \repeatTie
                ~
                d'2
            }

    ..  container:: example

        Detaches ties before attach:

        >>> voice = abjad.Voice("d'2 ~ d'8 ~ d'8 ~ d'8 ~ d'8", name="Voice")
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                d'2
                ~
                d'8
                ~
                d'8
                ~
                d'8
                ~
                d'8
            }

        >>> abjad.tie(voice[:], repeat=(4, 8))
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                d'2
                d'8
                \repeatTie
                ~
                d'8
                ~
                d'8
                ~
                d'8
            }

    """
    if callable(repeat):
        pass
    elif repeat in (None, False):

        def inequality(item):
            return item < 0

    elif repeat is True:

        def inequality(item):
            return item >= 0

    else:
        assert isinstance(repeat, tuple) and len(repeat) == 2, repr(repeat)

        def inequality(item):
            return item >= _duration.Duration(repeat)

    leaves = _select.leaves(argument)
    if len(leaves) < 2:
        raise Exception(f"must be two or more notes (not {leaves!r}).")
    for leaf in leaves:
        if not isinstance(leaf, _score.Note | _score.Chord):
            raise Exception(rf"tie note or chord (not {leaf!r}).")
    for current_leaf, next_leaf in _sequence.nwise(leaves):
        duration = current_leaf._get_duration()
        if inequality(duration):
            _bind.detach(_indicators.Tie, current_leaf)
            _bind.detach(_indicators.RepeatTie, next_leaf)
            repeat_tie = _indicators.RepeatTie()
            _bind.attach(repeat_tie, next_leaf, direction=direction, tag=tag)
        else:
            _bind.detach(_indicators.Tie, current_leaf)
            _bind.detach(_indicators.RepeatTie, next_leaf)
            tie = _indicators.Tie()
            _bind.attach(tie, current_leaf, direction=direction, tag=tag)


def trill_spanner(
    argument: _score.Component | typing.Sequence[_score.Component],
    *,
    start_trill_span: _indicators.StartTrillSpan | _tweaks.Bundle | None = None,
    stop_trill_span: _indicators.StopTrillSpan | None = None,
    tag: _tag.Tag | None = None,
) -> None:
    r"""
    Attaches trill spanner indicators.

    ..  container:: example

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> abjad.trill_spanner(voice[:])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \startTrillSpan
                d'4
                e'4
                f'4
                \stopTrillSpan
            }

    """
    start_trill_span = start_trill_span or _indicators.StartTrillSpan()
    stop_trill_span = stop_trill_span or _indicators.StopTrillSpan()
    leaves = _select.leaves(argument)
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    _bind.attach(start_trill_span, start_leaf, tag=tag)
    _bind.attach(stop_trill_span, stop_leaf, tag=tag)
