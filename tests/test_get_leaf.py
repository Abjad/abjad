import abjad


def test_get_leaf_01():
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

    leaves = abjad.select.leaves(staff)
    assert abjad.get.leaf(leaves[0], -1) is None
    assert abjad.get.leaf(leaves[0], 0) is leaves[0]
    assert abjad.get.leaf(leaves[0], 1) is leaves[1]


def test_get_leaf_02():
    """
    Voice.
    """

    voice = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4)])

    assert abjad.get.leaf(voice[0], 1) is voice[1]
    assert abjad.get.leaf(voice[1], 1) is voice[2]
    assert abjad.get.leaf(voice[2], 1) is voice[3]
    assert abjad.get.leaf(voice[3], 1) is None

    assert abjad.get.leaf(voice[0], -1) is None
    assert abjad.get.leaf(voice[1], -1) is voice[0]
    assert abjad.get.leaf(voice[2], -1) is voice[1]
    assert abjad.get.leaf(voice[3], -1) is voice[2]

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            cs'8
            d'8
            ef'8
        }
        """
    )


def test_get_leaf_03():
    """
    Staff.
    """

    staff = abjad.Staff([abjad.Note(i, (1, 8)) for i in range(4)])

    assert abjad.get.leaf(staff[0], 1) is staff[1]
    assert abjad.get.leaf(staff[1], 1) is staff[2]
    assert abjad.get.leaf(staff[2], 1) is staff[3]
    assert abjad.get.leaf(staff[3], 1) is None

    assert abjad.get.leaf(staff[0], -1) is None
    assert abjad.get.leaf(staff[1], -1) is staff[0]
    assert abjad.get.leaf(staff[2], -1) is staff[1]
    assert abjad.get.leaf(staff[3], -1) is staff[2]

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'8
            cs'8
            d'8
            ef'8
        }
        """
    )


def test_get_leaf_04():
    """
    Container.
    """

    container = abjad.Container([abjad.Note(i, (1, 8)) for i in range(4)])

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'8
            cs'8
            d'8
            ef'8
        }
        """
    )

    assert abjad.get.leaf(container[0], 1) is container[1]
    assert abjad.get.leaf(container[1], 1) is container[2]
    assert abjad.get.leaf(container[2], 1) is container[3]
    assert abjad.get.leaf(container[3], 1) is None

    assert abjad.get.leaf(container[0], -1) is None
    assert abjad.get.leaf(container[1], -1) is container[0]
    assert abjad.get.leaf(container[2], -1) is container[1]
    assert abjad.get.leaf(container[3], -1) is container[2]


def test_get_leaf_05():
    """
    Tuplet.
    """

    tuplet = abjad.Tuplet((2, 3), "c'8 cs'8 d'8")

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 3/2
        {
            c'8
            cs'8
            d'8
        }
        """
    )

    assert abjad.get.leaf(tuplet[0], 1) is tuplet[1]
    assert abjad.get.leaf(tuplet[1], 1) is tuplet[2]
    assert abjad.get.leaf(tuplet[2], 1) is None

    assert abjad.get.leaf(tuplet[0], -1) is None
    assert abjad.get.leaf(tuplet[1], -1) is tuplet[0]
    assert abjad.get.leaf(tuplet[2], -1) is tuplet[1]


