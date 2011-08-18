import os
import sys


def _open_file(file_name, application = None):
    '''Generic cross-platform file opener.
    '''

    if os.name == 'nt':
        os.startfile(file_name)
    else:
        if sys.platform.lower() == 'linux2':
            viewer = application or 'xdg-open'
        else:
            viewer = application or 'open'
        os.system('%s %s &' % (viewer, file_name))
