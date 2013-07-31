# -*- encoding: utf-8 -*-
def class_to_tools_package_qualified_class_name(current_class):
    r'''.. versionadded:: 2.10

    Change `current_class` to tools package-qualified class name:

    ::

        >>> introspectiontools.class_to_tools_package_qualified_class_name(Note)
        'notetools.Note'

    Return string.
    '''

    module_parts = current_class.__module__.split('.')
    tools_package_qualified_class_name = '.'.join(module_parts[-3:-1])

    return tools_package_qualified_class_name
