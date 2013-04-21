import os
from experimental import *


def test_SCFObject_public_methods_01():

    scf_object = scoremanagementtools.core.SCFObject()

    path = os.path.join(os.environ.get('SCFPATH'), 'scoremanager', 'ScoreManager', 'ScoreManager.py')
    assert scf_object.module_importable_name_to_path_name(
        'scoremanagementtools.scoremanager.ScoreManager.ScoreManager') == path

    path = os.environ.get('SCFPATH')
    assert scf_object.package_importable_name_to_path_name('scoremanagementtools') == path
