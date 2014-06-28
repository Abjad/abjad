# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_invoke_shell_01():

    input_ = 'red~example~score g A !pwd q'
    ide._run(input_=input_)

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'segment_01',
        )
    string = '\n{}\n'.format(path)
    assert string in ide._transcript.contents