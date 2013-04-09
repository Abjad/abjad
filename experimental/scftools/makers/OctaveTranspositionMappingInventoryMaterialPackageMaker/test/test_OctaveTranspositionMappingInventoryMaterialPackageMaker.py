from abjad.tools import pitchtools
import scftools


def test_OctaveTranspositionMappingInventoryMaterialPackageMaker_01():
    '''Stub material package.
    '''

    studio = scftools.studio.Studio()
    assert not studio.package_exists('materials.testoctavetrans')
    try:
        studio.run(user_input=
            'materials maker octave testoctavetrans default '
            'q'
            )
        mpp = scftools.makers.OctaveTranspositionMappingInventoryMaterialPackageMaker('materials.testoctavetrans')
        assert mpp.directory_contents == ['__init__.py', 'tags.py']
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testoctavetrans del remove default q')
        assert not studio.package_exists('materials.testoctavetrans')


def test_OctaveTranspositionMappingInventoryMaterialPackageMaker_02():
    '''Populate output material module.
    '''

    studio = scftools.studio.Studio()
    assert not studio.package_exists('materials.testoctavetrans')
    try:
        studio.run(user_input=
            'materials maker octave testoctavetrans '
            'testoctavetrans omi add add source [A0, C4) target 15 done '
            'add source [C4, C8) target 27 done done '
            'add add source [A0, C8] target -18 done done done default q'
            )
        mpp = scftools.makers.OctaveTranspositionMappingInventoryMaterialPackageMaker(
            'materials.testoctavetrans')
        assert mpp.directory_contents == ['__init__.py', 'output_material.py', 'tags.py']
        mapping_1 = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
        mapping_2 = pitchtools.OctaveTranspositionMapping([('[A0, C8]', -18)])
        inventory = pitchtools.OctaveTranspositionMappingInventory([mapping_1, mapping_2])
        assert mpp.output_material == inventory
    finally:
        studio.run(user_input='m testoctavetrans del remove default q')
        assert not studio.package_exists('materials.testoctavetrans')
