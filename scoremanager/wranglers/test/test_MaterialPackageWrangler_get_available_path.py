# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_MaterialPackageWrangler_get_available_path_01():

    session = scoremanager.core.Session()
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    storehouse = configuration.user_library_material_packages_directory_path
    result = wrangler.get_available_path(
        pending_user_input='foo',
        storehouse_path=storehouse,
        )
    path = os.path.join(
        storehouse,
        'foo',
        )
    assert result == path

    result = wrangler.get_available_path(pending_user_input='example~notes q')
    assert result is None


def test_MaterialPackageWrangler_get_available_path_02():

    session = scoremanager.core.Session()
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    wrangler._session._current_score_snake_case_name = 'red_example_score'
    result = wrangler.get_available_path(pending_user_input='foo')
    path = os.path.join(
        configuration.abjad_score_packages_directory_path,
        'red_example_score',
        'materials',
        'foo',
        )

    assert result == path


def test_MaterialPackageWrangler_get_available_path_03():

    session = scoremanager.core.Session()
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)

    result = wrangler.get_available_path(pending_user_input='q')
    assert result is None

    result = wrangler.get_available_path(pending_user_input='b')
    assert result is None

    result = wrangler.get_available_path(pending_user_input='h')
    assert result is None
