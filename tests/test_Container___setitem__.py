import abjad


def test_Container___setitem___01():
    """
    Replaces in-score leaf with out-of-score leaf.
    """

    voice = abjad.Voice("c'8 [ d'8 ] e'8 f'8")

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    )

    voice[1] = abjad.Note("c''8")

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            c''8
            e'8
            f'8
        }
        """
    )

    assert abjad.wf.wellformed(voice)


def test_Container___setitem___02():
    """
    Replaces in-score leaf with out-of-score container.
    """

    voice = abjad.Voice("c'8 [ d'8 ] e'8 f'8")

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    )

    voice[1] = abjad.Container("c'16 c'16 c'16")

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            {
                c'16
                c'16
                c'16
            }
            e'8
            f'8
        }
        """
    )

    assert abjad.wf.wellformed(voice)


def test_Container___setitem___03():
    """
    Replaces in-score container with out-of-score leaf.
    """

    voice = abjad.Voice("{ c'8 [ d'8 } { e'8 f'8 ] }")

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    )

    voice[1] = abjad.Note("c''8")

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
            c''8
        }
        """
    )

    assert abjad.wf.wellformed(voice)


def test_Container___setitem___04():
    """
    Replaces in-score container with out-of-score tuplet.
    """

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select(voice).leaves()
    abjad.beam(leaves)

    assert abjad.lilypond(voice) == abjad.String.normalize(
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

    voice[1] = abjad.Tuplet(abjad.Multiplier(2, 3), "c'8 d'8 e'8")

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
            \times 2/3 {
                c'8
                d'8
                e'8
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_Container___setitem___05():
    """
    Replaces in-score container with out-of-score leaf.
    """

    voice = abjad.Voice("{ c'8 [ d'8 } { e'8 f'8 ] }")

    assert abjad.lilypond(voice) == abjad.String.normalize(
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

    voice[1] = abjad.Note("c''8")

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
            c''8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_Container___setitem___06():
    """
    Replaces in-score container with out-of-score leaf.
    """

    voice = abjad.Voice(
        [abjad.Container("c'8 c'8 c'8 c'8"), abjad.Container("c'8 c'8 c'8 c'8")]
    )
    voice = abjad.Voice("{ c'8 d'8 e'8 f'8 } { g'8 a'8 b'8 c''8 }")

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    ), print(abjad.lilypond(voice))

    voice[1] = abjad.Rest("r2")

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                d'8
                e'8
                f'8
            }
            r2
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_Container___setitem___07():
    """
    Replaces note in one score with note from another score.
    """

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
        abjad.Note("g'8"),
        abjad.Note("a'8"),
    ]

    voice_1 = abjad.Voice(notes[:3])
    abjad.beam(voice_1[:])

    assert abjad.lilypond(voice_1) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            ]
        }
        """
    ), print(abjad.lilypond(voice_1))

    voice_2 = abjad.Voice(notes[3:])
    abjad.beam(voice_2[:])

    assert abjad.lilypond(voice_2) == abjad.String.normalize(
        r"""
        \new Voice
        {
            f'8
            [
            g'8
            a'8
            ]
        }
        """
    ), print(abjad.lilypond(voice_2))

    voice_1[1] = voice_2[1]

    assert abjad.lilypond(voice_1) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            g'8
            e'8
            ]
        }
        """
    ), print(abjad.lilypond(voice_1))

    assert abjad.wf.wellformed(voice_1)

    assert abjad.lilypond(voice_2) == abjad.String.normalize(
        r"""
        \new Voice
        {
            f'8
            [
            a'8
            ]
        }
        """
    ), print(abjad.lilypond(voice_2))

    assert abjad.wf.wellformed(voice_2)


def test_Container___setitem___08():
    r"""
    Replaces note in one score with container from another score.
    """

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
        abjad.Note("g'8"),
        abjad.Note("a'8"),
        abjad.Note("b'8"),
    ]
    voice_1 = abjad.Voice(notes[:3])
    abjad.beam(voice_1[:])

    assert abjad.lilypond(voice_1) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            ]
        }
        """
    ), print(abjad.lilypond(voice_1))

    voice_2 = abjad.Voice(notes[3:])
    abjad.mutate.wrap(voice_2[1:3], abjad.Container())
    leaves = abjad.select(voice_2).leaves()
    leaves = abjad.select(voice_2[1]).leaves()
    abjad.slur(leaves)

    assert abjad.lilypond(voice_2) == abjad.String.normalize(
        r"""
        \new Voice
        {
            f'8
            {
                g'8
                (
                a'8
                )
            }
            b'8
        }
        """
    ), print(abjad.lilypond(voice_2))

    voice_1[1] = voice_2[1]

    assert abjad.lilypond(voice_1) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            {
                g'8
                (
                a'8
                )
            }
            e'8
            ]
        }
        """
    ), print(abjad.lilypond(voice_1))

    assert abjad.wf.wellformed(voice_1)

    assert abjad.lilypond(voice_2) == abjad.String.normalize(
        r"""
        \new Voice
        {
            f'8
            b'8
        }
        """
    ), print(abjad.lilypond(voice_2))

    assert abjad.wf.wellformed(voice_2)


def test_Container___setitem___09():
    r"""Sets leaf between unspanned components."""

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    staff[2:2] = [abjad.Note("g'8")]

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            d'8
            g'8
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_Container___setitem___10():
    r"""Sets leaf between spanned compoennts."""

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.beam(staff[:])
    note = abjad.Note("g'8")
    staff[2:2] = [note]

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'8
            g'8
            e'8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_Container___setitem___11():
    r"""Sets multiple leaves between spanned components."""

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
        abjad.Note("g'8"),
        abjad.Note("a'8"),
    ]

    beginning = notes[:2]
    middle = notes[2:4]
    end = notes[4:]

    staff = abjad.Staff(beginning + end)
    abjad.beam(staff[:])

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'8
            g'8
            a'8
            ]
        }
        """
    ), print(abjad.lilypond(staff))

    staff[2:2] = middle

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
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
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_Container___setitem___12():
    r"""Replaces multiple spanned leaves with with single leaf."""

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.beam(staff[:])
    note = abjad.Note("c''8")
    staff[1:3] = [note]

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            c''8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_Container___setitem___13():
    r"""Replaces three spanned leaves with three different leaves."""

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.beam(staff[:])
    notes = [abjad.Note("b'8"), abjad.Note("a'8"), abjad.Note("g'8")]
    staff[1:3] = notes

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            b'8
            a'8
            g'8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_Container___setitem___14():
    r"""Replaces in-score container with contents of container."""

    staff = abjad.Staff("{ c'8 [ d'8 } { e'8 f'8 ] }")

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
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
    ), print(abjad.lilypond(staff))

    container = staff[0]
    staff[0:1] = container[:]

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'8
            {
                e'8
                f'8
                ]
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(container) == 0


