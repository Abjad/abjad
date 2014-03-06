# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PitchClassTransformCreationWizard__run_01():

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='q', is_test=True) == []

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='b', is_test=True) == []


def test_PitchClassTransformCreationWizard__run_02():

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='transpose q', is_test=True) == []

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='transpose b q', is_test=True) == []

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='invert q', is_test=True) == [('invert', ())]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='invert b', is_test=True) == [('invert', ())]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='multiply q', is_test=True) == []

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='multiply b q', is_test=True) == []


def test_PitchClassTransformCreationWizard__run_03():

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='transpose 1 q', is_test=True) == \
        [('transpose', (1,))]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='multiply 5 q', is_test=True) == \
        [('multiply', (5,))]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    input_ = 'transpose 1 multiply 5 q'
    assert wizard._run(pending_user_input=input_, is_test=True) == \
        [('transpose', (1,)), ('multiply', (5,))]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    string = 'transpose 1 invert multiply 5 q'
    assert wizard._run(pending_user_input=string, is_test=True) == \
        [('transpose', (1,)), ('invert', ()), ('multiply', (5,))]
