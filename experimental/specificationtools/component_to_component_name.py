def component_to_component_name(component):
    r'''.. versionadded:: 1.0
    
    Change `component` to component name. Return string unchanged.

    Return string.
    '''
    from abjad.tools import componenttools
    if isinstance(component, componenttools.Component):
        return component.name
    elif isinstance(component, str):
        return component
    else:
        raise Exception('{!r} is neither component nor string.'.format(component))
