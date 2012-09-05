import os
import time
from abjad.tools import configurationtools


# TODO: Remove code duplication between this and iotools.ly and iotools.show.
# TODO: Encapsulate stuff below.
def redo(target=-1, lily_time=10):
    r'''Rerender the last ``.ly`` file created in Abjad and then show the resulting PDF::

        >>> iotools.redo() # doctest: +SKIP

    Rerender the next-to-last ``.ly`` file created in Abjad and then show the resulting PDF::

        >>> iotools.redo(-2) # doctest: +SKIP

    Return none.
    '''
    from abjad import ABJCFG
    from abjad.tools import iotools
    from abjad.tools.iotools._open_file import _open_file
    from abjad.tools.iotools._run_lilypond import _run_lilypond
    from abjad.tools.iotools._verify_output_directory import _verify_output_directory

    current_directory = os.path.abspath('.')
    ABJADOUTPUT = ABJCFG['abjad_output']
    _verify_output_directory(ABJADOUTPUT)
    os.chdir(ABJADOUTPUT)

    # TODO: Encapsulate as a single function called cfg._find_target()
    # find target
    if isinstance(target, int) and target < 0:
        last_lilypond = iotools.get_last_output_file_name()
        if last_lilypond:
            last_number = last_lilypond.replace('.ly', '')
            target_number = int(last_number) + (target + 1)
            target_str = '%04d' % target_number
            target_ly = os.path.join(ABJADOUTPUT, target_str + '.ly')
        else:
            print 'Target LilyPond input file does not exist.'
    elif isinstance(target, int) and 0 <= target:
        target_str = '%04d' % target
        target_ly = os.path.join(ABJADOUTPUT, target_str + '.ly')
    elif isinstance(target, str):
        target_ly = os.path.join(ABJADOUTPUT, target)
    else:
        raise ValueError('can not get target LilyPond input from %s.' % target)

    # render
    start_time = time.time()
    _run_lilypond(target_ly, ABJCFG['lilypond_path'])
    stop_time = time.time()
    actual_lily_time = int(stop_time - start_time)

    os.chdir(current_directory)

    if lily_time <= actual_lily_time:
        print 'LilyPond processing time equal to %s seconds ...' % actual_lily_time

    # TODO: Encapsulate as cfg._open_pdf()
    # open pdf
    pdf_viewer = ABJCFG['pdf_viewer']
    ABJADOUTPUT = ABJCFG['abjad_output']
    ABJADOUTPUT = config['abjad_output']
    name = target_ly
    _open_file('%s.pdf' % name[:-3], pdf_viewer)
