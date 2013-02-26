def get_next_output_file_name(file_extension='ly', path=None):
    '''Get next output file name like ``6223.ly``.

    Read Abjad output directory when `path` is none.

    Return string.
    '''
    from abjad.tools import iotools
    from abjad.tools.iotools._warn_almost_full import _warn_almost_full

    assert file_extension.isalpha() and 0 < len(file_extension) < 4, repr(file_extension)

    last_output = iotools.get_last_output_file_name(path=path)
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