def test_get_leaf_06():
    """
    Contiguous containers inside a voice.
    """

    container_1 = abjad.Container([abjad.Note(i, (1, 8)) for i in range(4)])
    container_2 = abjad.Container([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    voice = abjad.Voice([container_1, container_2])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
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

    assert abjad.get.leaf(container_1[0], 1) is container_1[1]
    assert abjad.get.leaf(container_1[1], 1) is container_1[2]
    assert abjad.get.leaf(container_1[2], 1) is container_1[3]
    assert abjad.get.leaf(container_1[3], 1) is container_2[0]

    assert abjad.get.leaf(container_1[1], -1) is container_1[0]
    assert abjad.get.leaf(container_1[2], -1) is container_1[1]
    assert abjad.get.leaf(container_1[3], -1) is container_1[2]
    assert abjad.get.leaf(container_2[0], -1) is container_1[3]


def test_get_leaf_07():
    """
    Tuplets inside a voice.
    """

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 cs'8 d'8")
    tuplet_2 = abjad.Tuplet((2, 3), "ef'8 e'8 f'8")
    voice = abjad.Voice([tuplet_1, tuplet_2])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \tuplet 3/2
            {
                c'8
                cs'8
                d'8
            }
            \tuplet 3/2
            {
                ef'8
                e'8
                f'8
            }
        }
        """
    )

    assert abjad.get.leaf(tuplet_1[0], 1) is tuplet_1[1]
    assert abjad.get.leaf(tuplet_1[1], 1) is tuplet_1[2]
    assert abjad.get.leaf(tuplet_1[2], 1) is tuplet_2[0]

    assert abjad.get.leaf(tuplet_1[1], -1) is tuplet_1[0]
    assert abjad.get.leaf(tuplet_1[2], -1) is tuplet_1[1]
    assert abjad.get.leaf(tuplet_2[0], -1) is tuplet_1[2]


def test_get_leaf_08():
    """
    Does not continue across contiguous anonymous voices inside a staff.
    """

    voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4)])
    voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    staff = abjad.Staff([voice_1, voice_2])

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
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
        }
        """
    )

    assert abjad.get.leaf(voice_1[3], 1) is None
    assert abjad.get.leaf(voice_2[0], -1) is None


def test_get_leaf_09():
    """
    Does cross contiguous equally named voices inside a staff.
    """

    voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4)])
    voice_1.name = "My Voice"
    voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    voice_2.name = "My Voice"
    staff = abjad.Staff([voice_1, voice_2])

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \context Voice = "My Voice"
            {
                c'8
                cs'8
                d'8
                ef'8
            }
            \context Voice = "My Voice"
            {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        """
    )

    assert abjad.get.leaf(voice_1[0], 1) is voice_1[1]
    assert abjad.get.leaf(voice_1[1], 1) is voice_1[2]
    assert abjad.get.leaf(voice_1[2], 1) is voice_1[3]
    assert abjad.get.leaf(voice_1[3], 1) is voice_2[0]

    assert abjad.get.leaf(voice_1[1], -1) is voice_1[0]
    assert abjad.get.leaf(voice_1[2], -1) is voice_1[1]
    assert abjad.get.leaf(voice_1[3], -1) is voice_1[2]
    assert abjad.get.leaf(voice_2[0], -1) is voice_1[3]


def test_get_leaf_10():
    """
    Does not connect through contiguous unequally named voices.
    """

    voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4)])
    voice_1.name = "Your Voice"
    voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    voice_2.name = "My Voice"
    staff = abjad.Staff([voice_1, voice_2])

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \context Voice = "Your Voice"
            {
                c'8
                cs'8
                d'8
                ef'8
            }
            \context Voice = "My Voice"
            {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        """
    )

    assert abjad.get.leaf(voice_1[0], 1) is voice_1[1]
    assert abjad.get.leaf(voice_1[1], 1) is voice_1[2]
    assert abjad.get.leaf(voice_1[2], 1) is voice_1[3]
    assert abjad.get.leaf(voice_1[3], 1) is None

    voice_2.name = None
    assert abjad.get.leaf(voice_1[3], 1) is None

    assert abjad.get.leaf(voice_2[1], -1) is voice_2[0]
    assert abjad.get.leaf(voice_2[2], -1) is voice_2[1]
    assert abjad.get.leaf(voice_2[3], -1) is voice_2[2]
    assert abjad.get.leaf(voice_2[0], -1) is None


