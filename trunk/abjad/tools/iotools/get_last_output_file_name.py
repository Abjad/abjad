# -*- encoding: utf-8 -*-
import os
import re


def get_last_output_file_name(output_directory_path=None):
    r'''Gets last output file name in output directory.
    
    ::
        
        >>> iotools.get_last_output_file_name() # doctest: +SKIP
        '6222.ly'

    Gets last output file name in Abjad output directory when
    `output_directory_path` is none.

    Returns none when output directory contains no output files.

    Returns string or none.
    '''
    from abjad import abjad_configuration
    pattern = re.compile('\d{4,4}.[a-z]{2,3}')
    output_directory_path = \
        output_directory_path or abjad_configuration['abjad_output']
    all_file_names = os.listdir(output_directory_path)
    all_output = [x for x in all_file_names if pattern.match(x)]
    if all_output == []:
        last_output_file_name = None
    else:
        last_output_file_name = sorted(all_output)[-1]
    return last_output_file_name
