# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager


def test_StylesheetWrangler_remove_01():
    pytest.skip('FIXME: user asset library stylesheets should show up here.')

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    first_path = os.path.join(
        configuration.user_library_stylesheets_directory_path,
        'aaa.ly',
        )
    second_path = os.path.join(
        configuration.user_library_stylesheets_directory_path,
        'aab.ly',
        )

    assert not os.path.exists(first_path)
    assert not os.path.exists(second_path)

    file(first_path, 'w').write('')
    file(second_path, 'w').write('')

    assert os.path.exists(first_path)
    assert os.path.exists(second_path)

    try:
        score_manager._run(pending_user_input='y rm aaa-aab default q')
        assert not os.path.exists(first_path)
        assert not os.path.exists(second_path)
    finally:
        if os.path.exists(first_path):
            os.remove(first_path)
        if os.path.exists(second_path):
            os.remove(second_path)
        assert not os.path.exists(first_path)
        assert not os.path.exists(second_path)