def test_get_leaf_11():
    """
    Does connect through like-named staves containing like-named voices.
    """

    voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4)])
    voice_1.name = "low"
    voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    voice_2.name = "low"

    staff_1 = abjad.Staff([voice_1])
    staff_1.name = "mystaff"
    staff_2 = abjad.Staff([voice_2])
    staff_2.name = "mystaff"

    container = abjad.Container([staff_1, staff_2])

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \context Staff = "mystaff"
            {
                \context Voice = "low"
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
            \context Staff = "mystaff"
            {
                \context Voice = "low"
                {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
            }
        }
        """
    )

    assert abjad.get.leaf(voice_1[3], 1) is voice_2[0]
    assert abjad.get.leaf(voice_2[0], -1) is voice_1[3]


def test_get_leaf_12():
    """
    Does connect through like-named staves containing like-named voices.
    """

    lower_voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4)])
    lower_voice_1.name = "low"
    lower_voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    lower_voice_2.name = "low"
    higher_voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(12, 16)])
    higher_voice_1.name = "high"
    higher_voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(16, 20)])
    higher_voice_2.name = "high"

    staff_1 = abjad.Staff([higher_voice_1, lower_voice_1])
    staff_1.name = "mystaff"
    staff_1.simultaneous = True
    staff_2 = abjad.Staff([lower_voice_2, higher_voice_2])
    staff_2.name = "mystaff"
    staff_2.simultaneous = True

    container = abjad.Container([staff_1, staff_2])

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \context Staff = "mystaff"
            <<
                \context Voice = "high"
                {
                    c''8
                    cs''8
                    d''8
                    ef''8
                }
                \context Voice = "low"
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            >>
            \context Staff = "mystaff"
            <<
                \context Voice = "low"
                {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
                \context Voice = "high"
                {
                    e''8
                    f''8
                    fs''8
                    g''8
                }
            >>
        }
        """
    )

    assert abjad.get.leaf(lower_voice_1[3], 1) is lower_voice_2[0]
    assert abjad.get.leaf(higher_voice_1[3], 1) is higher_voice_2[0]

    assert abjad.get.leaf(lower_voice_2[0], -1) is lower_voice_1[3]
    assert abjad.get.leaf(higher_voice_2[0], -1) is higher_voice_1[3]


def test_get_leaf_13():
    """
    Does connect through symmetrical nested containers in a voice.
    """

    container_1 = abjad.Container([abjad.Note(i, (1, 8)) for i in range(4)])
    container_1 = abjad.Container([container_1])
    container_2 = abjad.Container([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    container_2 = abjad.Container([container_2])
    voice = abjad.Voice([container_1, container_2])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
            {
                {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
            }
        }
        """
    )

    assert abjad.get.leaf(container_1[0][0], 1) is container_1[0][1]
    assert abjad.get.leaf(container_1[0][1], 1) is container_1[0][2]
    assert abjad.get.leaf(container_1[0][2], 1) is container_1[0][3]
    assert abjad.get.leaf(container_1[0][3], 1) is container_2[0][0]

    assert abjad.get.leaf(container_2[0][1], -1) is container_2[0][0]
    assert abjad.get.leaf(container_2[0][2], -1) is container_2[0][1]
    assert abjad.get.leaf(container_2[0][3], -1) is container_2[0][2]
    assert abjad.get.leaf(container_2[0][0], -1) is container_1[0][3]


def test_get_leaf_14():
    """
    Tautological parentage asymmetries result in symmetric (balanced) logical
    voice parentage.
    """

    container_1 = abjad.Container([abjad.Note(i, (1, 8)) for i in range(4)])
    container_2 = abjad.Container([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    container_2 = abjad.Container([container_2])
    container_2 = abjad.Container([container_2])
    voice = abjad.Voice([container_1, container_2])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                cs'8
                d'8
                ef'8
            }
            {
                {
                    {
                        e'8
                        f'8
                        fs'8
                        g'8
                    }
                }
            }
        }
        """
    )

    assert abjad.get.leaf(container_1[0], 1) is container_1[1]
    assert abjad.get.leaf(container_1[1], 1) is container_1[2]
    assert abjad.get.leaf(container_1[2], 1) is container_1[3]
    assert abjad.get.leaf(container_1[3], 1) is container_2[0][0][0]

    assert abjad.get.leaf(container_2[0][0][1], -1) is container_2[0][0][0]
    assert abjad.get.leaf(container_2[0][0][2], -1) is container_2[0][0][1]
    assert abjad.get.leaf(container_2[0][0][3], -1) is container_2[0][0][2]
    assert abjad.get.leaf(container_2[0][0][0], -1) is container_1[3]


def test_get_leaf_15():
    """
    Tautological parentage asymmetries result in symmetric (balanced) lgoical
    voice parentage.
    """

    container_1 = abjad.Container([abjad.Note(i, (1, 8)) for i in range(4)])
    container_1 = abjad.Container([container_1])
    container_1 = abjad.Container([container_1])
    container_2 = abjad.Container([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    voice = abjad.Voice([container_1, container_2])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                {
                    {
                        c'8
                        cs'8
                        d'8
                        ef'8
                    }
                }
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

    assert abjad.get.leaf(container_1[0][0][0], 1) is container_1[0][0][1]
    assert abjad.get.leaf(container_1[0][0][1], 1) is container_1[0][0][2]
    assert abjad.get.leaf(container_1[0][0][2], 1) is container_1[0][0][3]
    assert abjad.get.leaf(container_1[0][0][3], 1) is container_2[0]

    assert abjad.get.leaf(container_2[0], -1) is container_1[0][0][3]
    assert abjad.get.leaf(container_2[1], -1) is container_2[0]
    assert abjad.get.leaf(container_2[2], -1) is container_2[1]
    assert abjad.get.leaf(container_2[3], -1) is container_2[2]


def test_get_leaf_16():
    """
    Does connect in sequence of alternating containers and notes.
    """

    container_1 = abjad.Container([abjad.Note(i, (1, 8)) for i in range(2)])
    container_2 = abjad.Container([abjad.Note(i, (1, 8)) for i in range(3, 5)])
    voice = abjad.Voice([container_1, abjad.Note(2, (1, 8)), container_2])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                cs'8
            }
            d'8
            {
                ef'8
                e'8
            }
        }
        """
    )

    assert abjad.get.leaf(container_1[1], 1) is voice[1]
    assert abjad.get.leaf(voice[1], 1) is container_2[0]

    assert abjad.get.leaf(voice[1], -1) is container_1[1]
    assert abjad.get.leaf(container_2[0], -1) is voice[1]


def test_get_leaf_17():
    """
    Does connect in sequence of alternating tuplets and notes.
    """

    notes = [abjad.Note(i, abjad.Duration(1, 8)) for i in range(3)]
    tuplet_1 = abjad.Tuplet((2, 3), notes)
    notes = [abjad.Note(i, abjad.Duration(1, 8)) for i in range(4, 7)]
    tuplet_2 = abjad.Tuplet((2, 3), notes)
    voice = abjad.Voice([tuplet_1, abjad.Note(3, (1, 8)), tuplet_2])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \tuplet 3/2
            {
                c'8
                cs'8
                d'8
            }
            ef'8
            \tuplet 3/2
            {
                e'8
                f'8
                fs'8
            }
        }
        """
    )

    assert abjad.get.leaf(tuplet_1[-1], 1) is voice[1]
    assert abjad.get.leaf(voice[1], 1) is tuplet_2[0]

    assert abjad.get.leaf(voice[1], -1) is tuplet_1[-1]
    assert abjad.get.leaf(tuplet_2[0], -1) is voice[1]


