def get_tab_width():
    r'''.. versionadded:: 2.9

    Get system tab width::

        >>> from abjad.tools import configurationtools

    ::

        >>> configurationtools.get_tab_width()
        4

    The value is used by various functions that generate or test code in the system.

    Return nonnegative integer.

    .. versionchanged:: 2.10
        renamed ``configurationtools.get_system_tab_width()`` to
        ``configurationtools.get_tab_width()``.
    '''

    return 4
