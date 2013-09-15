# -*- encoding: utf-8 -*-
import os


def run_lilypond(lilypond_file_name, lilypond_path):
    from abjad import abjad_configuration
    from abjad.tools import iotools
    abjad_output_directory_path = abjad_configuration['abjad_output']
    if not lilypond_path:
        lilypond_path = 'lilypond'
    log_file_path = os.path.join(abjad_output_directory_path, 'lily.log')
    command = '{} -dno-point-and-click {} > {} 2>&1'
    command = command.format(lilypond_path, lilypond_file_name, log_file_path)
    iotools.spawn_subprocess(command)
    postscript_file_name = lilypond_file_name.replace('.ly', '.ps')
    try:
        os.remove(postscript_file_name)
    except OSError:
        # no such file...
        pass
