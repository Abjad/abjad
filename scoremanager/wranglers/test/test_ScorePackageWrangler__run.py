# -*- encoding: utf-8 -*-
import os
import pytest
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
    assert not os.path.exists(path)
    input_ = 'new Test~score testscore 2012 q'

    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        assert os.path.exists(path)
        manager = scoremanager.managers.ScorePackageManager(name)
        assert manager.annotated_title == 'Test score (2012)'
        assert manager.composer is None
        assert manager.instrumentation is None
    finally:
        input_ = 'test removescore clobberscore remove default q'
        score_manager._run(pending_user_input=input_, is_test=True)
        assert not os.path.exists(path)
