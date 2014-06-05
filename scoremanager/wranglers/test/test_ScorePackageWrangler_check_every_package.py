# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_check_every_package_01():

    lines = [
        'Étude Example Score (2013):',
        '    Top level (9 assets): OK',
        '    Build (1 files): OK',
        '    Distribution (0 files): OK',
        '    Makers (0 files): OK',
        '    Materials (0 packages): OK',
        '    Segments (0 packages): OK',
        '    Stylesheets (0 files): OK',
        'Red Example Score (2013):',
        '    Top level (9 assets): OK',
        '    Build (18 files): OK',
        '    Distribution (2 files): OK',
        '    Makers (2 files): OK',
        '    Materials (5 packages):',
        '        Instrumentation: OK',
        '        Magic numbers: OK',
        '        Pitch range inventory: OK',
        '        Tempo inventory: OK',
        '        Time signatures: OK',
        '    Segments (3 packages):',
        '        A: OK',
        '        B: OK',
        '        C: OK',
        '    Stylesheets (2 files): OK',
        ]

    input_ = 'ck* y n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    for line in lines:
        assert line in contents