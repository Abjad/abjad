from abjad.tools import configurationtools
from abjad.tools.iotools.spawn_subprocess import spawn_subprocess
import os


def log():
    '''Open the LilyPond log file in operating system-specific text editor::

        abjad> iotools.log() # doctest: +SKIP

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

    Exit text editor in the usual way.

    Return none.
    '''

    ABJADOUTPUT = configurationtools.read_abjad_user_config_file('abjad_output')
    text_editor = configurationtools.get_text_editor()
    command = '{} {}'.format(text_editor, os.path.join(ABJADOUTPUT, 'lily.log'))
    # TODO: how do we get rid of this call to os.system()?
    #spawn_subprocess(command)
    os.system(command)
