# -*- encoding: utf-8 -*-
import os
import time
from abjad.tools import documentationtools


def log_render_lilypond_input(
    expr, 
    output_directory_path=None, 
    output_file_name_root=None,
    tagline=False, 
    docs=False,
    ):
    r'''Writes both .ly and .pdf files to `output_directory`.

    Writes to Abjad output directory when `output_directory` is none.

    Writes to next 4-digit numeric file name 
    when `output_file_name_root` is none.

    Returns file name, Abjad format time (in seconds) and LilyPond
    format time (in seconds).
    '''
    from abjad import abjad_configuration
    from abjad.tools import iotools

    # set timing thresholds
    lily_time = 2
    format_time = 2
    # change to output directory
    current_directory = os.path.abspath('.')
    output_directory_path = \
        output_directory_path or abjad_configuration['abjad_output']
    iotools.verify_output_directory(output_directory_path)
    os.chdir(output_directory_path)
    if output_file_name_root is None:
        name = iotools.get_next_output_file_name()
    else:
        name = output_file_name_root + '.ly'
    outfile = open(name, 'w')
    # catch Abjad tight loops that result in excessive format time
    start_format_time = time.time()
    if docs:
        expr = documentationtools.make_reference_manual_lilypond_file(expr)
    lilypond_file = iotools.insert_expr_into_lilypond_file(
        expr, tagline=tagline)
    formatted_lilypond_file = format(lilypond_file)
    stop_format_time = time.time()
    actual_format_time = int(stop_format_time - start_format_time)
    if format_time <= actual_format_time:
        message = 'Abjad format time equal to {} seconds ...'
        message = message.format(actual_format_time)
        print message
    outfile.write(formatted_lilypond_file)
    outfile.close()
    if getattr(lilypond_file, '_is_temporary', False):
        # TODO: eliminate this exception handler?
        try:
            music = lilypond_file.score_block.pop()
            delattr(music, '_lilypond_file')
        except (IndexError, AttributeError):
            pass
        del(lilypond_file)
    # render
    start_time = time.time()
    iotools.run_lilypond(name, abjad_configuration['lilypond_path'])
    stop_time = time.time()
    actual_lily_time = int(stop_time - start_time)
    os.chdir(current_directory)
    # catch LilyPond taking a long time to render
    if lily_time <= actual_lily_time:
        message = 'LilyPond processing time equal to {} seconds ...'
        message = message.format(actual_lily_time)
        print message
    return name, actual_format_time, actual_lily_time
