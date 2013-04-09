from abjad.tools import contexttools
import scftools


def test_TempoMarkInventoryMaterialPackageMaker_01():

    studio = scftools.studio.Studio()
    assert not studio.package_exists('materials.testtempoinventory')
    try:
        studio.run(user_input=
            'materials maker tempo testtempoinventory default '
            'testtempoinventory omi add ((1, 4), 60) add ((1, 4), 90) b default '
            'q '
            )
        mpp = scftools.makers.TempoMarkInventoryMaterialPackageMaker('materials.testtempoinventory')
        assert mpp.directory_contents == ['__init__.py', 'output_material.py', 'tags.py']
        inventory = contexttools.TempoMarkInventory([((1, 4), 60), ((1, 4), 90)])
        assert mpp.output_material == inventory
    finally:
        studio.run(user_input='m testtempoinventory del remove default q')
        assert not studio.package_exists('materials.testtempoinventory')
