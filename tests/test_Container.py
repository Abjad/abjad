import copy

import pytest

import abjad


def test_Container___contains___01():
    note = abjad.Note("c'4")
    voice = abjad.Voice([abjad.Note("c'4")])

    assert note not in voice


def test_Container___copy___01():
    """
    Containers copy ``simultaneous`` property.
    """

    container_1 = abjad.Container([abjad.Voice("c'8 d'8"), abjad.Voice("c''8 b'8")])
    container_1.set_simultaneous(True)
    container_2 = copy.copy(container_1)

    assert abjad.lilypond(container_1) == abjad.string.normalize(
        r"""
        <<
            \new Voice
            {
                c'8
                d'8
            }
            \new Voice
            {
                c''8
                b'8
            }
        >>
        """
    )

    assert abjad.lilypond(container_2) == abjad.string.normalize(
        r"""
        <<
        >>
        """
    )

    assert container_1 is not container_2


def test_Container___delitem___01():
    """
    Deletes in-score container.
    """

    voice = abjad.Voice("{ c'8 ( d'8 ) } { e'8 ( f'8 ) }")

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                (
                d'8
                )
            }
            {
                e'8
                (
                f'8
                )
            }
        }
        """
    )

    container = voice[0]
    del voice[0]

    # container no longer appears in score
    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                e'8
                (
                f'8
                )
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.is_wellformed(voice)

    # container leaves are still slurred
    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'8
            (
            d'8
            )
        }
        """
    ), print(abjad.lilypond(container))

    assert abjad.wf.is_wellformed(container)


def test_Container___delitem___02():
    """
    Deletes in-score leaf.
    """

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del voice[1]

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            e'8
            f'8
            ]
        }
        """
    )

    assert abjad.wf.is_wellformed(voice)


def test_Container___delitem___03():
    """
    Deletes slice in middle of container.
    """

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del voice[1:3]

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            f'8
            ]
        }
        """
    )

    assert abjad.wf.is_wellformed(voice)


def test_Container___delitem___04():
    """
    Delete slice at beginning of container.
    """

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del voice[:2]

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            e'8
            f'8
            ]
        }
        """
    )

    assert abjad.wf.is_wellformed(voice, do_not_check_overlapping_beams=True)


def test_Container___delitem___05():
    """
    Deletes slice at end of container.
    """

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del voice[2:]

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
        }
        """
    )

    assert abjad.wf.is_wellformed(voice)


def test_Container___delitem___06():
    """
    Deletes container contents.
    """

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del voice[:]

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
        }
        """
    )

    assert not len(voice)


def test_Container___delitem___07():
    """
    Deletes leaf from tuplet.
    """

    tuplet = abjad.Tuplet("3:2", "c'8 [ d'8 e'8 ]")
    del tuplet[1]
    abjad.makers.tweak_tuplet_bracket_edge_height(tuplet)

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak edge-height #'(0.7 . 0)
        \tuplet 3/2
        {
            c'8
            [
            e'8
            ]
        }
        """
    )

    assert abjad.wf.is_wellformed(tuplet)


def test_Container___delitem___08():
    """
    Deletes leaf from nested container.
    """

    voice = abjad.Voice("c'8 [ { d'8 e'8 } f'8 ]")
    leaves = abjad.select.leaves(voice)
    abjad.glissando(leaves)

    string = abjad.lilypond(voice)
    assert string == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \glissando
            {
                d'8
                \glissando
                e'8
                \glissando
            }
            f'8
            ]
        }
        """
    ), print(string)

    leaf = leaves[1]
    del voice[1][0]

    string = abjad.lilypond(voice)
    assert string == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \glissando
            {
                e'8
                \glissando
            }
            f'8
            ]
        }
        """
    ), print(string)

    assert abjad.wf.is_wellformed(voice)
    assert abjad.wf.is_wellformed(leaf)


