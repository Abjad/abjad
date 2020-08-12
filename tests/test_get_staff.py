import abjad


def test_get_staff_01():
    """
    Staff changes work on the first note of a staff.
    """

    staff_group = abjad.StaffGroup(
        [abjad.Staff("c'8 d'8 e'8 f'8"), abjad.Staff("c'8 d'8 e'8 f'8")]
    )
    staff_group.lilypond_type = "PianoStaff"
    staff_group.simultaneous = True
    staff_group[0].name = "RH"
    staff_group[1].name = "LH"
    staff_change = abjad.StaffChange("LH")
    abjad.attach(staff_change, staff_group[0][0])

    assert abjad.lilypond(staff_group) == abjad.String.normalize(
        r"""
        \new PianoStaff
        <<
            \context Staff = "RH"
            {
                \change Staff = LH
                c'8
                d'8
                e'8
                f'8
            }
            \context Staff = "LH"
            {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        """
    )

    assert abjad.wf.wellformed(staff_group)
    assert abjad.get.effective_staff(staff_group[0][0]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][1]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][2]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][3]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][0]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][1]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][2]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][3]) is staff_group[1]


def test_get_staff_02():
    """
    Staff changes work on middle notes of a staff.
    """

    staff_group = abjad.StaffGroup(
        [abjad.Staff("c'8 d'8 e'8 f'8"), abjad.Staff("c'8 d'8 e'8 f'8")]
    )
    staff_group.lilypond_type = "PianoStaff"
    staff_group.simultaneous = True
    staff_group[0].name = "RH"
    staff_group[1].name = "LH"
    staff_change = abjad.StaffChange("LH")
    abjad.attach(staff_change, staff_group[0][0])
    staff_change = abjad.StaffChange("RH")
    abjad.attach(staff_change, staff_group[0][2])

    assert abjad.lilypond(staff_group) == abjad.String.normalize(
        r"""
        \new PianoStaff
        <<
            \context Staff = "RH"
            {
                \change Staff = LH
                c'8
                d'8
                \change Staff = RH
                e'8
                f'8
            }
            \context Staff = "LH"
            {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        """
    )

    assert abjad.wf.wellformed(staff_group)
    assert abjad.get.effective_staff(staff_group[0][0]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][1]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][2]) is staff_group[0]
    assert abjad.get.effective_staff(staff_group[0][3]) is staff_group[0]
    assert abjad.get.effective_staff(staff_group[1][0]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][1]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][2]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][3]) is staff_group[1]


def test_get_staff_03():
    """
    Staff changes work on the last note of a staff.
    """

    staff_group = abjad.StaffGroup(
        [abjad.Staff("c'8 d'8 e'8 f'8"), abjad.Staff("c'8 d'8 e'8 f'8")]
    )
    staff_group.lilypond_type = "PianoStaff"
    staff_group.simultaneous = True
    staff_group[0].name = "RH"
    staff_group[1].name = "LH"
    staff_change = abjad.StaffChange("LH")
    abjad.attach(staff_change, staff_group[0][-1])

    assert abjad.lilypond(staff_group) == abjad.String.normalize(
        r"""
        \new PianoStaff
        <<
            \context Staff = "RH"
            {
                c'8
                d'8
                e'8
                \change Staff = LH
                f'8
            }
            \context Staff = "LH"
            {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        """
    )

    assert abjad.wf.wellformed(staff_group)


def test_get_staff_04():
    """
    Redudant staff changes are allowed.
    """

    staff_group = abjad.StaffGroup(
        [abjad.Staff("c'8 d'8 e'8 f'8"), abjad.Staff("c'8 d'8 e'8 f'8")]
    )
    staff_group.lilypond_type = "PianoStaff"
    staff_group.simultaneous = True
    staff_group[0].name = "RH"
    staff_group[1].name = "LH"
    staff_change = abjad.StaffChange("LH")
    abjad.attach(staff_change, staff_group[0][0])
    staff_change = abjad.StaffChange("LH")
    abjad.attach(staff_change, staff_group[0][1])

    assert abjad.lilypond(staff_group) == abjad.String.normalize(
        r"""
        \new PianoStaff
        <<
            \context Staff = "RH"
            {
                \change Staff = LH
                c'8
                \change Staff = LH
                d'8
                e'8
                f'8
            }
            \context Staff = "LH"
            {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        """
    )

    assert abjad.wf.wellformed(staff_group)
    assert abjad.get.effective_staff(staff_group[0][0]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][1]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][2]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][3]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][0]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][1]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][2]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][3]) is staff_group[1]
