import abjad


def test_mutate__set_leaf_duration_01():
    """
    Change leaf to tied duration.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:2])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._set_leaf_duration(voice[1], abjad.Duration(5, 32))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ~
            d'32
            ]
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__set_leaf_duration_02():
    """
    Change tied leaf to tied value.
    Duplicate ties are not created.
    """

    voice = abjad.Voice("c'8 c'8 c'8 c'8")
    abjad.tie(voice[:2])
    abjad.beam(voice[:2])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            ~
            c'8
            ]
            c'8
            c'8
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._set_leaf_duration(voice[1], abjad.Duration(5, 32))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            ~
            c'8
            ~
            c'32
            ]
            c'8
            c'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__set_leaf_duration_03():
    """
    Change leaf to nontied duration.
    Same as voice.written_duration = abjad.Duration(3, 16).
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:2])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._set_leaf_duration(voice[1], abjad.Duration(3, 16))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8.
            ]
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__set_leaf_duration_04():
    """
    Change leaf to tied duration without power-of-two denominator.
    abjad.Tuplet inserted over new tied notes.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:2])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._set_leaf_duration(voice[1], abjad.Duration(5, 48))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \tweak edge-height #'(0.7 . 0)
            \tuplet 3/2
            {
                d'8
                ~
                d'32
                ]
            }
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__set_leaf_duration_05():
    """
    Change leaf to untied duration without power-of-two denominator.
    Tuplet inserted over input leaf.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:2])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._set_leaf_duration(voice[1], abjad.Duration(1, 12))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \tweak edge-height #'(0.7 . 0)
            \tuplet 3/2
            {
                d'8
                ]
            }
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__set_leaf_duration_06():
    """
    Change leaf with LilyPond multiplier to untied duration with
    power-of-two denominator. LilyPond multiplier changes but leaf written
    duration does not.
    """

    note = abjad.Note(0, (1, 8), multiplier=(1, 2))

    assert abjad.lilypond(note) == "c'8 * 1/2"

    abjad.mutate._set_leaf_duration(note, abjad.Duration(1, 32))

    assert abjad.wf.wellformed(note)
    assert abjad.lilypond(note) == "c'8 * 1/4"


def test_mutate__set_leaf_duration_07():
    """
    Change leaf with LilyPond multiplier to untied duration with
    power-of-two denominator. LilyPond multiplier changes but leaf
    written duration does not.
    """

    note = abjad.Note(0, (1, 8), multiplier=(1, 2))

    assert abjad.lilypond(note) == "c'8 * 1/2"

    abjad.mutate._set_leaf_duration(note, abjad.Duration(3, 32))

    assert abjad.wf.wellformed(note)
    assert abjad.lilypond(note) == "c'8 * 3/4"


def test_mutate__set_leaf_duration_08():
    """
    Change leaf with LilyPond multiplier to tied duration with
    power-of-two denominator. LilyPond multiplier changes but leaf
    written duration does not.
    """

    note = abjad.Note(0, (1, 8), multiplier=(1, 2))

    assert abjad.lilypond(note) == "c'8 * 1/2"

    abjad.mutate._set_leaf_duration(note, abjad.Duration(5, 32))

    assert abjad.wf.wellformed(note)
    assert abjad.lilypond(note) == "c'8 * 5/4"


def test_mutate__set_leaf_duration_09():
    """
    Change leaf with LilyPond multiplier to duration without
    power-of-two denominator. LilyPond multiplier changes but leaf
    written duration does not.
    """

    note = abjad.Note(0, (1, 8), multiplier=(1, 2))

    assert abjad.lilypond(note) == "c'8 * 1/2"

    abjad.mutate._set_leaf_duration(note, abjad.Duration(1, 24))

    assert abjad.wf.wellformed(note)
    assert abjad.lilypond(note) == "c'8 * 1/3"


def test_mutate__set_leaf_duration_10():
    """
    Change leaf with LilyPond multiplier.
    Change to tie-necessitating duration without power-of-two denominator.
    LilyPond multiplier changes but leaf written duration does not.
    """

    note = abjad.Note(0, (1, 8), multiplier=(1, 2))

    assert abjad.lilypond(note) == "c'8 * 1/2"

    abjad.mutate._set_leaf_duration(note, abjad.Duration(5, 24))

    assert abjad.wf.wellformed(note)
    assert abjad.lilypond(note) == "c'8 * 5/3"


