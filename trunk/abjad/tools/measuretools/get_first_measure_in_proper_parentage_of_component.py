from abjad.tools.measuretools.Measure import Measure
from abjad.tools import componenttools


def get_first_measure_in_proper_parentage_of_component(component):
    r'''.. versionadded:: 2.0

    Get first measure in proper parentage of `component`::

        abjad> measure = Measure((2, 4), "c'8 d'8 e'8 f'8")
        abjad> staff = Staff([measure])

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 2/4
                c'8
                d'8
                e'8
                f'8
            }
        }

    ::

        abjad> measuretools.get_first_measure_in_proper_parentage_of_component(staff.leaves[0])
        Measure(2/4, [c'8, d'8, e'8, f'8])

    Return measure or none.
    '''

    return componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(
        component, Measure)
