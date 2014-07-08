# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_illustrate_output_py_01():
    r'''Works with literal material (like tempo inventory).
    '''

    illustration_ly = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'tempo_inventory',
        'illustration.ly',
        )
    illustration_pdf = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'tempo_inventory',
        'illustration.pdf',
        )

    with systemtools.FilesystemState(keep=[illustration_ly, illustration_pdf]):
        os.remove(illustration_ly)
        os.remove(illustration_pdf)
        assert not os.path.exists(illustration_ly)
        assert not os.path.exists(illustration_pdf)
        input_ = 'red~example~score m tempo~inventory oi q'
        ide._run(input_=input_)
        assert os.path.isfile(illustration_ly)
        assert os.path.isfile(illustration_pdf)
        assert systemtools.TestManager._compare_backup(illustration_ly)
        assert systemtools.TestManager._compare_backup(illustration_pdf)


def test_MaterialPackageManager_illustrate_output_py_02():
    r'''Works with type I maker (like sargasso measure maker).
    '''

    illustration_ly = os.path.join(
        ide._configuration.example_score_packages_directory,
        'blue_example_score',
        'materials',
        'sargasso_measures',
        'illustration.ly',
        )
    illustration_pdf = os.path.join(
        ide._configuration.example_score_packages_directory,
        'blue_example_score',
        'materials',
        'sargasso_measures',
        'illustration.pdf',
        )

    with systemtools.FilesystemState(keep=[illustration_ly, illustration_pdf]):
        os.remove(illustration_ly)
        os.remove(illustration_pdf)
        assert not os.path.exists(illustration_ly)
        assert not os.path.exists(illustration_pdf)
        input_ = 'blue~example~score m sargasso~measures oi q'
        ide._run(input_=input_)
        assert os.path.isfile(illustration_ly)
        assert os.path.isfile(illustration_pdf)
        assert systemtools.TestManager._compare_backup(illustration_ly)
        assert systemtools.TestManager._compare_backup(illustration_pdf)


def test_MaterialPackageManager_illustrate_output_py_03():
    r'''Works with type II maker (like talea rhythm-maker).
    '''

    illustration_ly = os.path.join(
        ide._configuration.example_score_packages_directory,
        'blue_example_score',
        'materials',
        'talea_rhythm_maker',
        'illustration.ly',
        )
    illustration_pdf = os.path.join(
        ide._configuration.example_score_packages_directory,
        'blue_example_score',
        'materials',
        'talea_rhythm_maker',
        'illustration.pdf',
        )

    with systemtools.FilesystemState(keep=[illustration_ly, illustration_pdf]):
        os.remove(illustration_ly)
        os.remove(illustration_pdf)
        assert not os.path.exists(illustration_ly)
        assert not os.path.exists(illustration_pdf)
        input_ = 'blue~example~score m talea~rhythm~maker oi q'
        ide._run(input_=input_)
        assert os.path.isfile(illustration_ly)
        assert os.path.isfile(illustration_pdf)
        assert systemtools.TestManager._compare_backup(illustration_ly)
        assert systemtools.TestManager._compare_backup(illustration_pdf)