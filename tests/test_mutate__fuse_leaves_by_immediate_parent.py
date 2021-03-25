import abjad


def test_mutate__fuse_leaves_by_immediate_parent_01():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    staff = abjad.Staff([abjad.Container("c'8 c'8"), abjad.Container("c'8 c'8")])
    leaves = abjad.select(staff).leaves()
    abjad.tie(leaves)

    logical_tie = abjad.get.logical_tie(leaves[1])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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

    assert abjad.lilypond(staff) == abjad.String.normalize(
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

    assert abjad.lilypond(staff) == abjad.String.normalize(
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

    assert abjad.lilypond(voice) == abjad.String.normalize(
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

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    abjad.attach(abjad.MetronomeMark((1, 4), 120), voice[0])
    logical_tie = abjad.get.logical_tie(voice[0])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \tempo 4=120
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

    voice = abjad.Voice(r"\times 8/13 { \time 4/4 c'8 ~ c'8 ~ c'16 ~ c'32 r16 } r4 r2")
    logical_tie = abjad.get.logical_tie(voice[0][0])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)
    staff = abjad.Staff([voice])

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                \times 8/13
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

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \grace {
                b'16
            }
            \time 3/4
            \clef "alto"
            c'4
            - \staccato
            - \accent
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

    staff = abjad.Staff(r"d'8 c'8 ~ c'32 r16 r16 r16 r4")

    indicators = (abjad.TimeSignature((3, 4)), abjad.StartBeam())
    for indicator in indicators:
        abjad.attach(indicator, staff[0])

    indicators = (
        abjad.BeforeGraceContainer("b'16"),
        abjad.Articulation("staccato"),
        abjad.Articulation("accent"),
        abjad.StopBeam(),
    )
    for indicator in indicators:
        abjad.attach(indicator, staff[1])

    logical_tie = abjad.get.logical_tie(staff[1])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            d'8
            [
            \grace {
                b'16
            }
            c'8
            - \staccato
            - \accent
            ~
            c'32
            ]
            r16
            r16
            r16
            r4
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

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \grace {
                b'16
            }
            \time 3/4
            \clef "alto"
            c'4
            :16
            - \staccato
            - \accent
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
