# -*- encoding: utf-8 -*-
import os


def show(expr, return_timing=False, suppress_pdf=False, docs=False):
    r'''Shows `expr`.

    ..  container:: example

        **Example 1.** Show a note:
            
        ::

            >>> note = Note("c'4")
            >>> show(note) # doctest: +SKIP

    ..  container:: example

        **Example 2.** Show a note and return Abjad and LilyPond processing
        times in seconds:

        ::

            >>> staff = Staff(Note("c'4") * 200)
            >>> show(note, return_timing=True) # doctest: +SKIP
            (0, 3)

    Wraps `expr` in a LilyPond file with settings and overrides suitable
    for the Abjad reference manual When `docs` is true.

    Abjad writes LilyPond input files to the ``~/.abjad/output`` 
    directory by default.

    You may change this by setting the ``abjad_output`` variable in 
    the ``config.py`` file.

    Returns none or timing tuple.
    '''
    from abjad import abjad_configuration
    from abjad.tools import iotools

    name, actual_format_time, actual_lily_time = \
        iotools.log_render_lilypond_input(expr, docs=docs)

    # do not open PDF if we're running py.test regression battery
    if not suppress_pdf:
        pdf_viewer = abjad_configuration['pdf_viewer']
        ABJADOUTPUT = abjad_configuration['abjad_output']
        name = os.path.join(ABJADOUTPUT, name)
        iotools.open_file('%s.pdf' % name[:-3], pdf_viewer)

    # return timing if requested
    if return_timing:
        return actual_format_time, actual_lily_time
