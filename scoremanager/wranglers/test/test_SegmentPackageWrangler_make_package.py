# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_make_package_01():
    r'''Makes segment package.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'segment_04',
        )
    directory_entries = [
        '__init__.py',
        '__make__.py',
        '__metadata__.py',
        'definition.py',
        'versions',
        ]

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'red~example~score g new segment~04 y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.wranglers.SegmentPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries