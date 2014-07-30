# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_list_every_versions_directory_01():

    input_ = 'red~example~score m vl* q'
    ide._run(input_=input_)
    transcript_lines = ide._transcript.lines

    lines = [
        '> vl*',
        'Magic numbers:',
        '    definition_0001.py output_0001.py',
        'Performer inventory:',
        '    output_0001.py',
        'Pitch range inventory:',
        '    illustration_0001.ly illustration_0001.pdf output_0001.py',
        'Tempo inventory:',
        '    illustration_0001.ly illustration_0001.pdf output_0001.py',
        '    illustration_0002.ly illustration_0002.pdf output_0002.py',
        '    illustration_0003.ly illustration_0003.pdf output_0003.py',
        'Time signatures:',
        '    versions directory is empty.',
        ]
    for line in lines:
        assert line in transcript_lines