def test_get_leaf_18():
    """
    Does connect through asymmetrically nested tuplets.
    """

    inner_tuplet = abjad.Tuplet((2, 3), "c'8 c'8 c'8")
    contents = [abjad.Note("c'4"), inner_tuplet, abjad.Note("c'4")]
    tuplet = abjad.Tuplet((2, 3), contents)

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 3/2
        {
            c'4
            \tuplet 3/2
            {
                c'8
                c'8
                c'8
            }
            c'4
        }
        """
    )

    assert abjad.get.leaf(tuplet[0], 1) is inner_tuplet[0]
    assert abjad.get.leaf(inner_tuplet[-1], 1) is tuplet[-1]
    assert abjad.get.leaf(tuplet[-1], -1) is inner_tuplet[-1]
    assert abjad.get.leaf(inner_tuplet[0], -1) is tuplet[0]


def test_get_leaf_19():
    """
    Returns none in asymmetric logical voice parentage structures.
    """

    voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(3)])
    note = abjad.Note(3, (1, 8))
    voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    staff = abjad.Staff([voice_1, note, voice_2])

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                c'8
                cs'8
                d'8
            }
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

    assert abjad.get.leaf(voice_1[-1], 1) is None
    assert abjad.get.leaf(note, 1) is None

    assert abjad.get.leaf(voice_2[0], -1) is None
    assert abjad.get.leaf(note, -1) is None


def test_get_leaf_20():
    """
    Noncontiguous or broken logical voices do not connect.
    """

    voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(3)])
    voice_1.name = "My Voice"
    voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    voice_2.name = "Your Voice"
    voice_3 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    voice_3.name = "My Voice"
    staff = abjad.Staff([voice_1, voice_2, voice_3])

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \context Voice = "My Voice"
            {
                c'8
                cs'8
                d'8
            }
            \context Voice = "Your Voice"
            {
                e'8
                f'8
                fs'8
                g'8
            }
            \context Voice = "My Voice"
            {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        """
    )

    assert abjad.get.leaf(voice_1[-1], 1) is None
    assert abjad.get.leaf(voice_2[-1], 1) is None

    voice_2.name = None

    assert abjad.get.leaf(voice_1[-1], 1) is None
    assert abjad.get.leaf(voice_2[-1], 1) is None

    assert abjad.get.leaf(voice_3[0], -1) is None
    assert abjad.get.leaf(voice_2[0], -1) is None


