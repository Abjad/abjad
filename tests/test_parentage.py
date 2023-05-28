import abjad


def test_Parentage__id_string_01():
    """
    Returns component name if it exists. Otherwise Python ID.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    parentage = abjad.get.parentage(staff)
    assert parentage._id_string(staff).startswith("Staff-")


def test_Parentage__id_string_02():
    """
    Returns component name if it exists. Otherwise Python ID.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    parentage = abjad.get.parentage(staff)
    staff.name = "foo"
    assert parentage._id_string(staff) == "Staff-'foo'"


def test_Parentage_logical_voice_01():
    """
    An anonymous staff and its contained unvoiced leaves share the same
    signature.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")

    containment = abjad.get.parentage(staff).logical_voice()
    for component in abjad.iterate.components(staff):
        assert abjad.get.parentage(component).logical_voice() == containment


def test_Parentage_logical_voice_02():
    """
    A named staff and its contained unvoiced leaves share the same signature.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    staff.name = "foo"

    containment = abjad.get.parentage(staff).logical_voice()
    for component in abjad.iterate.components(staff):
        assert abjad.get.parentage(component).logical_voice() == containment


def test_Parentage_logical_voice_03():
    """
    Leaves inside equally named sequential voices inside a staff share the
    same signature.
    """

    staff = abjad.Staff(
        [abjad.Voice("c'8 d'8 e'8 f'8"), abjad.Voice("c'8 d'8 e'8 f'8")]
    )
    staff[0].name = "foo"
    staff[1].name = "foo"

    containment = abjad.get.parentage(staff[0][0]).logical_voice()
    for leaf in abjad.iterate.leaves(staff):
        assert abjad.get.parentage(leaf).logical_voice() == containment


def test_Parentage_logical_voice_04():
    """
    Returns logical voice giving the root and first voice, staff and score in
    the parentage of component.
    """

    voice = abjad.Voice(
        r"""
        c'8
        d'8
        <<
            \new Voice {
                e'8
                f'8
            }
            \new Voice {
                g'8
                a'8
            }
        >>
        b'8
        c''8
        """
    )

    abjad.override(voice).NoteHead.color = "#red"

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        \with
        {
            \override NoteHead.color = #red
        }
        {
            c'8
            d'8
            <<
                \new Voice
                {
                    e'8
                    f'8
                }
                \new Voice
                {
                    g'8
                    a'8
                }
            >>
            b'8
            c''8
        }
        """
    )

    signatures = [
        abjad.get.parentage(leaf).logical_voice()
        for leaf in abjad.iterate.leaves(voice)
    ]

    assert signatures[0] == signatures[1]
    assert signatures[0] != signatures[2]
    assert signatures[0] != signatures[4]
    assert signatures[0] == signatures[6]

    assert signatures[2] == signatures[3]
    assert signatures[2] != signatures[4]


def test_Parentage_logical_voice_05():
    """
    Returns logical voice giving the root and first voice, staff and score in
    parentage of component.
    """

    voice = abjad.Voice(
        r"""
        c'8
        d'8
        <<
            \context Voice = "foo" {
                e'8
                f'8
            }
            \new Voice {
                g'8
                a'8
            }
        >>
        b'8
        c''8
        """
    )

    abjad.override(voice).NoteHead.color = "#red"
    voice.name = "foo"

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \context Voice = "foo"
        \with
        {
            \override NoteHead.color = #red
        }
        {
            c'8
            d'8
            <<
                \context Voice = "foo"
                {
                    e'8
                    f'8
                }
                \new Voice
                {
                    g'8
                    a'8
                }
            >>
            b'8
            c''8
        }
        """
    )

    signatures = [
        abjad.get.parentage(leaf).logical_voice()
        for leaf in abjad.iterate.leaves(voice)
    ]

    signatures[0] == signatures[1]
    signatures[0] == signatures[2]
    signatures[0] != signatures[4]
    signatures[0] == signatures[6]

    signatures[2] == signatures[0]
    signatures[2] == signatures[3]
    signatures[2] == signatures[4]
    signatures[2] == signatures[6]

    signatures[4] != signatures[0]
    signatures[4] != signatures[2]
    signatures[4] == signatures[5]
    signatures[4] == signatures[6]


