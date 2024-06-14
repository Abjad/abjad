import abjad


def test_mutate__are_contiguous_logical_voice_01():
    """
    Components that start at the same moment are bad.
    Even if components are all part of the same logical voice.
    """

    voice = abjad.Voice(
        r"""
        {
            c'8
            d'8
        }
        \new Voice {
            e'8
            f'8
        }
        {
            g'8
            a'8
        }
        """
    )

    voices = [voice, voice[0]]
    assert not abjad.mutate._are_contiguous_logical_voice(voices)
    voices = list(voice[0:1]) + list(voice[0])
    assert not abjad.mutate._are_contiguous_logical_voice(voices)
    voices = list(voice[-1:]) + list(voice[-1])
    assert not abjad.mutate._are_contiguous_logical_voice(voices)


def test_mutate__are_contiguous_logical_voice_02():
    """
    Is true for strictly contiguous leaves in same staff.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    assert abjad.mutate._are_contiguous_logical_voice(staff[:])


def test_mutate__are_contiguous_logical_voice_03():
    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
    ]
    assert abjad.mutate._are_contiguous_logical_voice(notes)


def test_mutate__are_contiguous_logical_voice_04():
    """
    Is false for time-reordered leaves in staff.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    leaves = list(staff[2:]) + list(staff[:2])
    assert not abjad.mutate._are_contiguous_logical_voice(leaves)


def test_mutate__are_contiguous_logical_voice_05():
    """
    Is true for unincorporated component.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    assert abjad.mutate._are_contiguous_logical_voice([staff])


def test_mutate__are_contiguous_logical_voice_06():
    """
    Is true for empty input.
    """

    assert abjad.mutate._are_contiguous_logical_voice([])


def test_mutate__are_contiguous_logical_voice_07():
    """
    False when components belonging to same logical voice are ommitted.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8 g'8 a'8")
    abjad.beam(voice[:])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            f'8
            g'8
            a'8
            ]
        }
        """
    )

    leaves = list(voice[:2]) + list(voice[-2:])
    assert not abjad.mutate._are_contiguous_logical_voice(leaves)


def test_mutate__are_contiguous_logical_voice_08():
    """
    False when components belonging to same logical voice are ommitted.
    """

    voice = abjad.Voice(
        r"""
        {
            c'8
            [
            d'8
        }
        {
            e'8
            f'8
        }
        {
            g'8
            a'8
            ]
        }
        """
    )

    components = list(voice[:1]) + list(voice[-1:])
    assert not abjad.mutate._are_contiguous_logical_voice(components)


def test_mutate__are_contiguous_same_parent_01():
    """
    Is true for strictly contiguous leaves in voice.
    Is false for other time orderings of leaves in voice.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")

    assert abjad.mutate._are_contiguous_same_parent(voice[:])

    other = list(reversed(voice[:]))
    assert not abjad.mutate._are_contiguous_same_parent(other)

    components = []
    components.extend(voice[2:])
    components.extend(voice[:2])
    assert not abjad.mutate._are_contiguous_same_parent(components)

    components = []
    components.extend(voice[3:4])
    components.extend(voice[:1])
    assert not abjad.mutate._are_contiguous_same_parent(components)
    components = [voice]
    components.extend(voice[:])
    assert not abjad.mutate._are_contiguous_same_parent(components)


