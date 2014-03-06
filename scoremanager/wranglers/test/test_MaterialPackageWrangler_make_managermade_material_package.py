# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_managermade_material_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testsargasso',
        )
    assert not os.path.exists(path)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'user_input.py',
        ]

    try:
        input_ = 'sargasso testsargasso q'
        wrangler.make_managermade_material_package(pending_user_input=input_)
        assert os.path.exists(path)
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            path=path)
        assert manager._list() == directory_entries
    finally:
        manager._remove()
        assert not os.path.exists(path)


def test_MaterialPackageWrangler_make_managermade_material_package_02():
    r'''Menu title is correct.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='lmm nmm q', is_test=True)

    transcript = score_manager._transcript
    string = 'Select material manager:'
    assert transcript.last_title == string
