# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_list_metadata_py_01():

    metadata_py_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'stylesheets',
        '__metadata__.py',
        )

    input_ = 'red~example~score y mdl q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert metadata_py_path in contents


def test_StylesheetWrangler_list_metadata_py_02():

    input_ = 'yy mdl q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert ide._configuration.wrangler_views_metadata_file in contents