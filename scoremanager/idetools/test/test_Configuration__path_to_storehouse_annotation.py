# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.idetools.Configuration()


def test_Configuration__path_to_storehouse_annotation_01():
    r'''Library paths annotate composer last name.
    '''

    path = configuration.library
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == configuration.composer_last_name

    path = configuration.makers_library
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == configuration.composer_last_name

    path = configuration.materials_library
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == configuration.composer_last_name

    path = configuration.stylesheets_library
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == configuration.composer_last_name


def test_Configuration__path_to_storehouse_annotation_02():
    r'''Example asset storehouse paths annotate 'Abjad'.
    '''

    path = configuration.example_stylesheets_directory
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == 'Abjad'


def test_Configuration__path_to_storehouse_annotation_03():
    r'''Score paths annotate score title.
    '''

    path = os.path.join(
        configuration.example_score_packages_directory,
        'red_example_score',
        )
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == 'Red Example Score'