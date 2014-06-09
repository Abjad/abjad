# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_StylesheetWrangler_remove_files_01():
    r'''Do not use FilesystemState here because test
    adds back to repository.
    '''

    path = os.path.join(
        score_manager._configuration.abjad_stylesheets_directory,
        'clean-letter-14.ily',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'y rm clean-letter-14.ily remove q'
        score_manager._run(input_=input_)
        assert not os.path.exists(path)
        assert os.path.exists(path + '.backup')
        shutil.copyfile(path + '.backup', path)
        manager = scoremanager.wranglers.PackageManager(
            path=path,
            session=score_manager._session,
            )
        manager.add_to_repository()