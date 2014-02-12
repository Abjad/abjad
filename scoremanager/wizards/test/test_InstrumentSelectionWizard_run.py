# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentSelectionWizard_run_01():

    wizard = scoremanager.wizards.InstrumentSelectionWizard()
    wizard.session.snake_case_current_score_name = 'red_example_score'

    assert wizard._run(pending_user_input='hor') == \
        instrumenttools.FrenchHorn()
    assert wizard._run(pending_user_input='other xyl') == \
        instrumenttools.Xylophone()


def test_InstrumentSelectionWizard_run_02():

    wizard = scoremanager.wizards.InstrumentSelectionWizard()
    wizard.session.snake_case_current_score_name = 'red_example_score'
    whistle = instrumenttools.UntunedPercussion(
        instrument_name='whistle',
        short_instrument_name='whistle',
        )
    wizard._run(pending_user_input='other untuned whis')
    assert wizard.target == whistle
