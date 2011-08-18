from abjad.cfg._read_config_file import _read_config_file
from abjad.tools.iotools.get_last_output_file_name import get_last_output_file_name
import os


def save_last_ly_as(file_name):
    r'''.. versionadded:: 2.0

    Save last ly file as `file_name`::

        abjad> iotools.save_last_ly_as('/project/output/example-1.ly') # doctest: +SKIP

    Return none.
    '''

    ABJADOUTPUT = _read_config_file()['abjad_output']
    last_ly = get_last_output_file_name()
    last_ly_full_name = os.path.join(ABJADOUTPUT, last_ly)
    old = open(last_ly_full_name, 'r')
    new = open(file_name, 'w')
    new.write(''.join(old.readlines()))
    old.close()
    new.close()