def test_Container___delitem___09():
    """
    REGRESSION. Container deletion does not orphan dependent wrappers.
    """

    voice = abjad.Voice("{ c'4 [ } d'4")

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'4
                [
            }
            d'4
        }
        """
    )

    assert len(voice._dependent_wrappers) == 1

    del voice[0]

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            d'4
        }
        """
    ), print(abjad.lilypond(voice))

    assert len(voice._dependent_wrappers) == 0

    assert abjad.wf.is_wellformed(voice)


def test_Container___getitem___01():
    """
    Gets item at positive index.
    """

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
    ]
    voice = abjad.Voice(notes)

    assert voice[0] is notes[0]
    assert voice[1] is notes[1]
    assert voice[2] is notes[2]
    assert voice[3] is notes[3]


def test_Container___getitem___02():
    """
    Gets item at negative index.
    """

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
    ]
    voice = abjad.Voice(notes)

    assert voice[-1] is notes[3]
    assert voice[-2] is notes[2]
    assert voice[-3] is notes[1]
    assert voice[-4] is notes[0]


def test_Container___getitem___03():
    """
    Gets slice.
    """

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
    ]
    voice = abjad.Voice(notes)

    assert voice[:1] == notes[:1]
    assert voice[:2] == notes[:2]
    assert voice[:3] == notes[:3]
    assert voice[:4] == notes[:4]


def test_Container___getitem___04():
    """
    Raises IndexError on bad index.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")

    with pytest.raises(IndexError):
        voice[99]


def test_Container___getitem___05():
    """
    Raises exception on bad name.
    """

    score = abjad.Score()

    with pytest.raises(Exception):
        score["Foo"]


def test_Container___getitem___06():
    """
    Raises exception on duplicate named contexts.
    """

    score = abjad.Score(
        [
            abjad.Staff(
                [abjad.Voice(name="First_Violin_Voice")],
                name="First_Violin_Staff",
            ),
            abjad.Staff(
                [abjad.Voice(name="Cello_Voice")],
                name="Cello_Staff",
            ),
        ]
    )

    assert score["First_Violin_Voice"].get_name() == "First_Violin_Voice"

    score["Cello_Staff"].append(abjad.Voice(name="First_Violin_Voice"))

    with pytest.raises(Exception):
        score["First_Violin_Voice"]

    extra_first_violin_voice = score["Cello_Staff"].pop()

    assert score["First_Violin_Voice"].get_name() == "First_Violin_Voice"
    assert score["First_Violin_Voice"] is not extra_first_violin_voice


def test_Container___init___01():
    """
    Initializes empty container.
    """

    container = abjad.Container([])

    assert isinstance(container, abjad.Container)
    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
        }
        """
    )


