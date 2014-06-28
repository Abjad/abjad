# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_remove_files_01():
    r'''Do not use FilesystemState here because test
    adds back to repository.
    '''

    path = os.path.join(
        ide._configuration.example_stylesheets_directory,
        'clean-letter-14.ily',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'Y rm clean-letter-14.ily remove q'
        ide._run(input_=input_)
        assert not os.path.exists(path)
        assert os.path.exists(path + '.backup')
        shutil.copyfile(path + '.backup', path)
        manager = scoremanager.idetools.PackageManager(
            path=path,
            session=ide._session,
            )
        manager.add()