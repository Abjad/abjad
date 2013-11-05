# -*- encoding: utf-8 -*-


def warn_almost_full(last_number):
    r'''Prints warning when Abjad output directory is almost full.

    Returns none.
    '''
    from abjad import abjad_configuration
    abjad_output = abjad_configuration['abjad_output']
    max_number = 10000
    lines = []
    lines.append('')
    lines.append('WARNING: Abjad output directory almost full!')
    line = 'Abjad output directory contains {} files and only {} are allowed.'
    line = line.format(last_number, max_number)
    lines.append(line)
    line = 'Please empty {} soon!'.format(abjad_output)
    lines.append(line)
    lines.append('')
    for line in lines:
        print line.center(80)
