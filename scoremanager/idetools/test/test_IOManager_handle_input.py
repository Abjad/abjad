# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_IOManager_handle_input_01():
    r'''Command repetition works.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = '>> . . . q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Blue Example Score (2013)',
        'Étude Example Score (2013)',
        'Red Example Score (2013)',
        'Blue Example Score (2013)',
        ]
    assert ide._transcript.titles == titles