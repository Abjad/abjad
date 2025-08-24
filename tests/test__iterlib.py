import abjad


def test__iterlib_are_logical_voice_01():
    """
    Orphan leaves do not share a logical voice.
    Orphan leaves do not share a root component.
    False if not allow orphans; true if allow orphans.
    """

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
    ]
    assert abjad._iterlib.are_logical_voice(notes)


def test__iterlib_are_logical_voice_02():
    """
    Container and leaves all in same logical voice.
    """

    container = abjad.Container("c'8 d'8 e'8 f'8")

    r"""
    {
        c'8
        d'8
        e'8
        f'8
    }
    """

    components = abjad.select.components(container)
    assert abjad._iterlib.are_logical_voice(components)


def test__iterlib_are_logical_voice_03():
    """
    Tuplet and leaves all in same logical voice.
    """

    tuplet = abjad.Tuplet("3:2", "c'8 d'8 e'8")

    r"""
    \tuplet 3/2
    {
        c'8
        d'8
        e'8
    }
    """

    components = abjad.select.components(tuplet)
    assert abjad._iterlib.are_logical_voice(components)


def test__iterlib_are_logical_voice_04():
    """
    Voice and leaves all appear in same logical voice.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")

    r"""
    \new Voice {
        c'8
        d'8
        e'8
        f'8
    }
    """

    components = abjad.select.components(voice)
    assert abjad._iterlib.are_logical_voice(components)


def test__iterlib_are_logical_voice_05():
    """
    Anonymous staff and leaves all appear in same logical voice.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")

    r"""
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    """

    components = abjad.select.components(staff)
    assert abjad._iterlib.are_logical_voice(components)


def test__iterlib_are_logical_voice_06():
    """
    Voice, sequential and leaves all appear in same logical voice.
    """

    voice = abjad.Voice(
        r"""
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
        """
    )

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

    components = abjad.select.components(voice)
    assert abjad._iterlib.are_logical_voice(components)