def test_get_leaf_21():
    """
    Does not connect through nested anonymous voices.
    """

    inner_voice = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(3)])
    outer_voice = abjad.Voice([inner_voice, abjad.Note(3, (1, 8))])

    assert abjad.lilypond(outer_voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \new Voice
            {
                c'8
                cs'8
                d'8
            }
            ef'8
        }
        """
    )

    assert abjad.get.leaf(inner_voice[0], 1) is inner_voice[1]
    assert abjad.get.leaf(inner_voice[1], 1) is inner_voice[2]
    assert abjad.get.leaf(inner_voice[2], 1) is None

    assert abjad.get.leaf(inner_voice[1], -1) is inner_voice[0]
    assert abjad.get.leaf(inner_voice[2], -1) is inner_voice[1]
    assert abjad.get.leaf(outer_voice[1], -1) is None


def test_get_leaf_22():
    """
    Does not connect through nested anonymous voices.
    """

    inner_voice = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(1, 4)])
    outer_voice = abjad.Voice([abjad.Note(0, (1, 8)), inner_voice])

    assert abjad.lilypond(outer_voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            \new Voice
            {
                cs'8
                d'8
                ef'8
            }
        }
        """
    )

    assert abjad.get.leaf(inner_voice[0], 1) is inner_voice[1]
    assert abjad.get.leaf(inner_voice[1], 1) is inner_voice[2]
    assert abjad.get.leaf(outer_voice[0], 1) is None

    assert abjad.get.leaf(inner_voice[1], -1) is inner_voice[0]
    assert abjad.get.leaf(inner_voice[2], -1) is inner_voice[1]
    assert abjad.get.leaf(inner_voice[0], -1) is None


def test_get_leaf_23():
    """
    Does connect through nested equally named voices.
    """

    inner_voice = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(3)])
    inner_voice.name = "My Voice"
    outer_voice = abjad.Voice([inner_voice, abjad.Note(3, (1, 8))])
    outer_voice.name = "My Voice"

    assert abjad.lilypond(outer_voice) == abjad.string.normalize(
        r"""
        \context Voice = "My Voice"
        {
            \context Voice = "My Voice"
            {
                c'8
                cs'8
                d'8
            }
            ef'8
        }
        """
    )

    assert abjad.get.leaf(inner_voice[0], 1) is inner_voice[1]
    assert abjad.get.leaf(inner_voice[1], 1) is inner_voice[2]
    assert abjad.get.leaf(inner_voice[2], 1) is outer_voice[1]

    assert abjad.get.leaf(inner_voice[1], -1) is inner_voice[0]
    assert abjad.get.leaf(inner_voice[2], -1) is inner_voice[1]
    assert abjad.get.leaf(outer_voice[1], -1) is inner_voice[-1]


def test_get_leaf_24():
    """
    Does connect through nested equally named voices.
    """

    inner_voice = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(1, 4)])
    inner_voice.name = "My Voice"
    outer_voice = abjad.Voice([abjad.Note(0, (1, 8)), inner_voice])
    outer_voice.name = "My Voice"

    assert abjad.lilypond(outer_voice) == abjad.string.normalize(
        r"""
        \context Voice = "My Voice"
        {
            c'8
            \context Voice = "My Voice"
            {
                cs'8
                d'8
                ef'8
            }
        }
        """
    )

    assert abjad.get.leaf(inner_voice[0], 1) is inner_voice[1]
    assert abjad.get.leaf(inner_voice[1], 1) is inner_voice[2]
    assert abjad.get.leaf(outer_voice[0], 1) is inner_voice[0]

    assert abjad.get.leaf(inner_voice[1], -1) is inner_voice[0]
    assert abjad.get.leaf(inner_voice[2], -1) is inner_voice[1]
    assert abjad.get.leaf(inner_voice[0], -1) is outer_voice[0]


