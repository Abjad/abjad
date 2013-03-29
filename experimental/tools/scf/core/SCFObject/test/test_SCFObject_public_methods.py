import os
import scf


def test_SCFObject_public_methods_01():

    scf_object = scf.core.SCFObject()

    path = os.path.join(os.environ.get('SCFPATH'), 'studio', 'Studio', 'Studio.py')
    assert scf_object.module_importable_name_to_path_name('scf.studio.Studio.Studio') == path

    path = os.environ.get('SCFPATH')
    assert scf_object.package_importable_name_to_path_name('scf') == path
