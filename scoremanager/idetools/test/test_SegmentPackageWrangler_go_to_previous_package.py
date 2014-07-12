# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageWrangler_go_to_previous_package_01():
    r'''To previous segment package.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g < < < < q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - C',
        'Red Example Score (2013) - segments directory - B',
        'Red Example Score (2013) - segments directory - A',
        'Red Example Score (2013) - segments directory - C',
        ]
    assert ide._transcript.titles == titles