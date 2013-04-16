from abjad import *
from experimental import *


def test_InstrumentSelectionWizard_run_01():

    wizard = scoremanagementtools.wizards.InstrumentSelectionWizard()
    wizard.session.current_score_package_short_name = 'example_score_1'

    assert wizard.run(user_input='hor') == instrumenttools.FrenchHorn()
    assert wizard.run(user_input='other xyl') == instrumenttools.Xylophone()


def test_InstrumentSelectionWizard_run_02():

    wizard = scoremanagementtools.wizards.InstrumentSelectionWizard()
    wizard.session.current_score_package_short_name = 'example_score_1'
    whistle = instrumenttools.UntunedPercussion(
        instrument_name='whistle',
        short_instrument_name='whistle',
        )
    wizard.run(user_input='other untuned whis')
    assert wizard.target == whistle
