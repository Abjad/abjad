from abjad import *


def test_containertools_eject_contents_of_container_01():

    container = Container("c'8 d'8 e'8 f'8")

    contents = containertools.eject_contents_of_container(container)

    assert len(container) == 0
    assert len(contents) == 4
