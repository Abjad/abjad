# -*- encoding: utf-8 -*-
import os
import pytest
import shutil
from abjad import *
import scoremanager


def test_ScorePackageWrangler__run_01():
    r'''Create score package. Remove score package.
    '''
    pytest.skip('unskip after deciding about cache.')

    score_manager = scoremanager.core.ScoreManager()
    path = os.path.join(
        score_manager._configuration.abjad_score_packages_directory_path,
        'testscore',
        )
    input_ = 'new test~score testscore 2012 q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path, session=session)
        assert manager.annotated_title == 'Test score (2012)'
        assert manager.composer is None
        assert manager.instrumentation is None
        input_ = 'test removescore clobberscore remove default q'
        score_manager._run(pending_user_input=input_, is_test=True)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)
