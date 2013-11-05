# -*- encoding: utf-8 -*-
import os
import shutil


def write_expr_to_pdf(expr, file_name, print_status=False, tagline=False):
    r'''Writes `expr` to PDF `file_name`.

    ::

        >>> note = Note("c'4")
        >>> iotools.write_expr_to_pdf(note, 'one_note.pdf') # doctest: +SKIP

    Returns none.
    '''
    from abjad import abjad_configuration
    from abjad.tools import iotools

    # massage file_name
    file_name = os.path.expanduser(file_name)
    if not file_name.endswith('.pdf'):
        file_name += '.pdf'

    name, actual_format_time, actual_lilypond_file = \
        iotools.log_render_lilypond_input(expr, tagline=tagline)

    # copy PDF file to file_name
    pdf_name = name[:-3] + '.pdf'
    ABJADOUTPUT = abjad_configuration['abjad_output']
    full_path_pdf_name = os.path.join(ABJADOUTPUT, pdf_name)
    shutil.move(full_path_pdf_name, file_name)

    if print_status:
        print 'PDF written to %r ...' % os.path.basename(file_name)
