from abjad import *


def test_componenttools_all_are_orphan_components_01():

    assert componenttools.all_are_orphan_components([])
    assert componenttools.all_are_orphan_components([Note("c'8")])


def test_componenttools_all_are_orphan_components_02():

    voice = Voice("c'8 d'8 e'8")

    assert not componenttools.all_are_orphan_components(voice)
