import dataclasses
import typing

from . import _getlib, _iterlib
from . import bind as _bind
from . import cyclictuple as _cyclictuple
from . import duration as _duration
from . import enums as _enums
from . import indicators as _indicators
from . import iterate as _iterate
from . import overrides as _overrides
from . import pcollections as _pcollections
from . import pitch as _pitch
from . import score as _score
from . import select as _select
from . import setclass as _setclass
from . import tweaks as _tweaks
from . import verticalmoment as _verticalmoment


def _attach(label, leaf, *, deactivate=False, direction=None, tag=None):
    _bind.attach(label, leaf, deactivate=deactivate, direction=direction, tag=tag)


def _color_leaf(leaf, color, *, deactivate=False, tag=None):
    if isinstance(leaf, _score.Skip):
        color = color[1:]
        comment = _indicators.LilyPondLiteral(f"% {color}", site="before")
        _attach(comment, leaf, deactivate=deactivate, tag=tag)
    else:
        assert color.startswith("#")
        string = rf"\abjad-color-music #'{color[1:]}"
        literal = _indicators.LilyPondLiteral(string, site="before")
        _attach(literal, leaf)
    return leaf


pc_number_to_color = {
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


def color_container(container, color="#red") -> None:
    r"""
    Colors contents of ``container``.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8")
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.label.color_container(staff, "#red")
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

    """
    _overrides.override(container).Accidental.color = color
    _overrides.override(container).Beam.color = color
    _overrides.override(container).Dots.color = color
    _overrides.override(container).NoteHead.color = color
    _overrides.override(container).Rest.color = color
    _overrides.override(container).Stem.color = color
    _overrides.override(container).TupletBracket.color = color
    _overrides.override(container).TupletNumber.color = color


def color_leaves(argument, color="#red", *, deactivate=False, tag=None) -> None:
    r"""
    Colors leaves in ``argument``.

    ..  container:: example

        >>> staff = abjad.Staff("cs'8. r8. s8. <c' cs' a'>8.")
        >>> abjad.label.color_leaves(staff, "#red")
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \abjad-color-music #'red
                cs'8.
                \abjad-color-music #'red
                r8.
                % red
                s8.
                \abjad-color-music #'red
                <c' cs' a'>8.
            }

    """
    if isinstance(color, str):
        for leaf in _iterate.leaves(argument):
            _color_leaf(leaf, color, deactivate=deactivate, tag=tag)
    else:
        assert isinstance(color, typing.Sequence)
        colors = _cyclictuple.CyclicTuple(color)
        for i, item in enumerate(argument):
            color = colors[i]
            color_leaves(item, color, deactivate=deactivate, tag=tag)


def color_note_heads(argument, color_map=pc_number_to_color) -> None:
    r"""
    Colors note note-heads.

    ..  container:: example

        >>> chord = abjad.Chord([12, 14, 18, 21, 23], (1, 4))
        >>> pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
        >>> colors = ["#red", "#blue", "#green"]
        >>> color_map = abjad.ColorMap(colors=colors, pitch_iterables=pitches)
        >>> abjad.label.color_note_heads(chord, color_map)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <
                \tweak Accidental.color #red
                \tweak color #red
                c''
                \tweak Accidental.color #red
                \tweak color #red
                d''
                \tweak Accidental.color #green
                \tweak color #green
                fs''
                \tweak Accidental.color #green
                \tweak color #green
                a''
                \tweak Accidental.color #blue
                \tweak color #blue
                b''
            >4

    ..  container:: example

        Colors note note-head:

        >>> note = abjad.Note("c'4")
        >>> abjad.label.color_note_heads(note, color_map)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            \tweak Accidental.color #red
            \tweak color #red
            c'4

        Colors nothing:

        >>> staff = abjad.Staff()
        >>> abjad.label.color_note_heads(staff, color_map)

        Colors note-heads:

        >>> string = "c'8 cs'8 d'8 ds'8 e'8 f'8 fs'8 g'8 gs'8 a'8 as'8 b'8 c''8"
        >>> staff = abjad.Staff(string)
        >>> abjad.label.color_note_heads(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak Accidental.color #(x11-color 'red)
                \tweak color #(x11-color 'red)
                c'8
                \tweak Accidental.color #(x11-color 'MediumBlue)
                \tweak color #(x11-color 'MediumBlue)
                cs'8
                \tweak Accidental.color #(x11-color 'orange)
                \tweak color #(x11-color 'orange)
                d'8
                \tweak Accidental.color #(x11-color 'LightSlateBlue)
                \tweak color #(x11-color 'LightSlateBlue)
                ds'8
                \tweak Accidental.color #(x11-color 'ForestGreen)
                \tweak color #(x11-color 'ForestGreen)
                e'8
                \tweak Accidental.color #(x11-color 'MediumOrchid)
                \tweak color #(x11-color 'MediumOrchid)
                f'8
                \tweak Accidental.color #(x11-color 'firebrick)
                \tweak color #(x11-color 'firebrick)
                fs'8
                \tweak Accidental.color #(x11-color 'DeepPink)
                \tweak color #(x11-color 'DeepPink)
                g'8
                \tweak Accidental.color #(x11-color 'DarkOrange)
                \tweak color #(x11-color 'DarkOrange)
                gs'8
                \tweak Accidental.color #(x11-color 'IndianRed)
                \tweak color #(x11-color 'IndianRed)
                a'8
                \tweak Accidental.color #(x11-color 'CadetBlue)
                \tweak color #(x11-color 'CadetBlue)
                as'8
                \tweak Accidental.color #(x11-color 'SeaGreen)
                \tweak color #(x11-color 'SeaGreen)
                b'8
                \tweak Accidental.color #(x11-color 'red)
                \tweak color #(x11-color 'red)
                c''8
            }

    """
    color_map = color_map or pc_number_to_color
    for leaf in _iterate.leaves(argument):
        if isinstance(leaf, _score.Chord):
            for note_head in leaf.note_heads:
                number = note_head.written_pitch.number
                pc = _pitch.NumberedPitchClass(number)
                color = color_map.get(pc, None)
                if color is not None:
                    _tweaks.tweak(note_head, rf"\tweak Accidental.color {color}")
                    _tweaks.tweak(note_head, rf"\tweak color {color}")
        elif isinstance(leaf, _score.Note):
            note_head = leaf.note_head
            number = note_head.written_pitch.number
            pc = _pitch.NumberedPitchClass(number)
            color = color_map[pc.number]
            if color is not None:
                _tweaks.tweak(leaf.note_head, rf"\tweak Accidental.color {color}")
                _tweaks.tweak(leaf.note_head, rf"\tweak color {color}")


def remove_markup(argument) -> None:
    r"""
    Removes markup from leaves in ``argument``.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.label.with_pitches(staff)
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

        >>> abjad.label.remove_markup(staff)
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

    """
    for leaf in _iterate.leaves(argument):
        _bind.detach(_indicators.Markup, leaf)


def vertical_moments(
    argument, direction=_enums.UP, prototype=None, *, deactivate=False, tag=None
):
    r'''
    Labels vertical moments.

    ..  container:: example

        Labels indices:

        >>> staff_group = abjad.StaffGroup([])
        >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
        >>> staff_group.append(staff)
        >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
        >>> staff_group.append(staff)
        >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
        >>> staff_group.append(staff)
        >>> abjad.label.vertical_moments(staff_group)
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new StaffGroup
            <<
                \new Staff
                {
                    c'8
                    ^ \markup \tiny 0
                    d'4
                    ^ \markup \tiny 1
                    e'16
                    ^ \markup \tiny 3
                    f'16
                    ^ \markup \tiny 4
                }
                \new Staff
                {
                    \clef "alto"
                    g4
                    f4
                    ^ \markup \tiny 2
                }
                \new Staff
                {
                    \clef "bass"
                    c,2
                }
            >>

        Labels pitch numbers:

        >>> staff_group = abjad.StaffGroup([])
        >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
        >>> staff_group.append(staff)
        >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
        >>> staff_group.append(staff)
        >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
        >>> staff_group.append(staff)
        >>> abjad.label.vertical_moments(
        ...     staff_group,
        ...     prototype=abjad.NumberedPitch,
        ... )
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new StaffGroup
            <<
                \new Staff
                {
                    c'8
                    ^ \markup \tiny \column { 0 -5 -24 }
                    d'4
                    ^ \markup \tiny \column { 2 -5 -24 }
                    e'16
                    ^ \markup \tiny \column { 4 -7 -24 }
                    f'16
                    ^ \markup \tiny \column { 5 -7 -24 }
                }
                \new Staff
                {
                    \clef "alto"
                    g4
                    f4
                    ^ \markup \tiny \column { 2 -7 -24 }
                }
                \new Staff
                {
                    \clef "bass"
                    c,2
                }
            >>

    ..  container:: example

        Labels pitch-class numbers:

        >>> staff_group = abjad.StaffGroup([])
        >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
        >>> staff_group.append(staff)
        >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
        >>> staff_group.append(staff)
        >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
        >>> staff_group.append(staff)
        >>> prototype = abjad.NumberedPitchClass
        >>> abjad.label.vertical_moments(staff_group, prototype=prototype)
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new StaffGroup
            <<
                \new Staff
                {
                    c'8
                    ^ \markup \tiny \column { 7 0 }
                    d'4
                    ^ \markup \tiny \column { 7 2 0 }
                    e'16
                    ^ \markup \tiny \column { 5 4 0 }
                    f'16
                    ^ \markup \tiny \column { 5 0 }
                }
                \new Staff
                {
                    \clef "alto"
                    g4
                    f4
                    ^ \markup \tiny \column { 5 2 0 }
                }
                \new Staff
                {
                    \clef "bass"
                    c,2
                }
            >>

    ..  container:: example

        Labels interval numbers:

        >>> staff_group = abjad.StaffGroup([])
        >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
        >>> staff_group.append(staff)
        >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
        >>> staff_group.append(staff)
        >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
        >>> staff_group.append(staff)
        >>> prototype = abjad.NumberedInterval
        >>> abjad.label.vertical_moments(staff_group, prototype=prototype)
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new StaffGroup
            <<
                \new Staff
                {
                    c'8
                    ^ \markup \tiny \column { 15 12 }
                    d'4
                    ^ \markup \tiny \column { 16 12 }
                    e'16
                    ^ \markup \tiny \column { 17 11 }
                    f'16
                    ^ \markup \tiny \column { 18 11 }
                }
                \new Staff
                {
                    \clef "alto"
                    g4
                    f4
                    ^ \markup \tiny \column { 16 11 }
                }
                \new Staff
                {
                    \clef "bass"
                    c,2
                }
            >>

    ..  container:: example

        Labels interval-class numbers:

        >>> staff_group = abjad.StaffGroup([])
        >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
        >>> staff_group.append(staff)
        >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
        >>> staff_group.append(staff)
        >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
        >>> staff_group.append(staff)
        >>> prototype = abjad.NumberedIntervalClass
        >>> abjad.label.vertical_moments(staff_group, prototype=prototype)
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new StaffGroup
            <<
                \new Staff
                {
                    c'8
                    ^ \markup \tiny \column { 12 7 }
                    d'4
                    ^ \markup \tiny \column { 2 7 }
                    e'16
                    ^ \markup \tiny \column { 4 5 }
                    f'16
                    ^ \markup \tiny \column { 5 5 }
                }
                \new Staff
                {
                    \clef "alto"
                    g4
                    f4
                    ^ \markup \tiny \column { 2 5 }
                }
                \new Staff
                {
                    \clef "bass"
                    c,2
                }
            >>

    ..  container:: example

        Labels interval-class vectors:

        >>> staff_group = abjad.StaffGroup([])
        >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
        >>> staff_group.append(staff)
        >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
        >>> staff_group.append(staff)
        >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
        >>> staff_group.append(staff)
        >>> prototype = abjad.pcollections.make_interval_class_vector
        >>> abjad.label.vertical_moments(staff_group, prototype=prototype)
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new StaffGroup
            <<
                \new Staff
                {
                    c'8
                    ^ \markup \tiny \tiny 1000020
                    d'4
                    ^ \markup \tiny \tiny 0010020
                    e'16
                    ^ \markup \tiny \tiny 0100110
                    f'16
                    ^ \markup \tiny \tiny 1000020
                }
                \new Staff
                {
                    \clef "alto"
                    g4
                    f4
                    ^ \markup \tiny \tiny 0011010
                }
                \new Staff
                {
                    \clef "bass"
                    c,2
                }
            >>

    ..  container:: example

        Labels set-classes:

        >>> staff_group = abjad.StaffGroup([])
        >>> staff = abjad.Staff("c'8 d'4 e'16 f'16")
        >>> staff_group.append(staff)
        >>> staff = abjad.Staff(r"""\clef "alto" g4 f4""")
        >>> staff_group.append(staff)
        >>> staff = abjad.Staff(r"""\clef "bass" c,2""")
        >>> staff_group.append(staff)
        >>> prototype = abjad.SetClass()
        >>> abjad.label.vertical_moments(staff_group, prototype=prototype)
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
    prototype = prototype or int
    vertical_moments = _verticalmoment.iterate_vertical_moments(argument)
    for index, vertical_moment in enumerate(vertical_moments):
        label, string = None, None
        if prototype is int:
            string = str(index)
        elif prototype is _pitch.NumberedPitch:
            leaves = vertical_moment.leaves
            generator = _iterate.pitches(leaves)
            pitches = _pcollections.PitchSegment(generator)
            if not pitches:
                continue
            pitch_numbers = [str(pitch.number) for pitch in pitches]
            string = rf'\column {{ {" ".join(pitch_numbers)} }}'
        elif prototype is _pitch.NumberedPitchClass:
            leaves = vertical_moment.leaves
            generator = _iterate.pitches(leaves)
            pitches = _pcollections.PitchSegment(generator)
            if not pitches:
                continue
            pitch_classes = [pitch.pitch_class.number for pitch in pitches]
            pitch_classes = list(set(pitch_classes))
            pitch_classes.sort()
            pitch_classes.reverse()
            numbers = [str(_) for _ in pitch_classes]
            string = rf'\column {{ {" ".join(numbers)} }}'
        elif prototype is _pitch.NumberedInterval:
            leaves = vertical_moment.leaves
            notes = [_ for _ in leaves if isinstance(_, _score.Note)]
            if not notes:
                continue
            notes.sort(key=lambda x: x.written_pitch.number)
            notes.reverse()
            bass_note = notes[-1]
            upper_notes = notes[:-1]
            named_intervals = []
            for upper_note in upper_notes:
                named_interval = _pitch.NamedInterval.from_pitch_carriers(
                    bass_note.written_pitch, upper_note.written_pitch
                )
                named_intervals.append(named_interval)
            numbers = [str(x.number) for x in named_intervals]
            string = rf'\column {{ {" ".join(numbers)} }}'
        elif prototype is _pitch.NumberedIntervalClass:
            leaves = vertical_moment.leaves
            notes = [_ for _ in leaves if isinstance(_, _score.Note)]
            if not notes:
                continue
            notes.sort(key=lambda _: _.written_pitch.number)
            notes.reverse()
            bass_note = notes[-1]
            upper_notes = notes[:-1]
            numbers = []
            for upper_note in upper_notes:
                interval = _pitch.NamedInterval.from_pitch_carriers(
                    bass_note.written_pitch, upper_note.written_pitch
                )
                interval_class = _pitch.NumberedIntervalClass(interval)
                number = interval_class.number
                numbers.append(number)
            string = " ".join([str(_) for _ in numbers])
            string = rf"\column {{ {string} }}"
        elif prototype is _setclass.SetClass or isinstance(
            prototype, _setclass.SetClass
        ):
            if prototype is _setclass.SetClass:
                prototype = prototype()
            assert isinstance(prototype, _setclass.SetClass)
            leaves = vertical_moment.leaves
            generator = _iterate.pitches(leaves)
            pitch_class_set = _pcollections.PitchClassSet(generator)
            if not pitch_class_set:
                continue
            set_class = _setclass.SetClass.from_pitches(
                pitch_class_set,
                lex_rank=prototype.lex_rank,
                transposition_only=prototype.transposition_only,
            )
            string = str(set_class)
            string = rf'\line {{ "{string}" }}'
        elif callable(prototype):
            leaves = vertical_moment.leaves
            generator = _iterate.pitches(leaves)
            string = prototype(generator)
        else:
            raise TypeError(f"unknown prototype {prototype!r}.")
        assert string is not None
        label = _indicators.Markup(rf"\markup \tiny {string}")
        if direction is _enums.UP:
            leaf = vertical_moment.start_leaves[0]
        else:
            leaf = vertical_moment.start_leaves[-1]
        _attach(label, leaf, deactivate=deactivate, direction=direction, tag=tag)


def with_durations(
    argument, *, denominator=None, direction=_enums.UP, in_seconds: bool = False
):
    r"""
    Labels logical ties in ``argument`` with durations.

    ..  container:: example

        Labels logical tie durations:

        >>> staff = abjad.Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")
        >>> abjad.label.with_durations(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4.
                ^ \markup \fraction 3 8
                d'8
                ^ \markup \fraction 1 2
                ~
                d'4.
                e'16
                ^ \markup \fraction 1 16
                [
                ef'16
                ^ \markup \fraction 1 16
                ]
            }

    ..  container:: example

        Labels logical ties with preferred denominator:

        >>> staff = abjad.Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")
        >>> abjad.label.with_durations(staff, denominator=16)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4.
                ^ \markup \fraction 6 16
                d'8
                ^ \markup \fraction 8 16
                ~
                d'4.
                e'16
                ^ \markup \fraction 1 16
                [
                ef'16
                ^ \markup \fraction 1 16
                ]
            }

    Returns none.
    """
    for logical_tie in _iterate.logical_ties(argument):
        duration = _getlib._get_duration(logical_tie, in_seconds=in_seconds)
        pair = duration.pair
        if denominator is not None:
            pair = _duration.with_denominator(duration, denominator)
        n, d = pair
        label = _indicators.Markup(rf"\markup \fraction {n} {d}")
        _attach(label, logical_tie.head, direction=direction)


def with_indices(argument, direction=_enums.UP, prototype=None) -> None:
    r"""
    Labels logical ties in ``argument`` with indices.

    Labels logical tie indices:

    ..  container:: example

        >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
        >>> abjad.label.with_indices(staff)
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
                ^ \markup 0
                <g' a'>4
                ^ \markup 1
                af'8
                ^ \markup 2
                ~
                af'8
                gf'8
                ^ \markup 3
                ~
                gf'4
            }

    ..  container:: example

        Labels note indices:

        >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
        >>> abjad.label.with_indices(staff, prototype=abjad.Note)
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
                ^ \markup 0
                ~
                af'8
                ^ \markup 1
                gf'8
                ^ \markup 2
                ~
                gf'4
                ^ \markup 3
            }

    ..  container:: example

        Labels chord indices:

        >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
        >>> abjad.label.with_indices(staff, prototype=abjad.Chord)
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
                ^ \markup 0
                <g' a'>4
                ^ \markup 1
                af'8
                ~
                af'8
                gf'8
                ~
                gf'4
            }

    ..  container:: example

        Labels leaf indices:

        >>> staff = abjad.Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
        >>> abjad.label.with_indices(staff, prototype=abjad.Leaf)
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
                ^ \markup 0
                <g' a'>4
                ^ \markup 1
                af'8
                ^ \markup 2
                ~
                af'8
                ^ \markup 3
                gf'8
                ^ \markup 4
                ~
                gf'4
                ^ \markup 5
            }

    ..  container:: example

        Labels tuplet indices:

        >>> tuplet = abjad.Tuplet((2, 3), "c'8 [ d'8 e'8 ]")
        >>> tuplets = abjad.mutate.copy(tuplet, 4)
        >>> staff = abjad.Staff(tuplets)
        >>> abjad.label.with_indices(staff, prototype=abjad.Tuplet)
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
                \tuplet 3/2
                {
                    c'8
                    ^ \markup 0
                    [
                    d'8
                    e'8
                    ]
                }
                \tuplet 3/2
                {
                    c'8
                    ^ \markup 1
                    [
                    d'8
                    e'8
                    ]
                }
                \tuplet 3/2
                {
                    c'8
                    ^ \markup 2
                    [
                    d'8
                    e'8
                    ]
                }
                \tuplet 3/2
                {
                    c'8
                    ^ \markup 3
                    [
                    d'8
                    e'8
                    ]
                }
            }

    """
    if prototype is None:
        generator = _iterate.logical_ties(argument)
    else:
        generator = _iterate.components(argument, prototype=prototype)
    items = list(generator)
    for index, item in enumerate(items):
        label = _indicators.Markup(rf"\markup {index}")
        leaves = _select.leaves(item)
        first_leaf = leaves[0]
        _attach(label, first_leaf, direction=direction)


def with_intervals(argument, direction=_enums.UP, prototype=None) -> None:
    r"""
    Labels consecutive notes in ``argument`` with intervals.

    Labels consecutive notes with interval names:

    ..  container:: example

        >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
        >>> notes = abjad.makers.make_notes(pitch_numbers, [(1, 4)])
        >>> staff = abjad.Staff(notes)
        >>> abjad.label.with_intervals(staff, prototype=None)
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
                ^ \markup +A15
                cs'''4
                ^ \markup -M9
                b'4
                ^ \markup -A9
                af4
                ^ \markup -m7
                bf,4
                ^ \markup +A1
                b,4
                ^ \markup +m14
                a'4
                ^ \markup +m2
                bf'4
            }

    ..  container:: example

        Labels consecutive notes with interval-class names:

        >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
        >>> notes = abjad.makers.make_notes(pitch_numbers, [(1, 4)])
        >>> staff = abjad.Staff(notes)
        >>> prototype = abjad.NamedIntervalClass
        >>> abjad.label.with_intervals(staff, prototype=prototype)
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
                ^ \markup +A1
                cs'''4
                ^ \markup -M2
                b'4
                ^ \markup -A2
                af4
                ^ \markup -m7
                bf,4
                ^ \markup +A1
                b,4
                ^ \markup +m7
                a'4
                ^ \markup +m2
                bf'4
            }

    ..  container:: example

        Labels consecutive notes with interval numbers:

        >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
        >>> notes = abjad.makers.make_notes(pitch_numbers, [(1, 4)])
        >>> staff = abjad.Staff(notes)
        >>> prototype = abjad.NumberedInterval
        >>> abjad.label.with_intervals(staff, prototype=prototype)
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
                ^ \markup +25
                cs'''4
                ^ \markup -14
                b'4
                ^ \markup -15
                af4
                ^ \markup -10
                bf,4
                ^ \markup +1
                b,4
                ^ \markup +22
                a'4
                ^ \markup +1
                bf'4
            }

    ..  container:: example

        Labels consecutive notes with interval-class numbers:

        >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
        >>> notes = abjad.makers.make_notes(pitch_numbers, [(1, 4)])
        >>> staff = abjad.Staff(notes)
        >>> prototype = abjad.NumberedIntervalClass
        >>> abjad.label.with_intervals(staff, prototype=prototype)
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
                ^ \markup +1
                cs'''4
                ^ \markup -2
                b'4
                ^ \markup -3
                af4
                ^ \markup -10
                bf,4
                ^ \markup +1
                b,4
                ^ \markup +10
                a'4
                ^ \markup +1
                bf'4
            }

    ..  container:: example

        Labels consecutive notes with inversion-equivalent interval-class numbers:

        >>> pitch_numbers = [0, 25, 11, -4, -14, -13, 9, 10]
        >>> notes = abjad.makers.make_notes(pitch_numbers, [(1, 4)])
        >>> staff = abjad.Staff(notes)
        >>> prototype = abjad.NumberedInversionEquivalentIntervalClass
        >>> abjad.label.with_intervals(staff, prototype=prototype)
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
                ^ \markup 1
                cs'''4
                ^ \markup 2
                b'4
                ^ \markup 3
                af4
                ^ \markup 2
                bf,4
                ^ \markup 1
                b,4
                ^ \markup 2
                a'4
                ^ \markup 1
                bf'4
            }

    """
    prototype = prototype or _pitch.NamedInterval
    for note in _iterate.leaves(argument, _score.Note):
        label = None
        next_leaf = _iterlib._get_leaf(note, 1)
        if isinstance(next_leaf, _score.Note):
            interval = _pitch.NamedInterval.from_pitch_carriers(note, next_leaf)
            interval = prototype(interval)
            if hasattr(interval, "name"):
                label = _indicators.Markup(rf"\markup {interval.name}")
            elif isinstance(interval, _pitch.NumberedInversionEquivalentIntervalClass):
                label = _indicators.Markup(rf"\markup {interval.number}")
            elif isinstance(
                interval, _pitch.NumberedIntervalClass | _pitch.NumberedInterval
            ):
                label = _indicators.Markup(rf"\markup {interval.signed_string}")
            if label is not None:
                _attach(label, note, direction=direction)


def with_pitches(argument, direction=_enums.UP, locale=None, prototype=None):
    r"""
    Labels logical ties in ``argument`` with pitches.

    ..  container:: example

        Labels logical ties with pitch names:

        >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
        >>> abjad.label.with_pitches(staff, prototype=None)
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

        >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
        >>> abjad.label.with_pitches(staff, locale="us", prototype=None)
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

        >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
        >>> prototype = abjad.NumberedPitch
        >>> abjad.label.with_pitches(staff, prototype=prototype)
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
                ^ \markup \column { 6 2 -3 }
                g'4
                ^ \markup 7
                ~
                g'8
                r8
                fs''4
                ^ \markup 18
            }

    ..  container:: example

        Labels logical ties with pitch-class numbers:

        >>> staff = abjad.Staff("<a d' fs'>4 g'4 ~ g'8 r8 fs''4")
        >>> prototype = abjad.NumberedPitchClass
        >>> abjad.label.with_pitches(staff, prototype=prototype)
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
                ^ \markup \column { 6 2 9 }
                g'4
                ^ \markup 7
                ~
                g'8
                r8
                fs''4
                ^ \markup 6
            }

    ..  container:: example

        Labels logical ties with pitch names (filtered by selection):

        >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
        >>> string = 'Horizontal_bracket_engraver'
        >>> voice.consists_commands.append(string)
        >>> selections = [voice[:2], voice[-2:]]
        >>> for selection in selections:
        ...     abjad.horizontal_bracket(selection)
        ...
        >>> abjad.label.with_pitches(selections)
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

        >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
        >>> voice.consists_commands.append('Horizontal_bracket_engraver')
        >>> selections = [voice[:2], voice[-2:]]
        >>> for selection in selections:
        ...     abjad.horizontal_bracket(selection)
        ...
        >>> prototype = abjad.NumberedPitch
        >>> abjad.label.with_pitches(selections, prototype=prototype)
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
                ^ \markup 13
                \startGroup
                c''4
                ^ \markup 12
                \stopGroup
                f'4
                fs'4
                d''4
                ^ \markup 14
                \startGroup
                ds''4
                ^ \markup 15
                \stopGroup
            }

    ..  container:: example

        Labels logical ties with pitch-class numbers (filtered by selection):

        >>> voice = abjad.Voice("df''4 c''4 f'4 fs'4 d''4 ds''4")
        >>> voice.consists_commands.append('Horizontal_bracket_engraver')
        >>> selections = [voice[:2], voice[-2:]]
        >>> for selection in selections:
        ...     abjad.horizontal_bracket(selection)
        ...
        >>> prototype = abjad.NumberedPitchClass
        >>> abjad.label.with_pitches(selections, prototype=prototype)
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
                ^ \markup 1
                \startGroup
                c''4
                ^ \markup 0
                \stopGroup
                f'4
                fs'4
                d''4
                ^ \markup 2
                \startGroup
                ds''4
                ^ \markup 3
                \stopGroup
            }

    Returns none.
    """
    prototype = prototype or _pitch.NamedPitch
    logical_ties = _iterate.logical_ties(argument)
    for logical_tie in logical_ties:
        leaf = logical_tie.head
        label = None
        if prototype is _pitch.NamedPitch:
            if isinstance(leaf, _score.Note):
                string = leaf.written_pitch.get_name(locale=locale)
                if "#" in string:
                    string = '"' + string + '"'
                label = _indicators.Markup(rf"\markup {{ {string} }}")
            elif isinstance(leaf, _score.Chord):
                pitches = leaf.written_pitches
                pitches = reversed(pitches)
                names = []
                for pitch in pitches:
                    name = pitch.get_name(locale=locale)
                    name = '"' + name + '"'
                    names.append(name)
                string = " ".join(names)
                label = _indicators.Markup(rf"\markup \column {{ {string} }}")
        elif prototype is _pitch.NumberedPitch:
            if isinstance(leaf, _score.Note):
                pitch = leaf.written_pitch.number
                label = _indicators.Markup(rf"\markup {pitch}")
            elif isinstance(leaf, _score.Chord):
                pitches = leaf.written_pitches
                pitches = reversed(pitches)
                pitches = [str(_.number) for _ in pitches]
                string = " ".join(pitches)
                label = _indicators.Markup(rf"\markup \column {{ {string} }}")
        elif prototype is _pitch.NumberedPitchClass:
            if isinstance(leaf, _score.Note):
                pitch = leaf.written_pitch.pitch_class.number
                label = _indicators.Markup(rf"\markup {pitch}")
            elif isinstance(leaf, _score.Chord):
                pitches = leaf.written_pitches
                pitches = reversed(pitches)
                pitches = [str(_.pitch_class.number) for _ in pitches]
                string = " ".join(pitches)
                label = _indicators.Markup(rf"\markup \column {{ {string} }}")
        if label is not None:
            _attach(label, leaf, direction=direction)


def with_set_classes(argument, direction=_enums.UP, prototype=None):
    r"""
    Labels selections ``argument`` with set-classes.

    ..  container:: example

        Labels selections with Forte-ranked transposition-inversion set-classes:

        >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
        >>> voice = abjad.Voice(string)
        >>> voice.consists_commands.append('Horizontal_bracket_engraver')
        >>> selections = [voice[:4], voice[-4:]]
        >>> for selection in selections:
        ...     abjad.horizontal_bracket(selection)
        ...
        >>> abjad.label.with_set_classes(selections)
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

        Labels selections with lex-ranked transposition-inversion set-classes:

        >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
        >>> voice = abjad.Voice(string)
        >>> voice.consists_commands.append('Horizontal_bracket_engraver')
        >>> selections = [voice[:4], voice[-4:]]
        >>> for selection in selections:
        ...     abjad.horizontal_bracket(selection)
        ...
        >>> prototype = abjad.SetClass(lex_rank=True)
        >>> abjad.label.with_set_classes(selections, prototype=prototype)
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

        >>> string = "df''8 c''8 bf'8 a'8 f'4. fs'8 g'8 b'8 d''2."
        >>> voice = abjad.Voice(string)
        >>> voice.consists_commands.append('Horizontal_bracket_engraver')
        >>> selections = [voice[:4], voice[-4:]]
        >>> for selection in selections:
        ...     abjad.horizontal_bracket(selection)
        ...
        >>> prototype = abjad.SetClass(lex_rank=True, transposition_only=True)
        >>> abjad.label.with_set_classes(selections, prototype=prototype)
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
    prototype = prototype or _setclass.SetClass()
    if prototype is _setclass.SetClass:
        prototype = prototype()
    assert isinstance(prototype, _setclass.SetClass), repr(prototype)
    for selection in argument:
        generator = _iterate.pitches(selection)
        pitch_class_set = _pcollections.PitchClassSet(generator)
        if not pitch_class_set:
            continue
        set_class = _setclass.SetClass.from_pitches(
            pitch_class_set,
            lex_rank=prototype.lex_rank,
            transposition_only=prototype.transposition_only,
        )
        string = str(set_class)
        label = _indicators.Markup(rf'\markup \tiny \line {{ "{string}" }}')
        leaf = selection[0]
        _attach(label, leaf, direction=direction)


