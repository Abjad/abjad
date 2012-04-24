from abjad.tools.iotools.spawn_subprocess import spawn_subprocess
import os
import sys


# TODO: make public
def _open_file(file_name, application=None):
    '''Generic cross-platform file opener.
    '''

    if os.name == 'nt':
        os.startfile(file_name)
    else:
        if sys.platform.lower() == 'linux2':
            viewer = application or 'xdg-open'
        else:
            viewer = application or 'open'
        spawn_subprocess('{} {} &'.format(viewer, file_name))
