# -*- encoding: utf-8 -*-
from experimental import *


def test_SargassoMeasureMaterialPackageMaker_01():
    r'''Empty wrapper.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanagertools.materialpackages.testsargasso')
    try:
        score_manager._run(pending_user_input=
            'materials maker sargasso testsargasso default '
            'q'
            )
        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'scoremanagertools.materialpackages.testsargasso')
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        user_input_wrapper = scoremanagertools.editors.UserInputWrapper([
            ('measure_denominator', None),
            ('measure_numerator_talea', None),
            ('measure_division_denominator', None),
            ('measure_division_talea', None),
            ('total_duration', None),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        score_manager._run(pending_user_input='m testsargasso del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanagertools.materialpackages.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_02():
    r'''Load demo values.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanagertools.materialpackages.testsargasso')

    try:
        score_manager._run(pending_user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uil '
            'q'
            )
        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'scoremanagertools.materialpackages.testsargasso')
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        user_input_wrapper = scoremanagertools.editors.UserInputWrapper([
            ('measure_denominator', 4),
            ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
            ('measure_division_denominator', 16),
            ('measure_division_talea', [1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4]),
            ('total_duration', Duration(11, 2)),
            ('measures_are_scaled', True),
            ('measures_are_split', True),
            ('measures_are_shuffled', True)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        score_manager._run(pending_user_input='m testsargasso del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanagertools.materialpackages.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_03():
    r'''Load demo values and then clear all.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanagertools.materialpackages.testsargasso')
    try:
        score_manager._run(pending_user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uil uic '
            'q'
            )
        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'scoremanagertools.materialpackages.testsargasso')
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        user_input_wrapper = scoremanagertools.editors.UserInputWrapper([
            ('measure_denominator', None),
            ('measure_numerator_talea', None),
            ('measure_division_denominator', None),
            ('measure_division_talea', None),
            ('total_duration', None),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        score_manager._run(pending_user_input='m testsargasso del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanagertools.materialpackages.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_04():
    r'''Edit one value.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanagertools.materialpackages.testsargasso')
    try:
        score_manager._run(pending_user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso 3 16 '
            'q'
            )
        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'scoremanagertools.materialpackages.testsargasso')
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        user_input_wrapper = scoremanagertools.editors.UserInputWrapper([
            ('measure_denominator', None),
            ('measure_numerator_talea', None),
            ('measure_division_denominator', 16),
            ('measure_division_talea', None),
            ('total_duration', None),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        score_manager._run(pending_user_input='m testsargasso del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanagertools.materialpackages.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_05():
    r'''Populate wrapper.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanagertools.materialpackages.testsargasso')
    try:
        score_manager._run(pending_user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uip 5 '
            'Duration(11, 2) False True True 4 [2, 2, 2, 2, 1, 1, 4, 4] 16 [1, 1, 2, 3, 4] '
            'q'
            )
        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'scoremanagertools.materialpackages.testsargasso')
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        user_input_wrapper = scoremanagertools.editors.UserInputWrapper([
            ('measure_denominator', 4),
            ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
            ('measure_division_denominator', 16),
            ('measure_division_talea', [1, 1, 2, 3, 4]),
            ('total_duration', Duration(11, 2)),
            ('measures_are_scaled', False),
            ('measures_are_split', True),
            ('measures_are_shuffled', True)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        score_manager._run(pending_user_input='m testsargasso del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanagertools.materialpackages.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_06():
    r'''Partial population.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanagertools.materialpackages.testsargasso')
    try:
        score_manager._run(pending_user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uip 1 '
            '4 [2, 2, 3, 3] 16 [1, 1, 1, 1, 6, 6] b '
            'q'
            )
        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'scoremanagertools.materialpackages.testsargasso')
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        user_input_wrapper = scoremanagertools.editors.UserInputWrapper([
            ('measure_denominator', 4),
            ('measure_numerator_talea', [2, 2, 3, 3]),
            ('measure_division_denominator', 16),
            ('measure_division_talea', [1, 1, 1, 1, 6, 6]),
            ('total_duration', None),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        score_manager._run(pending_user_input='m testsargasso del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanagertools.materialpackages.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_07():
    r'''Set some values to none.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanagertools.materialpackages.testsargasso')
    try:
        score_manager._run(pending_user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uil 6 None 7 None 8 None '
            'q'
            )
        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'scoremanagertools.materialpackages.testsargasso')
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        user_input_wrapper = scoremanagertools.editors.UserInputWrapper([
            ('measure_denominator', 4),
            ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
            ('measure_division_denominator', 16),
            ('measure_division_talea', [1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4]),
            ('total_duration', Duration(11, 2)),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        score_manager._run(pending_user_input='m testsargasso del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanagertools.materialpackages.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_08():
    r'''Make output from demo values.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanagertools.materialpackages.testsargasso')
    try:
        score_manager._run(pending_user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uil omm default '
            'q'
            )
        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'scoremanagertools.materialpackages.testsargasso')
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'output_material.py', 
            'user_input.py',
            ]
        measures = [
            scoretools.Measure((4, 16), "c'16 c'16 c'8"),
            scoretools.Measure((2, 10), "c'8 c'8"),
            scoretools.Measure((3, 20), "c'8 c'16"),
            scoretools.Measure((4, 16), "c'8. c'16"),
            scoretools.Measure((4, 16), "c'8. c'16"),
            scoretools.Measure((11, 30), "c'16 c'16 c'8 c'8. c'4"),
            scoretools.Measure((15, 30), "c'8 c'16 c'8 c'8. c'4 c'16 c'16 c'16"),
            scoretools.Measure((2, 8), "c'8 c'8"),
            scoretools.Measure((10, 26), "c'8 c'8. c'4 c'16"),
            scoretools.Measure((4, 30), "c'16 c'16 c'16 c'16"),
            scoretools.Measure((15, 30), "c'16 c'4 c'16 c'16 c'8 c'8. c'16 c'8"),
            scoretools.Measure((7, 26), "c'16 c'4 c'16 c'16"),
            scoretools.Measure((3, 26), "c'16 c'16 c'16"),
            scoretools.Measure((1, 4), "c'4"),
            scoretools.Measure((10, 19), "c'8. c'4 c'16 c'16 c'16"),
            scoretools.Measure((6, 26), "c'16 c'16 c'4"),
            scoretools.Measure((6, 20), "c'4 c'16 c'16"),
            scoretools.Measure((2, 20), "c'16 c'16"),
            scoretools.Measure((9, 19), "c'16 c'4 c'16 c'16 c'8")]
        for measure in measures:
            measure.implicit_scaling = True
        assert format(Staff(measures))
        for measure in mpp.output_material:
            assert measure.implicit_scaling
        assert format(Staff(mpp.output_material))
        assert format(Staff(mpp.output_material)) == format(Staff(measures))
    finally:
        score_manager._run(pending_user_input='m testsargasso del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanagertools.materialpackages.testsargasso')
