# -*- encoding: utf-8 -*-


def get_next_output_file_name(file_extension='ly', output_directory_path=None):
    r'''Gets next output file name in output directory.
    
    ::

        >>> iotools.get_next_output_file_name() # doctest: +SKIP
        '6223.ly'

    Gets next output file name in Abjad output directory
    when `output_directory_path` is none.

    Returns string.
    '''
    from abjad.tools import iotools

    assert file_extension.isalpha() and \
        0 < len(file_extension) < 4, repr(file_extension)

    last_output = iotools.get_last_output_file_name(
        output_directory_path=output_directory_path,
        )
    if last_output is None:
        next_number = 0
        next_output_file_name = '0000.{}'.format(file_extension)
    else:
        last_number = int(last_output.split('.')[0])
        next_number = last_number + 1
        next_output_file_name = '{next_number:04d}.{file_extension}'
        next_output_file_name = next_output_file_name.format(
            next_number=next_number, 
            file_extension=file_extension,
            )
    if 9000 < next_number:
        iotools.warn_almost_full(last_number)
    return next_output_file_name
