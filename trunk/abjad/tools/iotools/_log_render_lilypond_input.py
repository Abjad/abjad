import os
import time
from abjad.tools import configurationtools
from abjad.tools import documentationtools
from abjad.tools.iotools._insert_expr_into_lilypond_file import _insert_expr_into_lilypond_file
from abjad.tools.iotools._run_lilypond import _run_lilypond
from abjad.tools.iotools._verify_output_directory import _verify_output_directory
from abjad.tools.iotools.get_next_output_file_name import get_next_output_file_name


# TODO: make public and possibly improve function name
def _log_render_lilypond_input(expr, tagline=False, docs=False):
    '''Write both .ly and .pdf files to the ``abjad_output`` directory.
    '''
    from abjad import ABJCFG

    lily_time = 2
    format_time = 2

    # log score
    current_directory = os.path.abspath('.')
    ABJADOUTPUT = ABJCFG['abjad_output']
    _verify_output_directory(ABJADOUTPUT)
    os.chdir(ABJADOUTPUT)
    name = get_next_output_file_name()
    outfile = open(name, 'w')

    # catch Abjad tight loops that result in excessive format time
    start_format_time = time.time()
    if docs:
        expr = documentationtools.make_reference_manual_lilypond_file(expr)
    lilypond_file = _insert_expr_into_lilypond_file(expr, tagline=tagline)
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
    _run_lilypond(name, ABJCFG['lilypond_path'])
    stop_time = time.time()
    actual_lily_time = int(stop_time - start_time)

    os.chdir(current_directory)

    # catch LilyPond taking a long time to render
    if lily_time <= actual_lily_time:
        print 'LilyPond processing time equal to %s seconds ...' % actual_lily_time

    return name, actual_format_time, actual_lily_time
