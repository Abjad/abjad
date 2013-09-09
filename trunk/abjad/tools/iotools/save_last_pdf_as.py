# -*- encoding: utf-8 -*-
import os


def save_last_pdf_as(file_name):
    r'''Save last PDF as `file_name`:

    ::

        >>> iotools.save_last_pdf_as('/project/output/example-1.pdf') # doctest: +SKIP

    Return none.
    '''
    from abjad import abjad_configuration
    from abjad.tools import iotools
    ABJADOUTPUT = abjad_configuration['abjad_output']
    last_output_file_name = iotools.get_last_output_file_name()
    if last_output_file_name.endswith('.ly'):
        basename = last_output_file_name[:-3]
    elif last_output_file_name.endswith('.pdf'):
        basename = last_output_file_name[:-4]
    elif last_output_file_name.endswith('.mid'):
        basename = last_output_file_name[:-4]
    elif last_output_file_name.endswith('.midi'):
        basename = last_output_file_name[:-5]
    else:
        raise Exception(last_output_file_name)
    last_pdf = basename + '.pdf'
    last_pdf_full_name = os.path.join(ABJADOUTPUT, last_pdf)
    old = open(last_pdf_full_name, 'r')
    new = open(file_name, 'w')
    new.write(''.join(old.readlines()))
    old.close()
    new.close()
