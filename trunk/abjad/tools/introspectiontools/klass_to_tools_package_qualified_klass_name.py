def klass_to_tools_package_qualified_klass_name(klass):
    r'''.. versionadded:: 2.10

    Change `klass` to tools package-qualified class name::

        >>> from abjad.tools import introspectiontools

    ::

        >>> introspectiontools.klass_to_tools_package_qualified_klass_name(Note)
        'notetools.Note'

    Return string.
    '''

    module_parts = klass.__module__.split('.')
    tools_package_qualified_class_name = '.'.join(module_parts[-3:-1])

    return tools_package_qualified_class_name
