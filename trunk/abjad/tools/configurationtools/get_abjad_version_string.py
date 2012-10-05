def get_abjad_version_string():
    '''.. versionadded:: 2.0

    Get Abjad version string::

        >>> from abjad.tools import configurationtools

    ::

        >>> configurationtools.get_abjad_version_string()
        '2.11'

    Return string.
    '''
    import abjad

    return abjad.__version__
