# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_version_every_package_01():
    r'''Red Example Score segments A, B, C should all require no versioning.

    This might or might not change with new versions of LilyPond.

    If that's the case then either this test will have to be updated
    or segments A, B, C will have to be versioned again to bring
    this test back up to date.
    '''
    
    next_version_paths = []
    segments = ('segment_01', 'segment_02', 'segment_03')
    file_names = ('definition.py', 'illustration.ly', 'illustration.pdf')
    for segment in segments:
        versions_directory = os.path.join(
            ide._configuration.example_score_packages_directory,
            'red_example_score',
            'segments',
            segment,
            'versions',
            )
        for file_name in file_names:
            root, extension = os.path.splitext(file_name)
            target_name = '{}_{}{}'.format(root, '0003', extension)
            next_version_path = os.path.join(versions_directory, target_name)
            next_version_paths.append(next_version_path)

    with systemtools.FilesystemState(remove=next_version_paths):
        input_ = 'red~example~score g vr* y q'
        ide._run(input_=input_)
        for path in next_version_paths:
            assert not os.path.isfile(path)

    contents = ide._transcript.contents
    assert 'Nothing to version ...' in contents
    for path in next_version_paths:
        assert path not in contents