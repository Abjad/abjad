# -*- encoding: utf-8 -*-
import os
import time


# TODO: Remove code duplication between this and iotools.ly and topleveltools.show.
# TODO: Encapsulate stuff below.
def redo(target=-1, lily_time=10):
    r'''Rerenders the last ``.ly`` file created in Abjad and
    then shows the resulting PDF.

    ..  container:: example

        **Example 1.** Redo the last LilyPond file created in Ajbad:

        ::

            >>> iotools.redo() # doctest: +SKIP

    ..  container:: example

        **Examle 2.** Redo the next-to-last LilyPond file created in Abjad:

        ::

            >>> iotools.redo(-2) # doctest: +SKIP

    Returns none.
    '''
    from abjad import abjad_configuration
    from abjad.tools import iotools

    current_directory = os.path.abspath('.')
    abjad_output = abjad_configuration['abjad_output']
    iotools.IOManager.ensure_directory_existence(abjad_output)
    os.chdir(abjad_output)

    # TODO: Encapsulate as a single function called cfg._find_target()
    # find target
    if isinstance(target, int) and target < 0:
        last_lilypond = iotools.get_last_output_file_name()
        if last_lilypond:
            last_number = last_lilypond.replace('.ly', '')
            last_number = last_lilypond.replace('.pdf', '')
            last_number = last_number.replace('.midi', '')
            last_number = last_number.replace('.mid', '')
            target_number = int(last_number) + (target + 1)
            target_str = '%04d' % target_number
            target_ly = os.path.join(abjad_output, target_str + '.ly')
        else:
            print 'Target LilyPond input file does not exist.'
    elif isinstance(target, int) and 0 <= target:
        target_str = '%04d' % target
        target_ly = os.path.join(abjad_output, target_str + '.ly')
    elif isinstance(target, str):
        target_ly = os.path.join(abjad_output, target)
    else:
        message = 'can not get target LilyPond input from {}.'.format(target)
        raise ValueError(message)

    # render
    start_time = time.time()
    iotools.run_lilypond(target_ly, abjad_configuration['lilypond_path'])
    stop_time = time.time()
    actual_lily_time = int(stop_time - start_time)

    os.chdir(current_directory)

    if lily_time <= actual_lily_time:
        message = 'LilyPond processing time equal to {} seconds ...'
        print message.format(actual_lily_time)

    # TODO: Encapsulate as cfg._open_pdf()
    # open pdf
    pdf_viewer = abjad_configuration['pdf_viewer']
    abjad_output = abjad_configuration['abjad_output']
    name = target_ly
    iotools.open_file('%s.pdf' % name[:-3], pdf_viewer)
