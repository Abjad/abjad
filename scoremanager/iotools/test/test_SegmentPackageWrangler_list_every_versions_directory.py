# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_list_every_versions_directory_01():

    input_ = 'red~example~score g vrls* q'
    score_manager._run(input_=input_)
    transcript_lines = score_manager._transcript.lines

    lines = [
        '> vrls*',
        'A:',
        '    definition_0001.py output_0001.ly output_0001.pdf',
        'B:',
        '    definition_0001.py output_0001.ly output_0001.pdf',
        'C:',
        '    definition_0001.py output_0001.ly output_0001.pdf',
        ]
    for line in lines:
        assert line in transcript_lines