def test_mutate__are_contiguous_same_parent_02():
    """
    Is true for unincorporated components when orphans allowed.
    Is false for unincorporated components when orphans not allowed.
    """

    voice = abjad.Voice(
        r"""
        {
            c'8
            d'8
        }
        {
            e'8
            f'8
        }
        """
    )

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }
        """
    )

    assert abjad.mutate._are_contiguous_same_parent([voice])

    assert abjad.mutate._are_contiguous_same_parent(voice[:])

    assert abjad.mutate._are_contiguous_same_parent(voice[0][:])
    assert abjad.mutate._are_contiguous_same_parent(voice[1][:])

    leaves = abjad.select.leaves(voice)
    assert not abjad.mutate._are_contiguous_same_parent(leaves)


def test_mutate__are_contiguous_same_parent_03():
    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
    ]

    assert abjad.mutate._are_contiguous_same_parent(notes)


def test_mutate__are_contiguous_same_parent_04():
    """
    Empty selection returns true.
    """

    assert abjad.mutate._are_contiguous_same_parent([])


def test_mutate__fuse_leaves_by_immediate_parent_01():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    staff = abjad.Staff([abjad.Container("c'8 c'8"), abjad.Container("c'8 c'8")])
    leaves = abjad.select.leaves(staff)
    abjad.tie(leaves)

    logical_tie = abjad.get.logical_tie(leaves[1])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            {
                c'4
                ~
            }
            {
                c'4
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert len(result) == 2
    assert abjad.wf.wellformed(staff)


def test_mutate__fuse_leaves_by_immediate_parent_02():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    abjad.tie(staff[:])

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'8
            ~
            c'8
            ~
            c'8
            ~
            c'8
        }
        """
    ), print(abjad.lilypond(staff))

    logical_tie = abjad.get.logical_tie(staff[1])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'2
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 1


def test_mutate__fuse_leaves_by_immediate_parent_03():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    note = abjad.Note("c'4")
    logical_tie = abjad.get.logical_tie(note)
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)
    assert len(result) == 1
    assert abjad.wf.wellformed(note)


def test_mutate__fuse_leaves_by_immediate_parent_04():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    voice = abjad.Voice(r"c'16 ~ c'16 ~ c'16 ~ c'16 ~ c'16 r16 r16 r16 r4 r4")
    logical_tie = abjad.get.logical_tie(voice[0])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            ~
            c'16
            r16
            r16
            r16
            r4
            r4
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)
    assert len(result) == 1


def test_mutate__fuse_leaves_by_immediate_parent_05():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    voice = abjad.Voice(r"c'16 ~ c'16 ~ c'16 ~ c'16 ~ c'16 r16 r16 r16 r4 r4")
    abjad.attach(abjad.BeforeGraceContainer("b'16"), voice[0])
    logical_tie = abjad.get.logical_tie(voice[0])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \grace {
                b'16
            }
            c'4
            ~
            c'16
            r16
            r16
            r16
            r4
            r4
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)
    assert len(result) == 1


def test_mutate__fuse_leaves_by_immediate_parent_06():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    voice = abjad.Voice(r"c'16 ~ c'16 ~ c'16 ~ c'16 ~ c'16 r16 r16 r16 r4 r4")
    logical_tie = abjad.get.logical_tie(voice[0])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            ~
            c'16
            r16
            r16
            r16
            r4
            r4
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)
    assert len(result) == 1


def test_mutate__fuse_leaves_by_immediate_parent_07():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    voice = abjad.Voice(r"\tuplet 13/8 { \time 4/4 c'8 ~ c'8 ~ c'16 ~ c'32 r16 } r4 r2")
    logical_tie = abjad.get.logical_tie(voice[0][0])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)
    staff = abjad.Staff([voice])
    abjad.Score([staff], name="Score")

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                \tuplet 13/8
                {
                    \time 4/4
                    c'4
                    ~
                    c'16.
                    r16
                }
                r4
                r2
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 1


def test_mutate__fuse_leaves_by_immediate_parent_08():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    staff = abjad.Staff(r"c'16 ~ c'16 ~ c'16 ~ c'16 ~ c'16 r16 r16 r16 r4 r4")
    abjad.Score([staff], name="Score")
    indicators = (
        abjad.BeforeGraceContainer("b'16"),
        abjad.Clef("alto"),
        abjad.TimeSignature((3, 4)),
        abjad.Articulation("staccato"),
        abjad.Articulation("accent"),
    )
    for indicator in indicators:
        abjad.attach(indicator, staff[0])
    logical_tie = abjad.get.logical_tie(staff[0])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \grace {
                b'16
            }
            \clef "alto"
            \time 3/4
            c'4
            - \accent
            - \staccato
            ~
            c'16
            r16
            r16
            r16
            r4
            r4
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 1


