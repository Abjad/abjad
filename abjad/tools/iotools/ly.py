# -*- encoding: utf-8 -*-
import os


def ly(target=-1):
    r'''Opens the last LilyPond output file in text editor.

    ..  container:: example

        **Example 1.** Open the last LilyPond output file:

        ::

            >>> iotools.ly() # doctest: +SKIP

        ::

            % Abjad revision 2162
            % 2009-05-31 14:29

            \version "2.12.2"
            \include "english.ly"

            {
                c'4
            }

    ..  container:: example

        **Example 2.** Open the next-to-last LilyPond output file:

        ::

            >>> iotools.ly(-2) # doctest: +SKIP

    Returns none.
    '''
    from abjad import abjad_configuration
    from abjad.tools import iotools

    ABJADOUTPUT = abjad_configuration['abjad_output']
    text_editor = abjad_configuration.get_text_editor()
    if isinstance(target, int) and target < 0:
        last_lilypond = iotools.get_last_output_file_name()
        if last_lilypond:
            last_number = last_lilypond
            last_number = last_number.replace('.ly', '')
            last_number = last_number.replace('.pdf', '')
            last_number = last_number.replace('.midi', '')
            last_number = last_number.replace('.mid', '')
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
        message = 'can not get target LilyPond input from {}.'
        message = message.format(target)
        raise ValueError(message)

    if os.stat(target_ly):
        command = '{} {}'.format(text_editor, target_ly)
        iotools.IOManager.spawn_subprocess(command)
    else:
        message = 'Target LilyPond input file {} does not exist.'
        message = message.format(target_ly)
        print message
