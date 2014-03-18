# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentSelectionWizard__run_01():

    wizard = scoremanager.wizards.InstrumentSelectionWizard()
    wizard._session._current_score_snake_case_name = 'red_example_score'

    input_ = 'hor'
    assert wizard._run(pending_user_input=input_) == \
        instrumenttools.FrenchHorn()
    input_ = 'other xyl'
    assert wizard._run(pending_user_input=input_) == \
        instrumenttools.Xylophone()


def test_InstrumentSelectionWizard__run_02():

    wizard = scoremanager.wizards.InstrumentSelectionWizard()
    wizard._session._current_score_snake_case_name = 'red_example_score'
    whistle = instrumenttools.UntunedPercussion(
        instrument_name='whistle',
        short_instrument_name='whistle',
        )
    input_ = 'other untuned whis'
    wizard._run(pending_user_input=input_)
    assert wizard.target == whistle