def test_mutate__fuse_leaves_by_immediate_parent_09():
    """
    Fuse leaves in logical tie with same immediate parent, with an indicator at
    the end of the logical tie after fusing.
    """

    voice = abjad.Voice(r"d'8 c'8 ~ c'32 r16 r16 r16 r4")
    staff = abjad.Staff([voice])
    abjad.Score([staff], name="Score")

    indicators = (abjad.TimeSignature((3, 4)), abjad.StartBeam())
    for indicator in indicators:
        abjad.attach(indicator, voice[0])

    indicators = (
        abjad.BeforeGraceContainer("b'16"),
        abjad.Articulation("staccato"),
        abjad.Articulation("accent"),
        abjad.StopBeam(),
    )
    for indicator in indicators:
        abjad.attach(indicator, voice[1])

    logical_tie = abjad.get.logical_tie(voice[1])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                \time 3/4
                d'8
                [
                \grace {
                    b'16
                }
                c'8
                - \accent
                - \staccato
                ~
                c'32
                ]
                r16
                r16
                r16
                r4
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 1


def test_mutate__fuse_leaves_by_immediate_parent_10():
    """
    Fuse leaves in logical tie with same immediate parent, with an indicator at
    every leaf of the logical tie after fusing.
    """

    staff = abjad.Staff(r"c'16 ~ c'16 ~ c'16 ~ c'16 ~ c'16 r16 r16 r16 r4 r4")
    abjad.Score([staff], name="Score")
    indicators = (
        abjad.BeforeGraceContainer("b'16"),
        abjad.Clef("alto"),
        abjad.TimeSignature((3, 4)),
        abjad.Articulation("staccato"),
        abjad.Articulation("accent"),
        abjad.StemTremolo(16),
    )
    for indicator in indicators:
        abjad.attach(indicator, staff[0])
    logical_tie = abjad.get.logical_tie(staff[0])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \grace {
                b'16
            }
            \clef "alto"
            \time 3/4
            c'4
            :16
            - \accent
            - \staccato
            ~
            c'16
            :16
            r16
            r16
            r16
            r4
            r4
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 1


def test_mutate__immediately_precedes_01():
    voice = abjad.Voice("c'8 d'8 e'8 f'8")

    assert abjad.mutate._immediately_precedes(voice[0], voice[1])
    assert abjad.mutate._immediately_precedes(voice[1], voice[2])
    assert abjad.mutate._immediately_precedes(voice[2], voice[3])


def test_mutate__immediately_precedes_02():
    staff = abjad.Staff("c'8 d'8 e'8 f'8")

    assert abjad.mutate._immediately_precedes(staff[0], staff[1])
    assert abjad.mutate._immediately_precedes(staff[1], staff[2])
    assert abjad.mutate._immediately_precedes(staff[2], staff[3])


def test_mutate__immediately_precedes_03():
    container = abjad.Container("c'8 d'8 e'8 f'8")

    assert abjad.mutate._immediately_precedes(container[0], container[1])
    assert abjad.mutate._immediately_precedes(container[1], container[2])
    assert abjad.mutate._immediately_precedes(container[2], container[3])


def test_mutate__immediately_precedes_04():
    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")

    assert abjad.mutate._immediately_precedes(tuplet[0], tuplet[1])
    assert abjad.mutate._immediately_precedes(tuplet[1], tuplet[2])


def test_mutate__immediately_precedes_05():
    voice = abjad.Voice("{ c'8 d'8 e'8 f'8 } { g'8 a'8 b'8 c''8 }")

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8
                b'8
                c''8
            }
        }
        """
    )

    assert abjad.mutate._immediately_precedes(voice[0], voice[1])
    assert abjad.mutate._immediately_precedes(voice[0], voice[1][0])
    assert abjad.mutate._immediately_precedes(voice[0][-1], voice[1])
    assert abjad.mutate._immediately_precedes(voice[0][-1], voice[1][0])


def test_mutate__immediately_precedes_06():
    voice = abjad.Voice(r"\tuplet 3/2 { c'8 d'8 e'8 } \tuplet 3/2 { f'8 e'8 d'8 }")

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \tuplet 3/2
            {
                c'8
                d'8
                e'8
            }
            \tuplet 3/2
            {
                f'8
                e'8
                d'8
            }
        }
        """
    )

    assert abjad.mutate._immediately_precedes(voice[0], voice[1])
    assert abjad.mutate._immediately_precedes(voice[0], voice[1][0])
    assert abjad.mutate._immediately_precedes(voice[0][-1], voice[1])
    assert abjad.mutate._immediately_precedes(voice[0][-1], voice[1][0])


