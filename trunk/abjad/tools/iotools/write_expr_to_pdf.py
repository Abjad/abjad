from abjad.cfg._read_config_file import _read_config_file
from abjad.tools.iotools._log_render_lilypond_input import _log_render_lilypond_input
import os
import shutil


def write_expr_to_pdf(expr, file_name, template=None, print_status=True, tagline=False):
    '''Write `expr` to pdf `file_name`::

        abjad> note = Note("c'4")
        abjad> iotools.write_expr_to_pdf(note, 'one_note.pdf') # doctest: +SKIP

    Write `expr` to pdf `file_name` with `template`::

        abjad> note = Note("c'4")
        abjad> iotools.write_expr_to_pdf(note, 'one_note.pdf', template='paris') # doctest: +SKIP

    Return none.
    '''

    # massage file_name
    file_name = os.path.expanduser(file_name)
    if not file_name.endswith('.pdf'):
        file_name += '.pdf'

    name, actual_format_time, actual_lilypond_file = _log_render_lilypond_input(
        expr, template=template, tagline=tagline)

    # copy PDF file to file_name
    pdf_name = name[:-3] + '.pdf'
    ABJADOUTPUT = _read_config_file()['abjad_output']
    full_path_pdf_name = os.path.join(ABJADOUTPUT, pdf_name)
    shutil.move(full_path_pdf_name, file_name)

    if print_status:
        print 'PDF written to %r ...' % os.path.basename(file_name)
