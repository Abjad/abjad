from abjad import *
from experimental.tools.scoremanagementtools.editors import UserInputWrapper
from experimental import *


def test_SargassoMeasureMaterialPackageMaker_01():
    '''Empty wrapper.'''

    studio = scoremanagementtools.studio.Studio()
    assert not studio.package_exists('materials.testsargasso')
    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'q'
            )
        mpp = scoremanagementtools.makers.SargassoMeasureMaterialPackageMaker(
            'materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'tags.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
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
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('materials.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_02():
    '''Load demo values.'''

    studio = scoremanagementtools.studio.Studio()
    assert not studio.package_exists('materials.testsargasso')

    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uil '
            'q'
            )
        mpp = scoremanagementtools.makers.SargassoMeasureMaterialPackageMaker(
            'materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'tags.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
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
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('materials.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_03():
    '''Load demo values and then clear all.'''

    studio = scoremanagementtools.studio.Studio()
    assert not studio.package_exists('materials.testsargasso')
    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uil uic '
            'q'
            )
        mpp = scoremanagementtools.makers.SargassoMeasureMaterialPackageMaker(
            'materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'tags.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
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
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('materials.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_04():
    '''Edit one value.'''

    studio = scoremanagementtools.studio.Studio()
    assert not studio.package_exists('materials.testsargasso')
    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso 3 16 '
            'q'
            )
        mpp = scoremanagementtools.makers.SargassoMeasureMaterialPackageMaker(
            'materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'tags.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
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
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('materials.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_05():
    '''Populate wrapper.'''

    studio = scoremanagementtools.studio.Studio()
    assert not studio.package_exists('materials.testsargasso')
    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uip 5 '
            'Duration(11, 2) False True True 4 [2, 2, 2, 2, 1, 1, 4, 4] 16 [1, 1, 2, 3, 4] '
            'q'
            )
        mpp = scoremanagementtools.makers.SargassoMeasureMaterialPackageMaker(
            'materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'tags.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
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
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('materials.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_06():
    '''Partial population.'''

    studio = scoremanagementtools.studio.Studio()
    assert not studio.package_exists('materials.testsargasso')
    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uip 1 '
            '4 [2, 2, 3, 3] 16 [1, 1, 1, 1, 6, 6] b '
            'q'
            )
        mpp = scoremanagementtools.makers.SargassoMeasureMaterialPackageMaker(
            'materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'tags.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
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
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('materials.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_07():
    '''Set some values to none.'''

    studio = scoremanagementtools.studio.Studio()
    assert not studio.package_exists('materials.testsargasso')
    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uil 6 None 7 None 8 None '
            'q'
            )
        mpp = scoremanagementtools.makers.SargassoMeasureMaterialPackageMaker(
            'materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'tags.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
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
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('materials.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_08():
    '''Make output from demo values.'''

    studio = scoremanagementtools.studio.Studio()
    assert not studio.package_exists('materials.testsargasso')
    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uil omm default '
            'q'
            )
        mpp = scoremanagementtools.makers.SargassoMeasureMaterialPackageMaker('materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'output_material.py', 'tags.py', 'user_input.py']
        measures = [
            measuretools.Measure((4, 16), "c'16 c'16 c'8"),
            measuretools.Measure((2, 10), "c'8 c'8"),
            measuretools.Measure((3, 20), "c'8 c'16"),
            measuretools.Measure((4, 16), "c'8. c'16"),
            measuretools.Measure((4, 16), "c'8. c'16"),
            measuretools.Measure((11, 30), "c'16 c'16 c'8 c'8. c'4"),
            measuretools.Measure((15, 30), "c'8 c'16 c'8 c'8. c'4 c'16 c'16 c'16"),
            measuretools.Measure((2, 8), "c'8 c'8"),
            measuretools.Measure((10, 26), "c'8 c'8. c'4 c'16"),
            measuretools.Measure((4, 30), "c'16 c'16 c'16 c'16"),
            measuretools.Measure((15, 30), "c'16 c'4 c'16 c'16 c'8 c'8. c'16 c'8"),
            measuretools.Measure((7, 26), "c'16 c'4 c'16 c'16"),
            measuretools.Measure((3, 26), "c'16 c'16 c'16"),
            measuretools.Measure((1, 4), "c'4"),
            measuretools.Measure((10, 19), "c'8. c'4 c'16 c'16 c'16"),
            measuretools.Measure((6, 26), "c'16 c'16 c'4"),
            measuretools.Measure((6, 20), "c'4 c'16 c'16"),
            measuretools.Measure((2, 20), "c'16 c'16"),
            measuretools.Measure((9, 19), "c'16 c'4 c'16 c'16 c'8")]
        assert Staff(mpp.output_material).lilypond_format == Staff(measures).lilypond_format
    finally:
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('materials.testsargasso')
