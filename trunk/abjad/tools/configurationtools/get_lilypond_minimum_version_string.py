def get_lilypond_minimum_version_string():
    '''Get the x.x.0 version of LilyPond:

    ::

        >>> configurationtools.get_lilypond_minimum_version_string()
        '2.17.0'

    This is useful for documentation purposes, where all developers are
    using the development version of LilyPond, but not necessarily the exact
    same version.

    Return string.
    '''

    from abjad.tools import configurationtools
    version = configurationtools.get_lilypond_version_string()
    parts = version.split('.')[0:2]
    parts.append('0')
    return '.'.join(parts)
