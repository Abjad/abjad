import py
import scf
from scf.editors import UserInputWrapper
py.test.skip('REMOVE ME')


def test_ZaggedPitchClassMaterialPackageMaker_01():
    '''Emtpy wrapper.
    '''

    studio = scf.studio.Studio()
    assert not studio.package_exists('materials.testzagged')
    try:
        studio.run(user_input=
            'materials maker zagged testzagged default '
            'q'
            )
        mpp = scf.makers.ZaggedPitchClassMaterialPackageMaker(
            'materials.testzagged')
        assert mpp.directory_contents == ['__init__.py', 'tags.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
            ('pc_cells', None),
            ('division_cells', None),
            ('grouping_counts', None)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        studio.run(user_input='m testzagged del remove default q')
        assert not studio.package_exists('materials.testzagged')


def test_ZaggedPitchClassMaterialPackageMaker_02():
    '''Populate wrapper.
    '''

    studio = scf.studio.Studio()
    assert not studio.package_exists('materials.testzagged')
    try:
        studio.run(user_input=
            'materials maker zagged testzagged default '
            'testzagged uip 1 [[0, 7, 2, 10], [9, 6, 1, 8]] '
            '[[[1], [1], [1], [1, 1, 1]]] '
            '[1, 1, 2, 3] '
            'q'
            )
        mpp = scf.makers.ZaggedPitchClassMaterialPackageMaker(
            'materials.testzagged')
        assert mpp.directory_contents == ['__init__.py', 'tags.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
            ('pc_cells', [[0, 7, 2, 10], [9, 6, 1, 8]]),
            ('division_cells', [[[1], [1], [1], [1, 1, 1]]]),
            ('grouping_counts', [1, 1, 2, 3])])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        studio.run(user_input='m testzagged del remove default q')
        assert not studio.package_exists('materials.testzagged')
