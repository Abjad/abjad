from abjad.cfg.cfg import ABJADPATH
import os


def remove_abjad_pyc_files():
    '''Remove ``.pyc`` files from Abjad source tree::

        abjad> iotools.remove_abjad_pyc_files() # doctest: +SKIP

    Return none.
    '''

    project_root = ABJADPATH.rstrip('abjad')

    for root, dirs, files in os.walk(project_root):
        if '.svn' in dirs:
            dirs.remove('.svn')
        for file in files:
            if file.endswith('.pyc'):
                file_full_path = os.path.join(root, file)
                os.remove(file_full_path)
