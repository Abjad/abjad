from abjad.tools import configurationtools
from abjad.tools.iotools._open_file import _open_file
from abjad.tools.iotools.show import show
from abjad.tools.iotools.write_expr_to_ly import write_expr_to_ly
from abjad.tools.iotools.write_expr_to_pdf import write_expr_to_pdf


def write_expr_to_ly_and_to_pdf_and_show(expr, name, write = True):
    '''Write `expr` to named ``.ly`` and to PDF and then open the resulting PDF::

        >>> iotools.write_expr_to_ly_and_to_pdf_and_show(Note("c'8"), 'file_name_stem') # doctest: +SKIP

    Write `expr` to temporary ``.ly`` and to PDF and then open the resulting PDF::

        >>> iotools.write_expr_to_ly_and_to_pdf_and_show(Note("c'8"), 'file_name_stem', write = False) # doctest: +SKIP

    Return none.

    The purpose of this function is to save named ``.ly`` and PDF output.

    .. versionchanged:: 2.0
        renamed ``io.write_and_show()`` to
        ``io.write_expr_to_ly_and_to_pdf_and_show()``.
    '''

    if write:
        write_expr_to_ly(expr, name + '.ly')
        write_expr_to_pdf(expr, name + '.pdf')
        pdf_viewer = configurationtools.read_abjad_user_config_file('pdf_viewer')
        _open_file(name + '.pdf', pdf_viewer)
    else:
        show(expr)
