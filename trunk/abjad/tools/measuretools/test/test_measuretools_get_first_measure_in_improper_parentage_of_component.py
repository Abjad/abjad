from abjad import *


def test_measuretools_get_first_measure_in_improper_parentage_of_component_01():

    measure = Measure((2, 4), "c'8 d'8 e'8 f'8")
    staff = Staff([measure])

    assert measuretools.get_first_measure_in_improper_parentage_of_component(staff[0][0]) is measure
    assert measuretools.get_first_measure_in_improper_parentage_of_component(staff[0][1]) is measure
    assert measuretools.get_first_measure_in_improper_parentage_of_component(staff[0][2]) is measure
    assert measuretools.get_first_measure_in_improper_parentage_of_component(staff[0][3]) is measure

    assert measuretools.get_first_measure_in_improper_parentage_of_component(measure) is measure
    assert measuretools.get_first_measure_in_improper_parentage_of_component(staff) is None
