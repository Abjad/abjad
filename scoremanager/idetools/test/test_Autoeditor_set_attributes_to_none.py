# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_Autoeditor_set_attributes_to_none_01():

    material_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'test_rhythm_maker',
        )
    definition_py_path = os.path.join(material_path, 'definition.py')
    string = 'beam_specifier=rhythmmakertools.BeamSpecifier'

    with systemtools.FilesystemState(remove=[material_path]):
        input_ = 'red~example~score m new test~rhythm~maker y'
        input_ += ' da y TaleaRhythmMaker'
        input_ += ' t c (1, 2, 3, 4) done bs done done y q'
        ide._run(input_=input_)
        with open(definition_py_path, 'r') as file_pointer:
            lines = file_pointer.readlines()
            contents = ''.join(lines)
            assert string in contents
        input_ = 'red~example~score m test~rhythm~maker'
        input_ += ' da none bs done y q'
        ide._run(input_=input_)
        with open(definition_py_path, 'r') as file_pointer:
            lines = file_pointer.readlines()
            contents = ''.join(lines)
            assert not string in contents