def test_mutate__immediately_precedes_07():
    staff = abjad.Staff(
        [abjad.Voice("c'8 d'8 e'8 f'8"), abjad.Voice("g'8 a'8 b'8 c''8")]
    )

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
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
        """
    )

    assert abjad.mutate._immediately_precedes(staff[0], staff[1])
    assert abjad.mutate._immediately_precedes(staff[0], staff[1][0])
    assert abjad.mutate._immediately_precedes(staff[0][-1], staff[1])
    assert abjad.mutate._immediately_precedes(staff[0][-1], staff[1][0])


def test_mutate__immediately_precedes_08():
    staff = abjad.Staff(
        [abjad.Voice("c'8 d'8 e'8 f'8"), abjad.Voice("g'8 a'8 b'8 c''8")]
    )
    staff[0].name = "foo"
    staff[1].name = "foo"

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \context Voice = "foo"
            {
                c'8
                d'8
                e'8
                f'8
            }
            \context Voice = "foo"
            {
                g'8
                a'8
                b'8
                c''8
            }
        }
        """
    )

    assert abjad.mutate._immediately_precedes(staff[0], staff[1])
    assert abjad.mutate._immediately_precedes(staff[0], staff[1][0])
    assert abjad.mutate._immediately_precedes(staff[0][-1], staff[1])


def test_mutate__immediately_precedes_09():
    staff = abjad.Staff(
        [abjad.Voice("c'8 d'8 e'8 f'8"), abjad.Voice("g'8 a'8 b'8 c''8")]
    )
    staff[0].name = "foo"
    staff[1].name = "bar"

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \context Voice = "foo"
            {
                c'8
                d'8
                e'8
                f'8
            }
            \context Voice = "bar"
            {
                g'8
                a'8
                b'8
                c''8
            }
        }
        """
    )

    assert abjad.mutate._immediately_precedes(staff[0], staff[1])
    assert abjad.mutate._immediately_precedes(staff[0], staff[1][0])
    assert abjad.mutate._immediately_precedes(staff[0][-1], staff[1])


def test_mutate__immediately_precedes_10():
    staff_1 = abjad.Staff([abjad.Voice("c'8 d'8 e'8 f'8")])
    staff_2 = abjad.Staff([abjad.Voice("g'8 a'8 b'8 c''8")])
    container = abjad.Container([staff_1, staff_2])

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \new Staff
            {
                \new Voice
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }
            }
            \new Staff
            {
                \new Voice
                {
                    g'8
                    a'8
                    b'8
                    c''8
                }
            }
        }
        """
    )

    assert abjad.mutate._immediately_precedes(staff_1, staff_2)
    assert abjad.mutate._immediately_precedes(staff_1, staff_2[0])
    assert abjad.mutate._immediately_precedes(staff_1, staff_2[0][0])

    assert abjad.mutate._immediately_precedes(staff_1[0], staff_2)
    assert abjad.mutate._immediately_precedes(staff_1[0], staff_2[0])
    assert abjad.mutate._immediately_precedes(staff_1[0], staff_2[0][0])

    assert abjad.mutate._immediately_precedes(staff_1[0][-1], staff_2)
    assert abjad.mutate._immediately_precedes(staff_1[0][-1], staff_2[0])
    assert abjad.mutate._immediately_precedes(staff_1[0][-1], staff_2[0][0])


