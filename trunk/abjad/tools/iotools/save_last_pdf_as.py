import os
from abjad.tools import configurationtools


def save_last_pdf_as(file_name):
    r'''.. versionadded:: 2.0

    Save last PDF as `file_name`::

        >>> iotools.save_last_pdf_as('/project/output/example-1.pdf') # doctest: +SKIP

    Return none.
    '''
    from abjad import ABJCFG
    from abjad.tools import iotools

    ABJADOUTPUT = ABJCFG['abjad_output']
    last_ly = iotools.get_last_output_file_name()
    last_pdf = last_ly[:-3] + '.pdf'
    last_pdf_full_name = os.path.join(ABJADOUTPUT, last_pdf)
    old = open(last_pdf_full_name, 'r')
    new = open(file_name, 'w')
    new.write(''.join(old.readlines()))
    old.close()
    new.close()
