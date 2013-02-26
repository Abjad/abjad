import os
import re
from abjad.tools import configurationtools


def get_last_output_file_name(path=None):
    '''Get last output file name like ``6222.ly``.

    Read Abajd output directory when `path` is none.

    Return string.
    '''
    from abjad import ABJCFG

    pattern = re.compile('\d{4,4}.[a-z]{2,3}')
    path = path or ABJCFG['abjad_output']
    all_file_names = os.listdir(path)
    all_output = [fn for fn in all_file_names if pattern.match(fn)]
    if all_output == []:
        last_output_file_name = None
    else:
        last_output_file_name = sorted(all_output)[-1]
    return last_output_file_name
