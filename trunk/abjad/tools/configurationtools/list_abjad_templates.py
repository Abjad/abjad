from abjad.cfg.cfg import ABJADPATH
import os


def list_abjad_templates():
    '''.. versionadded:: 2.0

    List Abjad templates::

        abjad> from abjad.tools import configurationtools

    ::

        abjad> configurationtools.list_abjad_templates()
        ('coventry.ly', 'lagos.ly', 'oedo.ly', 'paris.ly', 'tangiers.ly', 'thebes.ly', 'tirnaveni.ly')

    Return tuple of zero or more strings.

    Abjad templates are housed in ``abjad/templates``.
    '''

    file_names = []
    for file_name in os.listdir(os.path.join(ABJADPATH, 'templates')):
        if file_name.endswith('.ly'):
            if not file_name.startswith('_'):
                file_names.append(file_name)
    return tuple(sorted(file_names))