def test_Container___init___02():
    """
    Initializes container with LilyPond note-entry string.
    """

    container = abjad.Container("c'8 d'8 e'8")

    assert isinstance(container, abjad.Container)
    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'8
            d'8
            e'8
        }
        """
    )


def test_Container___setitem___01():
    """
    Replaces in-score leaf with out-of-score leaf.
    """

    voice = abjad.Voice("c'8 [ d'8 ] e'8 f'8")

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
    )

    voice[1] = abjad.Note("c''8")

    assert abjad.lilypond(voice) == abjad.string.normalize(
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

    assert abjad.wf.is_wellformed(voice)


def test_Container___setitem___02():
    """
    Replaces in-score leaf with out-of-score container.
    """

    voice = abjad.Voice("c'8 [ d'8 ] e'8 f'8")

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
    )

    voice[1] = abjad.Container("c'16 c'16 c'16")

    assert abjad.lilypond(voice) == abjad.string.normalize(
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

    assert abjad.wf.is_wellformed(voice)


def test_Container___setitem___03():
    """
    Replaces in-score container with out-of-score leaf.
    """

    voice = abjad.Voice("{ c'8 [ d'8 } { e'8 f'8 ] }")

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
    )

    voice[1] = abjad.Note("c''8")

    assert abjad.lilypond(voice) == abjad.string.normalize(
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

    assert abjad.wf.is_wellformed(voice)


def test_Container___setitem___04():
    """
    Replaces in-score container with out-of-score tuplet.
    """

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)

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

    voice[1] = abjad.Tuplet("3:2", "c'8 d'8 e'8")

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
            \tuplet 3/2
            {
                c'8
                d'8
                e'8
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.is_wellformed(voice)


def test_Container___setitem___05():
    """
    Replaces in-score container with out-of-score leaf.
    """

    voice = abjad.Voice("{ c'8 [ d'8 } { e'8 f'8 ] }")

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

    voice[1] = abjad.Note("c''8")

    assert abjad.lilypond(voice) == abjad.string.normalize(
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

    assert abjad.wf.is_wellformed(voice)


def test_Container___setitem___06():
    """
    Replaces in-score container with out-of-score leaf.
    """

    voice = abjad.Voice(
        [abjad.Container("c'8 c'8 c'8 c'8"), abjad.Container("c'8 c'8 c'8 c'8")]
    )
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
    ), print(abjad.lilypond(voice))

    voice[1] = abjad.Rest("r2")

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
            r2
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.is_wellformed(voice)


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

    assert abjad.lilypond(voice_1) == abjad.string.normalize(
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

    assert abjad.lilypond(voice_2) == abjad.string.normalize(
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

    assert abjad.lilypond(voice_1) == abjad.string.normalize(
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

    assert abjad.wf.is_wellformed(voice_1)

    assert abjad.lilypond(voice_2) == abjad.string.normalize(
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

    assert abjad.wf.is_wellformed(voice_2)


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

    assert abjad.lilypond(voice_1) == abjad.string.normalize(
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
    leaves = abjad.select.leaves(voice_2)
    leaves = abjad.select.leaves(voice_2[1])
    abjad.slur(leaves)

    assert abjad.lilypond(voice_2) == abjad.string.normalize(
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

    assert abjad.lilypond(voice_1) == abjad.string.normalize(
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

    assert abjad.wf.is_wellformed(voice_1)

    assert abjad.lilypond(voice_2) == abjad.string.normalize(
        r"""
        \new Voice
        {
            f'8
            b'8
        }
        """
    ), print(abjad.lilypond(voice_2))

    assert abjad.wf.is_wellformed(voice_2)


def test_Container___setitem___09():
    """
    Sets leaf between unspanned components.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    staff[2:2] = [abjad.Note("g'8")]

    assert abjad.lilypond(staff) == abjad.string.normalize(
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

    assert abjad.wf.is_wellformed(staff)


def test_Container___setitem___10():
    """
    Sets leaf between spanned compoennts.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    note = abjad.Note("g'8")
    voice[2:2] = [note]

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
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
    ), print(abjad.lilypond(voice))

    assert abjad.wf.is_wellformed(voice)


def test_Container___setitem___11():
    """
    Sets leaves between spanned components.
    """

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

    voice = abjad.Voice(beginning + end)
    abjad.beam(voice[:])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            g'8
            a'8
            ]
        }
        """
    ), print(abjad.lilypond(voice))

    voice[2:2] = middle

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
    ), print(abjad.lilypond(voice))

    assert abjad.wf.is_wellformed(voice)


def test_Container___setitem___12():
    """
    Replaces multiple spanned leaves with with single leaf.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    note = abjad.Note("c''8")
    voice[1:3] = [note]

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            c''8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.is_wellformed(voice)


def test_Container___setitem___13():
    """
    Replaces three spanned leaves with three different leaves.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    notes = [abjad.Note("b'8"), abjad.Note("a'8"), abjad.Note("g'8")]
    voice[1:3] = notes

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
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
    ), print(abjad.lilypond(voice))

    assert abjad.wf.is_wellformed(voice)


