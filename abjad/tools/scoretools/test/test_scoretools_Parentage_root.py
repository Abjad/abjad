import abjad


def test_scoretools_Parentage_root_01():

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    staff = abjad.Staff([tuplet])
    leaves = abjad.select(staff).leaves()

    assert abjad.inspect(staff).get_parentage().root is staff
    assert abjad.inspect(tuplet).get_parentage().root is staff
    assert abjad.inspect(leaves[0]).get_parentage().root is staff
    assert abjad.inspect(leaves[1]).get_parentage().root is staff
    assert abjad.inspect(leaves[2]).get_parentage().root is staff
