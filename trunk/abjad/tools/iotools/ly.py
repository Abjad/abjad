import os
from abjad.tools import configurationtools


def ly(target=-1):
    r'''Open the last LilyPond output file in text editor::

        >>> iotools.ly() # doctest: +SKIP

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

        >>> iotools.ly(-2) # doctest: +SKIP

    Exit text editor in the usual way.

    Return none.
    '''
    from abjad import ABJCFG
    from abjad.tools import iotools

    ABJADOUTPUT = ABJCFG['abjad_output']
    text_editor = configurationtools.get_text_editor()
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
        raise ValueError('can not get target LilyPond input from {}.'.format(target))

    if os.stat(target_ly):
        command = '{} {}'.format(text_editor, target_ly)
        # TODO: how do we get rid of this last tricky call to os.system()?
        #spawn_subprocess(command)
        os.system(command)
    else:
        print 'Target LilyPond input file {} does not exist.'.format(target_ly)
