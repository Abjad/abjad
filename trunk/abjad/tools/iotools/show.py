from abjad.cfg._read_config_file import _read_config_file
from abjad.tools.iotools._log_render_lilypond_input import _log_render_lilypond_input
from abjad.tools.iotools._open_file import _open_file
import os


def show(expr, template = None, return_timing = False, suppress_pdf = False):
    '''Show `expr`::

        abjad> note = Note("c'4")
        abjad> show(note) # doctest: +SKIP

    Show `expr` with `template`::

        abjad> note = Note("c'4")
        abjad> show(note, template = 'tangiers') # doctest: +SKIP

    Show `expr` and return both Abjad and LilyPond processing time in seconds::

        abjad> staff = Staff(Note("c'4") * 200)
        abjad> show(note, return_timing = True) # doctest: +SKIP
        (0, 3)

    Return none or timing tuple.

    Abjad writes LilyPond input files to the ``~/.abjad/output`` directory by default.

    You may change this by setting the ``abjad_output`` variable in the ``config.py`` file.
    '''

    name, actual_format_time, actual_lily_time = _log_render_lilypond_input(expr, template = template)

    # do not open PDF if we're running py.test regression battery
    if not suppress_pdf:
        config = _read_config_file()
        pdf_viewer = config['pdf_viewer']
        ABJADOUTPUT = config['abjad_output']
        name = os.path.join(ABJADOUTPUT, name)
        _open_file('%s.pdf' % name[:-3], pdf_viewer)

    # return timing if requested
    if return_timing:
        return actual_format_time, actual_lily_time
