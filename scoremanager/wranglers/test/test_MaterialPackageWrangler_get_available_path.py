# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_MaterialPackageWrangler_get_available_path_01():

    session = scoremanager.core.Session(is_test=True)
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    storehouse = configuration.user_library_material_packages_directory_path
    input_ = 'foo'
    result = wrangler.get_available_path(
        pending_user_input=input_,
        storehouse_path=storehouse,
        )
    path = os.path.join(
        storehouse,
        'foo',
        )
    assert result == path

    input_ = 'example~notes q'
    result = wrangler.get_available_path(pending_user_input=input_)
    assert result is None


def test_MaterialPackageWrangler_get_available_path_02():

    session = scoremanager.core.Session(is_test=True)
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    wrangler._session._current_score_snake_case_name = 'red_example_score'
    input_ = 'foo'
    result = wrangler.get_available_path(pending_user_input=input_)
    path = os.path.join(
        configuration.abjad_score_packages_directory_path,
        'red_example_score',
        'materials',
        'foo',
        )

    assert result == path


def test_MaterialPackageWrangler_get_available_path_03():

    session = scoremanager.core.Session(is_test=True)
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)

    input_ = 'q'
    result = wrangler.get_available_path(pending_user_input=input_)
    assert result is None

    input_ = 'b'
    result = wrangler.get_available_path(pending_user_input=input_)
    assert result is None

    input_ = 'h'
    result = wrangler.get_available_path(pending_user_input=input_)
    assert result is None