def test_Parentage_logical_voice_06():
    """
    Returns logical voice giving the root and first voice, staff and score in
    parentage of component.
    """

    container = abjad.Container(
        [abjad.Staff([abjad.Voice("c'8 d'8")]), abjad.Staff([abjad.Voice("e'8 f'8")])]
    )
    container[0].name = "staff1"
    container[1].name = "staff2"
    container[0][0].name = "voicefoo"
    container[1][0].name = "voicefoo"
    leaves = abjad.select.leaves(container)
    abjad.beam(leaves[:2])
    abjad.beam(leaves[2:])

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \context Staff = "staff1"
            {
                \context Voice = "voicefoo"
                {
                    c'8
                    [
                    d'8
                    ]
                }
            }
            \context Staff = "staff2"
            {
                \context Voice = "voicefoo"
                {
                    e'8
                    [
                    f'8
                    ]
                }
            }
        }
        """
    )

    signatures = [abjad.get.parentage(leaf).logical_voice() for leaf in leaves]

    signatures[0] == signatures[1]
    signatures[0] != signatures[2]

    signatures[2] != signatures[2]
    signatures[2] == signatures[3]


def test_Parentage_logical_voice_07():
    """
    Returns logical voice giving the root and first voice, staff and score in
    parentage of component.
    """

    container = abjad.Container(
        r"""
        c'8
        <<
            \context Voice = "alto" {
                d'8
            }
            \context Voice = "soprano" {
                e'8
            }
        >>
        {
            \context Voice = "alto" {
                f'8
            }
            \context Voice = "soprano" {
                g'8
            }
        }
        a'8
        """
    )

    abjad.override(container[1][1]).NoteHead.color = "#red"
    abjad.override(container[2][1]).NoteHead.color = "#red"

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'8
            <<
                \context Voice = "alto"
                {
                    d'8
                }
                \context Voice = "soprano"
                \with
                {
                    \override NoteHead.color = #red
                }
                {
                    e'8
                }
            >>
            {
                \context Voice = "alto"
                {
                    f'8
                }
                \context Voice = "soprano"
                \with
                {
                    \override NoteHead.color = #red
                }
                {
                    g'8
                }
            }
            a'8
        }
        """
    )

    signatures = [
        abjad.get.parentage(leaf).logical_voice()
        for leaf in abjad.iterate.leaves(container)
    ]

    signatures[0] != signatures[1]
    signatures[0] != signatures[2]
    signatures[0] != signatures[3]
    signatures[0] != signatures[4]
    signatures[0] == signatures[5]

    signatures[1] != signatures[0]
    signatures[1] != signatures[2]
    signatures[1] == signatures[3]
    signatures[1] != signatures[4]
    signatures[1] != signatures[5]

    signatures[2] != signatures[0]
    signatures[2] != signatures[1]
    signatures[2] != signatures[3]
    signatures[2] == signatures[4]
    signatures[2] != signatures[5]


def test_Parentage_logical_voice_08():
    """
    Unicorporated leaves carry equivalent containment signatures.
    """

    note_1 = abjad.Note(0, (1, 8))
    note_2 = abjad.Note(0, (1, 8))

    signature_1 = abjad.get.parentage(note_1).logical_voice()
    signature_2 = abjad.get.parentage(note_2).logical_voice()
    assert signature_1 == signature_2


def test_Parentage_logical_voice_09():
    """
    Notes appear in the same logical voice.
    """

    staff_1 = abjad.Staff([abjad.Voice([abjad.Note(0, (1, 8))])])
    staff_1.name = "staff"
    staff_1[0].name = "voice"

    staff_2 = abjad.Staff([abjad.Voice([abjad.Note(0, (1, 8))])])
    staff_2.name = "staff"
    staff_2[0].name = "voice"

    staff_1_leaf_signature = abjad.get.parentage(staff_1[0][0]).logical_voice()
    staff_2_leaf_signature = abjad.get.parentage(staff_2[0][0]).logical_voice()
    assert staff_1_leaf_signature == staff_2_leaf_signature


def test_Parentage_logical_voice_10():
    """
    Measure and leaves must carry same logical voice signature.
    """

    staff = abjad.Staff(
        r"""
        {
            \time 2/8
            c'8
            d'8
        }
        e'8
        f'8
        """
    )
    abjad.Score([staff], name="Score")

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                d'8
            }
            e'8
            f'8
        }
        """
    )

    assert (
        abjad.get.parentage(staff[0]).logical_voice()
        == abjad.get.parentage(staff[-1]).logical_voice()
    )
    assert (
        abjad.get.parentage(staff[0]).logical_voice()
        == abjad.get.parentage(staff[0][0]).logical_voice()
    )
    assert (
        abjad.get.parentage(staff[0][0]).logical_voice()
        == abjad.get.parentage(staff[-1]).logical_voice()
    )


def test_Parentage_logical_voice_11():
    """
    Leaves inside different staves have different logical voice signatures,
    even when the staves have the same name.
    """

    container = abjad.Container([abjad.Staff("c'8 c'8"), abjad.Staff("c'8 c'8")])
    container[0].name = container[1].name = "staff"

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \context Staff = "staff"
            {
                c'8
                c'8
            }
            \context Staff = "staff"
            {
                c'8
                c'8
            }
        }
        """
    )

    leaves = abjad.select.leaves(container)
    assert (
        abjad.get.parentage(leaves[0]).logical_voice()
        == abjad.get.parentage(leaves[1]).logical_voice()
    )
    assert (
        abjad.get.parentage(leaves[0]).logical_voice()
        != abjad.get.parentage(leaves[2]).logical_voice()
    )
    assert (
        abjad.get.parentage(leaves[2]).logical_voice()
        == abjad.get.parentage(leaves[3]).logical_voice()
    )
    assert (
        abjad.get.parentage(leaves[2]).logical_voice()
        != abjad.get.parentage(leaves[0]).logical_voice()
    )


def test_Parentage_orphan_01():
    staff = abjad.Staff("c'8 d'8 e'8 f'8")

    assert abjad.get.parentage(staff).orphan
    for note in staff:
        assert not abjad.get.parentage(note).orphan


def test_Parentage_root_01():
    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    staff = abjad.Staff([tuplet])
    leaves = abjad.select.leaves(staff)

    assert abjad.get.parentage(staff).root is staff
    assert abjad.get.parentage(tuplet).root is staff
    assert abjad.get.parentage(leaves[0]).root is staff
    assert abjad.get.parentage(leaves[1]).root is staff
    assert abjad.get.parentage(leaves[2]).root is staff
