# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageManager_list_versions_directory_01():
    r'''Abjad IDE displays informative string when no versions
    directory exists and raises no exceptions.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g 1 vl q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    string = 'definition_0001.py illustration_0001.ly illustration_0001.pdf'
    assert string in contents