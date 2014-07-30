# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_check_every_output_py_01():

    package_names = (
        'magic_numbers', 
        'performer_inventory',
        'pitch_range_inventory', 
        'tempo_inventory',
        'time_signatures',
        )
    output_py_paths = []
    for name in package_names:
        path = os.path.join(
            ide._configuration.example_score_packages_directory,
            'red_example_score',
            'materials',
            name,
            'output.py',
            )
        output_py_paths.append(path)

    with systemtools.FilesystemState(keep=output_py_paths):
        input_ = 'red~example~score m oc* y q'
        ide._run(input_=input_)
        contents = ide._transcript.contents
        assert 'Will check ...' in contents
        for output_py_path in output_py_paths:
            message = '{} OK.'.format(output_py_path)
            assert message in contents