# -*- coding: utf-8 -*-
import os
import shutil
import tempfile


def show(expr):
    r'''A replacement for Ajbad's show function for IPython Notebook.
    '''
    from abjad.tools import systemtools
    from abjad.tools import topleveltools
    from IPython.core.display import display_png
    assert '__illustrate__' in dir(expr)
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
    for png in pngs:
        display_png(png, raw=True)


def load_ipython_extension(ipython):
    import abjad
    from abjad.tools import topleveltools
    abjad.show = show
    topleveltools.show = show
    ipython.push({'show': show})
