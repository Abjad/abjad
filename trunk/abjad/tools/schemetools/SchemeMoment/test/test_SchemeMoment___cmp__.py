from abjad import *


def test_SchemeMoment___cmp___01():

    scheme_moment_1 = schemetools.SchemeMoment(1, 68)
    scheme_moment_2 = schemetools.SchemeMoment(1, 68)
    scheme_moment_3 = schemetools.SchemeMoment(1, 60)

    assert      scheme_moment_1 == scheme_moment_1
    assert      scheme_moment_1 == scheme_moment_2
    assert not scheme_moment_1 == scheme_moment_3

    assert not scheme_moment_1 != scheme_moment_1
    assert not scheme_moment_1 != scheme_moment_2
    assert      scheme_moment_1 != scheme_moment_3

    assert not scheme_moment_1 <  scheme_moment_1
    assert not scheme_moment_1 <  scheme_moment_2
    assert      scheme_moment_1 <  scheme_moment_3

    assert      scheme_moment_1 <= scheme_moment_1
    assert      scheme_moment_1 <= scheme_moment_2
    assert      scheme_moment_1 <= scheme_moment_3

    assert not scheme_moment_1 > scheme_moment_1
    assert not scheme_moment_1 > scheme_moment_2
    assert not scheme_moment_1 > scheme_moment_3

    assert      scheme_moment_1 >= scheme_moment_1
    assert      scheme_moment_1 >= scheme_moment_2
    assert not scheme_moment_1 >= scheme_moment_3
