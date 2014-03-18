# -*- encoding: utf-8 -*-
import os
import pytest
import shutil
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_managermade_material_package_01():

    session = scoremanager.core.Session()
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    path = os.path.join(
        wrangler._configuration.user_library_material_packages_directory_path,
        'testsargasso',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'user_input.py',
        ]

    assert not os.path.exists(path)
    try:
        input_ = 'sargasso testsargasso q'
        wrangler.make_managermade_material_package(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.SargassoMeasureMaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler_make_managermade_material_package_02():
    r'''Menu title is correct.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._run(pending_user_input='lmm nmm q')

    transcript = score_manager._transcript
    string = 'Select material manager:'
    assert transcript.last_title == string