def test_Container___setitem___14():
    """
    Replaces in-score container with contents of container.
    """

    staff = abjad.Staff("{ c'8 [ d'8 } { e'8 f'8 ] }")

    assert abjad.lilypond(staff) == abjad.string.normalize(
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

    assert abjad.lilypond(staff) == abjad.string.normalize(
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

    assert abjad.wf.is_wellformed(staff)
    assert len(container) == 0


def test_Container___setitem___15():
    """
    Sets first slice of staff equal to first element of first container in
    staff.
    """

    staff = abjad.Staff("{ c'8 [ d'8 } { e'8 f'8 ] }")

    assert abjad.lilypond(staff) == abjad.string.normalize(
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

    assert abjad.lilypond(staff) == abjad.string.normalize(
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

    assert abjad.wf.is_wellformed(staff)


def test_Container___setitem___16():
    """
    Sets first slice of staff equal to contents of first container in staff.

    Empties first container in staff.

    Leaves empty container in staff.
    """

    staff = abjad.Staff("{ c'8 [ d'8 } { e'8 f'8 ] }")

    assert abjad.lilypond(staff) == abjad.string.normalize(
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

    assert abjad.lilypond(staff) == abjad.string.normalize(
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
    """
    Sets first slice of staff equal to contents of first container in staff;
    empties first container in staff.

    Sets contents of empty first container in staff equal to first component in
    second container in staff.
    """

    staff = abjad.Staff("{ c'8 [ d'8 } { e'8 f'8 ] }")

    assert abjad.lilypond(staff) == abjad.string.normalize(
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

    assert abjad.lilypond(staff) == abjad.string.normalize(
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

    assert abjad.wf.is_wellformed(staff)


def test_Container___setitem___18():
    """
    Extremely small coequal indices indicate first slice in staff.
    """

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    voice[-1000:-1000] = [abjad.Rest("r8")]

    assert abjad.lilypond(voice) == abjad.string.normalize(
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

    assert abjad.lilypond(voice) == abjad.string.normalize(
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

    assert abjad.wf.is_wellformed(voice)


def test_Container___setitem___19():
    """
    Extremely large coequal indices indicate last slice in staff.
    """

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    voice[1000:1000] = [abjad.Rest("r8")]

    assert abjad.lilypond(voice) == abjad.string.normalize(
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

    assert abjad.wf.is_wellformed(voice)


def test_Container___setitem___20():
    """
    You can use setitem to empty the contents of a container.
    """

    staff = abjad.Staff("c'8 d'8 [ e'8 ] f'8")
    inner_container = abjad.Container()
    abjad.mutate.wrap(staff[1:3], inner_container)
    outer_container = abjad.Container()
    abjad.mutate.wrap(inner_container, outer_container)

    assert abjad.lilypond(staff) == abjad.string.normalize(
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
    assert abjad.lilypond(staff) == abjad.string.normalize(
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

    assert abjad.lilypond(inner_container) == abjad.string.normalize(
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

    assert abjad.lilypond(staff) == abjad.string.normalize(
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
    assert abjad.lilypond(staff) == abjad.string.normalize(
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
    assert abjad.lilypond(inner_container) == abjad.string.normalize(
        r"""
        {
            d'8
            [
            e'8
            ]
        }
        """
    ), print(abjad.lilypond(inner_container))


def test_Container_append_01():
    """
    Appends container to voice.
    """

    voice = abjad.Voice("c'8 d'8")
    abjad.beam(voice[:])
    voice.append(abjad.Container("e'8 f'8"))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            {
                e'8
                f'8
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.is_wellformed(voice)


def test_Container_append_02():
    """
    Appends leaf to tuplet.
    """

    tuplet = abjad.Tuplet("3:2", "c'8 d'8 e'8")
    abjad.Voice([tuplet])
    abjad.beam(tuplet[:])
    tuplet.append(abjad.Note(5, (1, 16)), preserve_duration=True)

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 7/4
        {
            c'8
            [
            d'8
            e'8
            ]
            f'16
        }
        """
    ), print(abjad.lilypond(tuplet))

    assert abjad.wf.is_wellformed(tuplet)


def test_Container_append_03():
    """
    Raises TypeError when trying to append noncomponent to container.
    """

    voice = abjad.Voice("c'8 d'8 e'8")
    abjad.beam(voice[:])

    with pytest.raises(Exception):
        voice.append("foo")
    with pytest.raises(Exception):
        voice.append(99)
    with pytest.raises(Exception):
        voice.append([])
    with pytest.raises(Exception):
        voice.append([abjad.Note(0, (1, 8))])


def test_Container_append_04():
    """
    Appends spanned leaf from donor container to recipient container.
    """

    voice_1 = abjad.Voice("c'8 d'8 e'8")
    abjad.beam(voice_1[:])

    assert abjad.lilypond(voice_1) == abjad.string.normalize(
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

    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice_2[:])

    assert abjad.lilypond(voice_2) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(voice_2))

    voice_1.append(voice_2[-1])

    assert abjad.lilypond(voice_1) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            ]
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(voice_1))

    assert abjad.lilypond(voice_2) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
        }
        """
    ), print(abjad.lilypond(voice_2))


def test_Container_append_05():
    """
    Appends spanned leaf from donor container to recipient container.
    Donor and recipient containers are the same.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
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
            ]
        }
        """
    ), print(abjad.lilypond(voice))

    voice.append(voice[1])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            e'8
            f'8
            ]
            d'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.is_wellformed(voice)


def test_Container_append_06():
    """
    Can not insert grace container into container.
    """

    staff = abjad.Staff("c' d' e'")
    grace_container = abjad.BeforeGraceContainer("f'16 g'")

    with pytest.raises(Exception):
        staff.append(grace_container)


def test_Container_extend_01():
    """
    Extends container with list of leaves.
    """

    voice = abjad.Voice("c'8 d'8")
    abjad.beam(voice[:])
    voice.extend([abjad.Note("c'8"), abjad.Note("d'8")])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            c'8
            d'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.is_wellformed(voice)


def test_Container_extend_02():
    """
    Extends container with contents of other container.
    """

    voice_1 = abjad.Voice("c'8 d'8")
    abjad.beam(voice_1[:])

    voice_2 = abjad.Voice("e'8 f'8")
    abjad.beam(voice_2[:])
    voice_1.extend(voice_2)

    assert abjad.lilypond(voice_1) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            e'8
            [
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(voice_1))

    assert abjad.wf.is_wellformed(voice_1)


def test_Container_extend_03():
    """
    Leaves container unchanged when extending container with empty list.
    """

    voice = abjad.Voice("c'8 d'8")
    abjad.beam(voice[:])
    voice.extend([])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.is_wellformed(voice)


def test_Container_extend_04():
    """
    Leaves both containers unchanged when one container extends the other.
    """

    voice = abjad.Voice("c'8 d'8")
    abjad.beam(voice[:])
    voice.extend(abjad.Voice([]))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.is_wellformed(voice)


def test_Container_extend_05():
    """
    Raises TypeError when trying to extend container with noncomponent.
    """

    voice = abjad.Voice("c'8 d'8")
    abjad.beam(voice[:])

    with pytest.raises(Exception):
        voice.extend(7)
    with pytest.raises(Exception):
        voice.extend("foo")


def test_Container_extend_06():
    """
    Raises exception when trying to extend container with noncontainer.
    """

    voice = abjad.Voice("c'8 d'8")
    abjad.beam(voice[:])

    with pytest.raises(Exception):
        voice.extend(abjad.Note("c'4"))

    with pytest.raises(Exception):
        voice.extend(abjad.Chord("<c' d' e'>4"))


def test_Container_extend_07():
    """
    Extends container with partial and spanned contents of other container.
    """

    voice_1 = abjad.Voice("c'8 d'8")
    abjad.beam(voice_1[:])

    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice_2[:])

    voice_1.extend(voice_2[-2:])

    assert abjad.lilypond(voice_1) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            e'8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(voice_1))

    assert abjad.lilypond(voice_2) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
        }
        """
    ), print(abjad.lilypond(voice_2))


def test_Container_extend_08():
    """
    Extends container with partial and spanned contents of other container.
    Covered span comes with components from donor container.
    """

    voice_1 = abjad.Voice("c'8 d'8")
    abjad.beam(voice_1[:])

    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice_2[:])
    abjad.slur(voice_2[-2:])

    assert abjad.lilypond(voice_2) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            (
            f'8
            )
            ]
        }
        """
    ), print(abjad.lilypond(voice_2))

    voice_1.extend(voice_2[-2:])

    assert abjad.lilypond(voice_1) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            e'8
            (
            f'8
            )
            ]
        }
        """
    ), print(abjad.lilypond(voice_1))

    assert abjad.lilypond(voice_2) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
        }
        """
    ), print(abjad.lilypond(voice_2))


def test_Container_extend_09():
    """
    Extends container with LilyPond input string.
    """

    container = abjad.Container([])
    container.extend("c'4 ( d'4 e'4 f'4 )")

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'4
            (
            d'4
            e'4
            f'4
            )
        }
        """
    ), print(abjad.lilypond(container))

    assert abjad.wf.is_wellformed(container)


def test_Container_extend_10():
    """
    Lists must be flattened.
    """

    duration = abjad.Duration(1, 4)
    lists = [
        abjad.makers.make_notes(abjad.makers.make_pitches([0, 2]), [duration]),
        abjad.makers.make_notes(abjad.makers.make_pitches([4, 5]), [duration]),
        abjad.makers.make_notes(abjad.makers.make_pitches([7, 9]), [duration]),
        abjad.makers.make_notes(abjad.makers.make_pitches([11, 12]), [duration]),
    ]
    components = abjad.sequence.flatten(lists, depth=-1)
    container = abjad.Container()
    container.extend(components)

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
            g'4
            a'4
            b'4
            c''4
        }
        """
    ), print(abjad.lilypond(container))

    assert abjad.wf.is_wellformed(container)


def test_Container_index_01():
    """
    Elements that compare equal return different indices in container.
    """

    container = abjad.Container("c'4 c'4 c'4 c'4")

    assert container.index(container[0]) == 0
    assert container.index(container[1]) == 1
    assert container.index(container[2]) == 2
    assert container.index(container[3]) == 3


def test_Container_insert_01():
    """
    Inserts component into container at index i.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    voice.insert(0, abjad.Rest((1, 8)))

    assert abjad.wf.is_wellformed(voice)
    assert abjad.lilypond(voice) == abjad.string.normalize(
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
    )


def test_Container_insert_02():
    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    voice.insert(1, abjad.Note(1, (1, 8)))

    assert abjad.wf.is_wellformed(voice)
    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            cs'8
            d'8
            e'8
            f'8
            ]
        }
        """
    )


def test_Container_insert_03():
    voice = abjad.Voice([abjad.Note(n, (1, 8)) for n in range(4)])
    abjad.beam(voice[:])
    voice.insert(4, abjad.Rest((1, 4)))

    assert abjad.wf.is_wellformed(voice)
    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            cs'8
            d'8
            ef'8
            ]
            r4
        }
        """
    )


def test_Container_insert_04():
    """
    Insert works with really big positive values.
    """

    voice = abjad.Voice([abjad.Note(n, (1, 8)) for n in range(4)])
    abjad.beam(voice[:])
    voice.insert(1000, abjad.Rest((1, 4)))

    assert abjad.wf.is_wellformed(voice)
    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            cs'8
            d'8
            ef'8
            ]
            r4
        }
        """
    )


def test_Container_insert_05():
    """
    Insert works with negative values.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    voice.insert(-1, abjad.Note(4.5, (1, 8)))

    assert abjad.wf.is_wellformed(voice)
    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            eqs'8
            f'8
            ]
        }
        """
    )


def test_Container_insert_06():
    """
    Insert works with really big negative values.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    voice.insert(-1000, abjad.Rest((1, 8)))

    assert abjad.wf.is_wellformed(voice)
    assert abjad.lilypond(voice) == abjad.string.normalize(
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
    )


def test_Container_insert_07():
    """
    Inserting a note from one container into another container
    changes note parent from first container to second.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")
    note = voice[0]
    staff.insert(1, voice[0])

    assert abjad.wf.is_wellformed(voice)
    assert abjad.wf.is_wellformed(staff)
    assert note not in voice
    assert abjad.get.parentage(note).get_parent() is staff


def test_Container_insert_08():
    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    voice.insert(1, abjad.Note("cs'8"))

    assert abjad.wf.is_wellformed(voice)
    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            cs'8
            d'8
            e'8
            f'8
            ]
        }
        """
    )


def test_Container_is_simultaneous_01():
    """
    Is true when container encloses contents in LilyPond << >> brackets.
    """

    assert not abjad.Container().get_simultaneous()
    assert not abjad.Tuplet().get_simultaneous()
    assert abjad.Score().get_simultaneous()
    assert not abjad.Container().get_simultaneous()
    assert not abjad.Staff().get_simultaneous()
    assert abjad.StaffGroup().get_simultaneous()
    assert not abjad.Voice().get_simultaneous()


def test_Container_is_simultaneous_02():
    """
    Is true when container encloses contents in LilyPond << >> brackets.
    """

    container = abjad.Container([])
    container.set_simultaneous(True)
    assert container.get_simultaneous()


def test_Container_is_simultaneous_03():
    """
    The ``simultaneous`` property is settable.
    """

    container = abjad.Container([])
    assert not container.get_simultaneous()

    container.set_simultaneous(True)
    assert container.get_simultaneous()


def test_Container_is_simultaneous_04():
    """
    Simultaneous container can hold contexts.
    """

    container = abjad.Container([abjad.Voice("c'8 cs'8"), abjad.Voice("d'8 ef'8")])
    container.set_simultaneous(True)

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        <<
            \new Voice
            {
                c'8
                cs'8
            }
            \new Voice
            {
                d'8
                ef'8
            }
        >>
        """
    )


