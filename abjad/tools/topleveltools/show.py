# -*- encoding: utf-8 -*-
import os


def show(expr, return_timing=False):
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
            >>> show(staff, return_timing=True) # doctest: +SKIP
            (0, 1)

    Wraps `expr` in a LilyPond file with settings and overrides suitable
    for the Abjad reference manual When `docs` is true.

    Abjad writes LilyPond input files to the ``~/.abjad/output``
    directory by default.

    You may change this by setting the ``abjad_output`` variable in
    the ``config.py`` file.

    Returns none or timing tuple.
    '''
    from abjad.tools import systemtools
    from abjad.tools import topleveltools
    assert '__illustrate__' in dir(expr)
    pdf_file_path, abjad_formatting_time, lilypond_rendering_time = \
        topleveltools.persist(expr).as_pdf()
    systemtools.IOManager.open_file(pdf_file_path)
    if return_timing:
        return abjad_formatting_time, lilypond_rendering_time
