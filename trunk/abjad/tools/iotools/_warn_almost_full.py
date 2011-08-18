from abjad.cfg._read_config_file import _read_config_file


def _warn_almost_full(last_number):
    ABJADOUTPUT = _read_config_file()['abjad_output']
    max_number = 10000
    lines = [
        '',
        'WARNING: Abjad output directory almost full!',
        'Abjad output directory contains %s files and only %s are allowed.' % (
            last_number, max_number),
        'Please empty %s soon!' % ABJADOUTPUT,
        '']
    for line in lines:
        print line.center(80)
