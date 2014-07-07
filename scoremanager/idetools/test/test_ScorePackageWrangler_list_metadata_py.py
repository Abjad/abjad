# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_list_metadata_py_01():

    input_ = 'mdl q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert ide._configuration.wrangler_views_metadata_file in contents