def test_get_leaf_25():
    """
    Returns none on nested differently named voices.
    """

    inner_voice = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(3)])
    inner_voice.name = "Your Voice"
    outer_voice = abjad.Voice([inner_voice, abjad.Note(3, (1, 8))])
    outer_voice.name = "My Voice"

    assert abjad.lilypond(outer_voice) == abjad.string.normalize(
        r"""
        \context Voice = "My Voice"
        {
            \context Voice = "Your Voice"
            {
                c'8
                cs'8
                d'8
            }
            ef'8
        }
        """
    )

    assert abjad.get.leaf(inner_voice[0], 1) is inner_voice[1]
    assert abjad.get.leaf(inner_voice[1], 1) is inner_voice[2]
    assert abjad.get.leaf(inner_voice[2], 1) is None

    assert abjad.get.leaf(inner_voice[1], -1) is inner_voice[0]
    assert abjad.get.leaf(inner_voice[2], -1) is inner_voice[1]
    assert abjad.get.leaf(outer_voice[1], -1) is None


def test_get_leaf_26():
    """
    Returns none on nested differently named voices.
    """

    voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(1, 4)])
    voice_2.name = "Voice 2"
    voice_1 = abjad.Voice([abjad.Note(0, (1, 8)), voice_2])
    voice_1.name = "Voice 1"

    assert abjad.lilypond(voice_1) == abjad.string.normalize(
        r"""
        \context Voice = "Voice 1"
        {
            c'8
            \context Voice = "Voice 2"
            {
                cs'8
                d'8
                ef'8
            }
        }
        """
    )

    assert abjad.get.leaf(voice_2[0], 1) is voice_2[1]
    assert abjad.get.leaf(voice_2[1], 1) is voice_2[2]
    assert abjad.get.leaf(voice_1[0], 1) is None

    assert abjad.get.leaf(voice_2[1], -1) is voice_2[0]
    assert abjad.get.leaf(voice_2[2], -1) is voice_2[1]
    assert abjad.get.leaf(voice_1[1], -1) is voice_2[-1]


def test__inspect_are_logical_voice_01():
    """
    Unincorporated leaves do not share a logical voice.
    Unicorporated leaves do not share a root component.
    False if not allow orphans; True if allow orphans.
    """

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
    ]
    assert abjad._getlib._are_logical_voice(notes)


