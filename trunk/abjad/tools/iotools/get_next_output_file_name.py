def get_next_output_file_name(file_extension='ly'):
    '''Get next output file name like ``6223.ly``.

    Return string.
    '''
    from abjad.tools import iotools
    from abjad.tools.iotools._warn_almost_full import _warn_almost_full

    assert file_extension.isalpha() and 0 < len(file_extension) < 4

    last_output = iotools.get_last_output_file_name()
    if last_output is None:
        next_number = 0
        next_output_file_name = '0000.{}'.format(file_extension)
    else:
        last_number = int(last_output.split('.')[0])
        next_number = last_number + 1
        next_output_file_name = '{next_number:04d}.{file_extension}'.format(
            next_number=next_number, file_extension=file_extension)
    if 9000 < next_number:
        _warn_almost_full(last_number)
    return next_output_file_name
