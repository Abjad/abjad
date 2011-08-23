from abjad.cfg._get_text_editor import _get_text_editor
from abjad.cfg._read_config_file import _read_config_file
from abjad.tools.iotools.get_last_output_file_name import get_last_output_file_name
import os


def ly(target = -1):
    r'''Open the last LilyPond output file in text editor::

        abjad> iotools.ly() # doctest: +SKIP

    ::

        % Abjad revision 2162
        % 2009-05-31 14:29

        \version "2.12.2"
        \include "english.ly"
        \include "/Path/to/abjad/trunk/abjad/cfg/abjad.scm"

        {
            c'4
        }

    Open the next-to-last LilyPond output file in text editor::

        abjad> iotools.ly(-2) # doctest: +SKIP

    Exit text editor in the usual way.

    Return none.
    '''

    ABJADOUTPUT = _read_config_file()['abjad_output']
    text_editor = _get_text_editor()
    if isinstance(target, int) and target < 0:
        last_lilypond = get_last_output_file_name()
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

    if os.stat(target_ly):
        command = '%s %s' % (text_editor, target_ly)
        os.system(command)
    else:
        print 'Target LilyPond input file %s does not exist.' % target_ly
