from abjad.cfg._read_config_file import _read_config_file
import os
import re


def get_last_output_file_name():
    '''Get last output file name like ``6222.ly``.

    Return string.
    '''

    pattern = re.compile('\d{4,4}.ly')
    all_file_names = os.listdir(_read_config_file()['abjad_output'])
    all_output = [fn for fn in all_file_names if pattern.match(fn)]
    if all_output == []:
        last_output_file_name = None
    else:
        last_output_file_name = sorted(all_output)[-1]
    return last_output_file_name
