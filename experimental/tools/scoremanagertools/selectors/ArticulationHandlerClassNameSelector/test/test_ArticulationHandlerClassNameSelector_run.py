# -*- encoding: utf-8 -*-
from experimental import *


def test_ArticulationHandlerClassNameSelector_run_01():

    selector = scoremanagertools.selectors.ArticulationHandlerClassNameSelector()

    assert selector._run(pending_user_input='reiterated') == 'ReiteratedArticulationHandler'
