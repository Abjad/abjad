# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_rename_package_01():
    r'''Creates package. Renames package.
    '''

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'segment_04',
        )
    new_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'renamed_segment_04',
        )

    with systemtools.FilesystemState(remove=[path, new_path]):
        input_ = 'red~example~score g new segment~04 y q'
        ide._run(input_=input_)
        assert os.path.exists(path)
        input_ = 'red~example~score g ren segment~04 renamed_segment_04 y q'
        ide._run(input_=input_)
        assert not os.path.exists(path)
        assert os.path.exists(new_path)