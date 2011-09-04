from abjad.cfg.cfg import ABJADVERSIONFILE


def get_abjad_revision_string():
    '''.. versionadded:: 2.0

    Get Abjad revision string::

        abjad> configurationtools.get_abjad_revision_string() # doctest: +SKIP
        '4392'

    Return string.
    '''

    return file(ABJADVERSIONFILE, 'r').read().strip()
