from abjad.cfg.cfg import ABJADPATH
from abjad.tools.iotools._insert_expr_into_lily_file import _insert_expr_into_lily_file
import os


def write_expr_to_ly(expr, file_name, template = None, print_status = True):
    '''Write `expr` to `file_name`::

        abjad> note = Note("c'4")
        abjad> iotools.write_expr_to_ly(note, '/home/user/foo.ly') # doctest: +SKIP

    Write `expr` to `file_name` with `template`::

        abjad> note = Note("c'4")
        abjad> iotools.write_expr_to_ly(note, '/home/user/foo.ly', 'paris') # doctest: +SKIP

    Retur none.

    .. versionchanged:: 2.0
        renamed ``io.write_ly()`` to
        ``io.write_expr_to_ly()``.
    '''

    file_name = os.path.expanduser(file_name)
    if not file_name.endswith('.ly'):
        file_name += '.ly'
    try:
        outfile = open(file_name, 'w')
        lily_file = _insert_expr_into_lily_file(expr, template = template)
        # the following line is necessary for Windows *not* to keep outfile open after writing;
        # why this should be the case is, however, a complete mystery.
        output = lily_file.format
        outfile.write(output)
        outfile.close()
    except IOError:
        print 'ERROR: cound not open file %s' % file_name
        dirname = os.path.dirname(file_name)
        if dirname:
            print 'Make sure "%s" exists in your system.' % dirname

    if print_status:
        print 'LilyPond input file written to "%s" ...' % os.path.basename(file_name)
