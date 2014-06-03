# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_make_package_01():
    r'''Makes score package.
    '''

    path = os.path.join(
        score_manager._configuration.user_score_packages_directory,
        'example_score',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'build',
        'distribution',
        'makers',
        'materials',
        'segments',
        'stylesheets',
        ]

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'new example~score q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries