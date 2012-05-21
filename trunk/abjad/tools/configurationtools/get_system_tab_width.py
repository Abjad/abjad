def get_system_tab_width():
    r'''.. versionadded:: 2.9

    Get system tab width::

        abjad> from abjad.tools import configurationtools

    ::

        abjad> configurationtools.get_system_tab_width()
        3

    The value is used by various functions that generate or test code in the system.

    Return nonnegative integer.
    '''

    return 3