def test_Container___setitem___15():
    r"""Sets first slice of staff equal to first element of first container in
    staff.
    """

    staff = abjad.Staff("{ c'8 [ d'8 } { e'8 f'8 ] }")

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
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
    ), print(abjad.lilypond(staff))

    staff[0:0] = staff[0][:1]

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            {
                d'8
            }
            {
                e'8
                f'8
                ]
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_Container___setitem___16():
    r"""Sets first slice of staff equal to contents of first container in
    staff.

    Empties first container in staff.

    Leaves empty container in staff.
    """

    staff = abjad.Staff("{ c'8 [ d'8 } { e'8 f'8 ] }")

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
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
    ), print(abjad.lilypond(staff))

    staff[0:0] = staff[0][:]

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'8
            {
            }
            {
                e'8
                f'8
                ]
            }
        }
        """
    ), print(abjad.lilypond(staff))


def test_Container___setitem___17():
    r"""Set first slice of staff equal to contents of first container in staff;
    empties first container in staff.

    Sets contents of empty first container in staff equal to first component in
    second container in staff.
    """

    staff = abjad.Staff("{ c'8 [ d'8 } { e'8 f'8 ] }")

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
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
    ), print(abjad.lilypond(staff))

    container = staff[0]
    staff[0:0] = container[:]
    container[0:0] = staff[-1][:1]

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'8
            {
                e'8
            }
            {
                f'8
                ]
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_Container___setitem___18():
    r"""
    Extremely small coequal indices indicate first slice in staff.
    """

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    voice[-1000:-1000] = [abjad.Rest("r8")]

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            r8
            c'8
            [
            d'8
            e'8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            r8
            c'8
            [
            d'8
            e'8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_Container___setitem___19():
    r"""Extremely large coequal indices indicate last slice in staff."""

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    voice[1000:1000] = [abjad.Rest("r8")]

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            f'8
            ]
            r8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_Container___setitem___20():
    r"""
    You can use setitem to empty the contents of a container.
    """

    staff = abjad.Staff("c'8 d'8 [ e'8 ] f'8")
    inner_container = abjad.Container()
    abjad.mutate.wrap(staff[1:3], inner_container)
    outer_container = abjad.Container()
    abjad.mutate.wrap(inner_container, outer_container)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            {
                {
                    d'8
                    [
                    e'8
                    ]
                }
            }
            f'8
        }
        """
    ), print(abjad.lilypond(staff))

    # sets contents of outer container to nothing
    outer_container[:] = []

    # outer container is empty and remains in score
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            {
            }
            f'8
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.lilypond(inner_container) == abjad.String.normalize(
        r"""
        {
            d'8
            [
            e'8
            ]
        }
        """
    ), print(abjad.lilypond(inner_container))

    # ALTERNATIVE: use del(container)
    staff = abjad.Staff("c'8 d'8 [ e'8 ] f'8")
    inner_container = abjad.Container()
    abjad.mutate.wrap(staff[1:3], inner_container)
    outer_container = abjad.Container()
    abjad.mutate.wrap(inner_container, outer_container)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            {
                {
                    d'8
                    [
                    e'8
                    ]
                }
            }
            f'8
        }
        """
    ), print(abjad.lilypond(staff))

    # deletes outer container
    del outer_container[:]

    # outer container is empty and remains in score (as before)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            {
            }
            f'8
        }
        """
    ), print(abjad.lilypond(staff))

    # inner container leaves are still spanned
    assert abjad.lilypond(inner_container) == abjad.String.normalize(
        r"""
        {
            d'8
            [
            e'8
            ]
        }
        """
    ), print(abjad.lilypond(inner_container))
