# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.idetools.Configuration()


def test_Configuration__path_to_storehouse_01():
    
    storehouse = os.path.join(
        configuration.library,
        'stylesheets',
        )

    assert configuration._path_to_storehouse(storehouse) == storehouse

    path_1 = os.path.join(storehouse, 'foo')
    assert configuration._path_to_storehouse(path_1) == storehouse
        
    path_2 = os.path.join(storehouse, 'foo', 'bar')
    assert configuration._path_to_storehouse(path_1) == storehouse


def test_Configuration__path_to_storehouse_02():
    
    storehouse = os.path.join(
        configuration.user_score_packages_directory,
        'foo_score',
        'stylesheets',
        )

    assert configuration._path_to_storehouse(storehouse) == storehouse

    path_1 = os.path.join(storehouse, 'foo')
    assert configuration._path_to_storehouse(path_1) == storehouse
        
    path_2 = os.path.join(storehouse, 'foo', 'bar')
    assert configuration._path_to_storehouse(path_1) == storehouse


def test_Configuration__path_to_storehouse_03():
    
    storehouse = os.path.join(
        configuration.example_score_packages_directory,
        'red_example_score',
        'stylesheets',
        )

    assert configuration._path_to_storehouse(storehouse) == storehouse

    path_1 = os.path.join(storehouse, 'foo')
    assert configuration._path_to_storehouse(path_1) == storehouse
        
    path_2 = os.path.join(storehouse, 'foo', 'bar')
    assert configuration._path_to_storehouse(path_1) == storehouse


def test_Configuration__path_to_storehouse_04():
    
    storehouse = configuration.example_stylesheets_directory

    assert configuration._path_to_storehouse(storehouse) == storehouse

    path_1 = os.path.join(storehouse, 'foo')
    assert configuration._path_to_storehouse(path_1) == storehouse
        
    path_2 = os.path.join(storehouse, 'foo', 'bar')
    assert configuration._path_to_storehouse(path_1) == storehouse