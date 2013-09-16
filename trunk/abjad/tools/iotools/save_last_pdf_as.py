# -*- encoding: utf-8 -*-
import os


def save_last_pdf_as(file_path):
    r'''Saves last PDF created in Abjad as `file_path`.

    ::

        >>> file_path = '/project/output/example-1.pdf'
        >>> iotools.save_last_pdf_as(file_path) # doctest: +SKIP

    Returns none.
    '''
    from abjad import abjad_configuration
    from abjad.tools import iotools
    ABJADOUTPUT = abjad_configuration['abjad_output']
    last_output_file_name = iotools.get_last_output_file_name()
    without_extension, extension = os.path.splitext(last_output_file_name)
    last_pdf = without_extension + '.pdf'
    last_pdf_full_name = os.path.join(ABJADOUTPUT, last_pdf)
    old = open(last_pdf_full_name, 'r')
    new = open(file_path, 'w')
    new.write(''.join(old.readlines()))
    old.close()
    new.close()
