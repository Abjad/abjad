# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_open_versioned_output_pdf_01():

    input_ = 'red~example~score g A vopo 1 q'
    ide._run(input_=input_)

    assert ide._session._attempted_to_open_file