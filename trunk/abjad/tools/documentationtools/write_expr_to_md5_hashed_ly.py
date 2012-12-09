import hashlib
import os
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools


def write_expr_to_md5_hashed_ly(expr, directory, overwrite=True):
    '''Write `expr` to a file in `directory`, whose name is the MD5 hash of the
    LilyPond format of that `expr`.

    `expr` will be wrapped in a LilyPondFile, and written to disk with all
    unique information (like Abjad version and time stamp) removed.

    This ensures that expressions with equivalent notational realizations will
    result in identically named files.

    Return the MD5 hash.
    '''
    if not isinstance(expr, lilypondfiletools.LilyPondFile):
        expr = lilypondfiletools.make_basic_lilypond_file(expr)
    directory = os.path.expanduser(directory)
    assert os.path.exists(directory) and os.path.isdir(directory)

    # remove unique tokens
    tokens = expr.file_initial_system_comments[:]
    expr.file_initial_system_comments[:] = []
    expr.header_block.tagline = markuptools.Markup('""')

    md5 = hashlib.md5(expr.lilypond_format).hexdigest()
    path = os.path.join(directory, md5 + '.ly')

    if overwrite or not os.path.exists(path):
        with open(path, 'w') as f:
            f.write(expr.lilypond_format)

    # reinstate unique tokens
    expr.file_initial_system_comments[:] = tokens

    return md5
