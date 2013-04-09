import os
import scftools


def test_SCFObject_public_methods_01():

    scf_object = scftools.core.SCFObject()

    path = os.path.join(os.environ.get('SCFPATH'), 'studio', 'Studio', 'Studio.py')
    assert scf_object.module_importable_name_to_path_name('scftools.studio.Studio.Studio') == path

    path = os.environ.get('SCFPATH')
    assert scf_object.package_importable_name_to_path_name('scftools') == path
