from abjad.tools import configurationtools
from abjad.tools.iotools._log_render_lilypond_input import _log_render_lilypond_input
from abjad.tools.iotools._open_file import _open_file
import os


def show(expr, return_timing=False, suppress_pdf=False, docs=False):
    '''Show `expr`::

        >>> note = Note("c'4")
        >>> show(note) # doctest: +SKIP

    Show `expr` and return both Abjad and LilyPond processing time in seconds::

        >>> staff = Staff(Note("c'4") * 200)
        >>> show(note, return_timing=True) # doctest: +SKIP
        (0, 3)

    Wrap `expr` in a LilyPond file with settings and overrides suitable
    for the Abjad reference manual When `docs` is true. 

    Return none or timing tuple.

    Abjad writes LilyPond input files to the ``~/.abjad/output`` directory by default.

    You may change this by setting the ``abjad_output`` variable in the ``config.py`` file.
    '''

    from abjad import ABJCFG

    name, actual_format_time, actual_lily_time = _log_render_lilypond_input(expr, docs=docs)

    # do not open PDF if we're running py.test regression battery
    if not suppress_pdf:
        # FIXME: the value returned should never be the string 'None'
        pdf_viewer = ABJCFG['pdf_viewer']
        # FIXME: these two lines are a temporary hack that can be removed later
        if pdf_viewer == 'None':
            pdf_viewer = None
        ABJADOUTPUT = ABJCFG['abjad_output']
        name = os.path.join(ABJADOUTPUT, name)
        _open_file('%s.pdf' % name[:-3], pdf_viewer)

    # return timing if requested
    if return_timing:
        return actual_format_time, actual_lily_time
