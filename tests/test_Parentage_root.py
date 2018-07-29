import abjad


def test_Parentage_root_01():

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    staff = abjad.Staff([tuplet])
    leaves = abjad.select(staff).leaves()

    assert abjad.inspect(staff).parentage().root is staff
    assert abjad.inspect(tuplet).parentage().root is staff
    assert abjad.inspect(leaves[0]).parentage().root is staff
    assert abjad.inspect(leaves[1]).parentage().root is staff
    assert abjad.inspect(leaves[2]).parentage().root is staff