def test_mutate__set_leaf_duration_11():
    """
    Change rest duration.
    """

    voice = abjad.Voice("c'8 r8 e'8 f'8")
    abjad.beam(voice[:3])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            r8
            e'8
            ]
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._set_leaf_duration(voice[1], abjad.Duration(5, 32))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            r8
            r32
            e'8
            ]
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__split_container_by_duration_01():
    """
    Split one container in score.
    Adds tie after split.
    """

    voice = abjad.Voice()
    voice.append(abjad.Container("c'8 d'8"))
    voice.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
                d'8
                ]
            }
            {
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._split_container_by_duration(voice[0], abjad.Duration(1, 32))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'32
                [
                (
                ~
            }
            {
                c'16.
                d'8
                ]
            }
            {
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__split_container_by_duration_02():
    """
    Split in-score container at split offset with non-power-of-two denominator.
    """

    voice = abjad.Voice()
    voice.append(abjad.Container("c'8 d'8"))
    voice.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
                d'8
                ]
            }
            {
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._split_container_by_duration(voice[0], abjad.Duration(1, 5))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
                \tweak edge-height #'(0.7 . 0)
                \tuplet 5/4
                {
                    d'16.
                    ~
                }
            }
            {
                \tweak edge-height #'(0.7 . 0)
                \tuplet 5/4
                {
                    d'16
                    ]
                }
            }
            {
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__split_leaf_by_durations_01():
    """
    Splits note into assignable notes.

    Does tie split notes.
    """

    staff = abjad.Staff("c'8 [ d'8 e'8 ]")

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'8
            e'8
            ]
        }
        """
    ), print(abjad.lilypond(staff))

    abjad.mutate._split_leaf_by_durations(staff[1], [abjad.Duration(1, 32)])

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'32
            ~
            d'16.
            e'8
            ]
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_mutate__split_leaf_by_durations_02():
    """
    REGRESSION.

    Splits note into tuplet monads and then fuses monads.

    Ties split notes.

    This test comes from #272 in GitHub.
    """

    voice = abjad.Voice(r"\tuplet 3/2 { c'8 [ d'8 e'8 ] }")
    leaf = abjad.get.leaf(voice, 0)
    abjad.mutate._split_leaf_by_durations(leaf, [abjad.Duration(1, 20)])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \tuplet 3/2
            {
                \tuplet 5/4
                {
                    c'16.
                    [
                    ~
                    c'16
                }
                d'8
                e'8
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__split_leaf_by_durations_03():
    """
    Leaf duration less than split duration produces no change.
    """

    staff = abjad.Staff("c'4")
    abjad.mutate._split_leaf_by_durations(staff[0], [abjad.Duration(3, 4)])

    assert len(staff) == 1
    assert isinstance(staff[0], abjad.Note)
    assert staff[0].written_duration == abjad.Duration(1, 4)


def test_mutate__split_leaf_by_durations_04():
    """
    Returns selection of new leaves.
    """

    note = abjad.Note("c'4")
    new_leaves = abjad.mutate._split_leaf_by_durations(note, [abjad.Duration(1, 16)])
    assert all(isinstance(_, abjad.Note) for _ in new_leaves)


def test_mutate__split_leaf_by_durations_05():
    """
    Lone spanned leaf results in two spanned leaves.
    """

    staff = abjad.Staff([abjad.Note("c'4")])
    abjad.mutate._split_leaf_by_durations(staff[0], [abjad.Duration(1, 8)])

    assert len(staff) == 2
    assert abjad.wf.wellformed(staff)


def test_mutate__split_leaf_by_durations_06():
    """
    Returns three leaves with two tied.
    """

    staff = abjad.Staff([abjad.Note("c'4")])
    new_leaves = abjad.mutate._split_leaf_by_durations(
        staff[0], [abjad.Duration(5, 32)]
    )

    assert all(isinstance(_, abjad.Note) for _ in new_leaves)
    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'8
            ~
            c'32
            ~
            c'16.
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_mutate__split_leaf_by_durations_07():
    """
    After grace notes are removed from first split leaf.
    """

    note = abjad.Note("c'4")
    after_grace = abjad.AfterGraceContainer([abjad.Note(0, (1, 32))])
    abjad.attach(after_grace, note)

    new_leaves = abjad.mutate._split_leaf_by_durations(note, [abjad.Duration(1, 8)])
    staff = abjad.Staff(new_leaves)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'8
            ~
            \afterGrace
            c'8
            {
                c'32
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.get.after_grace_container(new_leaves[0]) is None
    assert len(abjad.get.after_grace_container(new_leaves[1])) == 1
    abjad.wf.wellformed(staff)


def test_mutate__split_leaf_by_durations_08():
    """
    After grace notes are removed from first split leaf.
    """

    note = abjad.Note("c'4")
    grace = abjad.AfterGraceContainer([abjad.Note(0, (1, 32))])
    abjad.attach(grace, note)

    new_leaves = abjad.mutate._split_leaf_by_durations(note, [abjad.Duration(5, 32)])
    staff = abjad.Staff(new_leaves)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'8
            ~
            c'32
            ~
            \afterGrace
            c'16.
            {
                c'32
            }
        }
        """
    ), print(abjad.lilypond(staff))

    abjad.wf.wellformed(staff)


