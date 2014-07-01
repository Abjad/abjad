# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_interpret_every_illustration_ly_01():
    r'''Works when illustration.ly already exists.
    '''

    package_names = (
        'magic_numbers', 
        'pitch_range_inventory', 
        'tempo_inventory',
        )
    input_paths = []
    for name in package_names:
        path = os.path.join(
            ide._configuration.example_score_packages_directory,
            'red_example_score',
            'materials',
            name,
            'illustration.ly',
            )
        input_paths.append(path)
    output_paths = []
    for path in input_paths:
        path = path.replace('.ly', '.pdf')
        output_paths.append(path)

    keep = input_paths + output_paths
    with systemtools.FilesystemState(keep=keep):
        for path in output_paths:
            os.remove(path)
        assert not any(os.path.exists(_) for _ in output_paths)
        input_ = 'red~example~score m ii* y q'
        ide._run(input_=input_)
        contents = ide._transcript.contents
        assert all(os.path.isfile(_) for _ in output_paths)
        assert 'Will interpret ...' in contents
        assert 'INPUT:' in contents
        assert 'OUTPUT:' in contents
        assert 'Interpreted' in contents
        for output_path in output_paths:
            assert systemtools.TestManager.compare_pdfs(
                output_path, 
                output_path + '.backup',
                )