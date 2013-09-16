# -*- encoding: utf-8 -*-
import os
from abjad.tools import documentationtools


def write_expr_to_ly(
    expr,
    file_name,
    print_status=False,
    tagline=False,
    docs=False,
    ):
    r'''Writes `expr` to `file_name`.

    ::

        >>> note = Note("c'4")
        >>> iotools.write_expr_to_ly(note, '/home/user/foo.ly') # doctest: +SKIP

    Returns none.
    '''
    from abjad.tools import iotools

    file_name = os.path.expanduser(file_name)
    if not file_name.endswith('.ly'):
        file_name += '.ly'
    try:
        outfile = open(file_name, 'w')
        if docs:
            expr = documentationtools.make_reference_manual_lilypond_file(expr)
        lilypond_file = iotools.insert_expr_into_lilypond_file(
            expr, tagline=tagline)
        # the following line is necessary for Windows *not* to keep 
        # outfile open after writing;
        # why this should be the case is, however, a complete mystery.
        output = lilypond_file.lilypond_format
        outfile.write(output)
        outfile.close()
    except IOError:
        print 'ERROR: cound not open file %s' % file_name
        dirname = os.path.dirname(file_name)
        if dirname:
            print 'Make sure "%s" exists in your system.' % dirname

    if print_status:
        print 'LilyPond file written to %r ...' % os.path.basename(file_name)