def test_mutate__split_leaf_by_durations_09():
    """
    Grace notes are removed from second split leaf.
    """

    note = abjad.Note("c'4")
    grace = abjad.BeforeGraceContainer([abjad.Note(0, (1, 32))])
    abjad.attach(grace, note)

    new_leaves = abjad.mutate._split_leaf_by_durations(note, [abjad.Duration(1, 16)])
    staff = abjad.Staff(new_leaves)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \grace {
                c'32
            }
            c'16
            ~
            c'8.
        }
        """
    ), print(abjad.lilypond(staff))

    abjad.wf.wellformed(staff)


def test_mutate__split_leaf_by_durations_10():
    """
    Split one leaf in score.
    Ties after split.
    """

    voice = abjad.Voice()
    voice.append(abjad.Container("c'8 d'8"))
    voice.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
                d'8
                ]
            }
            {
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._split_leaf_by_durations(leaves[0], [abjad.Duration(1, 32)])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'32
                [
                (
                ~
                c'16.
                d'8
                ]
            }
            {
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_split_01():
    """
    Cyclically splits note in score.
    """

    voice = abjad.Voice()
    voice.append(abjad.Container("c'8 d'8"))
    voice.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
                d'8
                ]
            }
            {
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    notes = voice[0][1:2]
    result = abjad.mutate.split(notes, [abjad.Duration(3, 64)], cyclic=True)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
                d'32.
                ~
                d'32.
                ~
                d'32
                ]
            }
            {
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)
    assert len(result) == 3


def test_mutate_split_02():
    """
    Cyclically splits consecutive notes in score.
    """

    voice = abjad.Voice([abjad.Container("c'8 d'"), abjad.Container("e'8 f'")])
    staff = abjad.Staff([voice])
    abjad.Score([staff], name="Score")
    for container in voice:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \time 2/8
                    c'8
                    [
                    (
                    d'8
                    ]
                }
                {
                    \time 2/8
                    e'8
                    [
                    f'8
                    )
                    ]
                }
            }
        }
        """
    ), print(abjad.lilypond(staff))

    result = abjad.mutate.split(leaves, [abjad.Duration(3, 32)], cyclic=True)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \time 2/8
                    c'16.
                    [
                    (
                    ~
                    c'32
                    d'16
                    ~
                    d'16
                    ]
                }
                {
                    \time 2/8
                    e'32
                    [
                    ~
                    e'16.
                    f'16.
                    ~
                    f'32
                    )
                    ]
                }
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 6


