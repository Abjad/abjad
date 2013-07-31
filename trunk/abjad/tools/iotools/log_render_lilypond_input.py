import os
import time
from abjad.tools import documentationtools


def log_render_lilypond_input(expr, tagline=False, docs=False):
    r'''Write both .ly and .pdf files to the ``abjad_output`` directory.
    '''
    from abjad import abjad_configuration
    from abjad.tools import iotools

    lily_time = 2
    format_time = 2

    # log score
    current_directory = os.path.abspath('.')
    ABJADOUTPUT = abjad_configuration['abjad_output']
    iotools.verify_output_directory(ABJADOUTPUT)
    os.chdir(ABJADOUTPUT)
    name = iotools.get_next_output_file_name()
    outfile = open(name, 'w')

    # catch Abjad tight loops that result in excessive format time
    start_format_time = time.time()
    if docs:
        expr = documentationtools.make_reference_manual_lilypond_file(expr)
    lilypond_file = iotools.insert_expr_into_lilypond_file(
        expr, tagline=tagline)
    formatted_lilypond_file = lilypond_file.lilypond_format
    stop_format_time = time.time()
    actual_format_time = int(stop_format_time - start_format_time)
    if format_time <= actual_format_time:
        print 'Abjad format time equal to %s seconds ...' % actual_format_time
    outfile.write(formatted_lilypond_file)
    outfile.close()

    if getattr(lilypond_file, '_is_temporary', False):
        # TODO: eliminate this exception handler? #
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
        print 'LilyPond processing time equal to %s seconds ...' % actual_lily_time

    return name, actual_format_time, actual_lily_time
