# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentSelectionWizard__run_01():

    wizard = scoremanager.wizards.InstrumentSelectionWizard()
    wizard._session._current_score_snake_case_name = 'red_example_score'

    assert wizard._run(pending_user_input='hor', is_test=True) == \
        instrumenttools.FrenchHorn()
    assert wizard._run(pending_user_input='other xyl', is_test=True) == \
        instrumenttools.Xylophone()


def test_InstrumentSelectionWizard__run_02():

    wizard = scoremanager.wizards.InstrumentSelectionWizard()
    wizard._session._current_score_snake_case_name = 'red_example_score'
    whistle = instrumenttools.UntunedPercussion(
        instrument_name='whistle',
        short_instrument_name='whistle',
        )
    wizard._run(pending_user_input='other untuned whis', is_test=True)
    assert wizard.target == whistle
