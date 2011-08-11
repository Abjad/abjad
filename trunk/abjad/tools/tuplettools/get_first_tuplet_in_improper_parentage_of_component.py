from abjad.tools.tuplettools.Tuplet import Tuplet
from abjad.tools import componenttools


def get_first_tuplet_in_improper_parentage_of_component(component):
    r'''.. versionadded:: 2.0

    Get first tuplet in improper parentage of `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> Tuplet(Fraction(2, 3), staff[:3])
        Tuplet(2/3, [c'8, d'8, e'8])

    ::

        abjad> f(staff)
        \new Staff {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            f'8
        }

    ::

        abjad> tuplettools.get_first_tuplet_in_improper_parentage_of_component(staff.leaves[1])
        Tuplet(2/3, [c'8, d'8, e'8])

    Return tuplet or none.
    '''

    return componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        component, Tuplet)
