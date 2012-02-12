from abjad.cfg.cfg import ABJADPATH
import os
import shutil


def remove_abjad___pycache___directories():
    '''Remove ``__pycache__`` directories from Abjad source tree::

        abjad> iotools.remove_abjad___pycache___directories() # doctest: +SKIP

    Return none.
    '''

    project_root = ABJADPATH.rstrip('abjad')

    for root, directories, files in os.walk(project_root):
        if '.svn' in directories:
            directories.remove('.svn')
        for directory in directories:
            if directory == '__pycache__':
                file_full_path = os.path.join(root, directory)
                shutil.rmtree(file_full_path)
