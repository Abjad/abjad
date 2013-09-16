# -*- encoding: utf-8 -*-
import os


def save_last_ly_as(file_path):
    r'''Saves last LilyPond file created in Abjad as `file_path`.

    ::

        >>> file_path = '/project/output/example-1.ly'
        >>> iotools.save_last_ly_as(file_path) # doctest: +SKIP

    Returns none.
    '''
    from abjad import abjad_configuration
    from abjad.tools import iotools
    ABJADOUTPUT = abjad_configuration['abjad_output']
    last_output_file_path = iotools.get_last_output_file_name()
    without_extension, extension = os.path.splitext(last_output_file_path)
    last_ly = without_extension + '.ly'
    last_ly_full_name = os.path.join(ABJADOUTPUT, last_ly)
    old = open(last_ly_full_name, 'r')
    new = open(file_path, 'w')
    new.write(''.join(old.readlines()))
    old.close()
    new.close()
