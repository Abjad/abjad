from abjad import *


def test_componenttools_get_improper_contents_of_component_01():

    staff = Staff("c' d' e' f'")

    assert componenttools.get_improper_contents_of_component(staff) == [staff] + staff[:]
