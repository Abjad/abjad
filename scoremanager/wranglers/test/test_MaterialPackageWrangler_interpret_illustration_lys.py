# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_interpret_illustration_lys_01():
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
            score_manager._configuration.example_score_packages_directory_path,
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
        input_ = 'red~example~score m ilyi y q'
        score_manager._run(pending_input=input_)
        contents = score_manager._transcript.contents
        assert all(os.path.isfile(_) for _ in output_paths)
        assert 'Will interpret ...' in contents
        assert 'INPUT:' in contents
        assert 'OUTPUT:' in contents
        assert 'Interpreted' in contents
        #for output_path, backup_output_path in pairs:
        #    assert diff-pdf(output_path, backup_output_path)