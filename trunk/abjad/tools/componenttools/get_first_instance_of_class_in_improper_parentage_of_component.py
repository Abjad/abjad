def get_first_instance_of_class_in_improper_parentage_of_component(
    component, parentage_class):
    '''.. versionadded:: 2.0

    Get first instance of `parentage_class` in 
    improper parentage of `component`:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> componenttools.get_first_instance_of_class_in_improper_parentage_of_component(
        ...     staff[0], Note)
        Note("c'8")

    Return component or none.
    '''
    for parent in component.select_parentage(include_self=True):
        if isinstance(parent, parentage_class):
            return parent
