# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_to_all_materials_01():
    r'''From score segments to all materials.
    '''

    input_ = 'red~example~score g M q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Abjad IDE - materials',
        ]
    assert ide._transcript.titles == titles


def test_SegmentPackageWrangler_go_to_all_materials_02():
    r'''From all segments to all materials.
    '''

    input_ = 'G M q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments',
        'Abjad IDE - materials',
        ]
    assert ide._transcript.titles == titles