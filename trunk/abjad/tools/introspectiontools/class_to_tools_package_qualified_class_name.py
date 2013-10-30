# -*- encoding: utf-8 -*-


def class_to_tools_package_qualified_class_name(current_class):
    r'''Change `current_class` to tools package-qualified class name:

    ::

        >>> introspectiontools.class_to_tools_package_qualified_class_name(Note)
        'scoretools.Note'

    Returns string.
    '''
    module_parts = current_class.__module__.split('.')
    unique_parts = [module_parts[0]]
    for part in module_parts[1:]:
        if part != unique_parts[-1]:
            unique_parts.append(part)
    tools_package_qualified_class_name = '.'.join(unique_parts[-2:])
    return tools_package_qualified_class_name
