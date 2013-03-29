import scf


def test_ConstellationCircuitSelectionMaterialPackageMaker_01():

    studio = scf.studio.Studio()
    assert not studio.package_exists('materials.testconst')
    try:
        studio.run(user_input=
            'materials maker constellation testconst '
            "(1, 18) (2, 48) done b default q "
            )
        mpp = scf.makers.ListMaterialPackageMaker('materials.testconst')
        assert mpp.directory_contents == ['__init__.py', 'output_material.py', 'tags.py']
        assert mpp.output_material == [(1, 18), (2, 48)]
    finally:
        studio.run(user_input='m testconst del remove default q')
        assert not studio.package_exists('materials.testconst')
