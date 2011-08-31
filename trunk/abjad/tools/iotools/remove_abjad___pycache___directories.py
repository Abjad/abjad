from abjad.cfg.cfg import ABJADPATH
import os
import shutil


def remove_abjad___pycache___directories():
    '''Remove ``__pycache__`` directories from Abjad source tree::

        abjad> iotools.remove_abjad___pycache___directories() # doctest: +SKIP

    Return none.
    '''

    project_root = ABJADPATH.rstrip('abjad')

    for root, dirs, files in os.walk(project_root):
        if '.svn' in dirs:
            dirs.remove('.svn')
        for dir in dirs:
            if dir == '__pycache__':
                file_full_path = os.path.join(root, dir)
                shutil.rmtree(file_full_path)
