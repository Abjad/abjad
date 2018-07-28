import abjad


def test_Parentage__get_governor_01( ):
    """
    Returns the last sequential container in the parentage of client
    such that the next element in the parentage of client is
    either a simultaneous container or None.
    """

    voice = abjad.Voice([abjad.Container([abjad.Voice("c'8 d'8"), abjad.Voice("e'8 f'8")])])
    voice[0].is_simultaneous = True
    voice[0][0].name = 'voice 1'
    voice[0][1].name = 'voice 2'

    r"""
    \new Voice {
        <<
            \context Voice = "voice 1" {
                c'8
                d'8
            }
            \context Voice = "voice 2" {
                e'8
                f'8
            }
        >>
    }
    """

    leaves = abjad.select(voice).leaves()
    assert abjad.inspect(leaves[0]).parentage()._get_governor() is voice[0][0]
    assert abjad.inspect(leaves[1]).parentage()._get_governor() is voice[0][0]
    assert abjad.inspect(leaves[2]).parentage()._get_governor() is voice[0][1]
    assert abjad.inspect(leaves[3]).parentage()._get_governor() is voice[0][1]


def test_Parentage__get_governor_02( ):
    """
    Unicorporated leaves have no governor.
    """

    note = abjad.Note(0, (1, 8))
    assert abjad.inspect(note).parentage()._get_governor() is None


def test_Parentage__get_governor_03( ):
    """
    Returns the last sequential container in the parentage of client
    such that the next element in the parentage of client is
    either a simultaneous container or None.
    """

    staff = abjad.Staff([abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8")])])

    r"""
    \new Staff {
        \new Voice {
            {
                c'8
                d'8
                e'8
                f'8
            }
        }
    }
    """

    leaves = abjad.select(staff).leaves()
    assert abjad.inspect(leaves[0]).parentage()._get_governor() is staff
    assert abjad.inspect(leaves[1]).parentage()._get_governor() is staff
    assert abjad.inspect(leaves[2]).parentage()._get_governor() is staff
    assert abjad.inspect(leaves[3]).parentage()._get_governor() is staff


def test_Parentage__get_governor_04( ):
    """
    Returns the last sequential container in the parentage of client
    such that the next element in the parentage of client is
    either a simultaneous container or None.
    """

    staff = abjad.Staff([abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8")])])

    r"""
    \new Staff {
        \new Voice {
            {
                c'8
                d'8
                e'8
                f'8
            }
        }
    }
    """

    assert abjad.inspect(staff[0][0]).parentage()._get_governor() is staff
    assert abjad.inspect(staff[0]).parentage()._get_governor() is staff
    assert abjad.inspect(staff).parentage()._get_governor() is staff
