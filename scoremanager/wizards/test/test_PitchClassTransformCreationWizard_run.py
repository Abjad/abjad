# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PitchClassTransformCreationWizard_run_01():

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='q') == []

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='b') == []


def test_PitchClassTransformCreationWizard_run_02():

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='transpose q') == []

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='transpose b q') == []

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='invert q') == [('invert', ())]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='invert b') == [('invert', ())]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='multiply q') == []

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='multiply b q') == []


def test_PitchClassTransformCreationWizard_run_03():

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='transpose 1 q') == [('transpose', (1,))]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='multiply 5 q') == [('multiply', (5,))]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='transpose 1 multiply 5 q') == [
        ('transpose', (1,)), ('multiply', (5,))]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    assert wizard._run(pending_user_input='transpose 1 invert multiply 5 q') == [
        ('transpose', (1,)), ('invert', ()), ('multiply', (5,))]
