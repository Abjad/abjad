from abjad.cfg._get_text_editor import _get_text_editor
from abjad.cfg._read_config_file import _read_config_file
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

    ABJADOUTPUT = _read_config_file()['abjad_output']
    text_editor = _get_text_editor()
    command = '%s %s' % (text_editor, os.path.join(ABJADOUTPUT, 'lily.log'))
    os.system(command)