def test_mutate_split_03():
    """
    Cyclically splits note in score.
    """

    voice = abjad.Voice([abjad.Container("c'8 d'"), abjad.Container("e'8 f'")])
    staff = abjad.Staff([voice])
    abjad.Score([staff], name="Score")
    for container in voice:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \time 2/8
                    c'8
                    [
                    (
                    d'8
                    ]
                }
                {
                    \time 2/8
                    e'8
                    [
                    f'8
                    )
                    ]
                }
            }
        }
        """
    ), print(abjad.lilypond(staff))

    notes = voice[0][1:]
    result = abjad.mutate.split(notes, [abjad.Duration(1, 32)], cyclic=True)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \time 2/8
                    c'8
                    [
                    (
                    d'32
                    ~
                    d'32
                    ~
                    d'32
                    ~
                    d'32
                    ]
                }
                {
                    \time 2/8
                    e'8
                    [
                    f'8
                    )
                    ]
                }
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 4


def test_mutate_split_04():
    """
    Cyclically splits consecutive notes in score.
    """

    voice = abjad.Voice([abjad.Container("c'8 d'"), abjad.Container("e'8 f'")])
    staff = abjad.Staff([voice])
    abjad.Score([staff], name="Score")
    for container in voice:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \time 2/8
                    c'8
                    [
                    (
                    d'8
                    ]
                }
                {
                    \time 2/8
                    e'8
                    [
                    f'8
                    )
                    ]
                }
            }
        }
        """
    ), print(abjad.lilypond(staff))

    result = abjad.mutate.split(leaves, [abjad.Duration(1, 16)], cyclic=True)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \time 2/8
                    c'16
                    [
                    (
                    ~
                    c'16
                    d'16
                    ~
                    d'16
                    ]
                }
                {
                    \time 2/8
                    e'16
                    [
                    ~
                    e'16
                    f'16
                    ~
                    f'16
                    )
                    ]
                }
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 8


def test_mutate_split_05():
    """
    Cyclically splits measure in score.
    """

    voice = abjad.Voice([abjad.Container("c'8 d'"), abjad.Container("e'8 f'")])
    staff = abjad.Staff([voice])
    abjad.Score([staff], name="Score")
    for container in voice:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \time 2/8
                    c'8
                    [
                    (
                    d'8
                    ]
                }
                {
                    \time 2/8
                    e'8
                    [
                    f'8
                    )
                    ]
                }
            }
        }
        """
    ), print(abjad.lilypond(staff))

    measures = voice[:1]
    result = abjad.mutate.split(measures, [abjad.Duration(1, 16)], cyclic=True)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \time 2/8
                    c'16
                    [
                    (
                    ~
                }
                {
                    c'16
                }
                {
                    d'16
                    ~
                }
                {
                    d'16
                    ]
                }
                {
                    \time 2/8
                    e'8
                    [
                    f'8
                    )
                    ]
                }
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 4


def test_mutate_split_06():
    """
    Cyclically splits consecutive measures in score.
    """

    voice = abjad.Voice([abjad.Container("c'8 d'"), abjad.Container("e'8 f'")])
    staff = abjad.Staff([voice])
    abjad.Score([staff], name="Score")
    for container in voice:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \time 2/8
                    c'8
                    [
                    (
                    d'8
                    ]
                }
                {
                    \time 2/8
                    e'8
                    [
                    f'8
                    )
                    ]
                }
            }
        }
        """
    ), print(abjad.lilypond(staff))

    measures = voice[:]
    result = abjad.mutate.split(measures, [abjad.Duration(3, 32)], cyclic=True)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \time 2/8
                    c'16.
                    [
                    (
                    ~
                }
                {
                    c'32
                    d'16
                    ~
                }
                {
                    d'16
                    ]
                }
                {
                    \time 2/8
                    e'32
                    [
                    ~
                }
                {
                    e'16.
                }
                {
                    f'16.
                    ~
                }
                {
                    f'32
                    )
                    ]
                }
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 6


