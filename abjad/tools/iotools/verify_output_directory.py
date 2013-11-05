# -*- encoding: utf-8 -*-
import os


def verify_output_directory(directory):
    r'''Verifies output `directory`.

    Returns none.
    '''
    if not os.path.isdir(directory):
        lines = []
        line = 'Attention: {!} does not exist on your system.'
        line = line.format(directory)
        lines.append(line)
        lines.append('Abjad will now create it to store all output files.')
        lines.append('Press any key to continue.')
        message = '\n'.join(lines)
        raw_input(message)
        os.makedirs(directory)
