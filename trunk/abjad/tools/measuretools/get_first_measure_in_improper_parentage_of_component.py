from abjad.tools import componenttools


def get_first_measure_in_improper_parentage_of_component(component):
    r'''.. versionadded:: 2.0

    Get first measure in improper parentage of `component`::

        >>> measure = Measure((2, 4), "c'8 d'8 e'8 f'8")
        >>> staff = Staff([measure])

    ::

        >>> f(staff)
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

        >>> measuretools.get_first_measure_in_improper_parentage_of_component(staff.leaves[0])
        Measure(2/4, [c'8, d'8, e'8, f'8])

    Return measure or none.
    '''
    from abjad.tools import measuretools

    return componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        component, measuretools.Measure)
