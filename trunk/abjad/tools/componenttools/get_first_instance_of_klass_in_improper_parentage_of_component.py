from abjad.tools.componenttools.get_improper_parentage_of_component import get_improper_parentage_of_component


def get_first_instance_of_klass_in_improper_parentage_of_component(component, klass):
    '''.. versionadded:: 2.0

    Get first instance of `klass` in improper parentage of `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(staff[0], Note)
        Note("c'8")

    Return component or none.
    '''

    for parent in get_improper_parentage_of_component(component):
        if isinstance(parent, klass):
            return parent
