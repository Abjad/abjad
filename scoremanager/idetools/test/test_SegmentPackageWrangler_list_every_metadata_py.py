# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_list_every_metadata_py_01():

    package_names = [
        'segment_01',
        'segment_02',
        'segment_03',
        ]
    paths = []
    for package_name in package_names:
        path = os.path.join(
            ide._configuration.example_score_packages_directory,
            'red_example_score',
            'segments',
            package_name,
            '__metadata__.py',
            )
        paths.append(path)

    input_ = 'red~example~score g mdl* y q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    for path in paths:
        assert path in contents
    assert '3 __metadata__.py files found.' in contents


def test_SegmentPackageWrangler_list_every_metadata_py_02():

    input_ = 'gg mdl* q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    path = ide._configuration.example_score_packages_directory
    paths = [
        os.path.join(path, 'red_example_score'),
        ]
    for path in paths:
        assert path in contents
    assert '__metadata__.py files found.' in contents