import abjad


def test_mutate_copy_01():
    """
    Deep copies components.
    Returns Python list of copied components.
    """

    voice = abjad.Voice(
        [
            abjad.Container("c'8 d'"),
            abjad.Container("e'8 f'"),
            abjad.Container("g'8 a'"),
        ],
        name="Voice",
    )
    staff = abjad.Staff([voice], name="Staff")
    score = abjad.Score([staff], name="Score")
    for container in voice:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select.leaves(voice)
    abjad.slur(leaves)
    abjad.trill_spanner(leaves)
    abjad.beam(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \context Voice = "Voice"
        {
            {
                \time 2/8
                c'8
                [
                (
                \startTrillSpan
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
                )
                \stopTrillSpan
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    result = abjad.mutate.copy(leaves[2:4])
    new = abjad.Staff(result)
    abjad.Score([new], name="Score")

    assert abjad.lilypond(new) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \time 2/8
            e'8
            f'8
        }
        """,
        print(abjad.lilypond(new)),
    )
    assert abjad.wf.wellformed(score)
    assert abjad.wf.wellformed(new)


def test_mutate_copy_02():
    """
    Copy one measure.
    """

    voice = abjad.Voice(
        [
            abjad.Container("c'8 d'"),
            abjad.Container("e'8 f'"),
            abjad.Container("g'8 a'"),
        ],
        name="Voice",
    )
    staff = abjad.Staff([voice], name="Staff")
    abjad.Score([staff], name="Score")
    for container in voice:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select.leaves(voice)
    abjad.slur(leaves)
    abjad.trill_spanner(leaves)
    abjad.beam(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \context Voice = "Voice"
        {
            {
                \time 2/8
                c'8
                [
                (
                \startTrillSpan
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
                )
                \stopTrillSpan
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    result = abjad.mutate.copy(voice[1:2])
    new = abjad.Voice(result, name="Foo")
    abjad.Score([new], name="Score")

    assert abjad.lilypond(new) == abjad.string.normalize(
        r"""
        \context Voice = "Foo"
        {
            {
                \time 2/8
                e'8
                f'8
            }
        }
        """
    ), print(abjad.lilypond(new))

    assert abjad.wf.wellformed(voice)
    assert abjad.wf.wellformed(new)


def test_mutate_copy_03():
    """
    Three notes crossing measure boundaries.
    """

    voice = abjad.Voice(
        [
            abjad.Container("c'8 d'"),
            abjad.Container("e'8 f'"),
            abjad.Container("g'8 a'"),
        ],
        name="Voice",
    )
    staff = abjad.Staff([voice], name="Staff")
    abjad.Score([staff], name="Score")
    for container in voice:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select.leaves(voice)
    abjad.slur(leaves)
    abjad.trill_spanner(leaves)
    abjad.beam(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \context Voice = "Voice"
        {
            {
                \time 2/8
                c'8
                [
                (
                \startTrillSpan
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
                )
                \stopTrillSpan
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    result = abjad.mutate.copy(leaves[-3:])
    new = abjad.Voice(result, name="Foo")
    abjad.Score([new], name="Score")

    assert abjad.lilypond(new) == abjad.string.normalize(
        r"""
        \context Voice = "Foo"
        {
            f'8
            \time 2/8
            g'8
            a'8
            )
            \stopTrillSpan
            ]
        }
        """
    ), print(abjad.lilypond(new))


def test_mutate_copy_04():
    voice = abjad.Voice(
        [
            abjad.Container("c'8 d'"),
            abjad.Container("e'8 f'"),
            abjad.Container("g'8 a'"),
            abjad.Container("b'8 c''"),
        ],
        name="Voice",
    )
    staff = abjad.Staff([voice], name="Staff")
    abjad.Score([staff], name="Score")
    for container in voice:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \context Voice = "Voice"
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    new_voice = abjad.mutate.copy(voice)
    new_staff = abjad.Staff([new_voice], name="New_Staff")
    abjad.Score([new_staff], name="Score")

    assert abjad.lilypond(new_voice) == abjad.string.normalize(
        r"""
        \context Voice = "Voice"
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(new_voice))

    assert abjad.wf.wellformed(new_voice)


