# -*- encoding: utf-8 -*-
import os
import sys


def open_file(file_path, application=None):
    r'''Opens `file_path` with operating system-specific file-opener
    with `application` is none.

    Opens `file_path` with `application` when `application` is not none.

    Returns none.
    '''
    from abjad.tools import iotools

    if os.name == 'nt':
        os.startfile(file_path)
        return

    if sys.platform.lower() == 'linux2':
        viewer = application or 'xdg-open'
    else:
        viewer = application or 'open'
    command = '{} {} &'.format(viewer, file_path)
    iotools.spawn_subprocess(command)
