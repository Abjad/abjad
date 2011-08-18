from abjad.tools.iotools._warn_almost_full import _warn_almost_full
from abjad.tools.iotools.get_last_output_file_name import get_last_output_file_name


def get_next_output_file_name():
    '''Get next output file name like ``6223.ly``.

    Return string.
    '''

    last_output = get_last_output_file_name()
    if last_output is None:
        next_number = 0
        next_output_file_name = '0000.ly'
    else:
        last_number = int(last_output.split('.')[0])
        next_number = last_number + 1
        next_output_file_name = '%04d.ly' % next_number
    if 9000 < next_number:
        _warn_almost_full(last_number)
    return next_output_file_name
