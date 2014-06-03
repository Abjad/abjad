# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_BuildFileWrangler_edit_interpret_open_front_cover_source_01():

    source_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'front-cover.tex',
        )
    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'front-cover.pdf',
        )

    with systemtools.FilesystemState(keep=[source_path, path]):
        os.remove(path)
        assert not os.path.exists(path)
        input_ = 'red~example~score u fceio q'
        score_manager._run(input_=input_)
        assert os.path.isfile(path)
        #assert diff-pdf(path, backup_path)

    assert score_manager._session._attempted_to_open_file