def test_mutate_copy_05():
    voice = abjad.Voice(
        [
            abjad.Container("c'8 d'"),
            abjad.Container("e'8 f'"),
            abjad.Container("g'8 a'"),
            abjad.Container("b'8 c''"),
        ],
        name="Voice",
    )
    staff = abjad.Staff([voice], name="Staff")
    abjad.Score([staff], name="Score")
    for container in voice:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \context Voice = "Voice"
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    result = abjad.mutate.copy(voice[1:])
    new_voice = abjad.Voice(result, name="New_Voice")
    new_staff = abjad.Staff([new_voice], name="New_Staff")
    abjad.Score([new_staff], name="Score")

    assert abjad.lilypond(new_voice) == abjad.string.normalize(
        r"""
        \context Voice = "New_Voice"
        {
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(new_voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_copy_06():
    voice = abjad.Voice(
        [
            abjad.Container("c'8 d'"),
            abjad.Container("e'8 f'"),
            abjad.Container("g'8 a'"),
            abjad.Container("b'8 c''"),
        ],
        name="Voice",
    )
    staff = abjad.Staff([voice], name="Staff")
    abjad.Score([staff], name="Score")
    for container in voice:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \context Voice = "Voice"
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    result = abjad.mutate.copy(leaves[:6])
    new_voice = abjad.Voice(result, name="New_Voice")
    new_staff = abjad.Staff([new_voice], name="New_Staff")
    abjad.Score([new_staff], name="New_Score")

    assert abjad.lilypond(new_voice) == abjad.string.normalize(
        r"""
        \context Voice = "New_Voice"
        {
            \time 2/8
            c'8
            [
            (
            d'8
            \time 2/8
            e'8
            f'8
            \time 2/8
            g'8
            a'8
        }
        """
    ), print(abjad.lilypond(new_voice))


def test_mutate_copy_07():
    voice = abjad.Voice(
        [
            abjad.Container("c'8 d'"),
            abjad.Container("e'8 f'"),
            abjad.Container("g'8 a'"),
            abjad.Container("b'8 c''"),
        ],
        name="Voice",
    )
    staff = abjad.Staff([voice], name="Staff")
    abjad.Score([staff], name="Score")
    for container in voice:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \context Voice = "Voice"
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    result = abjad.mutate.copy(voice[-2:])
    new_voice = abjad.Voice(result, name="New_Voice")
    new_staff = abjad.Staff([new_voice], name="New_Staff")
    abjad.Score([new_staff], name="New_Score")

    assert abjad.lilypond(new_voice) == abjad.string.normalize(
        r"""
        \context Voice = "New_Voice"
        {
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(new_voice))


def test_mutate_copy_08():
    """
    Copies hairpin.
    """

    voice = abjad.Voice("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8", name="Voice")
    abjad.hairpin("< !", voice[:4])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \context Voice = "Voice"
        {
            c'8
            \<
            cs'8
            d'8
            ef'8
            \!
            e'8
            f'8
            fs'8
            g'8
        }
        """
    )

    new_notes = abjad.mutate.copy(voice[:4])
    voice.extend(new_notes)
    # abjad.Score([staff], name="Score")

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \context Voice = "Voice"
        {
            c'8
            \<
            cs'8
            d'8
            ef'8
            \!
            e'8
            f'8
            fs'8
            g'8
            c'8
            \<
            cs'8
            d'8
            ef'8
            \!
        }
        """
    )
    assert abjad.wf.wellformed(voice)


def test_mutate_copy_09():
    """
    Copies tweaks.
    """
    staff = abjad.Staff("c'4 cs' d' ds'")
    abjad.tweak(staff[1].note_head, r"\tweak color #red")
    abjad.tweak(staff[1].note_head, r"\tweak Accidental.color #red")
    copied_staff = abjad.mutate.copy(staff)
    string = abjad.lilypond(copied_staff)

    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'4
            \tweak Accidental.color #red
            \tweak color #red
            cs'4
            d'4
            ds'4
        }
        """
    ), print(string)
    assert abjad.wf.wellformed(staff)
