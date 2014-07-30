# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_list_every_metadata_py_01():

    input_ = 'red~example~score m mdl* y q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    package_names = [
        'magic_numbers',
        'performer_inventory',
        'pitch_range_inventory',
        'tempo_inventory',
        'time_signatures',
        ]
    paths = []
    for package_name in package_names:
        path = os.path.join(
            ide._configuration.example_score_packages_directory,
            'red_example_score',
            'materials',
            package_name,
            '__metadata__.py',
            )
        paths.append(path)

    for path in paths:
        assert path in contents
    assert '5 __metadata__.py files found.' in contents


def test_MaterialPackageWrangler_list_every_metadata_py_02():

    input_ = 'mm mdl* q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    path = ide._configuration.example_score_packages_directory
    paths = [
        os.path.join(path, 'red_example_score'),
        ]
    for path in paths:
        assert path in contents

    assert '__metadata__.py files found.' in contents