def test__inspect_are_logical_voice_02():
    """
    Container and leaves all logical voice.
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
    assert abjad._getlib._are_logical_voice(components)


def test__inspect_are_logical_voice_03():
    """
    Tuplet and leaves all logical voice.
    """

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")

    r"""
    \tuplet 3/2
    {
        c'8
        d'8
        e'8
    }
    """

    components = abjad.select.components(tuplet)
    assert abjad._getlib._are_logical_voice(components)


def test__inspect_are_logical_voice_04():
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
    assert abjad._getlib._are_logical_voice(components)


def test__inspect_are_logical_voice_05():
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
    assert abjad._getlib._are_logical_voice(components)


def test__inspect_are_logical_voice_06():
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
    assert abjad._getlib._are_logical_voice(components)


def test__inspect_are_logical_voice_07():
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
    assert abjad._getlib._are_logical_voice(components)


def test__inspect_are_logical_voice_08():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)
    assert not abjad._getlib._are_logical_voice(staff[:])


def test__inspect_are_logical_voice_09():
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
    assert abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_10():
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
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_11():
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
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_12():
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
    assert not abjad._getlib._are_logical_voice(leaves[:4])


def test__inspect_are_logical_voice_13():
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
    assert abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_14():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_15():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_16():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_17():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_18():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_19():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_20():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_21():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_22():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_23():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_24():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_25():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_26():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_27():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    voice = abjad.Voice([abjad.Note(n, (1, 8)) for n in range(4)])
    container = abjad.Container([voice])
    notes = [abjad.Note(n, (1, 8)) for n in range(4, 8)]
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_28():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    voice = abjad.Voice([abjad.Note(n, (1, 8)) for n in range(4)])
    voice.name = "foo"
    container = abjad.Container([voice])
    notes = [abjad.Note(n, (1, 8)) for n in range(4, 8)]
    container = abjad.Container([container] + notes)

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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_29():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    voice_1 = abjad.Voice([abjad.Note(n, (1, 8)) for n in range(4)])
    voice_1.name = "foo"
    voice_2 = abjad.Voice([voice_1])
    voice_2.name = "bar"
    notes = [abjad.Note(n, (1, 8)) for n in range(4, 8)]
    container = abjad.Container([voice_2] + notes)

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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_30():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    voice_1 = abjad.Voice([abjad.Note(n, (1, 8)) for n in range(4)])
    voice_2 = abjad.Voice([voice_1])
    notes = [abjad.Note(n, (1, 8)) for n in range(4, 8)]
    container = abjad.Container([voice_2] + notes)

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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_31():
    """
    Logical voice can not extend across differently named implicit voices.
    """

    notes = [abjad.Note(n, (1, 8)) for n in range(4)]
    voice_1 = abjad.Voice("c''8 c''8 c''8 c''8")
    voice_2 = abjad.Voice("c'8 c'8 c'8 c'8")
    container = abjad.Container([voice_1, voice_2])
    container.simultaneous = True
    container = abjad.Container(notes + [container])

    assert abjad.lilypond(container) == abjad.string.normalize(
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

    leaves = abjad.select.leaves(container)
    assert not abjad._getlib._are_logical_voice(leaves[:8])
    assert not abjad._getlib._are_logical_voice(leaves[4:])


def test__inspect_are_logical_voice_32():
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
    assert not abjad._getlib._are_logical_voice(leaves[:8])
    assert not abjad._getlib._are_logical_voice(leaves[4:])


def test__inspect_are_logical_voice_33():
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
    assert abjad._getlib._are_logical_voice([leaves[i] for i in outer])
    assert abjad._getlib._are_logical_voice([leaves[i] for i in middle])
    assert abjad._getlib._are_logical_voice([leaves[i] for i in inner])
    assert not abjad._getlib._are_logical_voice(leaves[:4])


def test__inspect_are_logical_voice_34():
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
    assert abjad._getlib._are_logical_voice([leaves[i] for i in outer])
    assert abjad._getlib._are_logical_voice([leaves[i] for i in middle])
    assert abjad._getlib._are_logical_voice([leaves[i] for i in inner])
    assert not abjad._getlib._are_logical_voice(leaves[:4])


def test__inspect_are_logical_voice_35():
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
    assert abjad._getlib._are_logical_voice(components)


def test__inspect_are_logical_voice_36():
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
    assert abjad._getlib._are_logical_voice([leaves[i] for i in outer])
    assert abjad._getlib._are_logical_voice([leaves[i] for i in inner])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_37():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_38():
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
    assert abjad._getlib._are_logical_voice([leaves[i] for i in outer])
    assert abjad._getlib._are_logical_voice([leaves[i] for i in inner])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_39():
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

    voice.name = "foo"

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
    assert abjad._getlib._are_logical_voice([leaves[i] for i in outer])
    assert abjad._getlib._are_logical_voice([leaves[i] for i in inner])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_40():
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
    assert abjad._getlib._are_logical_voice(leaves[:4])
    assert abjad._getlib._are_logical_voice(leaves[4:8])
    assert abjad._getlib._are_logical_voice(leaves[8:])
    assert not abjad._getlib._are_logical_voice(leaves[:8])
    assert not abjad._getlib._are_logical_voice(leaves[4:])
    assert not abjad._getlib._are_logical_voice(leaves)


def test__inspect_are_logical_voice_41():
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
    assert abjad._getlib._are_logical_voice([leaves[i] for i in outer])
    assert abjad._getlib._are_logical_voice(leaves[2:6])
    assert abjad._getlib._are_logical_voice(leaves[6:10])
    assert not abjad._getlib._are_logical_voice(leaves[:6])
    assert not abjad._getlib._are_logical_voice(leaves)