def test__iterlib_are_logical_voice_07():
    """
    Anonymous voice, tuplets and leaves all appear in same logical voice.
    """

    voice = abjad.Voice(
        r"""
        \tuplet 3/2
        {
            c'8
            d'8
            e'8
        }
        \tuplet 3/2
        {
            f'8
            g'8
            a'8
        }
        """
    )

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
                g'8
                a'8
            }
        }
        """
    )

    components = abjad.select.components(voice)
    assert abjad._iterlib.are_logical_voice(components)


def test__iterlib_are_logical_voice_08():
    """
    Logical voice does not extend across anonymous voices.
    """

    staff = abjad.Staff(
        r"""
        \new Voice {
            c'8
            d'8
            e'8
            f'8
        }
        \new Voice {
            g'8
            a'8
            b'8
            c''8
        }
        """
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

    leaves = abjad.select.leaves(staff)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)
    assert not abjad._iterlib.are_logical_voice(staff[:])


def test__iterlib_are_logical_voice_09():
    """
    Logical voice encompasses across like-named voices.
    """

    staff = abjad.Staff(
        r"""
        \context Voice = "foo" {
            c'8
            d'8
            e'8
            f'8
        }
        \context Voice = "foo" {
            g'8
            a'8
            b'8
            c''8
        }
        """
    )

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

    leaves = abjad.select.leaves(staff)
    assert abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_10():
    """
    Logical voice does not extend across differently named voices.
    """

    staff = abjad.Staff(
        r"""
        \context Voice = "foo" {
            c'8
            d'8
        }
        \context Voice = "bar" {
            e'8
            f'8
        }
        """
    )

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \context Voice = "foo"
            {
                c'8
                d'8
            }
            \context Voice = "bar"
            {
                e'8
                f'8
            }
        }
        """
    )

    leaves = abjad.select.leaves(staff)
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_11():
    """
    Logical voice does not across anonymous voices.
    Logical voice does not extend across anonymous staves.
    """

    container = abjad.Container(
        r"""
        \new Staff {
            \new Voice {
                c'8
                d'8
            }
        }
        \new Staff {
            \new Voice {
                e'8
                f'8
            }
        }
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \new Staff
            {
                \new Voice
                {
                    c'8
                    d'8
                }
            }
            \new Staff
            {
                \new Voice
                {
                    e'8
                    f'8
                }
            }
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_12():
    """
    Logical voice does not extend across anonymous voices.
    Logical voice does not extend across anonymous staves.
    """

    container = abjad.Container(
        r"""
        \new Staff <<
            \new Voice {
                c'8
                d'8
            }
            \new Voice {
                e'8
                f'8
            }
        >>
        \new Staff <<
            \new Voice {
                g'8
                a'8
            }
            \new Voice {
                b'8
                c''8
            }
        >>
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \new Staff
            <<
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
            >>
            \new Staff
            <<
                \new Voice
                {
                    g'8
                    a'8
                }
                \new Voice
                {
                    b'8
                    c''8
                }
            >>
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert not abjad._iterlib.are_logical_voice(leaves[:4])


def test__iterlib_are_logical_voice_13():
    """
    Anonymous voice, sequentials and leaves all appear in same logical voice.
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

    leaves = abjad.select.leaves(voice)
    assert abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_14():
    """
    Logical voice can extend across like-named staves.
    Logical voice can not extend across differently named implicit voices.
    """

    container = abjad.Container(
        r"""
        \context Staff = "foo" {
            c'8
            cs'8
            d'8
            ef'8
        }
        \context Staff = "foo" {
            e'8
            f'8
            fs'8
            g'8
        }
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \context Staff = "foo"
            {
                c'8
                cs'8
                d'8
                ef'8
            }
            \context Staff = "foo"
            {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_15():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    container = abjad.Container(
        r"""
        {
            c'8
            d'8
            e'8
            f'8
        }
        \new Voice {
            g'8
            a'8
            b'8
            c''8
        }
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
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

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_16():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    container = abjad.Container(
        r"""
        \new Voice {
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
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \new Voice
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

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_17():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    container = abjad.Container(
        r"""
        {
            c'8
            d'8
            e'8
            f'8
        }
        \context Voice = "foo" {
            g'8
            a'8
            b'8
            c''8
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_18():
    """
    Logical voice can not extend acrossdifferently named implicit voices.
    """

    container = abjad.Container(
        r"""
        \context Voice = "foo" {
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
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \context Voice = "foo"
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

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_19():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    container = abjad.Container(
        r"""
        {
            c'8
            d'8
            e'8
            f'8
        }
        \new Staff {
            g'8
            a'8
            b'8
            c''8
        }
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            {
                c'8
                d'8
                e'8
                f'8
            }
            \new Staff
            {
                g'8
                a'8
                b'8
                c''8
            }
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_20():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    container = abjad.Container(
        r"""
        \new Staff {
            c'8
            cs'8
            d'8
            ef'8
        }
        {
            e'8
            f'8
            fs'8
            g'8
        }
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \new Staff
            {
                c'8
                cs'8
                d'8
                ef'8
            }
            {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_21():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    container = abjad.Container(
        r"""
        c'8
        cs'8
        d'8
        ef'8
        \new Voice {
            e'8
            f'8
            fs'8
            g'8
        }
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'8
            cs'8
            d'8
            ef'8
            \new Voice
            {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_22():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    container = abjad.Container(
        r"""
        \new Voice {
            c'8
            cs'8
            d'8
            ef'8
        }
        e'8
        f'8
        fs'8
        g'8
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \new Voice
            {
                c'8
                cs'8
                d'8
                ef'8
            }
            e'8
            f'8
            fs'8
            g'8
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_23():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    container = abjad.Container(
        r"""
        c'8
        cs'8
        d'8
        ef'8
        \context Voice = "foo" {
            e'8
            f'8
            fs'8
            g'8
        }
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'8
            cs'8
            d'8
            ef'8
            \context Voice = "foo"
            {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_24():
    """
    Logical voice can not extend across differently named implicit voices.
    NOTE: THIS IS THE LILYPOND LACUNA.
    LilyPond *does* extend logical voice in this case.
    Abjad does not.
    """

    container = abjad.Container(
        r"""
        \context Voice = "foo" {
            c'8
            cs'8
            d'8
            ef'8
        }
        e'8
        f'8
        fs'8
        g'8
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \context Voice = "foo"
            {
                c'8
                cs'8
                d'8
                ef'8
            }
            e'8
            f'8
            fs'8
            g'8
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_25():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    container = abjad.Container(
        r"""
        c'8
        cs'8
        d'8
        ef'8
        \new Voice {
            e'8
            f'8
            fs'8
            g'8
        }
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'8
            cs'8
            d'8
            ef'8
            \new Voice
            {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_26():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    container = abjad.Container(
        r"""
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        g'8
        a'8
        b'8
        c''8
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
            }
            g'8
            a'8
            b'8
            c''8
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_27():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    pitches = abjad.pitch.pitches([0, 1, 2, 3])
    duration = abjad.Duration(1, 8)
    notes = [abjad.Note.from_duration_and_pitch(duration, _) for _ in pitches]
    voice = abjad.Voice(notes)
    container = abjad.Container([voice])
    pitches = abjad.pitch.pitches([4, 5, 6, 7])
    notes = [abjad.Note.from_duration_and_pitch(duration, _) for _ in pitches]
    container = abjad.Container([container] + notes)

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            {
                \new Voice
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
            e'8
            f'8
            fs'8
            g'8
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_28():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    voice = abjad.Voice("c'8 cs' d' ef'", name="foo")
    container = abjad.Container([voice])
    container = abjad.Container([container])
    container.extend("e'8 f'8 fs'8 g'8")

    r"""
    {
        {
            \context Voice = "foo" {
                c'8
                cs'8
                d'8
                ef'8
            }
        }
        e'8
        f'8
        fs'8
        g'8
    }
    """

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_29():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    voice_1 = abjad.Voice("c'8 cs'8 d'8 ef'8", name="foo")
    voice_2 = abjad.Voice([voice_1], name="bar")
    container = abjad.Container([voice_2])
    container.extend("e'8 f'8 fs'8 g'8")

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \context Voice = "bar"
            {
                \context Voice = "foo"
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
            e'8
            f'8
            fs'8
            g'8
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_30():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    voice_1 = abjad.Voice("c'8 cs'8 d'8 ef'8")
    voice_2 = abjad.Voice([voice_1])
    container = abjad.Container([voice_2])
    container.extend("e'8 f'8 fs'8 g'8")

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \new Voice
            {
                \new Voice
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
            e'8
            f'8
            fs'8
            g'8
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_31():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    container_1 = abjad.Container("c'8 cs'8 d'8 ef'8")
    voice_1 = abjad.Voice("c''8 c''8 c''8 c''8")
    voice_2 = abjad.Voice("c'8 c'8 c'8 c'8")
    container_2 = abjad.Container([voice_1, voice_2])
    container_2.set_simultaneous(True)
    container_1.append(container_2)

    assert abjad.lilypond(container_1) == abjad.string.normalize(
        r"""
        {
            c'8
            cs'8
            d'8
            ef'8
            <<
                \new Voice
                {
                    c''8
                    c''8
                    c''8
                    c''8
                }
                \new Voice
                {
                    c'8
                    c'8
                    c'8
                    c'8
                }
            >>
        }
        """
    )

    leaves = abjad.select.leaves(container_1)
    assert not abjad._iterlib.are_logical_voice(leaves[:8])
    assert not abjad._iterlib.are_logical_voice(leaves[4:])


def test__iterlib_are_logical_voice_32():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    container = abjad.Container(
        r"""
        <<
            \new Voice {
                c'8
                cs'8
                d'8
                ef'8
            }
            \new Voice {
                e'8
                f'8
                fs'8
                g'8
            }
        >>
        af'8
        a'8
        bf'8
        b'8
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            <<
                \new Voice
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
                \new Voice
                {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
            >>
            af'8
            a'8
            bf'8
            b'8
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert not abjad._iterlib.are_logical_voice(leaves[:8])
    assert not abjad._iterlib.are_logical_voice(leaves[4:])


def test__iterlib_are_logical_voice_33():
    """
    Logical voice does extend across gaps.
    Logical voice can not extend across differently named voices.
    """

    container = abjad.Container(
        r"""
        c'8
        cs'8
        \new Voice {
            d'8
            ef'8
            \new Voice {
                e'8
                f'8
                fs'8
                g'8
            }
            af'8
            a'8
        }
        bf'8
        b'8
        """
    )

    outer = (0, 1, 10, 11)
    middle = (2, 3, 8, 9)
    inner = (4, 5, 6, 7)

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'8
            cs'8
            \new Voice
            {
                d'8
                ef'8
                \new Voice
                {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
                af'8
                a'8
            }
            bf'8
            b'8
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice([leaves[i] for i in outer])
    assert abjad._iterlib.are_logical_voice([leaves[i] for i in middle])
    assert abjad._iterlib.are_logical_voice([leaves[i] for i in inner])
    assert not abjad._iterlib.are_logical_voice(leaves[:4])


def test__iterlib_are_logical_voice_34():
    """
    Logical voice does extend across gaps.
    Logical voice can not extend across differently named implicit voices.
    """

    staff = abjad.Staff(
        r"""
        c'8
        cs'8
        \new Staff {
            d'8
            ef'8
            \new Staff {
                e'8
                f'8
                fs'8
                g'8
            }
            af'8
            a'8
        }
        bf'8
        b'8
        """
    )

    outer = (0, 1, 10, 11)
    middle = (2, 3, 8, 9)
    inner = (4, 5, 6, 7)

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'8
            cs'8
            \new Staff
            {
                d'8
                ef'8
                \new Staff
                {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
                af'8
                a'8
            }
            bf'8
            b'8
        }
        """
    )

    leaves = abjad.select.leaves(staff)
    assert abjad._iterlib.are_logical_voice([leaves[i] for i in outer])
    assert abjad._iterlib.are_logical_voice([leaves[i] for i in middle])
    assert abjad._iterlib.are_logical_voice([leaves[i] for i in inner])
    assert not abjad._iterlib.are_logical_voice(leaves[:4])


def test__iterlib_are_logical_voice_35():
    """
    Containers and leaves all appear in same logical voice.
    """

    container = abjad.Container(
        r"""
        c'8
        cs'8
        {
            d'8
            ef'8
            {
                e'8
                f'8
                fs'8
                g'8
            }
            af'8
            a'8
        }
        bf'8
        b'8
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'8
            cs'8
            {
                d'8
                ef'8
                {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
                af'8
                a'8
            }
            bf'8
            b'8
        }
        """
    )

    components = abjad.select.components(container)
    assert abjad._iterlib.are_logical_voice(components)


def test__iterlib_are_logical_voice_36():
    """
    Logical voice can not extend across differently named voices.
    """

    container = abjad.Container(
        r"""
        c'8
        cs'8
        {
            {
                \context Voice = "foo" {
                    d'8
                    ef'8
                    e'8
                    f'8
                }
            }
        }
        fs'8
        g'8
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'8
            cs'8
            {
                {
                    \context Voice = "foo"
                    {
                        d'8
                        ef'8
                        e'8
                        f'8
                    }
                }
            }
            fs'8
            g'8
        }
        """
    )

    outer = (0, 1, 6, 7)
    inner = (2, 3, 4, 5)

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice([leaves[i] for i in outer])
    assert abjad._iterlib.are_logical_voice([leaves[i] for i in inner])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_37():
    """
    Logical voice does not extend over differently named voices.
    """

    container = abjad.Container(
        r"""
        {
            {
                \context Voice = "foo" {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
        }
        e'8
        f'8
        fs'8
        g'8
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            {
                {
                    \context Voice = "foo"
                    {
                        c'8
                        cs'8
                        d'8
                        ef'8
                    }
                }
            }
            e'8
            f'8
            fs'8
            g'8
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_38():
    """
    Can not nest across differently named implicit voices.
    """

    container = abjad.Voice(
        r"""
        {
            {
                {
                    c'8
                    cs'8
                    \new Voice {
                        d'8
                        ef'8
                        e'8
                        f'8
                    }
                    fs'8
                    g'8
                }
            }
        }
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                {
                    {
                        c'8
                        cs'8
                        \new Voice
                        {
                            d'8
                            ef'8
                            e'8
                            f'8
                        }
                        fs'8
                        g'8
                    }
                }
            }
        }
        """
    )

    outer = (0, 1, 6, 7)
    inner = (2, 3, 4, 5)

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice([leaves[i] for i in outer])
    assert abjad._iterlib.are_logical_voice([leaves[i] for i in inner])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_39():
    """
    Logical voice can not extend across differently named voices.
    """

    voice = abjad.Voice(
        r"""
        c'8
        cs'8
        {
            d'8
            ef'8
            {
                e'8
                f'8
                \context Voice = "bar" {
                    fs'8
                    g'8
                    af'8
                    a'8
                }
                bf'8
                b'8
            }
            c''8
            cs''8
        }
        d''8
        ef''8
        """
    )

    voice.set_name("foo")

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \context Voice = "foo"
        {
            c'8
            cs'8
            {
                d'8
                ef'8
                {
                    e'8
                    f'8
                    \context Voice = "bar"
                    {
                        fs'8
                        g'8
                        af'8
                        a'8
                    }
                    bf'8
                    b'8
                }
                c''8
                cs''8
            }
            d''8
            ef''8
        }
        """
    )

    outer = (0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15)
    inner = (6, 7, 8, 9)

    leaves = abjad.select.leaves(voice)
    assert abjad._iterlib.are_logical_voice([leaves[i] for i in outer])
    assert abjad._iterlib.are_logical_voice([leaves[i] for i in inner])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_40():
    """
    Logical voice can not extend across differently named anonymous voices.
    """

    container = abjad.Container(
        r"""
        \new Voice {
            c'8
            cs'8
            d'8
            ef'8
        }
        \new Voice {
            e'8
            f'8
            fs'8
            g'8
        }
        af'8
        a'8
        bf'8
        b'8
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \new Voice
            {
                c'8
                cs'8
                d'8
                ef'8
            }
            \new Voice
            {
                e'8
                f'8
                fs'8
                g'8
            }
            af'8
            a'8
            bf'8
            b'8
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice(leaves[:4])
    assert abjad._iterlib.are_logical_voice(leaves[4:8])
    assert abjad._iterlib.are_logical_voice(leaves[8:])
    assert not abjad._iterlib.are_logical_voice(leaves[:8])
    assert not abjad._iterlib.are_logical_voice(leaves[4:])
    assert not abjad._iterlib.are_logical_voice(leaves)


def test__iterlib_are_logical_voice_41():
    """
    Logical voice can not extend across differently named anonymous voices.
    """

    container = abjad.Container(
        r"""
        c'8
        cs'8
        <<
            \new Voice {
                d'8
                ef'8
                e'8
                f'8
            }
            \new Voice {
                fs'8
                g'8
                af'8
                a'8
            }
        >>
        bf'8
        b'8
        """
    )

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'8
            cs'8
            <<
                \new Voice
                {
                    d'8
                    ef'8
                    e'8
                    f'8
                }
                \new Voice
                {
                    fs'8
                    g'8
                    af'8
                    a'8
                }
            >>
            bf'8
            b'8
        }
        """
    )

    outer = (0, 1, 10, 11)

    leaves = abjad.select.leaves(container)
    assert abjad._iterlib.are_logical_voice([leaves[i] for i in outer])
    assert abjad._iterlib.are_logical_voice(leaves[2:6])
    assert abjad._iterlib.are_logical_voice(leaves[6:10])
    assert not abjad._iterlib.are_logical_voice(leaves[:6])
    assert not abjad._iterlib.are_logical_voice(leaves)
