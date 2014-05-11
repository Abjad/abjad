# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_remove_stylesheets_01():
    r'''Do not use FilesystemState here because test
    adds back to repository.
    '''

    path = os.path.join(
        score_manager._configuration.abjad_stylesheets_directory_path,
        'clean-letter-14.ily',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'y rm clean-letter-14.ily remove q'
        score_manager._run(pending_input=input_)
        assert not os.path.exists(path)
        assert os.path.exists(path + '.backup')
        #shutil.move(path + '.backup', path)
        shutil.copyfile(path + '.backup', path)
        manager = scoremanager.managers.Manager(
            path=path,
            session=score_manager._session,
            )
        manager.add_to_repository(prompt=False)