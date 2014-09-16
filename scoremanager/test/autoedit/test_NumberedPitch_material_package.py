# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_NumberedPitch_material_package_01():

    materials_directory = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        )
    material_package = os.path.join(materials_directory, 'numbered_pitch')
    definition_py = os.path.join(material_package, 'definition.py')
    output_py = os.path.join(material_package, 'output.py')

    with systemtools.FilesystemState(keep=[materials_directory]):
        assert not os.path.exists(material_package)
        input_ = 'red~example~score m new numbered~pitch y'
        input_ += ' da y NumberedPitch pn 13.5 done dp y q'
        ide._run(input_=input_)
        assert os.path.exists(material_package)
        assert os.path.isfile(definition_py)
        assert os.path.isfile(output_py)
        line = 'numbered_pitch = pitchtools.NumberedPitch(13.5)'
        with open(definition_py, 'r') as file_pointer:
            contents = file_pointer.readlines()
            assert line in contents
        with open(output_py, 'r') as file_pointer:
            contents = file_pointer.readlines()
            assert line in contents