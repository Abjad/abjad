# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PitchClassTransformCreationWizard__run_01():

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    input_ = 'q'
    assert wizard._run(pending_user_input=input_) == []

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    input_ = 'b'
    assert wizard._run(pending_user_input=input_) == []


def test_PitchClassTransformCreationWizard__run_02():

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    input_ = 'transpose q'
    assert wizard._run(pending_user_input=input_) == []

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    input_ = 'transpose b q'
    assert wizard._run(pending_user_input=input_) == []

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    input_ = 'invert q'
    assert wizard._run(pending_user_input=input_) == [('invert', ())]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    input_ = 'invert b'
    assert wizard._run(pending_user_input=input_) == [('invert', ())]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    input_ = 'multiply q'
    assert wizard._run(pending_user_input=input_) == []

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    input_ = 'multiply b q'
    assert wizard._run(pending_user_input=input_) == []


def test_PitchClassTransformCreationWizard__run_03():

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    input_ = 'transpose 1 q'
    assert wizard._run(pending_user_input=input_) == \
        [('transpose', (1,))]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    input_ = 'multiply 5 q'
    assert wizard._run(pending_user_input=input_) == \
        [('multiply', (5,))]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    input_ = 'transpose 1 multiply 5 q'
    assert wizard._run(pending_user_input=input_) == \
        [('transpose', (1,)), ('multiply', (5,))]

    wizard = scoremanager.wizards.PitchClassTransformCreationWizard()
    string = 'transpose 1 invert multiply 5 q'
    assert wizard._run(pending_user_input=string) == \
        [('transpose', (1,)), ('invert', ()), ('multiply', (5,))]
