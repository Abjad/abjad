# -*- coding: utf-8 -*-
import os
import shutil
import tempfile


class Show(object):
    r'''IPython replacement callable for `topleveltools.show()`.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''A replacement for Ajbad's show function for IPython Notebook.
        '''
        from abjad.tools import systemtools
        from abjad.tools import topleveltools
        from IPython.core.display import display_png
        assert systemtools.IOManager.find_executable('lilypond')
        assert systemtools.IOManager.find_executable('convert')
        assert hasattr(expr, '__illustrate__')
        temporary_directory = tempfile.mkdtemp()
        temporary_file_path = os.path.join(
            temporary_directory,
            'output.png',
            )
        result = topleveltools.persist(expr).as_png(temporary_file_path)
        pngs = []
        for file_path in result[0]:
            command = 'convert {file_path} -trim {file_path}'
            command = command.format(file_path=file_path)
            systemtools.IOManager.spawn_subprocess(command)
            with open(file_path, 'rb') as file_pointer:
                file_contents = file_pointer.read()
                pngs.append(file_contents)
        shutil.rmtree(temporary_directory)
        for png in pngs:
            display_png(png, raw=True)
