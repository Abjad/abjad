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
    wrangler._session._pending_user_input = input_
    result = wrangler.get_available_path(
        storehouse_path=storehouse,
        )
    path = os.path.join(
        storehouse,
        'foo',
        )
    assert result == path

    input_ = 'example~notes q'
    wrangler._session._pending_user_input = input_
    result = wrangler.get_available_path()
    assert result is None


def test_MaterialPackageWrangler_get_available_path_02():

    session = scoremanager.core.Session(is_test=True)
    session._set_test_score('red_example_score')
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    input_ = 'foo'
    wrangler._session._pending_user_input = input_
    result = wrangler.get_available_path()
    path = os.path.join(
        configuration.example_score_packages_directory_path,
        'red_example_score',
        'materials',
        'foo',
        )

    assert result == path


def test_MaterialPackageWrangler_get_available_path_03():

    session = scoremanager.core.Session(is_test=True)
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)

    input_ = 'q'
    wrangler._session._pending_user_input = input_
    result = wrangler.get_available_path()
    assert result is None

    input_ = 'b'
    wrangler._session._pending_user_input = input_
    result = wrangler.get_available_path()
    assert result is None

    input_ = 'h'
    wrangler._session._pending_user_input = input_
    result = wrangler.get_available_path()
    assert result is None