def with_start_offsets(
    argument,
    brackets=None,
    clock_time=None,
    direction=None,
    global_offset=None,
    markup_command=None,
):
    r"""
    Labels logical ties in ``argument`` with start offsets.

    ..  container:: example

        Labels logical tie start offsets:

        >>> string = r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4"
        >>> staff = abjad.Staff(string)
        >>> abjad.label.with_start_offsets(staff, direction=abjad.UP)
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
                \tuplet 3/2
                {
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

        >>> staff = abjad.Staff(r"c'2 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
        >>> abjad.attach(mark, staff[0])
        >>> abjad.label.with_start_offsets(staff, clock_time=True)
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

        Labels logical tie start offsets with clock time and custom markup command. No
        PDF shown here because command is custom:

        >>> staff = abjad.Staff(r"c'2 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
        >>> abjad.attach(mark, staff[0])
        >>> abjad.label.with_start_offsets(
        ...     staff,
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
                ^ \dark_cyan_markup { 0'00'' }
                d'2
                ^ \dark_cyan_markup { 0'02'' }
                e'2
                ^ \dark_cyan_markup { 0'04'' }
                f'2
                ^ \dark_cyan_markup { 0'06'' }
            }
        >>

    Returns total duration.
    """
    direction = direction or _enums.UP
    if global_offset is not None:
        assert isinstance(global_offset, _duration.Duration)
    for logical_tie in _iterate.logical_ties(argument):
        if clock_time:
            timespan = logical_tie.head._get_timespan(in_seconds=True)
            start_offset = timespan.start_offset
            if global_offset is not None:
                start_offset += global_offset
            string = start_offset.to_clock_string()
        else:
            timespan = logical_tie.head._get_timespan()
            start_offset = timespan.start_offset
            if global_offset is not None:
                start_offset += global_offset
            string = str(start_offset)
        if brackets:
            string = f"[{string}]"
        if markup_command is not None:
            label = _indicators.Markup(rf"{markup_command} {{ {string} }}")
        else:
            label = _indicators.Markup(rf"\markup {{ {string} }}")
        _attach(label, logical_tie.head, direction=direction)
    total_duration = _duration.Duration(timespan.stop_offset)
    if global_offset is not None:
        total_duration += global_offset
    return total_duration


