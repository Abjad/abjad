# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_ScoreManagerConfiguration__path_to_storehouse_annotation_01():
    r'''User library paths annotate composer last name.
    '''

    path = configuration.user_library_directory_path
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == configuration.composer_last_name
    
    path = configuration.user_library_editors_directory_path
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == configuration.composer_last_name

    path = configuration.user_library_makers_directory_path
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == configuration.composer_last_name
    
    path = configuration.user_library_material_managers_directory_path
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == configuration.composer_last_name

    path = configuration.user_library_material_packages_directory_path
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == configuration.composer_last_name

    path = configuration.user_library_stylesheets_directory_path
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == configuration.composer_last_name


def test_ScoreManagerConfiguration__path_to_storehouse_annotation_02():
    r'''Abjad library paths annotate 'Abjad'.
    '''

    path = configuration.abjad_editors_directory_path
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == 'Abjad'

    path = configuration.abjad_material_managers_directory_path
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == 'Abjad'

    path = configuration.abjad_material_packages_directory_path
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == 'Abjad'

    path = configuration.abjad_stylesheets_directory_path
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == 'Abjad'


def test_ScoreManagerConfiguration__path_to_storehouse_annotation_03():
    r'''Score paths annotate score title.
    '''

    path = os.path.join(
        configuration.abjad_score_packages_directory_path,
        'red_example_score',
        )
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == 'Red Example Score'