# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_check_output_py_01():

    output_py = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'magic_numbers',
        'output.py',
        )
    exception_file = os.path.join(
        score_manager._configuration.boilerplate_directory,
        'exception.py',
        )

    with systemtools.FilesystemState(keep=[output_py_path]):
        input_ = 'red~example~score m magic~numbers oc y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        message = '{} OK.'.format(output_py_path)
        assert message in contents
        shutil.copyfile(exception_file, output_py_path)
        input_ = 'red~example~score m magic~numbers oc y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        message = '{} FAILED:'.format(output_py_path)
        assert message in contents
        assert 'Exception' in contents