@dataclasses.dataclass(slots=True)
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
        >>> color_map
        ColorMap(colors=['#red', '#green', '#blue'], pitch_iterables=[[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]])

    """

    colors: typing.Any = None
    pitch_iterables: typing.Any = None
    _color_dictionary: dict = dataclasses.field(compare=False, init=False, repr=False)

    def __post_init__(self):
        self.pitch_iterables = self.pitch_iterables or []
        self.colors = self.colors or []
        assert len(self.pitch_iterables) == len(self.colors)
        self._color_dictionary = {}
        self._initialize_color_dictionary()

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
        pitch_class = _pitch.NumberedPitchClass(pitch_class)
        return self._color_dictionary[pitch_class.number]

    def _initialize_color_dictionary(self):
        for pitch_iterable, color in zip(self.pitch_iterables, self.colors):
            for pitch in pitch_iterable:
                pc = _pitch.NumberedPitchClass(pitch)
                keys = set(self._color_dictionary.keys())
                if pc.number in keys:
                    print(pc, list(self._color_dictionary.keys()))
                    raise KeyError("duplicated pitch-class in color map: {pc!r}.")
                self._color_dictionary[pc.number] = color

    def __hash__(self):
        """
        Makes hash.
        """
        return hash(repr(self))

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
    def pairs(self) -> list[tuple[int, str]]:
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
