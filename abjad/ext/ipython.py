# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
from IPython.core.display import display_png


def _get_png(expr):
    r'''Calls lilypond and converts output to (multi-page) PNGs.
    '''
    from abjad.tools import systemtools
    from abjad.tools import topleveltools
    temporary_directory = tempfile.mkdtemp()
    temporary_file_path = os.path.join(
        temporary_directory,
        'output.png',
        )
    result = topleveltools.persist(expr).as_png(temporary_file_path)
    pngs = []
    for file_path in result[0]:
        command = 'convert {file_path} -trim {file_path}'.format(
            file_path=file_path,
            )
        systemtools.IOManager.spawn_subprocess(command)
        with open(file_path, 'rb') as file_pointer:
            file_contents = file_pointer.read()
            pngs.append(file_contents)
    shutil.rmtree(temporary_directory)
    return pngs


def show(expr):
    r'''A replacement for Ajbad's show function for IPython Notebook.
    '''
    assert '__illustrate__' in dir(expr)
    pngs = _get_png(expr)
    for png in pngs:
        display_png(png, raw=True)


def load_ipython_extension(ipython):
    import abjad
    from abjad.tools import topleveltools
    abjad.show = show
    topleveltools.show = show
    ipython.push({'show': show})
