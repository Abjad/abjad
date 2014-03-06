# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_material_navigation_01():
    r'''Next material.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score m mtn mtn mtn mtn q'
    score_manager._run(pending_user_input=string, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - magic numbers',
        'Red Example Score (2013) - materials - pitch range inventory',
        'Red Example Score (2013) - materials - tempo inventory',
        'Red Example Score (2013) - materials - magic numbers',
        ]
    assert score_manager._transcript.titles == titles      


def test_MaterialPackageWrangler_material_navigation_02():
    r'''Previous material.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score m mtp mtp mtp mtp q'
    score_manager._run(pending_user_input=string, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - tempo inventory',
        'Red Example Score (2013) - materials - pitch range inventory',
        'Red Example Score (2013) - materials - magic numbers',
        'Red Example Score (2013) - materials - tempo inventory',
        ]
    assert score_manager._transcript.titles == titles      
