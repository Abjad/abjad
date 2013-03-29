import scf


def test_ListMaterialPackageMaker_01():

    studio = scf.studio.Studio()
    assert not studio.package_exists('materials.testlist')
    try:
        studio.run(user_input=
            'materials maker list testlist '
            "17 foo done b default q "
            )
        mpp = scf.makers.ListMaterialPackageMaker('materials.testlist')
        assert mpp.directory_contents == ['__init__.py', 'output_material.py', 'tags.py']
        assert mpp.output_material == [17, 'foo']
    finally:
        studio.run(user_input='m testlist del remove default q')
        assert not studio.package_exists('materials.testlist')
