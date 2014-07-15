# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_edit_init_py_01():
    r'''Works when __init__.py doesn't exist.
    '''

    input_ = 'red~example~score g A ne q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    string = 'Can not find' in contents