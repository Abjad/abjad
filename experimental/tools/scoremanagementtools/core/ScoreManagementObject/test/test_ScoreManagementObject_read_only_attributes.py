import os
from experimental import *


def test_ScoreManagementObject_read_only_attributes_01():

    scf_object = scoremanagementtools.core.ScoreManagementObject()

    path = os.path.join(os.environ.get('SCFPATH'), 'boilerplate')
    assert scf_object.boilerplate_directory_name == path

    assert isinstance(scf_object.breadcrumb_stack, list)
    assert scf_object.class_name == 'ScoreManagementObject'
    assert scf_object.help_item_width == 5

    path = os.path.join(os.environ.get('SCFPATH'), 'makers')
    assert scf_object.makers_directory_name == path

    assert scf_object.makers_package_importable_name == 'scoremanagementtools.makers'
    assert scf_object.scf_package_importable_name == 'scoremanagementtools'

    path = os.environ.get('SCFPATH')
    assert scf_object.scf_package_path_name == path

    assert isinstance(scf_object.session, scoremanagementtools.core.Session)
    assert scf_object.score_external_chunks_package_importable_name == 'sketches'

    path = os.path.join(os.environ.get('SCFPATH'), 'core', 'ScoreManagementObject', 'ScoreManagementObject.py')
    assert scf_object.source_file_name == path

    assert scf_object.spaced_class_name == 'score management object'
    assert scf_object.score_external_materials_package_importable_name == 'materials'


    path = os.path.join(os.environ.get('SCFPATH'), 'stylesheets')
    assert scf_object.stylesheets_directory_name == path

    assert scf_object.stylesheets_package_importable_name == 'scoremanagementtools.stylesheets'
    assert isinstance(scf_object.transcript, list)
    assert isinstance(scf_object.transcript_signature, tuple)
    assert isinstance(scf_object.ts, tuple)