def test_mutate__immediately_precedes_11():
    upper_voice_1 = abjad.Voice("c''8 d''8 e''8 f''8")
    upper_voice_2 = abjad.Voice("g''8 a''8 b''8 c''8")
    lower_voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    lower_voice_2 = abjad.Voice("g'8 a'8 b'8 c''8")
    staff_1 = abjad.Staff([upper_voice_1, lower_voice_1])
    staff_2 = abjad.Staff([upper_voice_2, lower_voice_2])
    staff_1.simultaneous = True
    staff_2.simultaneous = True
    container = abjad.Container([staff_1, staff_2])

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \new Staff
            <<
                \new Voice
                {
                    c''8
                    d''8
                    e''8
                    f''8
                }
                \new Voice
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>
            \new Staff
            <<
                \new Voice
                {
                    g''8
                    a''8
                    b''8
                    c''8
                }
                \new Voice
                {
                    g'8
                    a'8
                    b'8
                    c''8
                }
            >>
        }
        """
    )

    assert abjad.mutate._immediately_precedes(staff_1, staff_2)
    assert abjad.mutate._immediately_precedes(staff_1, staff_2[0])
    assert abjad.mutate._immediately_precedes(staff_1, staff_2[0][0])
    assert abjad.mutate._immediately_precedes(staff_1, staff_2[1])
    assert abjad.mutate._immediately_precedes(staff_1, staff_2[1][0])

    assert abjad.mutate._immediately_precedes(staff_1[0], staff_2)
    assert abjad.mutate._immediately_precedes(staff_1[0], staff_2[0])
    assert abjad.mutate._immediately_precedes(staff_1[0], staff_2[0][0])
    assert abjad.mutate._immediately_precedes(staff_1[0], staff_2[1])
    assert abjad.mutate._immediately_precedes(staff_1[0], staff_2[1][0])

    assert abjad.mutate._immediately_precedes(staff_1[0][-1], staff_2)
    assert abjad.mutate._immediately_precedes(staff_1[0][-1], staff_2[0])
    assert abjad.mutate._immediately_precedes(staff_1[0][-1], staff_2[0][0])
    assert abjad.mutate._immediately_precedes(staff_1[0][-1], staff_2[1])
    assert abjad.mutate._immediately_precedes(staff_1[0][-1], staff_2[1][0])

    assert abjad.mutate._immediately_precedes(staff_1[1], staff_2)
    assert abjad.mutate._immediately_precedes(staff_1[1], staff_2[0])
    assert abjad.mutate._immediately_precedes(staff_1[1], staff_2[0][0])
    assert abjad.mutate._immediately_precedes(staff_1[1], staff_2[1])
    assert abjad.mutate._immediately_precedes(staff_1[1], staff_2[1][0])

    assert abjad.mutate._immediately_precedes(staff_1[1][-1], staff_2)
    assert abjad.mutate._immediately_precedes(staff_1[1][-1], staff_2[0])
    assert abjad.mutate._immediately_precedes(staff_1[1][-1], staff_2[0][0])
    assert abjad.mutate._immediately_precedes(staff_1[1][-1], staff_2[1])
    assert abjad.mutate._immediately_precedes(staff_1[1][-1], staff_2[1][0])


def test_mutate__immediately_precedes_12():
    voice = abjad.Voice("{ { c'8 d'8 e'8 f'8 } } { { g'8 a'8 b'8 c''8 } }")

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }
            }
            {
                {
                    g'8
                    a'8
                    b'8
                    c''8
                }
            }
        }
        """
    )

    assert abjad.mutate._immediately_precedes(voice[0], voice[1])
    assert abjad.mutate._immediately_precedes(voice[0], voice[1][0])
    assert abjad.mutate._immediately_precedes(voice[0], voice[1][0][0])

    assert abjad.mutate._immediately_precedes(voice[0][0], voice[1])
    assert abjad.mutate._immediately_precedes(voice[0][0], voice[1][0])
    assert abjad.mutate._immediately_precedes(voice[0][0], voice[1][0][0])

    assert abjad.mutate._immediately_precedes(voice[0][0][-1], voice[1])
    assert abjad.mutate._immediately_precedes(voice[0][0][-1], voice[1][0])
    assert abjad.mutate._immediately_precedes(voice[0][0][-1], voice[1][0][0])