def test_mutate_split_07():
    """
    Splits tuplet in score
    """

    voice = abjad.Voice()
    voice.append(abjad.Tuplet((2, 3), "c'8 d'8 e'8"))
    voice.append(abjad.Tuplet((2, 3), "f'8 g'8 a'8"))
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)

    tuplets = voice[1:2]
    abjad.mutate.split(tuplets, [abjad.Duration(1, 12)])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \tuplet 3/2
            {
                c'8
                [
                d'8
                e'8
            }
            \tweak edge-height #'(0.7 . 0)
            \tuplet 3/2
            {
                f'8
            }
            \tweak edge-height #'(0.7 . 0)
            \tuplet 3/2
            {
                g'8
                a'8
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_split_08():
    """
    Splits in-score measure with power-of-two denominator.
    """

    voice = abjad.Voice()
    voice.append(abjad.Container("c'8 d'8 e'8"))
    voice.append(abjad.Container("f'8 g'8 a'8"))
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)

    measures = voice[1:2]
    abjad.mutate.split(measures, [abjad.Duration(1, 8)])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
                e'8
            }
            {
                f'8
            }
            {
                g'8
                a'8
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_split_09():
    """
    Splits container in middle.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")

    result = abjad.mutate.split([voice], [abjad.Duration(1, 4)])

    assert not len(voice)

    voice_1 = result[0][0]
    voice_2 = result[1][0]

    assert abjad.lilypond(voice_1) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            d'8
        }
        """
    ), print(abjad.lilypond(voice_1))

    assert abjad.wf.wellformed(voice_1)

    assert abjad.lilypond(voice_2) == abjad.string.normalize(
        r"""
        \new Voice
        {
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice_2))

    assert abjad.wf.wellformed(voice_2)


def test_mutate_split_10():
    """
    Splits voice at negative index.
    """

    staff = abjad.Staff([abjad.Voice("c'8 d'8 e'8 f'8")])
    voice = staff[0]

    result = abjad.mutate.split([voice], [abjad.Duration(1, 4)])

    left = result[0][0]
    right = result[1][0]

    assert abjad.lilypond(left) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            d'8
        }
        """
    ), print(abjad.lilypond(left))

    assert abjad.lilypond(right) == abjad.string.normalize(
        r"""
        \new Voice
        {
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(right))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                c'8
                d'8
            }
            \new Voice
            {
                e'8
                f'8
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_mutate_split_11():
    """
    Splits container in score.
    """

    voice = abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8")])
    container = voice[0]
    leaves = abjad.select.leaves(container)
    abjad.beam(leaves)

    result = abjad.mutate.split([container], [abjad.Duration(1, 4)])

    left = result[0][0]
    right = result[1][0]

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
            {
                e'8
                f'8
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.lilypond(left) == abjad.string.normalize(
        r"""
        {
            c'8
            [
            d'8
        }
        """
    ), print(abjad.lilypond(left))

    assert abjad.lilypond(right) == abjad.string.normalize(
        r"""
        {
            e'8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(right))

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
        }
        """
    ), print(abjad.lilypond(container))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
            {
                e'8
                f'8
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_split_12():
    """
    Splits tuplet in score.
    """

    tuplet = abjad.Tuplet((4, 5), "c'8 c'8 c'8 c'8 c'8")
    voice = abjad.Voice([tuplet])
    staff = abjad.Staff([voice])
    abjad.beam(tuplet[:])

    result = abjad.mutate.split([tuplet], [abjad.Duration(1, 5)])

    left = result[0][0]
    right = result[1][0]

    assert abjad.lilypond(left) == abjad.string.normalize(
        r"""
        \tweak edge-height #'(0.7 . 0)
        \tuplet 5/4
        {
            c'8
            [
            c'8
        }
        """
    ), print(abjad.lilypond(left))

    assert abjad.lilypond(right) == abjad.string.normalize(
        r"""
        \tweak edge-height #'(0.7 . 0)
        \tuplet 5/4
        {
            c'8
            c'8
            c'8
            ]
        }
        """
    ), print(abjad.lilypond(right))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/4
        {
        }
        """
    ), print(abjad.lilypond(tuplet))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \tweak edge-height #'(0.7 . 0)
            \tuplet 5/4
            {
                c'8
                [
                c'8
            }
            \tweak edge-height #'(0.7 . 0)
            \tuplet 5/4
            {
                c'8
                c'8
                c'8
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                \tweak edge-height #'(0.7 . 0)
                \tuplet 5/4
                {
                    c'8
                    [
                    c'8
                }
                \tweak edge-height #'(0.7 . 0)
                \tuplet 5/4
                {
                    c'8
                    c'8
                    c'8
                    ]
                }
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_mutate_split_13():
    """
    Splits cyclically.
    """

    voice = abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    note = voice[0]
    abjad.mutate.split(note, [abjad.Duration(1, 8), abjad.Duration(3, 8)], cyclic=True)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
            }
            {
                d'8
                e'8
                f'8
            }
            {
                g'8
            }
            {
                a'8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_split_14():
    """
    Cyclically splits all components in container.
    """

    voice = abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8")])
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
                d'8
                e'8
                f'8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    container = voice[0]
    abjad.mutate.split(container, [abjad.Duration(1, 8)], cyclic=True)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
            }
            {
                d'8
            }
            {
                e'8
            }
            {
                f'8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_split_15():
    """
    Splits leaf at non-assignable, non-power-of-two offset.
    """

    staff = abjad.Staff("c'4")

    notes = staff[:1]
    abjad.mutate.split(notes, [abjad.Duration(5, 24)])

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \tuplet 3/2
            {
                c'4
                ~
                c'16
                ~
                c'16
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
