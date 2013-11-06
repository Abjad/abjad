# -*- encoding: utf-8 -*-
import os


def log():
    r'''Opens the LilyPond log file in operating system-specific text editor.

    ::

        >>> iotools.log() # doctest: +SKIP

    ::

        GNU LilyPond 2.12.2
        Processing `0440.ly'
        Parsing...
        Interpreting music...
        Preprocessing graphical objects...
        Finding the ideal number of pages...
        Fitting music on 1 page...
        Drawing systems...
        Layout output to `0440.ps'...
        Converting to `./0440.pdf'...

    Returns none.
    '''
    from abjad import abjad_configuration
    from abjad.tools import iotools
    abjad_output = abjad_configuration['abjad_output']
    text_editor = abjad_configuration.get_text_editor()
    log_file_path = os.path.join(abjad_output, 'lily.log')
    command = '{} {}'.format(text_editor, log_file_path)
    iotools.IOManager.spawn_subprocess(command)
