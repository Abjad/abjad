from abjad.cfg import cfg


def get_abjad_version_string():
    '''.. versionadded:: 2.0

    Get Abjad version string::

        abjad> from abjad.tools import cfgtools

    ::

        abjad> cfgtools.get_abjad_version_string()
        '1.1.2'

    Return string.
    '''

    return vars(cfg)['abjad_version_number']
