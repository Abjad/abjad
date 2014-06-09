# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_list_every_versions_directory_01():

    input_ = 'red~example~score m vrls* q'
    score_manager._run(input_=input_)
    transcript_lines = score_manager._transcript.lines

    lines = [
        '> vrls*',
        'Instrumentation (AE):',
        '    output_0001.py',
        'Magic numbers:',
        '    definition_0001.py output_0001.py',
        'Pitch range inventory (AE):',
        '    illustration_0001.ly illustration_0001.pdf output_0001.py',
        'Tempo inventory (AE):',
        '    illustration_0001.ly illustration_0001.pdf output_0001.py',
        '    illustration_0002.ly illustration_0002.pdf output_0002.py',
        '    illustration_0003.ly illustration_0003.pdf output_0003.py',
        'Time signatures:',
        '    versions directory is empty.',
        ]
    for line in lines:
        assert line in transcript_lines