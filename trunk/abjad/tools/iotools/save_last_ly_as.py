# -*- encoding: utf-8 -*-
import os


def save_last_ly_as(file_name):
    r'''Save last ly file as `file_name`:

    ::

        >>> iotools.save_last_ly_as('/project/output/example-1.ly') # doctest: +SKIP

    Return none.
    '''
    from abjad import abjad_configuration
    from abjad.tools import iotools
    ABJADOUTPUT = abjad_configuration['abjad_output']
    last_output_file_name = iotools.get_last_output_file_name()
    without_extension, extension = os.path.splitext(last_output_file_name)
    last_ly = without_extension + '.ly'
    last_ly_full_name = os.path.join(ABJADOUTPUT, last_ly)
    old = open(last_ly_full_name, 'r')
    new = open(file_name, 'w')
    new.write(''.join(old.readlines()))
    old.close()
    new.close()
