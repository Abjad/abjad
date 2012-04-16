from abjad.cfg import cfg


def get_abjad_version_string():
    '''.. versionadded:: 2.0

    Get Abjad version string::

        abjad> from abjad.tools import configurationtools

    ::

        abjad> configurationtools.get_abjad_version_string()
        '2.8'

    Return string.
    '''

    return vars(cfg)['abjad_version_number']
