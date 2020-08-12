import abjad


def test_get_leaf_01():

    staff = abjad.Staff(
        [abjad.Voice("c'8 d'8 e'8 f'8"), abjad.Voice("g'8 a'8 b'8 c''8")]
    )

    assert abjad.lilypond(staff) == abjad.String.normalize(
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

    leaves = abjad.select(staff).leaves()
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

    assert abjad.lilypond(voice) == abjad.String.normalize(
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

    assert abjad.lilypond(staff) == abjad.String.normalize(
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

    assert abjad.lilypond(container) == abjad.String.normalize(
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

    assert abjad.lilypond(tuplet) == abjad.String.normalize(
        r"""
        \times 2/3 {
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

    assert abjad.lilypond(voice) == abjad.String.normalize(
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

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \times 2/3 {
                c'8
                cs'8
                d'8
            }
            \times 2/3 {
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

    assert abjad.lilypond(staff) == abjad.String.normalize(
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

    assert abjad.lilypond(staff) == abjad.String.normalize(
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

    assert abjad.lilypond(staff) == abjad.String.normalize(
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

    assert abjad.lilypond(container) == abjad.String.normalize(
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

    assert abjad.lilypond(container) == abjad.String.normalize(
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

    assert abjad.lilypond(voice) == abjad.String.normalize(
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

    assert abjad.lilypond(voice) == abjad.String.normalize(
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

    assert abjad.lilypond(voice) == abjad.String.normalize(
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

    assert abjad.lilypond(voice) == abjad.String.normalize(
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

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \times 2/3 {
                c'8
                cs'8
                d'8
            }
            ef'8
            \times 2/3 {
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

    assert abjad.lilypond(tuplet) == abjad.String.normalize(
        r"""
        \times 2/3 {
            c'4
            \times 2/3 {
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

    assert abjad.lilypond(staff) == abjad.String.normalize(
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

    assert abjad.lilypond(staff) == abjad.String.normalize(
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

    assert abjad.lilypond(outer_voice) == abjad.String.normalize(
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

    assert abjad.lilypond(outer_voice) == abjad.String.normalize(
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

    assert abjad.lilypond(outer_voice) == abjad.String.normalize(
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

    assert abjad.lilypond(outer_voice) == abjad.String.normalize(
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

    assert abjad.lilypond(outer_voice) == abjad.String.normalize(
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

    assert abjad.lilypond(voice_1) == abjad.String.normalize(
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
