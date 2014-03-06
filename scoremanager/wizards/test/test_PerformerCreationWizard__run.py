# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PerformerCreationWizard__run_01():

    wizard = scoremanager.wizards.PerformerCreationWizard()
    assert wizard._run(pending_user_input='q', is_test=True) is None

    wizard = scoremanager.wizards.PerformerCreationWizard()
    assert wizard._run(pending_user_input='b', is_test=True) is None

    wizard = scoremanager.wizards.PerformerCreationWizard()
    assert wizard._run(pending_user_input='h', is_test=True) is None


def test_PerformerCreationWizard__run_02():

    wizard = scoremanager.wizards.PerformerCreationWizard()
    assert wizard._run(pending_user_input='vn default', is_test=True) == \
        instrumenttools.Performer(
            name='violinist', 
            instruments=[instrumenttools.Violin()],
            )


def test_PerformerCreationWizard__run_03():
    r'''Ranged.
    '''

    wizard = scoremanager.wizards.PerformerCreationWizard(is_ranged=True)
    input_ = 'vn, va default default'
    assert wizard._run(pending_user_input=input_, is_test=True) == [
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
    assert wizard._run(pending_user_input=input_, is_test=True) == [
        instrumenttools.Performer(name='violinist'),
        instrumenttools.Performer(name='violist'),
        ]


def test_PerformerCreationWizard__run_05():
    r'''More instruments.
    '''

    wizard = scoremanager.wizards.PerformerCreationWizard(is_ranged=True)
    input_ = 'vn, va skip more xyl'
    assert wizard._run(pending_user_input=input_, is_test=True) == [
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
    wizard._run(pending_user_input='vn more untuned cax', is_test=True)
    assert wizard.target == [
        instrumenttools.Performer(
            name='violinist', 
            instruments=[caxixi],
            ),
        ]
