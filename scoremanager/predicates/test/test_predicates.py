# -*- encoding: utf-8 -*-
from scoremanager.predicates import predicates
import scoremanager


def test_predicates_01():

    assert predicates.is_available_snake_case_package_name(
        'asdf')
    assert predicates.is_available_snake_case_package_name(
        'scoremanager.asdf')
    assert predicates.is_available_snake_case_package_name(
        'scoremanager.materials.asdf')

    assert not predicates.is_available_snake_case_package_name(
        'scoremanager')
    assert not predicates.is_available_snake_case_package_name(
        'scoremanager.materials')


def test_predicates_02():

    assert predicates.is_existing_package_name(
        'scoremanager')
    assert predicates.is_existing_package_name(
        'scoremanager.materials')

    assert not predicates.is_existing_package_name(
        'asdf')
    assert not predicates.is_existing_package_name(
        'scoremanager.asdf')
    assert not predicates.is_existing_package_name(
        'scoremanager.materials.asdf')



def test_predicates_03():

    assert predicates.is_boolean(True)
    assert predicates.is_boolean(False)

    assert not predicates.is_boolean(None)
    assert not predicates.is_boolean('')
    assert not predicates.is_boolean(0)
    assert not predicates.is_boolean(1)
