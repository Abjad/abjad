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
    pdf_filepath, abjad_formatting_time, lilypond_rendering_time = \
        topleveltools.persist(expr).as_pdf()
    systemtools.IOManager.open_file(pdf_filepath)
    if return_timing:
        return abjad_formatting_time, lilypond_rendering_time

#    # get the illustration
#    illustration = expr.__illustrate__()
#    timer = systemtools.Timer()
#
#    # get the lilypond format string
#    with timer:
#        illustration_format = format(illustration, 'lilypond')
#    actual_format_time = timer.elapsed_time
#
#    # write the lilypond file
#    lilypond_file_name = systemtools.IOManager.get_next_output_file_name()
#    lilypond_file_path = os.path.join(
#        abjad_configuration.abjad_output_directory_path,
#        lilypond_file_name,
#        )
#    with open(lilypond_file_path, 'w') as file_handle:
#        file_handle.write(illustration_format)
#
#    # generate the pdf
#    with timer:
#        systemtools.IOManager.run_lilypond(lilypond_file_path)
#    actual_lily_time = timer.elapsed_time
#
#    # open the pdf
#    pdf_file_path = '{}.pdf'.format(os.path.splitext(lilypond_file_path)[0])
#    systemtools.IOManager.open_file(pdf_file_path)
#
#    # return timing information
#    if return_timing:
#        return actual_format_time, actual_lily_time
