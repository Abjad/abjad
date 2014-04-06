# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_make_new_material_package_01():
    r'''Back works in path getter.
    '''

    input_ = 'm new b q'
    score_manager._run(pending_user_input=input_)
    first_lines = [
        'Score manager - example scores',
        '> m',
        'Score manager - material library',
        '> new',
        'Package name> b',
        'Score manager - material library',
        '> q',
        ]
    
    assert score_manager._transcript.first_lines == first_lines