def test_Container_is_simultaneous_05():
    """
    Simultaneous containers must contain only other containers.
    """

    container = abjad.Container(
        [abjad.Container("c'8 c'8 c'8 c'8"), abjad.Container("c'8 c'8 c'8 c'8")]
    )

    container = abjad.Container("c'8 c'8 c'8 c'8")
    with pytest.raises(Exception):
        container.set_simultaneous(True)


def test_Container_pop_01():
    """
    Containers pop leaves correctly.
    Popped leaves abjad.detach from parent.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.slur(voice[:])
    abjad.beam(voice[1:2], beam_lone_notes=True)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            (
            d'8
            [
            ]
            e'8
            f'8
            )
        }
        """
    ), print(abjad.lilypond(voice))

    result = voice.pop(1)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            (
            e'8
            f'8
            )
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.is_wellformed(voice)

    "Result is now d'8 [ ]"

    assert abjad.lilypond(result) == "d'8\n[\n]"
    assert abjad.wf.is_wellformed(result, do_not_check_beamed_lone_notes=True)


def test_Container_pop_02():
    """
    Containers pop nested containers correctly.
    """

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)

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

    container = voice.pop()

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.is_wellformed(voice)

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            e'8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(container))

    assert abjad.wf.is_wellformed(container)


def test_Container_remove_01():
    """
    Containers remove leaves correctly.
    Leaf abjad.detaches from parentage.
    Leaf returns after removal.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.slur(voice[:])
    abjad.beam(voice[1:2], beam_lone_notes=True)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            (
            d'8
            [
            ]
            e'8
            f'8
            )
        }
        """
    )

    note = voice[1]
    voice.remove(note)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            (
            e'8
            f'8
            )
        }
        """
    )

    "Note is now d'8 [ ]"

    assert abjad.lilypond(note) == "d'8\n[\n]"

    assert abjad.wf.is_wellformed(voice)
    assert abjad.wf.is_wellformed(note, do_not_check_beamed_lone_notes=True)


def test_Container_remove_02():
    """
    Containers remove nested containers correctly.
    Container detaches from parentage.
    Container returns after removal.
    """

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 }")
    container = voice[0]

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

    voice.remove(container)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                e'8
                f'8
            }
        }
        """
    )

    assert abjad.wf.is_wellformed(voice)

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'8
            d'8
        }
        """
    )

    assert abjad.wf.is_wellformed(container)


def test_Container_remove_03():
    """
    Container remove works on identity and not equality.
    """

    note = abjad.Note("c'4")
    container = abjad.Container([abjad.Note("c'4")])

    with pytest.raises(Exception):
        container.remove(note)
