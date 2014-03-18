# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PerformerCreationWizard__run_01():

    wizard = scoremanager.wizards.PerformerCreationWizard()
    input_ = 'q'
    assert wizard._run(pending_user_input=input_) is None

    wizard = scoremanager.wizards.PerformerCreationWizard()
    input_ = 'b'
    assert wizard._run(pending_user_input=input_) is None

    wizard = scoremanager.wizards.PerformerCreationWizard()
    input_ = 'h'
    assert wizard._run(pending_user_input=input_) is None


def test_PerformerCreationWizard__run_02():

    wizard = scoremanager.wizards.PerformerCreationWizard()
    input_ = 'vn default'
    assert wizard._run(pending_user_input=input_) == \
        instrumenttools.Performer(
            name='violinist', 
            instruments=[instrumenttools.Violin()],
            )


def test_PerformerCreationWizard__run_03():
    r'''Ranged.
    '''

    wizard = scoremanager.wizards.PerformerCreationWizard(is_ranged=True)
    input_ = 'vn, va default default'
    assert wizard._run(pending_user_input=input_) == [
        instrumenttools.Performer(
            name='violinist', 
            instruments=[instrumenttools.Violin()],
            ),
        instrumenttools.Performer(
            name='violist', 
            instruments=[instrumenttools.Viola()],
            ),
        ]


def test_PerformerCreationWizard__run_04():
    r'''Skipping instruments.
    '''

    wizard = scoremanager.wizards.PerformerCreationWizard(is_ranged=True)
    input_ = 'vn, va skip skip'
    assert wizard._run(pending_user_input=input_) == [
        instrumenttools.Performer(name='violinist'),
        instrumenttools.Performer(name='violist'),
        ]


def test_PerformerCreationWizard__run_05():
    r'''More instruments.
    '''

    wizard = scoremanager.wizards.PerformerCreationWizard(is_ranged=True)
    input_ = 'vn, va skip more xyl'
    assert wizard._run(pending_user_input=input_) == [
        instrumenttools.Performer(name='violinist'),
        instrumenttools.Performer(
            name='violist', 
            instruments=[instrumenttools.Xylophone()]
            ),
        ]


def test_PerformerCreationWizard__run_06():
    r'''Auxiliary percussion.
    '''

    wizard = scoremanager.wizards.PerformerCreationWizard(is_ranged=True)
    caxixi = instrumenttools.UntunedPercussion(
        instrument_name='caxixi', 
        short_instrument_name='caxixi',
        )
    input_ = 'vn more untuned cax'
    wizard._run(pending_user_input=input_)
    assert wizard.target == [
        instrumenttools.Performer(
            name='violinist', 
            instruments=[caxixi],
            ),
        ]
